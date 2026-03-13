import torch
from torch.utils.tensorboard import SummaryWriter
from tqdm.autonotebook import tqdm
import time
import numpy as np
import os
import shutil

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def train(model, train_dataloader, epochs, lr, loss_fn, val_dataloader=None, clip_grad=False, method=None, input_sequence=None):
    model.to(device)
    optim = torch.optim.Adam(lr=lr, params=model.parameters())

    train_losses = []
    for epoch in range(epochs):
        epoch_loss = 0
        batch_total = 0

        start_time = time.time()
        for step, (model_input, gt) in enumerate(train_dataloader):
            model_input = {k: v.to(device) for k, v in model_input.items()}
            gt = {k: v.to(device) for k, v in gt.items()}

            model_output = model(model_input)
            losses = loss_fn(model_output, gt)

            train_loss = 0.
            for loss_name, loss in losses.items():
                single_loss = loss.mean()
                train_loss += single_loss

            epoch_loss += train_loss.item()
            batch_total += 1
            train_losses.append(train_loss.item())

            optim.zero_grad()
            train_loss.backward()

            if clip_grad:
                if isinstance(clip_grad, bool):
                    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.)
                else:
                    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=clip_grad)

            optim.step()

        avg_train_loss = epoch_loss / max(batch_total, 1)

        model.eval()
        with torch.no_grad():
            val_loss_sum = 0.0
            val_batch_count = 0
            for (model_input, gt) in val_dataloader:
                model_input = {k: v.to(device) for k, v in model_input.items()}
                gt = {k: v.to(device) for k, v in gt.items()}
                model_output = model(model_input)
                losses = loss_fn(model_output, gt)
                batch_val = 0.0
                for loss_name, loss in losses.items():
                    batch_val += loss.mean().item()
                val_loss_sum += batch_val
                val_batch_count += 1
            avg_val_loss = val_loss_sum / max(val_batch_count, 1)

        epoch_time = time.time() - start_time

        # 每 50 个 epoch 打印一次当前 epoch 的 loss
        if epoch % 50 == 0:
            print("Epoch %d, Train loss %0.6f, Val loss %0.6f, time %0.4fs" % (epoch, avg_train_loss, avg_val_loss, epoch_time))
        model.train()


