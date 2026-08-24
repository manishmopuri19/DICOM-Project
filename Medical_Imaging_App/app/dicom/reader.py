from pathlib import Path

import SimpleITK as sitk

def get_series_ids(series_directory:Path)->list[str]:
    """
    Return all Dicom SeriesInstanceUIDs found in a directory.
    """

    series_directory=series_directory.resolve()

    if not series_directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {series_directory}")

    if not series_directory.is_dir():
        raise NotADirectoryError(f"Expected directory: {series_directory}")
    
    series_id=sitk.ImageSeriesReader.GetGDCMSeriesFileNames(
        str(series_directory)
    )

    return list(series_id or [])

def get_series_files(series_directory:Path,series_id:str)->list[Path]:
    """
    Return DICOM file beloging to one series.

    SimpleITK/GDCM sorts the files according to the scan direction.
    We should not sort CT slices alphabeticllay ourselfs.
    """

    file=sitk.ImageSeriesReader.GetGDCMSeriesFileNames(str(series_directory),series_id)

    return [path[file] for file in files]

def read_series(series_directory:Path,series_id:str)->sitk.Image:
    """
    Read one DICOM series into a 3D SimpleItk image
    """

    file_names=get_series_files(
        series_directory,
        series_id
    )

    if not file_names:
        raise ValueError(f"No Dicom file found for series: {series_id}")

        reader=sitk.ImageSeriesReader()
        reader.SetFileNames([str(file) for file in file_names])

        image=reader.Execute()
        return image
