import argparse
import datetime
import json
import os

from dotenv import load_dotenv
from pyesgf.logon import LogonManager

from src.cmip6_jrc_pkg.cmip6_tools import (
        connect_esg, 
        loggin_esgf,
        number_of_matchs,
        massive_search,
        get_ctx,
        massive_download,
)

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--json", help="insert parameters oilspill json format")
args = parser.parse_args()

with open(args.json) as f:
    jdata = json.load(f)

urls = [
    "esgf-node.llnl.gov/esg-search",
    "esgf-node.ipsl.upmc.fr/esg-search",
    "esgf-data.dkrz.de/esg-search",
    "esgf-index1.ceda.ac.uk/esg-search",
]

models = [
    "GFDL-ESM4_r1i1p1f1",
    "IPSL-CM6A-LR_r1i1p1f1",
    "MPI-ESM1-2-HR_r1i1p1f1",
    "MRI-ESM2-0_r1i1p1f1",
    "UKESM1-0-LL_r1i1p1f2",
    "CanESM5_r1i1p1f1",
    "CNRM-CM6-1_r1i1p1f2",
    "CNRM-ESM2-1_r1i1p1f2",
    "EC-Earth3_r1i1p1f1",
    "MIROC6_r1i1p1f1",
    "CMCC-ESM2_r1i1p1",
]

scenarios = [
    "historical",
    "ssp126",
    "ssp245",
    "ssp370",
]

variables = [
    "sfcWind",
    "ua",
    "uas",
    "va",
    "vas",
    "psl",
    "siconc",
]

frequencies = [
    "3hr",
    "6hr",
    "day",
    "mon",
]


lm = loggin_esgf()
print("Connection stablished... ", lm.is_logged_on())

#massive_download()
jdata["source"] = models[0].split("_")[0]
jdata["scenario"] = scenarios[0]
jdata["variable"] = "uas"
jdata["frequency"] = "3hr"
jdata["from_timestamp"] = "1980-01-01T00:00:00Z"
jdata["to_timestamp"] = "2010-01-01T00:00:00Z"
jdata["variant_label"] = models[0].split("_")[-1]


massive_download([urls[0]], [models[0]], [scenarios[0]], ["uas"], ["3hr"])

jferieji

conn = connect_esg(urls[0])
print("mathcs = ", number_of_matchs(conn, jdata))
ctx = get_ctx(conn, jdata)
ds = ctx.search()[0]

fc = ds.file_context()
print(fc.hit_count)
jfirjri

wget_script_content = fc.get_download_script()
download_dir = "data/"
script_name = "script1.sh"
#download_dir = tempfile.mkstemp(suffix='.sh', prefix='download-')[1]
with open(download_dir + script_name, "w") as writer:
    writer.write(wget_script_content)
    
import os, subprocess
os.chmod(download_dir, 0o750)

cmd = f"cd data/ && bash {script_name}"
p = subprocess.Popen(cmd, shell=True)

"""
massive_search(
        urls, 
        models, 
        scenarios, 
        variables, 
        frequencies
)
"""
print("===== DONE =======")
