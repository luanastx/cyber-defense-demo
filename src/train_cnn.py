#!/usr/bin/env python3
import argparse
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader
from torch import optim
from src.cnn_model import SimpleCNN1D
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def train(X, y, model_path="output/cnn.pth", epochs=10, batch_size=64):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    train_ds = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.float32))
    val_ds = TensorDataset(torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.float32))
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)
    model = SimpleCNN1D(X.shape[1])
    opt = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.BCELoss()

    for e in range(epochs):
        model.train()
        pbar = tqdm(train_loader, desc=f"Epoch {e+1}/{epochs}")
        for xb, yb in pbar:
            opt.zero_grad()
            preds = model(xb)
            loss = loss_fn(preds, yb)
            loss.backward()
            opt.step()
            pbar.set_postfix(loss=loss.item())
        # validação rápida
        model.eval()
        with torch.no_grad():
            losses = []
            correct = 0
            total = 0
            for xb, yb in val_loader:
                preds = model(xb)
                loss = loss_fn(preds, yb)
                losses.append(loss.item())
                pred_labels = (preds >= 0.5).int().numpy()
                correct += (pred_labels == yb.numpy().astype(int)).sum()
                total += len(yb)
            print(f"Val loss={np.mean(losses):.4f} acc={correct/total:.4f}")
    torch.save(model.state_dict(), model_path)
    print(f"Saved model to {model_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help=".npz com X e y")
    parser.add_argument("--model", default="output/cnn.pth")
    args = parser.parse_args()
    data = np.load(args.input)
    X = data["X"]
    y = data["y"]
    train(X, y, model_path=args.model, epochs=5)

if __name__ == "__main__":
    main()