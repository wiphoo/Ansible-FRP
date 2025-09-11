#!/bin/bash
# Set environment for collections
export ANSIBLE_COLLECTIONS_PATHS="./collections:~/.ansible/collections"
export ANSIBLE_ROLES_PATH="./roles:~/.ansible/roles"

# Install collection if not present
if [ ! -d "./collections/ansible_collections/wiphoo/frp" ]; then
    echo "Installing wiphoo.frp collection..."
    ansible-galaxy collection install wiphoo.frp -p ./collections
fi

# Run your playbook
ansible-playbook -i inventory site.yml
