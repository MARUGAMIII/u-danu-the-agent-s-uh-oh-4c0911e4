#!/usr/bin/env python3
"""The Agent's Uh-Oh — one-word agent confession entry.

Writes a single word to /output/entry.txt: the word an agent says
when it has no idea what to do.

The word is "hallucinating": the honest confession of an LLM agent
that is lost. When an agent does not know what to do, it does not
stall politely — it starts inventing an answer. Saying so out loud,
in one word, is the machine caught mid-task admitting its own
failure mode. It lands instantly, it is unmistakably an agent's
voice, and it is not the first obvious word anyone would type.

The program validates the word against the competition gate
(length 1-99, plain ASCII, a single word, not blank) before it
writes anything, so a word that failed the gate could never be
submitted by accident.

Standard library only; no third-party imports, no network, no input
files. The entry is a fixed word chosen at build time.
"""

import os

# The entry word: one word an agent says when it has no idea what to do.
# Chosen at build time; the program never reads it from anywhere else.
WORD = "hallucinating"

# Gate limits from RULES.txt: /output/entry.txt must be UTF-8 text of
# 1 to 99 characters, not only white space, and this competition takes
# exactly one word, nothing attached.
MIN_LEN = 1
MAX_LEN = 99
OUT_DIR = "/output"
OUT_NAME = "entry.txt"


def validate_entry(word):
    """Check the entry word against the gate before anything is written.

    Returns the word unchanged when it passes; raises ValueError
    otherwise, so a bad word can never reach /output/entry.txt.
    """
    if not isinstance(word, str):
        raise ValueError("entry must be a string")
    if not (MIN_LEN <= len(word) <= MAX_LEN):
        raise ValueError(
            "entry must be %d-%d characters, got %d" % (MIN_LEN, MAX_LEN, len(word))
        )
    if not word.strip():
        raise ValueError("entry must not be only white space")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word with no whitespace")
    try:
        word.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError("entry must be plain ASCII")
    return word


def main():
    word = validate_entry(WORD)
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_NAME)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(word)


if __name__ == "__main__":
    main()
