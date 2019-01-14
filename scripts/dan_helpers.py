import requests
import json
from lib.commands import *


def get_address_from_domain(domain):
    try:
        domain = domain.replace('+', '')
        domain = domain.strip()

        url = 'http://app1.kpay.to/api/Identity?identity={}'.format(domain)
        response = requests.get(url)
        response_str = response.content.decode('utf-8')
        response_obj = json.loads(response_str)
        addresses = response_obj['BtcAddresses']
        address = get_least_used_address(addresses)

    except Exception as e:
        address = None

    return address


def get_least_used_address(address_list):
    if address_list is None or len(address_list) is 0:
        raise AssertionError
    lowest_usage_count = get_address_usage_count(address_list[0])
    least_used_address_index = 0

    for i in range(0, len(address_list)):
        current_usage_count = get_address_usage_count(address_list[i])
        if current_usage_count < lowest_usage_count:
            lowest_usage_count = current_usage_count
            least_used_address_index = i

    return address_list[least_used_address_index]


def get_address_usage_count(address):
    url = 'http://app1.kpay.to/api/AddressUsage?address={}'.format(address)
    response = requests.get(url)
    response_str = response.content.decode('utf-8')
    response_obj = json.loads(response_str)
    return int(response_obj)


def increment_address_usage_count(address):
    sender = '0x994a635661d8017c0fba4d69569fb0af064031f6'
    url = 'http://app1.kpay.to/api/AddressUsage'
    headers = {"Content-Type": "application/json"}
    body = {"Address": address, "Sender": sender}
    requests.put(url,
                 data=json.dumps(body),
                 headers=headers)


def get_cmd_params():
    parser = get_parser()
    sendto = parser.parse_args().sendto
    amount = parser.parse_args().amount
    cmd_params_dict = {
        "sendto": sendto,
        "amount": amount
    }

    return cmd_params_dict


def is_domain_available(domain):
    return domain == 'dan'


def verify_auth_code(domain, code):
    return code == '123'


def register_domain(domain):
    print(domain + " registered")
