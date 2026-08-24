from pathlib import Path
from typing import Any
import pydicom

def read_metadata(path:Path)->dict[str,Any]:

    """
    Read Dicom metadata without loading pixel data
    Returns a dictionary containing the dicom elements.
    """
    if not path.exists():
        raise FileNotFoundError(f"Dicom file not found : {path}")
    
    dataset=pydicom.dcmread(
        path,
        stop_before_pixels=True,
        force=False
    )
    metadata:[str,Any]={}

    for element in dataset:
        metadata[element.keyword or str(element.tag)]=str(element.value)
    
    return metadata
