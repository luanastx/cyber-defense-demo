import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN1D(nn.Module):
    """
    Modelo 1D CNN simples para vetores de features.
    Entrada: (batch, features) -> reshape (batch, 1, features)
    Saída: probabilidade binária (0/1)
    """
    def __init__(self, n_features):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 8, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(8, 16, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(16, 1)

    def forward(self, x):
        # x: (batch, n_features)
        x = x.unsqueeze(1)  # (batch, 1, n)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = self.pool(x).squeeze(-1)  # (batch, channels)
        x = self.fc(x)
        return torch.sigmoid(x).squeeze(-1)