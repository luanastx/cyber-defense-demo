"""
Regras heurísticas simples para detecção imediata.
Exemplos:
- Too many attempts from same src_ip em janela curta
- Tráfego incomum em portas sensíveis (ex.: porta 22)
"""
from collections import defaultdict
import time

def simple_threshold_by_ip(rows, attempt_threshold=100, window_seconds=60):
    """
    rows: lista de dicionários com keys: timestamp, src_ip, ...
    Retorna lista de src_ip suspeitos.
    """
    now = time.time()
    counts = defaultdict(int)
    for r in rows:
        ts = r.get("timestamp", now)
        if now - ts <= window_seconds:
            counts[r["src_ip"]] += 1
    return [ip for ip,c in counts.items() if c >= attempt_threshold]

def suspicious_ports(rows, ports=(22,)):
    suspects = []
    for r in rows:
        if int(r.get("dst_port",0)) in ports:
            # Heurística simples: muitos pacotes para porta sensível
            if r.get("packets",0) > 20:
                suspects.append((r["src_ip"], r["dst_port"]))
    return suspects

if __name__ == "__main__":
    # Exemplo de uso
    sample = [
        {"timestamp": time.time(), "src_ip": "1.2.3.4", "dst_port": 22, "packets": 30},
        {"timestamp": time.time()-10, "src_ip": "1.2.3.4", "dst_port": 22, "packets": 5},
    ]
    print("threshold:", simple_threshold_by_ip(sample, attempt_threshold=2, window_seconds=60))
    print("suspicious:", suspicious_ports(sample, ports=(22,)))