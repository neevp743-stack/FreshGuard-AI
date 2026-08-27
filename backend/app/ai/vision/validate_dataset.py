import os
import json
from typing import Dict, Any, List, Tuple

DATASET_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../datasets/grocery_vision"))
CLASSES_JSON_PATH = os.path.join(os.path.dirname(__file__), "classes.json")

def load_classes() -> List[str]:
    if os.path.exists(CLASSES_JSON_PATH):
        with open(CLASSES_JSON_PATH, "r") as f:
            data = json.load(f)
            return data.get("classes", [])
    return []

def validate_dataset() -> Dict[str, Any]:
    """
    Automated pre-training dataset validator & readiness report generator.
    Enforces strict annotation format, checks for missing files, corrupt coordinates,
    class imbalance, and dataset session leakage.
    """
    classes = load_classes()
    num_classes = len(classes)

    splits = ["train", "val", "test"]
    split_image_counts = {s: 0 for s in splits}
    split_label_counts = {s: 0 for s in splits}

    objects_per_class = {c: 0 for c in classes}
    total_objects = 0
    invalid_labels = []
    missing_labels = []
    leakage_warnings = []

    # Track image hashes/names across splits to detect dataset leakage
    seen_file_roots: Dict[str, str] = {} # root_name -> split

    for s in splits:
        img_dir = os.path.join(DATASET_ROOT, "images", s)
        lbl_dir = os.path.join(DATASET_ROOT, "labels", s)

        if not os.path.exists(img_dir) or not os.path.exists(lbl_dir):
            continue

        img_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        split_image_counts[s] = len(img_files)

        for img_name in img_files:
            root_name, _ = os.path.splitext(img_name)

            # Data Leakage Check
            if root_name in seen_file_roots:
                leakage_warnings.append(
                    f"Duplicate image '{img_name}' found in both '{seen_file_roots[root_name]}' and '{s}' splits."
                )
            else:
                seen_file_roots[root_name] = s

            lbl_name = root_name + ".txt"
            lbl_path = os.path.join(lbl_dir, lbl_name)

            if not os.path.exists(lbl_path):
                missing_labels.append(f"{s}/{lbl_name}")
                continue

            split_label_counts[s] += 1

            # Validate Annotation Format
            try:
                with open(lbl_path, "r") as lf:
                    lines = lf.readlines()
                    for line_num, line in enumerate(lines, 1):
                        parts = line.strip().split()
                        if not parts:
                            continue
                        if len(parts) != 5:
                            invalid_labels.append(f"{s}/{lbl_name}: line {line_num} does not have 5 items")
                            continue

                        class_id = int(parts[0])
                        x_center, y_center, width, height = map(float, parts[1:])

                        if class_id < 0 or class_id >= num_classes:
                            invalid_labels.append(f"{s}/{lbl_name}: invalid class_id {class_id}")
                            continue

                        if not (0.0 <= x_center <= 1.0 and 0.0 <= y_center <= 1.0 and 0.0 <= width <= 1.0 and 0.0 <= height <= 1.0):
                            invalid_labels.append(f"{s}/{lbl_name}: coordinates out of bounds [0,1]")
                            continue

                        class_name = classes[class_id]
                        objects_per_class[class_name] += 1
                        total_objects += 1

            except Exception as ex:
                invalid_labels.append(f"{s}/{lbl_name}: read error {ex}")

    total_images = sum(split_image_counts.values())
    total_annotated = sum(split_label_counts.values())

    # Class Imbalance Calculation
    imbalance_warnings = []
    counts_list = list(objects_per_class.values())
    if counts_list:
        max_obj = max(counts_list)
        min_obj = min(counts_list)
        if min_obj == 0 and max_obj > 0:
            imbalance_warnings.append("Some classes have 0 annotated objects.")
        elif min_obj > 0 and (max_obj / min_obj) > 2.5:
            imbalance_warnings.append(f"High class imbalance: max class has {max_obj} objects, min class has {min_obj} objects.")

    is_valid = (
        total_annotated > 0 and
        len(invalid_labels) == 0 and
        len(missing_labels) == 0 and
        len(leakage_warnings) == 0
    )

    return {
        "is_valid": is_valid,
        "total_images": total_images,
        "annotated_images": total_annotated,
        "total_objects": total_objects,
        "split_image_counts": split_image_counts,
        "split_label_counts": split_label_counts,
        "objects_per_class": objects_per_class,
        "invalid_labels_count": len(invalid_labels),
        "missing_labels_count": len(missing_labels),
        "invalid_labels": invalid_labels,
        "missing_labels": missing_labels,
        "leakage_warnings": leakage_warnings,
        "imbalance_warnings": imbalance_warnings,
        "message": "Dataset validation complete."
    }

def print_readiness_report():
    report = validate_dataset()
    print("=== FINAL DATASET READINESS REPORT ===")
    print(f"Total Images: {report['total_images']}")
    print(f"Annotated Images: {report['annotated_images']}")
    print(f"Total Objects: {report['total_objects']}")
    print(f"Split Breakdown: {report['split_image_counts']}")
    print("\nObjects Per Class:")
    for c, cnt in report['objects_per_class'].items():
        print(f"  - {c}: {cnt}")
    print(f"\nInvalid Labels: {report['invalid_labels_count']}")
    print(f"Missing Label Files: {report['missing_labels_count']}")
    print(f"Leakage Warnings: {len(report['leakage_warnings'])}")
    if report['imbalance_warnings']:
        print(f"Imbalance Warnings: {report['imbalance_warnings']}")
    print(f"\nValidation Result: {'VALID [OK]' if report['is_valid'] else 'INVALID / NOT READY [FAIL]'}")

if __name__ == "__main__":
    print_readiness_report()
