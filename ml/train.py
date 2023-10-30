import os
import math
import pickle

import pytorch_optimizer
import pytorch_lightning as pl

import torch
from torch.utils.data import DataLoader, Dataset
from torch.nn import CrossEntropyLoss

from utils import helper, preprocess, lang_enum, vocab
from model import mbert


DF_PATHONLY_CACHE_PATH = "../datasets/cache/path_only.pickle"
MODEL_RESUME = None
PREPTRAIN_PATH = None
LOGS_DIR = "./logs"
BATCH_SIZE = 512
ACCUMULATE_MAP = {
    0: math.ceil(512 / BATCH_SIZE),
    60: math.ceil(1024 / BATCH_SIZE),
    200: math.ceil(1536 / BATCH_SIZE),
    350: math.ceil(2048 / BATCH_SIZE),
}
NUM_WORKERS = min(20, BATCH_SIZE)
MAX_EPOCHS = 1300
SEED = 9
MAX_INPUT_LEN = 128
WEIGHT_DECAY = 1e-1
BETAS = (0.9, 0.95)
LR = 2e-3
MIN_LR = 2e-4
LABEL_SMOOTHING = 0.15

pl.seed_everything(SEED)
torch.set_float32_matmul_precision("medium")


class CodeDataset(Dataset):
    max_len = 4096

    def __init__(self, df, aug=True):
        df["language_id"] = df["language_tag"].map(lang_enum.languages2num)
        self.paths = df["path"].tolist()
        self.labels = df["language_id"].tolist()

        df["weights"] = 1  # TODO: hotfix for overfitting
        df.loc[df["source"] == "overfit", "weights"] = 1000
        df.loc[df["source"] == "stackoverflow", "weights"] = 20

        self.weights = df["weights"].tolist()

        self.aug = aug

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        with open(self.paths[idx], "r") as f:
            text = f.read()

        if self.aug:
            text = helper.augment(text, lines_num_range=(5, 70))
        text = text[: self.max_len]

        is_empty = len(text) == 0

        attention_mask = torch.zeros(MAX_INPUT_LEN, dtype=torch.bool)
        inputs = preprocess.encode_text(text)[:MAX_INPUT_LEN]
        attention_mask[: len(inputs)] = True

        if len(inputs) < MAX_INPUT_LEN:
            inputs += [vocab.vocab_dict["<PAD>"]] * (MAX_INPUT_LEN - len(inputs))
        inputs = torch.tensor(inputs, dtype=torch.long)
        label = torch.tensor(self.labels[idx] if not is_empty else 0, dtype=torch.long)
        weights = torch.tensor(self.weights[idx], dtype=torch.float32)

        return inputs, attention_mask, label, weights


class LanguageClassifier(pl.LightningModule):
    def __init__(self, pretrain=None, weights=None):
        super().__init__()
        self.model = mbert.get_model(size="t")
        if pretrain is not None:
            self.model = self.model.from_pretrained(pretrain)
        self.weights = torch.tensor(weights, dtype=torch.float32) if weights is not None else None
        self.loss_function = CrossEntropyLoss(
            weight=self.weights, label_smoothing=LABEL_SMOOTHING, reduction="none"
        )

    def forward(self, input_ids, attention_mask=None):
        return self.model(input_ids, attention_mask).logits

    def training_step(self, batch, batch_idx):
        input_ids, attention_mask, labels, weights = batch
        logits = self(input_ids, attention_mask)
        loss = self.loss_function(logits, labels)
        loss = (loss * weights).mean()

        self.log("train/loss", loss, on_step=True, prog_bar=True, logger=True)
        return loss

    def configure_optimizers(self):
        parameters = self.model.parameters()
        optimizer = pytorch_optimizer.AdaBelief(parameters, LR, BETAS, WEIGHT_DECAY)
        train_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, MAX_EPOCHS, MIN_LR)

        return (
            {
                "optimizer": optimizer,
                "lr_scheduler": {
                    "scheduler": train_scheduler,
                    "interval": "epoch",
                    "frequency": 1,
                    "strict": True,
                },
            },
        )


if __name__ == "__main__":
    with open(DF_PATHONLY_CACHE_PATH, "rb") as f:
        df = pickle.load(f)

    dataset = CodeDataset(df)
    train_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)

    weights = helper.compute_class_weights(df, alpha=3.0)  # loss weight based on class frequency
    model = LanguageClassifier(pretrain=PREPTRAIN_PATH, weights=weights)

    exp_name = helper.generate_experiment_name({"bs": BATCH_SIZE, "epochs": MAX_EPOCHS})
    exp_dir = os.path.join(LOGS_DIR, exp_name)

    trainer_cfg = {
        "accelerator": "gpu",
        "devices": 2,
        "sync_batchnorm": True,
        "logger": [
            pl.loggers.TensorBoardLogger(save_dir=exp_dir),
            pl.loggers.WandbLogger(name=exp_name, project="tglang"),
        ],
        "precision": "16-mixed",
        "max_epochs": MAX_EPOCHS,
        "log_every_n_steps": 100,
        "gradient_clip_val": 2.0,
        "check_val_every_n_epoch": 1,
        "callbacks": [
            pl.callbacks.ModelCheckpoint(dirpath=exp_dir, every_n_epochs=1, save_top_k=-1),
            pl.callbacks.LearningRateMonitor(logging_interval="step"),
            pl.callbacks.GradientAccumulationScheduler(scheduling=ACCUMULATE_MAP),
        ],
    }

    trainer = pl.Trainer(**trainer_cfg)

    _ = trainer.fit(model, ckpt_path=MODEL_RESUME, train_dataloaders=train_loader)
