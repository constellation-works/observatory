"""
status: work-in-progress
"""


import os
from collections import defaultdict
from typing import BinaryIO
import regex as re
import heapq


PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
FILE_PATH = "/Users/daniel/workspace/constellation/codebases/parallax/data/R02-language-models/raw/TinyStoriesV2-GPT4-valid.txt"
SPECIAL_TOKEN = "<|endoftext|>"
VOCAB_SIZE = 500


def build_index(words):
    table = defaultdict(int)
    for word in words:
        key = tuple(word)
        table[key] += 1
    return table


def build_score(index):
    scores = {}
    for key, val in index.items():
        for i in range(len(key) - 1):
            key2 = key[i : i + 2]  # a pair, not a single symbol
            if key2 not in scores:
                scores[key2] = {"cnt": 0, "keys": set()}
            scores[key2]["cnt"] += val
            scores[key2]["keys"].add(key)
    return scores


def _find_chunk_boundaries(
    file: BinaryIO,
    desired_num_chunks: int,
    split_special_token: bytes,
) -> list[int]:
    assert isinstance(split_special_token, bytes), "Must represent special token as a bytestring"
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    chunk_size = file_size // desired_num_chunks
    chunk_boundaries = [i * chunk_size for i in range(desired_num_chunks + 1)]
    chunk_boundaries[-1] = file_size
    mini_chunk_size = 4096

    for bi in range(1, len(chunk_boundaries) - 1):
        initial_position = chunk_boundaries[bi]
        file.seek(initial_position)  # Start at boundary guess
        while True:
            mini_chunk = file.read(mini_chunk_size)  # Read a mini chunk
            if mini_chunk == b"":
                chunk_boundaries[bi] = file_size
                break
            # Find the special token in the mini chunk
            found_at = mini_chunk.find(split_special_token)
            if found_at != -1:
                chunk_boundaries[bi] = initial_position + found_at
                break
            initial_position += mini_chunk_size
    return sorted(set(chunk_boundaries))


def pretokenize(fpath, special_tokens):
    with open(fpath, "rb") as f:
        num_processes = 1
        boundaries = _find_chunk_boundaries(f, num_processes, b"<|endoftext|>")
        chunks = []
        for start, end in zip(boundaries[:-1], boundaries[1:]):
            f.seek(start)
            chunk = f.read(end - start).decode("utf-8", errors="ignore")
            safe_token = re.escape(special_tokens)
            # Pre-tokenize each document separately so no merge spans a boundary.
            words = []
            for segment in re.split(safe_token, chunk):
                words.extend(re.findall(PAT, segment))
            chunks.append(words)
        return chunks[0]


class BPETokenizer:
    def __init__(self, fpath=FILE_PATH, special_tokens=SPECIAL_TOKEN, vocab_size=VOCAB_SIZE):
        self.vocab: dict[int, bytes] = {}
        self.merge = []
        self.index = {}
        self.fpath = fpath
        self.special_tokens = special_tokens
        self.vocab_size = vocab_size
        self.prep()

    def prep(self):
        chunks = pretokenize(self.fpath, self.special_tokens)
        if not chunks:
            raise Exception("something went wrong")
        self.index = build_index(chunks)
        self.scores = build_score(self.index)

    def rebuild_score(self, changed_keys):
        new_scores = {}
        remove = set()
        for key in changed_keys:
            for i in range(len(key) - 1):
                key2 = key[i : i + 2]
                if key2 not in self.scores:
                    value = self.index[key]
                    new_scores[key2] = {"cnt": 0, "keys": set()}
                    self.scores[key[i]]["cnt"] -= value
                    self.scores[key[i + 1]]["cnt"] -= value
                self.scores[key2]["cnt"] += value
                self.scores[key2]["keys"].add(key)
            
        self.scores = new_scores | self.scores
        

    def iteration(self):
        if len(self.merge) >= self.vocab_size:
            return
        if not (self.scores and self.index):
            return

        index = self.index
        scores = self.scores

        heap = [(-v["cnt"], k) for k, v in scores.items()]
        heapq.heapify(heap)
        _, ckey = heapq.heappop(heap)
        okeys = scores.pop(ckey)["keys"]
        self.merge.append(ckey)
        changed_keys = set()

        for k in okeys:
            prev = index.pop(k)
            arr, i = [], 0
            while i < len(k):
                if k[i : i + 2] == ckey:
                    arr.append("".join(ckey))  # the merged token itself
                    i += 2
                else:
                    arr.append(k[i])
                    i += 1
            new_key = tuple(arr)
            index[new_key] = index.get(new_key, 0) + prev
            changed_keys.add(new_key)
        return changed_keys

    def tokenize(self):
        import json

        idx = 0
        while True:
            print(f"iteration {idx}")
            changed_keys = self.iteration()
            if not changed_keys:
                break
            idx += 1
            self.rebuild_score(changed_keys)
        with open("tokenized.json", "w") as file:
            json.dump(self.merge, file, indent=4)
            print("done")


if __name__ == "__main__":
    # out = tokenize()
    # print(out[0])
    tk = BPETokenizer()
    tk.tokenize()
