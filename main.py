import argparse
import json
import os

from dotenv import load_dotenv
from pyesgf.logon import LogonManager

from src.cmip6_jrc_pkg.cmip6_tools import (
        connect_esg, 
        number_of_matchs,
        massive_search
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

# Connect to esgf
lm = LogonManager()
lm.logoff()
lm.is_logged_on()

myproxy_host = 'esgf-data.dkrz.de'
lm.logon(username=os.environ.get("USERNAME"), password=os.environ.get("PASSWORD"), hostname=myproxy_host)
#lm.logon(username=os.environ.get("OPENID"), password=os.environ.get("PASSWORD"), hostname=myproxy_host)
lm.is_logged_on()

massive_download()

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
