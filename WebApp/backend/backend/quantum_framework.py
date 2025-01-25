import numpy as np
import qiskit
import torch
from torch import nn
from torch.autograd import Function
from qiskit_aer import AerSimulator


class QuantumCircuit:

    def __init__(self, n_qubits, backend, shots):

        self.circuit = qiskit.QuantumCircuit(n_qubits)

        all_qubits = [i for i in range(n_qubits)]
        self.thetas = [qiskit.circuit.Parameter(f"theta{i}") for i in range(n_qubits)]

        self.circuit.h(all_qubits)
        self.circuit.barrier()

        for qubit in all_qubits:
            self.circuit.ry(self.thetas[qubit], qubit)

        self.circuit.barrier()
        self.circuit.measure_all()

        self.backend = backend
        self.shots = shots
        self.n_qubits = n_qubits

    def run(self, thetas):
        binds = [{self.thetas[i]: [thetas[i]] for i in range(len(thetas))}]
        job = self.backend.run(self.circuit, shots=self.shots, parameter_binds=binds)

        result = job.result().get_counts()

        counts = torch.zeros(self.n_qubits)
        for i in range(self.n_qubits):
            for key in result.keys():
                if key[i] == "1":
                    counts[i] += result[key]

        probabilities = counts / self.shots
        return probabilities


class HybridFunction(Function):

    @staticmethod
    def forward(ctx, input, quantum_circuit, shift):
        ctx.shift = shift
        ctx.quantum_circuit = quantum_circuit
        result = (
            torch.stack([ctx.quantum_circuit.run(i.tolist()) for i in input]) * input
        )
        ctx.save_for_backward(input)

        return result

    @staticmethod
    def backward(ctx, grad_output):
        input = ctx.saved_tensors[0]

        shift_right = input + torch.ones_like(input) * ctx.shift
        shift_left = input - torch.ones_like(input) * ctx.shift

        gradients = []
        for i in range(input.shape[0]):
            expectation_right = ctx.quantum_circuit.run(shift_right[i])
            expectation_left = ctx.quantum_circuit.run(shift_left[i])

            gradient = expectation_right - expectation_left
            gradients.append(gradient)
        tensor = torch.stack(gradients).float() * grad_output.float()
        return tensor, None, None


class QuantumLayer(nn.Module):

    def __init__(self, size, backend, shots, shift):
        super().__init__()
        self.quantum_circuit = QuantumCircuit(size, backend, shots)
        self.shift = shift

    def forward(self, input):
        return HybridFunction.apply(input, self.quantum_circuit, self.shift)


class QuantumHybridModel(nn.Module):
    def __init__(self, qubits, shots, shift=np.pi / 2):
        super().__init__()

        self.backend = AerSimulator(method="density_matrix", device="CPU")
        self.fcs = nn.Sequential(
            nn.Linear(3, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 2),
        )
        self.softmax = nn.Softmax(dim=-1)
        self.relu = nn.ReLU()
        self.quantum = QuantumLayer(qubits, self.backend, shots, shift)

    def forward(self, x):

        x = self.fcs(x)
        x = self.quantum(x)

        x = self.softmax(x)

        return x
