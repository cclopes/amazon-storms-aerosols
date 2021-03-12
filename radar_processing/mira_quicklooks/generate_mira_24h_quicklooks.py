#!/home/cclopes/miniconda3/envs/amazon-storms-aerosols/bin/python

import shutil
import os
import sys
import time
from pathlib import Path
from glob import glob
from zipfile import ZipFile

from plot_mira_quicklooks import read_plot_mira_quicklooks


def unzip_files(file, path):
    """
    """
    bt = time.time()

    with ZipFile(file, "r") as zip_ref:
        zip_filenames = zip_ref.namelist()
        for filename in zip_filenames:
            if filename.endswith(".mmclx"):
                zip_ref.extract(filename, path + "temp/")

    paths = sorted(glob(path + "temp/" + file[-6:-4] + "/*"))

    print((time.time() - bt) / 60, " minutes to unzip files")

    return paths


data_path = "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/data/radar/mira_campina/"

# Criando pasta de quicklooks (se não existir)
Path(data_path + "quicklooks").mkdir(parents=True, exist_ok=True)

# Checando arquivos de quicklooks (se existirem)
if os.listdir(data_path + "quicklooks"):
    ql_folders = sorted(glob(data_path + "quicklooks/*/*/*/", recursive=True))
    ql_last = ql_folders[-1][-11:-1]
else:
    ql_last = ""

# Listando arquivos de dados
data_files = sorted(glob(data_path + "*/*/*.zip", recursive=True))

# Pegando próxima data depois da última com quicklooks
# (ou primeira se não tiver nenhum quicklook)
if data_path + ql_last + ".zip" in data_files:
    if (data_files.index(data_path + ql_last + ".zip") + 1) >= len(data_files):
        sys.exit("No new files")
    else:
        data_ql = data_files[data_files.index(data_path + ql_last + ".zip") + 1]
else:
    data_ql = data_files[0]

# Fazendo quicklooks de data_ql

# Descompactando os dados
files = unzip_files(data_ql, data_path)
if len(files) <= 3:
    Path(data_path + "quicklooks/" + ql_last + "/").mkdir(
        parents=True, exist_ok=True
    )
    sys.exit("Not enough files to plot")

# Plotando os dados
bt = time.time()
read_plot_mira_quicklooks(
    filenames=files, save_path=data_path + "quicklooks/", res=2
)
print((time.time() - bt) / 60, " minutes to generate quicklooks for")
print(data_ql)

# Excluindo arquivos temporários
shutil.rmtree(data_path + "temp/")
