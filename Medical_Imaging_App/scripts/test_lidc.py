from pathlib import Path

from app.dicom.scanner import scan_dicom_files


DATASET_ROOT = Path(
    "data/lidc_idri/LIDC-IDRI-0314/82159/75227"
)


def main():
    print("=" * 80)
    print("LIDC-IDRI DICOM SCANNER")
    print("=" * 80)

    print(f"Dataset root: {DATASET_ROOT.resolve()}")
    print()

    if not DATASET_ROOT.exists():
        raise FileNotFoundError(
            f"Dataset directory does not exist: "
            f"{DATASET_ROOT.resolve()}"
        )

    print("Scanning for DICOM files...")
    print()

    dicom_files = scan_dicom_files(DATASET_ROOT)

    print(f"DICOM files found: {len(dicom_files)}")
    print()

    for dicom_file in dicom_files[:20]:
        print(f"Path:     {dicom_file.path}")
        print(f"Study:    {dicom_file.study_instance_uid}")
        print(f"Series:   {dicom_file.series_instance_uid}")
        print(f"Modality: {dicom_file.modality}")
        print("-" * 80)


if __name__ == "__main__":
    main()