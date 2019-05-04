#!/usr/local/bin/python

from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(argument_spec={})
    return_value = {"hello": "world"}
    module.exit_json(change=False, meta=return_value)

if __name__ == '__main__':
    main()
