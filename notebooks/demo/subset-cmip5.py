#!/usr/bin/env python
# coding: utf-8

# # Subset CMIP5 Datasets with xarray
# 
# xarray: http://xarray.pydata.org/en/stable/index.html

# ## Search CMIP5 Dataset with ESGF pyclient
# 
# using: https://esgf-pyclient.readthedocs.io/en/latest/index.html

# In[ ]:


from pyesgf.search import SearchConnection
conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)


# In[ ]:


ctx = conn.new_context(
    project='CMIP5', 
    experiment='rcp45',
    model='HadCM3',
    ensemble='r1i1p1',
    time_frequency='mon',
    realm='atmos',
    data_node='esgf-data1.ceda.ac.uk',
    )
ctx.hit_count


# In[ ]:


result = ctx.search()[0]
result.dataset_id


# In[ ]:


files = result.file_context().search()
for file in files:
    if 'tasmax' in file.opendap_url:
        tasmax_url = file.opendap_url
        print(tasmax_url)


# ## ESGF Logon

# In[ ]:


from pyesgf.logon import LogonManager
lm = LogonManager()
lm.logoff()
lm.is_logged_on()


# In[ ]:


lm.logon(hostname='esgf-data.dkrz.de', interactive=True, bootstrap=True)
lm.is_logged_on()


# ## Subset single dataset with xarray
# 
# Using OpenDAP: http://xarray.pydata.org/en/stable/io.html?highlight=opendap#opendap

# In[ ]:


import xarray as xr
ds = xr.open_dataset(tasmax_url, chunks={'time': 120})
print(ds)


# In[ ]:


da = ds['tasmax']
da = da.isel(time=slice(0, 1))
da = da.sel(lat=slice(-50, 50), lon=slice(0, 50))


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
da.plot()


# ## Download to NetCDF

# In[ ]:


da.to_netcdf('tasmax.nc')

