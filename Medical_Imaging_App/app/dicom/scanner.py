""" this following program help us to find or scan then
    given repository and provide the files
"""

from dataclasses import dataclass
from pathlib import Path
import pydicom

@dataclass(frozen=True)
class DicomFile:
    path:Path
    study_instance_uid:str|None
    series_instance_uid:str|None
    modality:str|None

def is_dicom_file(path:Path)->bool:
        """
        Determine whether a file can bbe read as a DICOM dataset.
        we only read the metadata here, not pixel data
        this keeps the scanner relatively cheap.
        """

        if not path.is_file():
            return False
        
        try:
            pydicom.dcmread(path,stop_before_pixels=True,force=False)
            return True

        except(pydicom.errors.InvalidDicomError,OSError,EOFError):
            return False



def scan_dicom_files(root:Path)->list[DicomFile]:
    """
    Recursively scan a directory for Dicom files.
    Return on Dicomfile object for every detected dicom file.
    """

    root=root.resolve()

    if not root.exists():
        raise FileNotFoundError(f"Dataset directory does not exist: {root}")
    
    if not root.is_dir():
        raise NotADirectoryError(f"Expected directory :{root}")
    
    result:list[DicomFile]=[]

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if not is_dicom_file(path):
            continue

        try:
            dataset=pydicom.dcmread(
                path,stop_before_pixels=True,
                force=False
            )

            result.append(DicomFile(path=path,
            study_instance_uid=getattr(dataset,"StudyInstanceUID",None),
            series_instance_uid=getattr(dataset,"SeriesInstanceUID",None),
            modality=getattr(dataset,"Modality",None)))
        except(pydicom.errors.InvalidDicomError,OSError,EOFError):
            continue
    
    return result
