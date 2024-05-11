import numpy as np


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




# def encode_dna_bin(bin_seq: np.ndarray):
#     # split the sequence into 8-bit chunks
#     chunks = np.array(np.split(bin_seq, bin_seq.size // 8), dtype=object)
#     return chunks
