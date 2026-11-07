import hashlib
import json
from pathlib import Path

def file_hash_calc(file_path):
    #Calculate the SHA-256 hash of a file
    sha256 = hashlib.sha256()

    """
    Read mod with binary mode since crypto hash functions
    use bytes, not strings.
    """

    with open(file_path, "rb") as file:
        # Assign bytes into chunks while result is non empty
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()




def baseline(dir):
    """
    Scan a directory and save the SHA-256 hashes for
    all files in it

    - Important in keeping records of what files looked like
      in a certain point in time
    """

    dir = Path(dir)
    baseline = {}

    for file_path in dir.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(dir)
            file_hash = file_hash_calc(file_path)

            baseline[str(relative_path)] = file_hash

    with open("baseline.json", "w") as bf:
        json.dump(baseline, bf, indent=4)

    print(f"[!] Baseline created for {len(baseline)} files")



def load_baseline(baseline_path='baseline.json'):
    """
    Loads previously saved file hashes from
    the baseline.json file
    """

    with open(baseline_path, 'r') as file:
        # Converts JDON  data back into a python dict
        saved_baseline = json.load(file)
    return saved_baseline


def detect_changes(dir):
    '''
    Detects changes in files against the saved baseline

    Detects:
    - Added files
    - Modified files
    - Deleted files
    '''

    dir = Path(dir)

    # Verifies the dir exists
    if not dir.is_dir():
        raise NotADirectoryError(
            f'{dir} is not a valid directory'
        )

    # Loads saved baseline
    saved_baseline = load_baseline()

    # Store current file's fingerprints
    current_prints = {}

    for file_path in dir.rglob("*"):
        if file_path.is_file():
            rel_path = file_path.relative_to(dir)
            current_hash = file_hash_calc(file_path)

            current_prints[str(rel_path)] = current_hash

    added = []
    modified = []
    deleted = []

    # Checls for new or modified files
    for name, current_hash in current_prints.items():
        if name not in saved_baseline:
            added.append(name)
        elif current_hash != saved_baseline[name]:
            modified.append(name)

    # Checks for deleted files
    for name in saved_baseline:
        if name not in current_prints:
            deleted.append(name)

    return {
        'added': sorted(added),
        'modified': sorted(modified),
        'deleted': sorted(deleted)
    }

