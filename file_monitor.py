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
    Scan a directory and save the SHa-256 hashes for 
    all files in it

    - Important in keeping records of what files looked like
      in a certain point in time
    """

    dir = Path(dir)
    baseline = {}

    for file_path in dir.glob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(dir)
            file_hash = file_hash_calc(file_path)

            baseline[str(relative_path)] = file_hash

    with open("baseline.json", "w") as bf:
        json.dump(baseline, bf, indent=4)

    print(f"[!] Baseline created for {len(baseline)} files")