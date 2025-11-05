#!/usr/bin/env python3
"""
Extrai features básicas de pacotes/pcap para um CSV de fluxos.
Nota: capturar em interface real requer privilégios; use --pcap para ler de arquivo pcap.
Este script implementa extracao simplificada: agrega por tupla (src,dst,srcport,dstport,proto).
"""
import argparse
import csv
from collections import defaultdict
try:
    from scapy.all import sniff, rdpcap, IP, TCP, UDP
except Exception:
    sniff = None
    rdpcap = None
    IP = TCP = UDP = None

def packet_to_tuple(pkt):
    if not IP in pkt:
        return None
    ip = pkt[IP]
    proto = ip.proto
    sport = 0
    dport = 0
    if TCP in pkt:
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        proto = 6
    elif UDP in pkt:
        sport = pkt[UDP].sport
        dport = pkt[UDP].dport
        proto = 17
    return (ip.src, ip.dst, sport, dport, proto)

def process_packets(packets):
    flows = defaultdict(lambda: {"packets":0, "bytes":0, "first_ts":None, "last_ts":None})
    for pkt in packets:
        key = packet_to_tuple(pkt)
        if not key:
            continue
        ts = float(getattr(pkt, "time", 0.0))
        length = len(pkt)
        f = flows[key]
        f["packets"] += 1
        f["bytes"] += length
        if f["first_ts"] is None:
            f["first_ts"] = ts
        f["last_ts"] = ts
    # write out rows
    rows = []
    for (src,dst,sport,dport,proto), v in flows.items():
        duration = (v["last_ts"] - v["first_ts"]) if (v["first_ts"] and v["last_ts"]) else 0.0
        rows.append([int(v["first_ts"] or 0), src, dst, sport, dport, proto, v["packets"], v["bytes"], duration, ""])
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pcap", help="Arquivo pcap para ler (se omitido, tentará sniff na interface)")
    parser.add_argument("--output", default="data/flows_from_pcap.csv")
    args = parser.parse_args()

    if args.pcap:
        if rdpcap is None:
            raise RuntimeError("scapy não disponível")
        pkts = rdpcap(args.pcap)
        rows = process_packets(pkts)
    else:
        if sniff is None:
            raise RuntimeError("scapy não disponível")
        print("Sniffing por 10s (Ctrl-C para parar)...")
        pkts = sniff(timeout=10)
        rows = process_packets(pkts)
    # salvar CSV
    with open(args.output, "w", newline="") as f:
        import csv
        w = csv.writer(f)
        w.writerow(["timestamp","src_ip","dst_ip","src_port","dst_port","protocol","packets","bytes","duration","label"])
        for r in rows:
            w.writerow(r)
    print(f"Wrote {args.output}")

if __name__ == "__main__":
    main()