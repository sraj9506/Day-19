#!/usr/bin/env python3
import json
import boto3
def get_inventory():
    ec2 = boto3.client('ec2', region_name='us-east-1')  # Specify your region
    response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['instance']}])
    inventory = {
        'frontend': {
            'hosts': [],
            'vars': {}
        },
        'backend': {
            'hosts': [],
            'vars': {}
        },
        'database': {
            'hosts': [],
            'vars': {}
        },
        '_meta': {
            'hostvars': {}
        }
    }
    ssh_key_file = '/home/einfochips/Downloads/my-key.pem'  # Path to your SSH private key file
    ssh_user = 'ubuntu'  # SSH username
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            public_dns = instance.get('PublicDnsName', instance['InstanceId'])
            public_ip = instance.get('PublicIpAddress', instance['InstanceId']) 
            # Add the instance to multiple groups
            for group in inventory:
                if group != '_meta':
                    inventory[group]['hosts'].append(public_dns)
            # Add host variables for the instance
            inventory['_meta']['hostvars'][public_dns] = {
                'ansible_host': public_ip,
                'ansible_ssh_private_key_file': ssh_key_file,
                'ansible_user': ssh_user
            }

    return inventory
if __name__ == '__main__':
    print(json.dumps(get_inventory(), indent=4))
