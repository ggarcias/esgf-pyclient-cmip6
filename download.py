#!/usr/bin/env python
# coding: utf-8

# ## Examples of pyesgf download usage

# Obtain MyProxy credentials to allow downloading files:

# In[ ]:


from pyesgf.logon import LogonManager
lm = LogonManager()
lm.logoff()
lm.is_logged_on()


# In[ ]:


myproxy_host = 'esgf-data.dkrz.de'
lm.logon(username=None, password=None, hostname=myproxy_host)
lm.is_logged_on()


# Now download a file using the ESGF wget script extracted from the server:

# In[ ]:


from pyesgf.search import SearchConnection
conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=False)
ctx = conn.new_context(project='obs4MIPs', institute='FUB-DWD')
ds = ctx.search()[0]

import tempfile
fc = ds.file_context()
wget_script_content = fc.get_download_script()
script_path = tempfile.mkstemp(suffix='.sh', prefix='download-')[1]
with open(script_path, "w") as writer:
    writer.write(wget_script_content)
    
import os, subprocess
os.chmod(script_path, 0o750)
download_dir = os.path.dirname(script_path)
subprocess.check_output("{}".format(script_path), cwd=download_dir)


# … and the files will be downloaded to a temporary directory:

# In[ ]:


print(download_dir)


# If you are doing batch searching and things are running slow, you might be able to achieve a considerable speed up by sending the following argument to the search call:

# In[ ]:


ctx.search(ignore_facet_check=True)


# This cuts out an extra call that typically takes 2 seconds to return a response. Note that it may mean some of the functionality is affected (such as being able to view the available facets and access the hit count) so use this feature with care.

# You can also dictate how the search batches up its requests with:

# In[ ]:


ctx.search(batch_size=250)


# The ``batch_size`` argument does not affect the final result but may affect the speed of the response. The batch size can also be set as a default in the ``pyesgf.search.consts`` module.
