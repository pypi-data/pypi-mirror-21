#!/bin/bash

set -o xtrace
set -o errexit

# Enable unbuffered output for Ansible in Jenkins.
export PYTHONUNBUFFERED=1

source /etc/nodepool/provider

NODEPOOL_MIRROR_HOST=${NODEPOOL_MIRROR_HOST:-mirror.$NODEPOOL_REGION.$NODEPOOL_CLOUD.openstack.org}
NODEPOOL_MIRROR_HOST=$(echo $NODEPOOL_MIRROR_HOST|tr '[:upper:]' '[:lower:]')
NODEPOOL_PYPI_MIRROR=${NODEPOOL_PYPI_MIRROR:-http://$NODEPOOL_MIRROR_HOST/pypi/simple}

GIT_PROJECT_DIR=$(mktemp -d)

# Just for mandre :)
if [[ ! -f /etc/sudoers.d/jenkins ]]; then
    echo "jenkins ALL=(:docker) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/jenkins
fi

function clone_repos {
    cat > /tmp/clonemap <<EOF
clonemap:
 - name: openstack/kolla
   dest: ${GIT_PROJECT_DIR}/kolla
 - name: openstack/requirements
   dest: ${GIT_PROJECT_DIR}/requirements
EOF
    /usr/zuul-env/bin/zuul-cloner -m /tmp/clonemap --workspace "$(pwd)" \
        --cache-dir /opt/git git://git.openstack.org \
        openstack/kolla openstack/requirements
}

function setup_config {
    sudo cp -r etc/kolla /etc/
    # Generate passwords
    sudo tools/generate_passwords.py

    # Use Infra provided pypi.
    # Wheel package mirror may be not compatible. So do not enable it.
    PIP_CONF=$(mktemp)
    cat > ${PIP_CONF} <<EOF
[global]
timeout = 60
index-url = $NODEPOOL_PYPI_MIRROR
trusted-host = $NODEPOOL_MIRROR_HOST
EOF
    echo "RUN echo $(base64 -w0 ${PIP_CONF}) | base64 -d > /etc/pip.conf" | sudo tee /etc/kolla/header
    rm ${PIP_CONF}

    # Get base distro and install type from workspace. The full path looks like
    #   /home/jenkins/workspace/gate-kolla-ansible-dsvm-deploy-centos-source-centos-7-nv

    # NOTE(Jeffrey4l): use different a docker namespace name in case it pull image from hub.docker.io when deplying
    cat <<EOF | sudo tee /etc/kolla/kolla-build.conf
[DEFAULT]
include_header = /etc/kolla/header
namespace = lokolla
base = ${BASE_DISTRO}
install_type = ${INSTALL_TYPE}
profile = gate
registry = 127.0.0.1:4000
push = true

[profiles]
gate = cron,fluentd,glance,haproxy,keepalived,keystone,kolla-toolbox,mariadb,memcached,neutron,nova,openvswitch,rabbitmq,horizon
EOF

    if [[ "${DISTRO}" == "Debian" ]]; then
        # Infra does not sign thier mirrors so we ignore gpg signing in the gate
        echo "RUN echo 'APT::Get::AllowUnauthenticated \"true\";' > /etc/apt/apt.conf" | sudo tee -a /etc/kolla/header

        # Optimize the repos to take advantage of the Infra provided mirrors for Ubuntu
        cat << EOF | sudo tee -a /etc/kolla/kolla-build.conf
apt_sources_list = /etc/kolla/sources.list
EOF
        sudo cp /etc/apt/sources.list /etc/kolla/sources.list
        sudo cat /etc/apt/sources.list.available.d/ubuntu-cloud-archive.list | sudo tee -a /etc/kolla/sources.list
        # Append non-infra provided repos to list
        cat << EOF | sudo tee -a /etc/kolla/sources.list
deb http://nyc2.mirrors.digitalocean.com/mariadb/repo/10.0/ubuntu xenial main
deb http://repo.percona.com/apt xenial main
deb http://packages.elastic.co/elasticsearch/2.x/debian stable main
deb http://packages.elastic.co/kibana/4.6/debian stable main
EOF
    fi
}

function detect_distro {
    DISTRO=$(ansible all -i "localhost," -msetup -clocal | awk -F\" '/ansible_os_family/ {print $4}')
}

# NOTE(sdake): This works around broken nodepool on systems with only one
#              private interface
#              The big regex checks for IP addresses in the file
function setup_workaround_broken_nodepool {
    if [[ `grep -E -o "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" /etc/nodepool/node_private | wc -l` -eq 0 ]]; then
        cp /etc/nodepool/node /etc/nodepool/node_private
        cp /etc/nodepool/sub_nodes /etc/nodepool/sub_nodes_private
    fi
}

function setup_ssh {
    # Generate a new keypair that Ansible will use
    ssh-keygen -f /home/jenkins/.ssh/kolla -N ''
    cat /home/jenkins/.ssh/kolla.pub >> /home/jenkins/.ssh/authorized_keys

    # Push the public key around to all of the nodes
    for ip in $(cat /etc/nodepool/sub_nodes_private); do
        scp /home/jenkins/.ssh/kolla.pub ${ip}:/home/jenkins/.ssh/authorized_keys
        # TODO(SamYaple): Remove this root key pushing once Kolla doesn't
        # require root anymore.
        ssh ${ip} -i /home/jenkins/.ssh/kolla 'sudo mkdir -p /root/.ssh; sudo cp /home/jenkins/.ssh/* /root/.ssh/'
    done

    # From now on use the new IdentityFile for connecting to other hosts
    echo "IdentityFile /home/jenkins/.ssh/kolla" >> /home/jenkins/.ssh/config
}

function setup_inventory {
    local counter=0

    echo -e "127.0.0.1\tlocalhost" > /tmp/hosts
    for ip in $(cat /etc/nodepool/{node_private,sub_nodes_private}); do
        : $((counter++))
        # FIXME(jeffrey4l): do not set two hostnames in oneline. this is a
        # wordround fix for the rabbitmq failed when deploy on CentOS in the CI
        # gate. the ideal fix should set the hostname in setup_gate.sh script.
        # But it do not work as expect with unknown reason
        echo -e "${ip}\tnode${counter}" >> /tmp/hosts
        echo -e "${ip}\t$(ssh ${ip} hostname)" >> /tmp/hosts
        echo "node${counter}" >> ${RAW_INVENTORY}
    done

    sudo chown root: /tmp/hosts
    sudo chmod 644 /tmp/hosts
    sudo mv /tmp/hosts /etc/hosts
}

function setup_ansible {
    RAW_INVENTORY=/tmp/kolla/raw_inventory
    mkdir /tmp/kolla

    # TODO(SamYaple): Move to virtualenv
    sudo -H pip install -U "ansible>=2" "docker-py>=1.6.0" "python-openstackclient" "python-neutronclient" "ara"
    detect_distro

    setup_inventory

    # Record the running state of the environment as seen by the setup module
    ansible all -i ${RAW_INVENTORY} -m setup > /tmp/logs/ansible/initial-setup

    sudo mkdir /etc/ansible
    sudo tee /etc/ansible/ansible.cfg<<EOF
[defaults]
callback_plugins = /usr/lib/python2.7/site-packages/ara/plugins/callbacks:\$VIRTUAL_ENV/lib/python2.7/site-packages/ara/plugins/callbacks
EOF
}

function setup_node {
    ansible-playbook -i ${RAW_INVENTORY} tools/playbook-setup-nodes.yml
}

function setup_logging {
    # This directory is the directory that is copied with the devstack-logs
    # publisher. It must exist at /home/jenkins/workspace/<job-name>/logs
    mkdir logs

    # For ease of access we symlink that logs directory to a known path
    ln -s $(pwd)/logs /tmp/logs
    mkdir -p /tmp/logs/{ansible,build,kolla,kolla_configs,system_logs}
}

function prepare_images {
    docker run -d -p 4000:5000 --restart=always -v /tmp/kolla_registry/:/var/lib/registry --name registry registry:2

    # NOTE(Jeffrey4l): Zuul adds all changes depend on to ZUUL_CHANGES
    # variable. if find "openstack/kolla:" string, it means this patch depends
    # on one of Kolla patch. Then build image by using Kolla's code.
    # Otherwise, pull images from tarballs.openstack.org site.
    if echo "$ZUUL_CHANGES" | grep -q -i "openstack/kolla:"; then
        pushd "${GIT_PROJECT_DIR}/kolla"
        sudo tox -e "build-${BASE_DISTRO}-${INSTALL_TYPE}"
        popd
    else
        BRANCH=$(echo "$ZUUL_BRANCH" | cut -d/ -f2)
        filename=${BASE_DISTRO}-${INSTALL_TYPE}-registry-${BRANCH}.tar.gz
        wget -q -c -O "/tmp/$filename" \
            "http://tarballs.openstack.org/kolla/images/$filename"
        sudo tar xzf "/tmp/$filename" -C /tmp/kolla_registry
    fi
}

setup_logging
tools/dump_info.sh
clone_repos
setup_workaround_broken_nodepool
setup_ssh
setup_ansible
setup_node
setup_config
prepare_images

sudo tools/deploy_aio.sh "${BASE_DISTRO}" "${INSTALL_TYPE}"

tools/dump_info.sh
