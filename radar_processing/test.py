from read_mira_radar import read_mira
import pyart
import netCDF4

mira, mira_melthei = read_mira(
    "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/data/radar/mira_campina/test_files/20201115_0000.mmclx"
)
# print(print(pyart.util.datetimes_from_radar(mira)))
# print(mira.fields["SNR"]["data"] == "nan")

# ncobj = netCDF4.Dataset(
#     "/mnt/c/Users/ccl/OneDrive - usp.br/Documentos/GitHub/amazon-storms-aerosols/data/radar/mira_campina/test_files/20201115_0000.mmclx"
# )
# if ncobj['tpow'][:].all() == 0:
#     print('Transmit Power Off')
# ql_res = 2
# orig_res = float(ncobj.hrd[ncobj.hrd.find("AVE") + 4 : ncobj.hrd.find("\nC")])
# res = round(ql_res * 60 / orig_res)
# print(res)
