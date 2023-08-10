import requests
import socket
import os
import ssl
import time
import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import json

def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def print_banner():
    clear_screen()
    print('\033[91m' + " __         ___            ____  " + '\033[0m')
    print('\033[31m' + "/ _\       / __\__ _ _ __ |___ \ " + '\033[0m')
    print('\033[31m' + "\ \ _____ / /  / _` | '_ \  __) |" + '\033[0m')
    print('\033[31;2m' + "_\ \_____/ /__| (_| | | | |/ __/" + '\033[0m')
    print('\033[31;2m' + "\__/     \____/\__,_|_| |_|_____| [CODEBREAKERS]\n" + '\033[0m')
    print("\033[1;31;40mS-can2.py | Professional Security Osint tool for Codebreakers Community.\n")
    print("\033[1;36;40mCoded by SqLoSt / https://github.com/SqLoSt\n")

def print_color(text, color):
    colors = {
        'red': '\033[91m',
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'reset': '\033[0m'
    }
    if color in colors:
        print(f"{colors[color]}{text}{colors['reset']}")
    else:
        print(text)

def get_host_info(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    print_color("[*] Host Information:", 'cyan')
    print(f" [-] Host: {host}")

    try:
        ip_address = socket.gethostbyname(host)
        print(f" [-] DNS Information: {ip_address}")
    except socket.gaierror:
        print_color("[!] DNS resolution failed.", 'red')

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        print(f" [-] Method: {response.request.method}")
        print(f" [-] Status Code: {response.status_code} ({response.reason})")
    except requests.exceptions.RequestException:
        print_color("[!] Failed to retrieve method and status code.", 'red')

    return ip_address

def check_security(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    print_color("[*] Security Information:", 'cyan')

    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                subject = dict(x[0] for x in cert['subject'])
                issuer = dict(x[0] for x in cert['issuer'])
                valid_until = ssl.cert_time_to_seconds(cert['notAfter'])
                version = ssl.get_protocol_name(ssock.version())
                print(f" [-] SSL Certificate:")
                print(f"     - Subject: {subject}")
                print(f"     - Issued by: {issuer}")
                print(f"     - Valid until: {time.ctime(valid_until)}")
                print(f"     - Security Protocol: {version}")
    except ssl.SSLError:
        print_color("[!] SSL certificate is not valid.", 'red')
    except socket.gaierror:
        print_color("[!] Failed to establish SSL connection.", 'red')

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        security_headers = response.headers
        print(" [-] Security Headers:")
        for header, value in security_headers.items():
            print(f"     - {header}: {value}")
    except requests.exceptions.RequestException:
        print_color("[!] Failed to retrieve security headers.", 'red')

def get_website_title(url):
    print_color("[*] Website Title:", 'cyan')
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip() if soup.title else "Not found"
        print(f" [-] Title: {title}")
    except requests.exceptions.RequestException:
        print_color("[!] Failed to retrieve website title.", 'red')

def get_website_headers(url):
    print_color("[*] Website Headers:", 'cyan')
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        headers = response.headers
        for header, value in headers.items():
            print(f" [-] {header}: {value}")
    except requests.exceptions.RequestException:
        print_color("[!] Failed to retrieve website headers.", 'red')

def perform_whois_lookup(domain_name):
    print_color("[*] WHOIS Lookup:", 'cyan')
    try:
        whois_result = socket.getaddrinfo(domain_name, None, socket.AF_INET, socket.SOCK_STREAM)
        for result in whois_result:
            ip = result[-1][0]
            print(f" [-] IP Address: {ip}")
    except Exception as e:
        print_color(f"[!] WHOIS lookup failed: {str(e)}", 'red')

def check_ports(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    print_color("[*] Port Information:", 'cyan')
    try:
        for port in range(1, 100):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f" [-] Port {port} is open")
            sock.close()
    except socket.gaierror:
        print_color("[!] Failed to check open ports.", 'red')

def ask_another():
    answer = input("\n[?] Do you want to check another URL? (y/n): ")
    if answer.lower() == 'y':
        main()
    else:
        print("\n[*] Thanks For Using S-Can2 Program terminated.")
        sys.exit()

def main():
    print_banner()
    print_color("[?] Please enter the URL or IP address (with http / https):", 'yellow')
    url = input("[URL/IP] ")

    ip_address = get_host_info(url)
    print()
    check_security(url)
    print()
    get_website_title(url)
    print()
    get_website_headers(url)
    print()
    perform_whois_lookup(ip_address)
    print()
    check_ports(url)

    ask_another()

main()
