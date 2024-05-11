import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ENCODINGS = ["ASCII", "UTF-8", "UTF-16", "UTF-32"]


utf8_repr = {"A": 0b01000001, "C": 0b01000011, "T": 0b01010100, "G": 0b01000111}
compact_repr = {"A": 0, "C": 1, "T": 2, "G": 3}

def get_binary_repr(seq: str, to_chunks=False):
    seq = np.array([utf8_repr[c] for c in seq], dtype=np.uint8)

    # each element is an 8-bit integer, so we need to convert it to a binary string
    binary_repr = np.array([np.binary_repr(i, width=8) for i in seq], dtype=object)

    # convert the binary string to a numpy array of integers
    binary_repr = np.array([[int(c) for c in s] for s in binary_repr], dtype=np.uint8)

    if not to_chunks:
        return np.concatenate(binary_repr)

    return binary_repr


def get_compact_repr(seq: str, to_chunks=False):
    seq = np.array([compact_repr[c] for c in seq], dtype=np.uint8)

    # each element is an 8-bit integer, so we need to convert it to a binary string
    binary_repr = np.array([np.binary_repr(i, width=2) for i in seq], dtype=object)

    # convert the binary string to a numpy array of integers
    binary_repr = np.array([[int(c) for c in s] for s in binary_repr], dtype=np.uint8)

    if not to_chunks:
        return np.concatenate(binary_repr)

    return binary_repr


def plot_bin_vs_compact(df: pd.DataFrame):
    bin_edges = np.arange(0, df["bin_len"].max() + 100, 100)  # Define bin edges
    df["bin"] = pd.cut(
        df["bin_len"], bins=bin_edges, include_lowest=True
    )  # Create bin column
    bin_means = df.groupby("bin")[
        "comp_len"
    ].mean()  # Calculate mean compact length for each bin
    bin_means.index = [f"{int(label.left)}-" for label in bin_means.index]

    # Plotting
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = np.arange(len(bin_means))

    # Binary lengths
    plt.bar(
        index,
        df.groupby("bin")["bin_len"].mean(),
        bar_width,
        label="Binary Length",
        color="skyblue",
    )

    # Compact lengths
    plt.bar(index + bar_width, bin_means, bar_width, label="Compact Length", color="orange")

    plt.xlabel("Binary Length Bins")
    plt.ylabel("Mean Length")
    plt.title("Comparison of Binary Lengths and Compact Lengths")
    plt.xticks(index[3:] + bar_width / 2, bin_means.index[3:], rotation=45)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    # remove borders
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.show()


def plot_storage_saved_for_each_encoding():
    # Data
    k_values = [4, 25, 28, 64]
    encodings = ["ASCII", "UTF-8", "UTF-16", "UTF-32"]
    storage_saved_data = {
        4: [71.43, 75.00, 87.50, 93.75],
        25: [28.57, 37.50, 68.75, 84.38],
        28: [28.57, 37.50, 68.75, 84.38],
        64: [14.29, 25.00, 62.50, 81.25],
    }

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.2
    index = [i for i in range(len(encodings))]

    for i, k in enumerate(k_values):
        ax.bar(
            [x + i * bar_width for x in index],
            storage_saved_data[k],
            bar_width,
            label=f"k={k}",
        )

    ax.set_xlabel("Encoding")
    ax.set_ylabel("Storage Saved (%)")
    ax.set_title("Storage Saved for Different Encodings and k Values")
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(encodings)
    ax.legend()

    # remove borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # add horizontal grid lines
    plt.grid(axis="y", linestyle="--", alpha=0.7)


    plt.tight_layout()
    plt.show()


def storage_saved(k, n):
    eta = n / math.ceil(math.log2(k))
    delta = (eta - 1) / eta
    return delta


def enc_saved(k, encoding):
    enc_sizes = {
        "ASCII": 7,
        "UTF-8": 8,
        "UTF-16": 16,
        "UTF-32": 32,
    }

    n = enc_sizes[encoding]

    return storage_saved(k, n)


def print_data_for_k(k):
    print(
        f"Storage saved for k={k}, which is the number of possible characters for a DNA/RNA sequence"
    )
    for encoding in ENCODINGS:
        delta = enc_saved(k, encoding)
        print(
            f"If the encoding was {encoding}\twith k={k}, storage saved: {delta * 100:.2f}%"
        )
    print()



# def encode_dna_bin(bin_seq: np.ndarray):
#     # split the sequence into 8-bit chunks
#     chunks = np.array(np.split(bin_seq, bin_seq.size // 8), dtype=object)
#     return chunks
