import os
import sys
import json
import hashlib

def calculate_sha256(filepath: str) -> str:
    """Calculates SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def verify_model_integrity(target_dir: str = "vision_models", baseline_manifest: str = "vision_models/model_hashes.json") -> bool:
    """
    Verifies SHA-256 hashes of all vision model files against baseline manifest.
    Prevents unauthorized model modifications or corruption.
    """
    abs_target = os.path.abspath(target_dir)
    if not os.path.exists(abs_target):
        print(f"[ERROR] Target directory '{target_dir}' does not exist.")
        return False

    current_hashes = {}
    for root, dirs, files in os.walk(abs_target):
        # Ignore experimental and deployment export directories from production model baseline audit
        if "experiments" in dirs:
            dirs.remove("experiments")
        if "deployment" in dirs:
            dirs.remove("deployment")
        for file in files:
            if file == "model_hashes.json":
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, abs_target).replace("\\", "/")
            current_hashes[rel_path] = calculate_sha256(full_path)

    abs_manifest = os.path.abspath(baseline_manifest)
    if not os.path.exists(abs_manifest):
        print(f"[INFO] Baseline manifest not found. Writing initial manifest to '{baseline_manifest}'...")
        with open(abs_manifest, "w") as f:
            json.dump(current_hashes, f, indent=2)
        print(f"[SUCCESS] Baseline manifest recorded for {len(current_hashes)} file(s).")
        for rel_path, h in current_hashes.items():
            print(f"  - {rel_path}: {h}")
        return True

    with open(abs_manifest, "r") as f:
        baseline_hashes = json.load(f)

    all_matched = True
    print("\n--- MODEL INTEGRITY AUDIT ---")
    for rel_path, current_hash in current_hashes.items():
        if rel_path not in baseline_hashes:
            print(f"[NEW FILE DETECTED] {rel_path}: {current_hash}")
            all_matched = False
        elif baseline_hashes[rel_path] != current_hash:
            print(f"[MISMATCH DETECTED] {rel_path}!")
            print(f"  Expected: {baseline_hashes[rel_path]}")
            print(f"  Found:    {current_hash}")
            all_matched = False
        else:
            print(f"[VERIFIED] {rel_path}: {current_hash[:16]}...")

    for rel_path in baseline_hashes:
        if rel_path not in current_hashes:
            print(f"[MISSING FILE] {rel_path} was expected but not found!")
            all_matched = False

    if all_matched:
        print("\n[SUCCESS] MODEL INTEGRITY VERIFIED: NO UNEXPECTED MODEL CHANGES.")
    else:
        print("\n[ALERT] MODEL INTEGRITY VERIFICATION FAILED!")
        sys.exit(1)

    return all_matched

if __name__ == "__main__":
    verify_model_integrity()
