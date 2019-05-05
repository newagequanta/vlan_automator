#!/usr/local/bin/python

from ansible.module_utils.basic import *
import json

def main():
    '''
    Ansible arguments supported:
        - mac_addr - The MAC address whose VLAN must be changed
        - hostname - Field to exchange the switch hostname (if found)
    '''

    fields = {
        'mac_addr': {'default': True, 'type': 'str'},
        'hostname': {'default': False, 'type': 'str'}
    }

    module = AnsibleModule(argument_spec=fields)

    mac_addr = module.params['mac_addr']

    #Find the Switch with the VLAN

    try:
        with open('mac_db_mac_based.json', 'r') as f_obj:
            macs = json.load(f_obj)['macs'][0]
    except:
        return_value = {"MAC Database file not found"}
        module.exit_json(change=False, meta=return_value)
        return
    
    if mac_addr in macs:
        #module.params.update({'hostname': 'SW1'})
        module.params.update({'hostname': macs[mac_addr][0]})
        module.exit_json(change=True, meta=module.params)
    else:    
        module.exit_json(change=False)

if __name__ == '__main__':
    main()
