import string

with open("./vocabulary.txt", "r") as f:
    vocab_list = f.read().split("\n")

vocab_list = [word for word in vocab_list if word]

vocab_list += [" ", "\n", "\t", "\t\t", "\t\t\t", "  ", "    ", "        ", "            "] + list(
    string.punctuation
)
letters_pose = len(vocab_list)
vocab_list += list(string.digits) + list(string.ascii_lowercase)

vocab_list += ["<PAD>", "<UNK>"]
unk_idx = len(vocab_list) - 1

vocab_dict = {c: i for i, c in enumerate(vocab_list)}

spaces_range = [vocab_dict[" "], vocab_dict["            "]]
max_line_len = 10
max_size = 128

max_word_len = max([len(word) for word in vocab_list])
