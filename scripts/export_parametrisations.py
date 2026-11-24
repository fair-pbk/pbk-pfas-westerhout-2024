"""Export parametrisation CSV files and a ZIP archive for the PBK PFAS model.

Run from the repository root with:
    python scripts/export_parametrisations.py
"""

import csv
from pathlib import Path
import shutil


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PARAMETRISATIONS_PATH = REPOSITORY_ROOT / "parametrisations"
OUTPUT_PATH = PARAMETRISATIONS_PATH / "exports" / "pbk_pfas_westerhout_2024"
MODEL_INSTANCES_FILE = PARAMETRISATIONS_PATH / "pbk_model_instances.csv"
PARAMETER_FILES = sorted(PARAMETRISATIONS_PATH.glob("*.params.csv"))


def export_parametrisations() -> None:
    if not MODEL_INSTANCES_FILE.is_file():
        raise FileNotFoundError(f"Model instances CSV not found: {MODEL_INSTANCES_FILE}")
    if not PARAMETER_FILES:
        raise FileNotFoundError(
            f"No parameter CSV files found directly under {PARAMETRISATIONS_PATH}"
        )

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        MODEL_INSTANCES_FILE,
        OUTPUT_PATH / "PbkModelInstances.csv",
    )

    output_file = OUTPUT_PATH / "PbkModelInstanceParameters.csv"
    expected_header = None
    with output_file.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        for parameter_file in PARAMETER_FILES:
            with parameter_file.open(encoding="utf-8-sig", newline="") as source:
                reader = csv.reader(source)
                header = next(reader, None)
                if header is None:
                    raise ValueError(f"Parameter CSV is empty: {parameter_file}")
                if expected_header is None:
                    expected_header = header
                    writer.writerow(header)
                elif header != expected_header:
                    raise ValueError(
                        f"CSV header in {parameter_file} does not match "
                        f"{PARAMETER_FILES[0]}"
                    )

                writer.writerows(row for row in reader if row)

    shutil.make_archive(
        str(OUTPUT_PATH), "zip", root_dir=OUTPUT_PATH.parent, base_dir=OUTPUT_PATH.name
    )


if __name__ == "__main__":
    export_parametrisations()
