#!/usr/bin/env python3
"""
Gera um CSV simples com "fluxos" sintéticos para testes.
Cada linha contém:
timestamp,src_ip,dst_ip,src_port,dst_port,protocol,packets,bytes,duration,label
label: 0 benign, 1 malicious
"""
import csv
import random
import argparse
import time
from ipaddress import IPv4Address

def random_ip():
    return str(IPv4Address(random.getrandbits(32)))

def make_row(now):
    src = random_ip()
    dst = random_ip()
    sport = random.randint(1024, 65535)
    dport = random.choice([22, 80, 443, 8080, random.randint(1024,65535)])
    proto = random.choice([6, 17])  # TCP=6 UDP=17
    # Decide label with small probability for malicious
    label = 1 if random.random() < 0.1 else 0
    if label == 1:
        # malicious flows: many small packets or fast repeated connections
        packets = random.randint(10, 200)
        bytes_ = random.randint(100, 10000)
        duration = max(0.01, random.random()*5)
    else:
        packets = random.randint(1, 20)
        bytes_ = random.randint(40, 15000)
        duration = max(0.01, random.random()*60)
    return [now, src, dst, sport, dport, proto, packets, bytes_, duration, label]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--output", default="data/flows.csv")
    args = parser.parse_args()

    with open(args.output, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp","src_ip","dst_ip","src_port","dst_port","protocol","packets","bytes","duration","label"])
        now = int(time.time())
        for i in range(args.n):
            row = make_row(now + i)
            w.writerow(row)
    print(f"Wrote {args.output}")

if __name__ == "__main__":
    main()