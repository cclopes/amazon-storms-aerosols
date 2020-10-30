from glob import glob
from zipfile import ZipFile


def unzip_files(filepath):
    """
    """
    file = glob(filepath[:-1] + ".zip")[0]

    print("Unzipping files")
    with ZipFile(file, "r") as zip_ref:
        zip_filenames = zip_ref.namelist()
        for filename in zip_filenames:
            if filename.endswith(".mmclx"):
                zip_ref.extract(filename, filepath[:-3] + "temp/")

    paths = glob(filepath[:-3] + "temp/" + file[-6:-4] + "/*")

    return paths
