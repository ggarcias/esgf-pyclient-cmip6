#!/usr/bin/env python
# coding: utf-8

# ## Examples of pyesgf.logon usage

# **NOTE**: For the logon module you need to install the latest `myproxyclient` from pypi:
# ```
# $ conda create -c conda-forge -n esgf-pyclient python=3.6 pip esgf-pyclient
# $ conda activate esgf-pyclient
# (esgf-pyclient) pip install myproxyclient
# ```

# Obtain MyProxy credentials to allow downloading files or using secured OpenDAP:

# In[ ]:


from pyesgf.logon import LogonManager
lm = LogonManager()
lm.logoff()
lm.is_logged_on()


# **NOTE**: When you run it for the first time you need to set `bootstrap=True`.

# In[ ]:


OPENID = 'https://esgf-data.dkrz.de/esgf-idp/openid/USERNAME'
lm.logon_with_openid(openid=OPENID, password=None, bootstrap=True)
lm.is_logged_on()


# **NOTE**: you may be prompted for your username if not available via your OpenID.
# 

# Obtain MyProxy credentials from the MyProxy host in *interactive* mode asking you for *username* and *password*:

# In[ ]:


myproxy_host = 'esgf-data.dkrz.de'
lm.logon(hostname=myproxy_host, interactive=True, bootstrap=True)
lm.is_logged_on()


# **NOTE**: See the ``pyesgf.logon`` module documentation for details of how to use myproxy username instead of OpenID.
