
from ansible.module_utils.basic import AnsibleModule
import requests

def add_ipam_entry(api_url, ip, hostname, username, password):
 
    payload = {
        "ip": ip,
        "hostname": hostname,
        "username": username,
        "password": password
    }
    response = requests.post(f"{api_url}/ipam", json=payload)
    return response.status_code, response.json()

def main():
    module_args = dict(
        api_url=dict(type='str', required=True),
        ip=dict(type='str', required=True),
        hostname=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    api_url = module.params['api_url']
    ip = module.params['ip']
    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']

    if module.check_mode:
        module.exit_json(changed=False)

    status_code, response = add_ipam_entry(api_url, ip, hostname, username, password)

    if status_code == 201:
        module.exit_json(changed=True, response=response)
    else:
        module.fail_json(msg="Échec de l'ajout de l'entrée", status_code=status_code, response=response)

if __name__ == '__main__':
    main()