ansible address-instance-1 -m hostname -a name='lt-2021-094-webserver1' -i inventory --become
ansible address-instance-2 -m hostname -a name='lt-2021-094-webserver2' -i inventory --become