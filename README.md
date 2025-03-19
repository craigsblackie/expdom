# Domain Federation and Availability Checker

This script allows you to check the federation information and availability status of domains using the Microsoft Exchange Autodiscover service. It fetches the domain's federation info and verifies its registration status using WHOIS.

## Features

- Fetches federation information for domains.
- Checks the registration status of domains using WHOIS.
- Supports checking a single domain or processing a list of domains from a file.
- Displays the results in color-coded output (green for registered domains, red for non-registered).

## Requirements

To run this script, you'll need the following Python packages:

- `requests`: For making HTTP requests to the Autodiscover service.
- `whois`: To query domain registration information using WHOIS.
- `xml.etree.ElementTree`: For parsing XML responses.

You can install the necessary dependencies using pip:

```bash
pip install requests python-whois
```

## Usuage

Check a single domain:

To check the federation information and availability status of a single domain, run the script with the domain name as an argument:

```bash
python script.py <domain_name>
```

Check domains from a file:

To check multiple domains from a file, pass the file path as an argument. The file should contain one domain per line:

```bash
python script.py <file_path>
```
