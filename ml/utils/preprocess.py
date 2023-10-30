import re
from typing import List

from utils import vocab


def shift_lines_left(lines: List[List[int]]) -> List[List[int]]:
    min_leading_spaces = float("inf")

    for line in lines:
        count = 0
        for token in line:
            if vocab.spaces_range[0] <= token <= vocab.spaces_range[1]:
                count += 1
            else:
                break

        min_leading_spaces = min(min_leading_spaces, count)

    if min_leading_spaces == 0 or min_leading_spaces == float("inf"):
        return lines

    for i, line in enumerate(lines):
        lines[i] = line[min_leading_spaces:]

    return lines


def joinlines(lines: List[List[int]]):
    lines = shift_lines_left(lines)
    encoded_text = []
    for i, line in enumerate(lines):
        encoded_text += line
        if i != len(lines) - 1:
            encoded_text.append(vocab.vocab_dict["\n"])
    return encoded_text


def remove_duplicate_starting(lines):
    total_len = sum([len(line) + 1 for line in lines])

    def get_starting_char(mline):
        for v in mline:
            if not (vocab.spaces_range[0] <= v <= vocab.spaces_range[1]):
                return v
        return None

    last_val = None
    filtered_lines = []

    for line_id, line in enumerate(lines):
        start_char = get_starting_char(line)

        if (start_char is not None and start_char != last_val) or start_char == vocab.unk_idx:
            filtered_lines.append(line)
        else:
            total_len -= len(line) + 1

        if total_len <= vocab.max_size:
            break

        last_val = start_char

    return filtered_lines + lines[line_id + 1 :]


def filter_encoded(encoded_text: List[int]):
    if len(encoded_text) <= vocab.max_size:
        return encoded_text

    lines = []
    cur_line = []
    for v in encoded_text:
        if v == vocab.vocab_dict["\n"]:
            lines.append(cur_line)
            cur_line = []
        else:
            cur_line.append(v)

    if len(cur_line) > 0:
        lines.append(cur_line)

    total_len = sum([len(line) + 1 for line in lines])
    left_lines_num = max(int(total_len / len(lines)), vocab.max_line_len)

    for i in range(len(lines)):
        if len(lines[i]) <= left_lines_num:
            continue

        rem_len = len(lines[i]) - left_lines_num

        lines[i] = lines[i][:left_lines_num]
        total_len -= rem_len

        if total_len <= vocab.max_size:
            return joinlines(lines)
    return joinlines(remove_duplicate_starting(lines))


def remove_minimum_leading(raw):
    lines = raw.splitlines()

    def count_leading(s):
        count = 0
        for char in s:
            if char in " \t":
                count += 1
            else:
                break
        return count

    leadings = [count_leading(line) for line in lines if line.strip()]
    if not leadings:
        return raw
    min_leading = min(leadings)
    result = [line[min_leading:].rstrip() for line in lines if line.strip()]
    if not result:
        return raw
    return "\n".join(result)


def remove_quoted_text(s):
    s = re.sub(r'"[^"]*"', '""', s)
    s = re.sub(r"'[^']*'", "''", s)
    return s


def replace_continuous_with_N(nums, range_start, N):
    i = 0
    new_list = []
    while i < len(nums):
        if range_start <= nums[i]:
            new_list.append(N)
            while i < len(nums) and range_start <= nums[i]:
                i += 1
        else:
            new_list.append(nums[i])
            i += 1
    return new_list


def encode_text(text):
    text = remove_minimum_leading(remove_quoted_text(text.lower()))

    encoded_text = []
    i = 0
    while i < len(text):
        for j in range(min(i + vocab.max_word_len, len(text)), i, -1):
            word = text[i:j]
            if word in vocab.vocab_dict:
                encoded_text.append(vocab.vocab_dict[word])
                i = j
                break
        else:
            encoded_text.append(vocab.vocab_dict["<UNK>"])
            i += 1

    encoded_text = replace_continuous_with_N(
        encoded_text, vocab.letters_pose, len(vocab.vocab_list) - 1
    )

    if len(encoded_text) > vocab.max_size:
        encoded_text = filter_encoded(encoded_text)

    return encoded_text


def decode_text(encoded_text):
    return "".join([vocab.vocab_list[c] for c in encoded_text])
