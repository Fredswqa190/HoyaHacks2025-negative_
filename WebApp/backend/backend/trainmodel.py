import copy
import datetime
import os
import time

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm
import pandas as pd

from quantum_framework import QuantumHybridModel

starttime = time.time()
NUM_EPOCHS = 100
BATCH_SIZE = 128
CHECKPOINT_DIR = f"data/checkpoints/{int(starttime)}_quantum/"
LOG_DIR = f"data/logs/{int(starttime)}_quantum"
NUM_WORKERS = 16

training_df = pd.read_csv("train_data.csv").drop("date", axis=1)
validation_df = pd.read_csv("validation_data.csv").drop("date", axis=1)
training_data = TensorDataset(
    torch.tensor(training_df.drop("Occupancy", axis=1).values, dtype=torch.float),
    torch.tensor(training_df["Occupancy"].values, dtype=torch.int64),
)
validation_data = TensorDataset(
    torch.tensor(training_df.drop("Occupancy", axis=1).values, dtype=torch.float),
    torch.tensor(training_df["Occupancy"].values, dtype=torch.int64),
)

train_loader = DataLoader(
    training_data,
    batch_size=BATCH_SIZE,
    shuffle=True,
    # pin_memory=True,
    num_workers=NUM_WORKERS,
)

val_loader = DataLoader(
    validation_data,
    batch_size=BATCH_SIZE,
    shuffle=True,
    # pin_memory=True,
    num_workers=NUM_WORKERS,
)

model = QuantumHybridModel(qubits=2, shots=1000)

optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()

os.makedirs(CHECKPOINT_DIR, exist_ok=True)
writer = SummaryWriter(LOG_DIR)
best_accuracy = 0.0
best_model_wts = copy.deepcopy(model.state_dict())

for epoch in range(NUM_EPOCHS):
    print(f"Epoch {epoch+1}/{NUM_EPOCHS}")
    print("=" * 61)

    running_loss = 0.0
    running_corrects = 0

    model.train()
    print("Training")

    progressbar = tqdm(train_loader, unit="steps", dynamic_ncols=True)

    for index, (inputs, labels) in enumerate(progressbar):

        inputs, labels = inputs, labels

        optimizer.zero_grad()

        outputs = model(inputs)

        loss = loss_fn(outputs, labels)
        loss.backward()

        optimizer.step()

        running_loss += loss.item()
        running_corrects += (outputs.argmax(1) == labels).sum() / BATCH_SIZE

        progressbar.set_description(
            f"Loss: {running_loss/(index+1):.5f}, Accuracy: {running_corrects/(index+1):.2%}"
        )
        progressbar.refresh()

    epoch_loss = running_loss / len(train_loader)
    epoch_accuracy = running_corrects / len(train_loader)

    running_loss = 0.0
    running_corrects = 0

    model.eval()
    print("\nValidation")

    progressbar = tqdm(val_loader, unit="steps", dynamic_ncols=True)

    for index, (inputs, labels) in enumerate(progressbar):

        inputs, labels = inputs, labels

        with torch.no_grad():
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)

        running_loss += loss.item()
        running_corrects += (outputs.argmax(1) == labels).sum() / BATCH_SIZE

        progressbar.set_description(
            f"Loss: {running_loss/(index+1):.5f}, Accuracy: {running_corrects/(index+1):.2%}"
        )
        progressbar.refresh()

    val_loss = running_loss / len(val_loader)
    val_accuracy = running_corrects / len(val_loader)

    if val_accuracy > best_accuracy:
        best_accuracy = val_accuracy
        best_model_wts = copy.deepcopy(model.state_dict())
        torch.save(
            best_model_wts,
            os.path.join(CHECKPOINT_DIR, "best_weights.pth"),
        )

    loss_data = {"Training": epoch_loss, "Validation": val_loss}
    accuracy_data = {"Training": epoch_accuracy, "Validation": val_accuracy}
    writer.add_scalars("Loss", loss_data, epoch + 1)
    writer.add_scalars("Accuracy", accuracy_data, epoch + 1)
    writer.flush()

    checkpoint_path = os.path.join(CHECKPOINT_DIR, f"checkpoint-{epoch:03d}.pth")

    torch.save(model.state_dict(), checkpoint_path)
    print(f"Checkpoint saved to {checkpoint_path}\n")
writer.close()

time_elapsed = time.time() - starttime
print(f"Training complete in {datetime.timedelta(seconds=time_elapsed)}")

model.load_state_dict(best_model_wts)

print("Saving model")

savepath = f"data/models/{int(starttime)}_quantum.pth"
savepath_weights = f"data/models/{int(starttime)}_weights_quantum.pth"

torch.save(model.state_dict(), savepath_weights)
torch.save(model, savepath)
print("Model saved!")
