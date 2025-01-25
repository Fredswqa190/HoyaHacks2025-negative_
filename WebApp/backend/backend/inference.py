import torch

from quantum_framework import QuantumHybridModel


def load_model(filename):
    model = QuantumHybridModel(2, 1000)
    model.load_state_dict(torch.load(filename))
    model.eval()

    return model
