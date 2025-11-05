#!/usr/bin/env python3
"""
Exibe explicações com SHAP para um classificador treinado (CNN).
Usamos KernelExplainer para modelos que expõem predict_proba-like function.
Observação: KernelExplainer é lento; usar em amostras pequenas.
"""
import argparse
import numpy as np
import torch
import shap
from src.cnn_model import SimpleCNN1D
import matplotlib.pyplot as plt

def load_model(path, n_features):
    model = SimpleCNN1D(n_features)
    model.load_state_dict(torch.load(path))
    model.eval()
    return model

def model_predict_fn(model, X_numpy):
    # X_numpy: (n, features)
    with torch.no_grad():
        t = torch.tensor(X_numpy, dtype=torch.float32)
        preds = model(t).numpy()
        # KernelExplainer expects probability for cada classe ou único output
        return np.vstack([1-preds, preds]).T

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    data = np.load(args.input)
    X = data["X"]
    y = data["y"]
    model = load_model(args.model, X.shape[1])
    # Escolher background pequeno
    background = X[np.random.choice(len(X), size=min(50,len(X)), replace=False)]
    explainer = shap.KernelExplainer(lambda x: model_predict_fn(model, x)[:,1], background)
    # Explicar primeiras 5 amostras
    to_explain = X[:5]
    shap_values = explainer.shap_values(to_explain, nsamples=100)
    print("SHAP values shape:", np.array(shap_values).shape)
    # plot para a primeira amostra
    shap.force_plot(explainer.expected_value, shap_values[0], to_explain[0], matplotlib=True, show=True)
    plt.show()

if __name__ == "__main__":
    main()