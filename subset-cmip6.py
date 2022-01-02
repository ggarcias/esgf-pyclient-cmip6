#!/usr/bin/env python
# coding: utf-8

# # Subset CMIP6 Datasets with xarray
# 
# xarray: http://xarray.pydata.org/en/stable/index.html

# ## Search CMIP6 Dataset with ESGF pyclient
# 
# using: https://esgf-pyclient.readthedocs.io/en/latest/index.html

# In[ ]:


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
    conn = SearchConnection("https://" + url, distrib=True)
    return conn

conn = connect_esg(urls[0])

# In[ ]:


ctx = conn.new_context(
    project='CMIP6', 
    source_id='UKESM1-0-LL', 
    experiment_id='historical', 
    variable='tas', 
    frequency='mon', 
    variant_label='r1i1p1f2',
    data_node='esgf-data3.ceda.ac.uk')
ctx.hit_count


# In[ ]:


result = ctx.search()[0]
result.dataset_id


# In[ ]:


files = result.file_context().search()
for file in files:
    print(file.opendap_url)


# ## Subset single dataset with xarray
# 
# Using OpenDAP: http://xarray.pydata.org/en/stable/io.html?highlight=opendap#opendap

# In[ ]:


import xarray as xr
ds = xr.open_dataset(files[0].opendap_url, chunks={'time': 120})
print(ds)


# In[ ]:


da = ds['tas']
da = da.isel(time=slice(0, 1))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
da.plot()


# ## Subset over multiple datasets
# 

# In[ ]:


ds_agg = xr.open_mfdataset([files[0].opendap_url, files[1].opendap_url], chunks={'time': 120}, combine='nested', concat_dim='time')
print(ds_agg)


# In[ ]:


da = ds_agg['tas']
da = da.isel(time=slice(1200, 1201))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))


# In[ ]:


da.plot()


# ## Download dataset

# In[ ]:


da.to_netcdf('tas_africa_19500116.nc')

