import datetime

from pyesgf.search import SearchConnection


cmip_project = "CMIP6"


def connect_esg(url):
    """
    comments
    """
    conn = SearchConnection("https://" + url, distrib=True)
    return conn


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
        variant_label = jdata["variant_label"],
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
        variant_label = jdata["variant_label"],
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


def massive_download(urls, models, scenarios, variables, frequencies):
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

