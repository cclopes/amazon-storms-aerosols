from glob import glob
from zipfile import ZipFile


def unzip_files(filepath):
    """
    """
    files = glob(filepath + "*.zip")
    paths = []

    print("Unzipping files")
    for file in files:
        with ZipFile(file, "r") as zip_ref:
            zip_filenames = zip_ref.namelist()
            for filename in zip_filenames:
                if filename.endswith(".mmclx"):
                    zip_ref.extract(filename, filepath + "temp/")
        paths.append(glob(filepath + "temp/" + file[-6:-4] + "/*"))

    return paths
