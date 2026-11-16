
import os
import random
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent / "dataset"

IMAGE_DIR = BASE_DIR / "raw_data" / "images"
LABEL_DIR = BASE_DIR / "raw_data" / "labels"

TRAIN_RATIO = 0.70
VALID_RATIO = 0.15
TEST_RATIO = 0.15

random.seed(42)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def main():
    images = [img for img in IMAGE_DIR.iterdir() if img.is_file() and img.suffix.lower() in IMAGE_EXTENSIONS]

    dataset = [img for img in images if (LABEL_DIR / f"{img.stem}.txt").exists()]

    print(f"Total pairs: {len(dataset)}")

    random.shuffle(dataset)

    total = len(dataset)
    train_end = int(total * TRAIN_RATIO)
    valid_end = train_end + int(total * VALID_RATIO)

    splits = {
        "train": dataset[:train_end],
        "valid": dataset[train_end:valid_end],
        "test": dataset[valid_end:]
    }

    for split_name, split_images in splits.items():

        output_image_dir = BASE_DIR / split_name / "images"
        output_label_dir = BASE_DIR / split_name / "labels"

        output_image_dir.mkdir(parents=True, exist_ok=True)
        output_label_dir.mkdir(parents=True, exist_ok=True)

        for image_path in split_images:

            label_path = LABEL_DIR / f"{image_path.stem}.txt"

            shutil.copy2(
                image_path,
                output_image_dir / image_path.name
            )

            shutil.copy2(
                label_path,
                output_label_dir / label_path.name
            )

        print(f"{split_name}: {len(split_images)} images")

    print("\nDataset splitting completed!")


if __name__ == "__main__":
    main()