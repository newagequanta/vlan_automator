#!/usr/local/bin/python

from ansible.module_utils.basic import *
import json

def main():
    '''
    Ansible arguments supported:
        - mac_addr - The MAC address whose VLAN must be changed
        - hostname - Field to exchange the switch hostname (if found)
    '''

    '''
    module_args = {
        'mac_addr': {'default': True, 'type': 'str'},
        'hostname': {'default': False, 'type': 'str'},
        'switchport': {'default': False, 'type': 'str'}
    }
    '''
    module_args = dict(
        mac_addr=dict(default=True, type='str'),
        hostname=dict(default=False, type='str'),
        switchport=dict(default=False, type='str')
    )

    module = AnsibleModule(argument_spec=module_args)

    mac_addr = module.params['mac_addr']

    #Find the Switch with the VLAN

    try:
        with open('files/mac_database.json', 'r') as f_obj:
            macs = json.load(f_obj)
    except:
        return_value = {"MAC Database file not found"}
        module.exit_json(change=False, meta=return_value)
        return
    
    if mac_addr in macs:
        module.params.update({'hostname': macs[mac_addr][0]})
        module.params.update({'switchport': macs[mac_addr][1]})
        module.exit_json(change=True, meta=module.params)
    else:    
        module.exit_json(change=False)

if __name__ == '__main__':
    main()
