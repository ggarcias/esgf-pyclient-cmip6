import datetime
import json
from pyesgf.search import SearchConnection


urls = [
        "esgf-node.llnl.gov/esg-search", 
        "esgf-node.ipsl.upmc.fr/esg-search",
        "esgf-data.dkrz.de/esg-search",
        "esgf-index1.ceda.ac.uk/esg-search",
]



def connect_esg(url):
    """
    comments
    """
    conn = SearchConnection("http://" + url, distrib=True)
    return conn


def number_of_matchs(conn, jdata):
    """
    comments
    """

    timestamp_ini = datetime.datetime.strptime("1980-01-01","%Y-%m-%d")
    timestamp_end = datetime.datetime.strptime("2010-12-31","%Y-%m-%d")

    ctx = conn.new_context(
        project = "CMIP6",
        source_id = "GFDL-ESM4",
        experiment_id = "historical",
        variable = "psl",
        time_frequency = "3hr",
        variant_label = "r1i1p1f1",
        from_timestamp = timestamp_ini.strftime("%Y-%m-%dT%H:%M:%SZ"),
        to_timestamp = timestamp_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )
    return ctx.hit_count


#conn = connect_esg(urls[0])

#matchs = number_of_matchs(conn, "kk")
#print(matchs)

for url in urls:
    conn = SearchConnection('https://'+urls[0],
                            distrib=True)

    ctx = conn.new_context(facets="*", project='CMIP6', 
            source_id="MRI-ESM2-0", 
            experiment_id="ssp245",
            variable="sfcWind",
            frequency="day",
            #variant_label="r1i1p1f1",
            #from_timestamp="2010-01-01T00:00:00Z",
            #to_timestamp="2100-12-31T00:00:00Z"
    )
    print(ctx.hit_count)

