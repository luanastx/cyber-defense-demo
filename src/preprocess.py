#!/usr/bin/env python3
"""
Lê CSV de fluxos e retorna arrays prontos para treino/inferência.
Operações:
- Hash simples de IP -> inteiro
- Normalização de colunas numéricas
- Separa X e y (se label presente)
Salva um .npz com X, y (opcional), and feature_names.
"""
import argparse
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import hashlib

def ip_to_int(ip):
    # hash simples (não reversível) para anonimizar
    h = hashlib.sha256(str(ip).encode()).hexdigest()
    return int(h[:16], 16) % (2**31)

def load_and_transform(path):
    df = pd.read_csv(path)
    # fill label if missing
    if "label" not in df.columns:
        df["label"] = 0
    df["src_ip_h"] = df["src_ip"].astype(str).apply(ip_to_int)
    df["dst_ip_h"] = df["dst_ip"].astype(str).apply(ip_to_int)
    features = ["src_ip_h","dst_ip_h","src_port","dst_port","protocol","packets","bytes","duration"]
    X = df[features].fillna(0).values.astype(float)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    y = df["label"].values.astype(int)
    return Xs, y, features, scaler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/preprocessed.npz")
    args = parser.parse_args()
    X, y, feats, scaler = load_and_transform(args.input)
    np.savez_compressed(args.output, X=X, y=y, features=feats)
    print(f"Saved {args.output} with X.shape={X.shape} y.shape={y.shape}")

if __name__ == "__main__":
    main()