#!/usr/local/bin/python

from ansible.module_utils.basic import AnsibleModule
import re
import csv
import json
import os

def main():
    '''
    Ansible arguments supported:
        - hostname - The hostname of the switch that will appear in the
                     database
        - raw_data
            - List variable
            - 0 Index - Output of the "show mac address-table"
            - 1 Index - Output of the "show interface status"
    '''
    '''
    module_args = {
        'hostname': {'default': True, 'type': 'str'},
        'raw_data': {'default': True, 'type': 'list'},
    }
    '''
    module_args = dict(
        hostname=dict(type='str', default=True),
        raw_data=dict(type='list', default=True)
    )

    #Mandatory for Ansible
    module = AnsibleModule(argument_spec=module_args)

    #RegEx to find MAC
    mac_exp = re.compile(r'(([\d,A-F,a-f]{4}\.){2}[\d,A-F,a-f]{4})')

    #List of all trunk interfaces
    trunks = []

    macs = []
    macs_dict_hostname = {}

    hostname = module.params['hostname']
    show_mac = module.params['raw_data'][0].split('\n')
    show_int_status = module.params['raw_data'][1].split('\n')

    #Load the file into a dictionary if it exists, create if it does not
    '''
    Since files will be separated on a host by host basis, this is not needed
    
    try:
        f_obj = open('mac_db_mac_based.json', 'r')
        macs_dict_mac = json.load(f_obj)['macs'][0]
        f_obj.close()
    except:
        macs_dict_mac = {}
    '''

    for line in show_int_status:
        if 'trunk' in line:
            trunks.append(line.split()[0])

    #print(trunks)

    macs_dict_mac = {}
    #for line in module.params['raw_data']:
    for line in show_mac:
        re_result = mac_exp.findall(line)
        if re_result:
            line_list = line.split()
            if line_list[3] in trunks:
                continue
            mac_addr = line_list[1]
            if_num = line_list[3]

            #Experimental CSV format
            macs.append([hostname, mac_addr, if_num])

            #Experimental JSON format keyed off the switch hostname
            if hostname in macs_dict_hostname:
                macs_dict_hostname[hostname].append([mac_addr, if_num])
            else:
                macs_dict_hostname[hostname] = [[mac_addr, if_num]]

            #Currently supported JSON format keyed off the MAC addresses
            macs_dict_mac[mac_addr] = [hostname, if_num]

    '''
    Filesnames are now based on hostnames and in a separate directory
    f_obj = open('mac_db_mac_based.json', 'w')
    #json.dump({"macs": [macs_dict_mac]}, f_obj)
    json.dump(macs_dict_mac, f_obj)
    f_obj.close()
    '''
    
    '''
    Removing the directory creation responsibility from Python as it was added
    to Ansible
    try:
        with open('temp_files/{}.json'.format(hostname), 'w') as f_obj:
            json.dump(macs_dict_mac, f_obj)
    except IOError:
        os.mkdir('temp_files')
        with open('temp_files/{}.json'.format(hostname), 'w')as f_obj:
            json.dump(macs_dict_mac, f_obj)
    '''
    with open('temp_files/{}.json'.format(hostname), 'w')as f_obj:
        json.dump(macs_dict_mac, f_obj)

    '''
    Uncomment this code for use with Python 3
    except FileNotFoundError:
        os.mkdir('temp_files')
        with open('temp_files/{}.json'.format(hostname), 'w')as f_obj:
            json.dump(macs_dict_mac, f_obj)
    '''

    return_value = {"file": "created"}
    module.exit_json(change=False, meta=return_value)

if __name__ == '__main__':
    main()
