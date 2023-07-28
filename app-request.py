#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import json
# URL of the API endpoint

url = 'http://localhost:5000/similarity_measure'
url = 'https://similaritymeasure-74h7jr6qka-oc.a.run.app/similarity_measure'

# Data to be sent in the request body
data = {'number': 2}

# Send POST request
response = requests.post(url, json=json.dumps(data))

# Check the response status code
if response.status_code == 200:
    # Request was successful
    print('POST request was successful.')
else:
    # Request failed
    print('POST request failed.')

# Print the response content
print(response.json())


# In[ ]:




