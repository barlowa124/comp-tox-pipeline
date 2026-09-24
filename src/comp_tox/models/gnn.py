"""GNN baseline: GIN over molecular graphs, Platt-calibrated on validation.

Small baseline architecture: 3x GINConv + global mean pool +
linear head. Trained with BCEWithLogitsLoss(pos_weight) for class imbalance;
Platt scaling is fit on validation logits exactly like the fingerprint
baselines so comparison is on identical splits and identical calibration.
"""

from __future__ import annotations

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from torch import nn
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GINConv, global_mean_pool


class GINNet(nn.Module):
    def __init__(self, in_dim: int = 8, hidden: int = 64):
        super().__init__()
        self.convs = nn.ModuleList(
            [
                GINConv(
                    nn.Sequential(
                        nn.Linear(in_dim if i == 0 else hidden, hidden),
                        nn.ReLU(),
                        nn.Linear(hidden, hidden),
                        nn.ReLU(),
                    )
                )
                for i in range(3)
            ]
        )
        self.head = nn.Linear(hidden, 1)

    def forward(self, x, edge_index, batch):
        for conv in self.convs:
            x = conv(x, edge_index)
        return self.head(global_mean_pool(x, batch)).squeeze(-1)


class GNNWrapper:
    """Sklearn-style predict_proba over lists of (x, edge_index, edge_attr)."""

    def __init__(self, net: GINNet, platt: LogisticRegression | None):
        self.net = net
        self.platt = platt

    def _logits(self, graphs) -> np.ndarray:
        self.net.eval()
        data = [
            Data(x=g[0], edge_index=g[1], edge_attr=g[2]) for g in graphs
        ]
        out = []
        with torch.no_grad():
            for batch in DataLoader(data, batch_size=256):
                out.append(
                    self.net(batch.x, batch.edge_index, batch.batch)
                )
        return torch.cat(out).numpy()

    def predict_proba(self, graphs) -> np.ndarray:
        logits = self._logits(graphs)
        if self.platt is not None:
            p = self.platt.predict_proba(logits.reshape(-1, 1))[:, 1]
        else:
            p = 1.0 / (1.0 + np.exp(-logits))
        return np.column_stack([1.0 - p, p])


def train_gnn(
    graphs, df, tr_mask, va_mask, seed: int, epochs: int = 20
) -> GNNWrapper:
    torch.manual_seed(seed)
    train_graphs = [graphs[i] for i in np.where(tr_mask)[0]]
    y_tr = df["label"].to_numpy()[tr_mask].astype(np.float32)

    net = GINNet()
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    pos_weight = torch.tensor([(len(y_tr) - y_tr.sum()) / max(y_tr.sum(), 1)])
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    loader = DataLoader(
        [
            Data(x=g[0], edge_index=g[1], edge_attr=g[2], y=torch.tensor([y]))
            for g, y in zip(train_graphs, y_tr)
        ],
        batch_size=64,
        shuffle=True,
    )
    net.train()
    for epoch in range(epochs):
        total = 0.0
        for batch in loader:
            opt.zero_grad()
            loss = loss_fn(
                net(batch.x, batch.edge_index, batch.batch), batch.y
            )
            loss.backward()
            opt.step()
            total += loss.item() * batch.num_graphs
        if (epoch + 1) % 5 == 0:
            print(f"  gnn epoch {epoch + 1}/{epochs} loss {total / len(y_tr):.4f}")

    wrapper = GNNWrapper(net, platt=None)
    valid_graphs = [graphs[i] for i in np.where(va_mask)[0]]
    y_va = df["label"].to_numpy()[va_mask]
    platt = LogisticRegression(max_iter=1000)
    platt.fit(wrapper._logits(valid_graphs).reshape(-1, 1), y_va)
    wrapper.platt = platt
    return wrapper
