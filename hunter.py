#!/usr/bin/env python3

from textract import process
from pathlib import Path
from itertools import chain

from typing import List

import re

def find_all_files(path: str, extensions=["docx", "doc", "txt", 'pdf']):
    return list(
        chain(*[Path(path).glob(f"*.{ext}") for ext in extensions]),
    )

def hunt_keywords(keywords: List[str], path: str, key_regex='[\d]{10}|[\d-]{11}'):
    result = dict()

    files = find_all_files(path)

    for path in files:
        text = process(path).decode('utf-8').lower()

        has_keyword = any([
            k.lower().strip() in text for k in keywords
        ])

        if has_keyword:
            if match := re.search(key_regex, text):
                key = match.group(0)

                content = result.get(key, [])
                result[cpr] = content + [str(path)]

    return result
