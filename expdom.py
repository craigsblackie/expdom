import requests
import sys
import xml.etree.ElementTree as ET
import whois
import os

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def is_primary_domain(domain_name):
    parts = domain_name.split('.')
    return len(parts) == 2 or (len(parts) == 3 and parts[1].lower() in ['co', 'com', 'org', 'net'])

def get_federation_information(domain):
    url = "https://autodiscover-s.outlook.com/autodiscover/autodiscover.svc"
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    body = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:exm="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:ext="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:a="http://www.w3.org/2005/08/addressing" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<soap:Header>
    <a:Action soap:mustUnderstand="1">http://schemas.microsoft.com/exchange/2010/Autodiscover/Autodiscover/GetFederationInformation</a:Action>
    <a:To soap:mustUnderstand="1">https://autodiscover-s.outlook.com/autodiscover/autodiscover.svc</a:To>
    <a:ReplyTo>
        <a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address>
    </a:ReplyTo>
</soap:Header>
<soap:Body>
    <GetFederationInformationRequestMessage xmlns="http://schemas.microsoft.com/exchange/2010/Autodiscover">
        <Request>
            <Domain>{domain}</Domain>
        </Request>
    </GetFederationInformationRequestMessage>
</soap:Body>
</soap:Envelope>"""

    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        namespaces = {
            'x': 'http://schemas.microsoft.com/exchange/2010/Autodiscover',
        }
        for domain_element in root.findall('.//x:Domain', namespaces):
            domain_name = domain_element.text
            if is_primary_domain(domain_name):
                check_domain_availability(domain_name)
    else:
        print(f"{RED}Error fetching federation information: {response.status_code}{RESET}")

def check_domain_availability(domain_name):
    try:
        domain_info = whois.whois(domain_name)
        if domain_info.status:
            print(f"{GREEN}{domain_name} is registered.{RESET}")
        else:
            print(f"{RED}{domain_name} is not registered or availability could not be determined.{RESET}")
    except whois.parser.PywhoisError:
        print(f"{RED}{domain_name} is not registered or availability could not be determined.{RESET}")
    except Exception as e:
        print(f"{RED}Error checking domain {domain_name}: {e}{RESET}")

def process_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        for domain in file:
            domain = domain.strip()
            if domain:  # Ensure the line is not empty
                get_federation_information(domain)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{RED}Usage: python script.py <domain or file path>{RESET}")
        sys.exit(1)

    input_arg = sys.argv[1]
    if os.path.isfile(input_arg):
        process_domains_from_file(input_arg)
    else:
        get_federation_information(input_arg)
