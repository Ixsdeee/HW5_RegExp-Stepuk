import os
import re
import shutil


def to_salted_language(text):
    return re.sub(r"([аеёиоуыэюяАЕЁИОУЫЭЮЯ])", r"\1с\1", text)


def extract_sets(path):
    with open(path) as inp:
        text = inp.read()
        chords = set()
        chords.update(re.findall(r"[A-G][#b]?[m]?[A-G]?", text))
        return chords


def rename_files(dir, pattern, new_pattern, sample_names, to_replace=False):
    if sample_names is None:
        sample_names = {}

    renamed = []
    for filename in os.listdir(dir):
        old_path = os.path.join(dir, filename)

        if not os.path.isfile(old_path):
            continue
        if not re.search(pattern, filename):
            continue

        new_name = filename
        if new_pattern:
            new_name = re.sub(pattern, new_pattern, new_name)
        for key, value in sample_names.items():
            new_name = new_name.replace(key, value)
        if new_name == filename:
            continue

        new_path = os.path.join(dir, new_name)
        if os.path.exists(new_path):
            print(f"Пропускаю: {new_name} уже существует")
            continue
        if to_replace:
            os.rename(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)

        renamed.append((old_path, new_path))

    return renamed


rename_files(
    dir="fastqs_test",
    pattern=r"Mix-(G\d).*_(R\d)_.*",
    new_pattern=r"\1_\2.fastq",
    sample_names={"G1": "WT_rep1", "G2": "WT_rep2"},
    to_replace=False,
)
