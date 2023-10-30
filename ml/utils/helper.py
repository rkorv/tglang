import datetime

import numpy as np

from utils import lang_enum


def augment(text, lines_num_range=(5, 120)):
    text_list = text.split("\n")
    random_len = min(np.random.randint(*lines_num_range), len(text_list))
    random_start = (
        np.random.randint(0, len(text_list) - random_len) if len(text_list) > random_len else 0
    )
    return "\n".join(text_list[random_start : random_start + random_len])


def generate_experiment_name(hyperparameters, prefix=None):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    hyperparameters_str = "_".join(f"{key}={value}" for key, value in hyperparameters.items())
    experiment_name = f"{date_time}_{hyperparameters_str}"

    if prefix is not None:
        experiment_name = f"{prefix}_{experiment_name}"

    return experiment_name


def compute_class_weights(df, alpha=6.0):
    groups = df.groupby("language_tag").count()
    labels = groups.index.values
    counts = groups.language.values

    counts = (counts.max() - counts) + counts.min()
    inv_freq = 1.0 / counts
    inv_freq_norm = inv_freq / np.sum(inv_freq)
    exponential_weights = np.power(counts, alpha) / np.sum(np.power(counts, alpha))
    combined_weights = inv_freq_norm * exponential_weights
    normalized_weights = combined_weights / np.sum(combined_weights)
    normalized_weights = normalized_weights * 1000 + 1

    weights = np.ones_like(labels, dtype=np.float32)
    for label, weight in zip(labels, normalized_weights):
        weights[lang_enum.languages2num[label]] = weight
    return weights / weights.mean()
