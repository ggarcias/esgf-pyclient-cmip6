import datetime
import subprocess
import os

from dotenv import load_dotenv
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection


load_dotenv()


cmip_project = "CMIP6"


def connect_esg(url):
    """
    comments
    """
    conn = SearchConnection("https://" + url, distrib=True)
    return conn


def loggin_esgf():
    # Connect to esgf
    lm = LogonManager()
    lm.logoff()
    lm.is_logged_on()

    #    myproxy_host = 'esgf-data.dkrz.de'
    #    myproxy_host = 'esgf-node.llnl.gov'
    myproxy_host = "esgf.nci.org.au"

    lm.logon(
        username  = os.environ.get("USERNAME"),
        password  = os.environ.get("PASSWORD"),
        hostname  = myproxy_host,
        bootstrap = True,
    )
    return lm


def number_of_matchs(conn, jdata):
    """
    comments
    """

    timestamp_ini = datetime.datetime.strptime(jdata["t0"], "%Y-%m-%d")
    timestamp_end = datetime.datetime.strptime(jdata["tf"], "%Y-%m-%d")

    ctx = conn.new_context(
        facets="*",
        project=cmip_project,
        source_id=jdata["source"],
        experiment_id=jdata["scenario"],
        variable=jdata["variable"],
        frequency=jdata["frequency"],
        variant_label=jdata["variant_label"],
        from_timestamp=timestamp_ini.strftime("%Y-%m-%dT%H:%M:%SZ"),
        to_timestamp=timestamp_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        #        data_node = "esgf-data3.ceda.ac.uk",
    )
    return ctx.hit_count


def get_ctx(conn, jdata):
    """
    comments
    """

    timestamp_ini = datetime.datetime.strptime(jdata["t0"], "%Y-%m-%d")
    timestamp_end = datetime.datetime.strptime(jdata["tf"], "%Y-%m-%d")

    ctx = conn.new_context(
        facets="*",
        project=cmip_project,
        source_id=jdata["source"],
        experiment_id=jdata["scenario"],
        variable=jdata["variable"],
        frequency=jdata["frequency"],
        variant_label=jdata["variant_label"],
        from_timestamp=timestamp_ini.strftime("%Y-%m-%dT%H:%M:%SZ"),
        to_timestamp=timestamp_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        #        data_node = "esgf-data3.ceda.ac.uk",
    )
    return ctx


def massive_search(urls, models, scenarios, variables, frequencies):
    """
    comments
    """

    with open("search_cmip6.txt", "w") as f:
        f.write("Searching data in CMIP6 using ESFG Pyclient API")

    counter = 0
    for url in urls:
        for model in models:
            for scenario in scenarios:
                for variable in variables:
                    for frequency in frequencies:
                        jdata = {}
                        if scenario == "historical":
                            jdata["t0"] = "1980-01-01"
                            jdata["tf"] = "2010-12-31"
                        else:
                            jdata["t0"] = "2010-01-01"
                            jdata["tf"] = "2100-12-31"

                        jdata["source"] = model.split("_")[0]
                        jdata["scenario"] = scenario
                        jdata["variable"] = variable
                        jdata["frequency"] = frequency
                        jdata["variant_label"] = model.split("_")[-1]

                        conn = connect_esg(url)
                        matchs = number_of_matchs(conn, jdata)
                        result_search = rf"""

    ================
    Search number {counter}

    url: {url}
    source: {model.split("_")[0]}
    scenario: {scenario}
    variable: {variable}
    frequency: {frequency}
    variant_label: {model.split("_")[-1]}
    from_timestamp: {jdata["t0"]}
    to_timestamp: {jdata["tf"]}

    matchs: {matchs}
    ================

    """
                        with open("search_cmip6.txt", "a") as f:
                            f.write(result_search)
                        counter += 1
        print("url: ", url, " analysed!")


def massive_download(urls, models, scenarios, variables, frequencies, download_dir):
    """
    comments
    """

    for url in urls:
        for model in models:
            for scenario in scenarios:
                for variable in variables:
                    for frequency in frequencies:
                        jdata = {}
                        if scenario == "historical":
                            jdata["t0"] = "1980-01-01"
                            jdata["tf"] = "2010-12-31"
                        else:
                            jdata["t0"] = "2010-01-01"
                            jdata["tf"] = "2100-12-31"

                        jdata["source"] = model.split("_")[0]
                        jdata["scenario"] = scenario
                        jdata["variable"] = variable
                        jdata["frequency"] = frequency
                        jdata["variant_label"] = model.split("_")[-1]

                        conn = connect_esg(url)
                        matchs = number_of_matchs(conn, jdata)

                        if matchs > 0:
                            ctx = get_ctx(conn, jdata)
                            ds = ctx.search()[0]

                            fc = ds.file_context()

                            wget_script_content = fc.get_download_script()
#                            download_dir = outdir
                            script_name = (
                                "wget_"
                                + jdata["source"]
                                + "_"
                                + jdata["variant_label"]
                                + "_"
                                + jdata["scenario"]
                                + "_"
                                + jdata["variable"]
                                + "_"
                                + jdata["frequency"]
                                + ".sh"
                            )
                            print("Generating script: ", script_name)

                            with open(download_dir + script_name, "w") as writer:
                                writer.write(wget_script_content)

                            os.chmod(download_dir + script_name, 0o750)

                            #print("Downloading data ... ")
                            #cmd = f"cd data/ && bash {script_name}"
                            #p = subprocess.Popen(cmd, shell=True)
                            #p.wait()
