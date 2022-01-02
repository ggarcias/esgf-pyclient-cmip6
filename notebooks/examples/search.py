#!/usr/bin/env python
# coding: utf-8

# ## Examples of pyesgf.search usage

# Prelude:

# In[ ]:


from pyesgf.search import SearchConnection
conn = SearchConnection('http://esgf-index1.ceda.ac.uk/esg-search', 
                        distrib=True)


# Find how many datasets containing *humidity* in a given experiment family:

# In[ ]:


ctx = conn.new_context(project='CMIP5', query='humidity')
ctx.hit_count


# In[ ]:


ctx.facet_counts['experiment_family']


# Search using a partial ESGF dataset ID (and get first download URL):

# In[ ]:


conn = SearchConnection('http://esgf-index1.ceda.ac.uk/esg-search', distrib=True)
ctx = conn.new_context()
dataset_id_pattern = "cordex.output.WAS-44.IITM.CCCma-CanESM2.historical.r1i1p1.*"
results = ctx.search(query="id:%s" % dataset_id_pattern)
files = results[0].file_context().search()
download_url = files[0].download_url
print(download_url)


# Find the OpenDAP URL for an aggregated dataset:

# In[ ]:


conn = SearchConnection('http://esgf-data.dkrz.de/esg-search', distrib=False)
ctx = conn.new_context(project='CMIP5', model='MPI-ESM-LR', experiment='decadal2000', time_frequency='day')
print('Hits: {}, Realms: {}, Ensembles: {}'.format(
    ctx.hit_count, 
    ctx.facet_counts['realm'], 
    ctx.facet_counts['ensemble']))


# In[ ]:


ctx = ctx.constrain(realm='atmos', ensemble='r1i1p1')
ctx.hit_count


# In[ ]:


result = ctx.search()[0]
agg_ctx = result.aggregation_context()
agg = agg_ctx.search()[0]
print(agg.opendap_url)


# Find download URLs for all files in a dataset:

# In[ ]:


conn = SearchConnection('http://esgf-data.dkrz.de/esg-search', distrib=False)
ctx = conn.new_context(project='obs4MIPs')
ctx.hit_count


# In[ ]:


ds = ctx.search()[0]
files = ds.file_context().search()
len(files)


# In[ ]:


for f in files:
    print(f.download_url)


# Define a search for datasets that includes a temporal range:

# In[ ]:


conn = SearchConnection('http://esgf-index1.ceda.ac.uk/esg-search', distrib=False)
ctx = conn.new_context(
    project="CMIP5", model="HadGEM2-ES",
    time_frequency="mon", realm="atmos", ensemble="r1i1p1", latest=True,
    from_timestamp="2100-12-30T23:23:59Z", to_timestamp="2200-01-01T00:00:00Z")
ctx.hit_count


# Or do the same thing by searching without temporal constraints and then applying the constraint:

# In[ ]:


ctx = conn.new_context(
    project="CMIP5", model="HadGEM2-ES",
    time_frequency="mon", realm="atmos", ensemble="r1i1p1", latest=True)
ctx.hit_count


# In[ ]:


ctx = ctx.constrain(from_timestamp = "2100-12-30T23:23:59Z", to_timestamp = "2200-01-01T00:00:00Z")
ctx.hit_count

