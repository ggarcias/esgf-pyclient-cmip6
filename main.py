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
    check_variables_exist,
)

load_dotenv()

# parser = argparse.ArgumentParser()
# parser.add_argument("--json", help="insert parameters oilspill json format")
# args = parser.parse_args()

# with open(args.json) as f:
#    jdata = json.load(f)

download_dir = "/BGFS/CLIMEX/feyenlu/garcgui/CMIP6/"

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
    "CMCC-ESM2_r1i1p1f1",
]

scenarios = [
    "historical",
    "ssp126",
    "ssp245",
    "ssp370",
    "ssp585",
]

variables = [
    #    "sfcWind",
    #    "ua",
    "uas",
    #    "va",
    "vas",
    "psl",
    #    "siconc",
]

frequencies = [
    "3hr",
    "6hr",
    "3hrPt",
    "6hrPt",
#    "day",
    #    "mon",
]


# lm = loggin_esgf()
# print("Connection stablished... ", lm.is_logged_on())

massive_download(
    urls,
    models,
    scenarios,
    variables,
    frequencies,
    download_dir,
)


for url in urls:
    for model in models:
        for scenario in scenarios:
            for frequency in frequencies:
                check_variables_exist(
                    url, model, scenario, variables, frequency, download_dir
                )

print("===== DONE =======")
