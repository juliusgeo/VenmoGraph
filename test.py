import requests
import networkx as nx
import matplotlib.pyplot as plt
g = nx.Graph()
cookies = {'csrftoken2':'OYjWQxuGxFHv5Pv4l1xAscRtRLrNj6aw', 'v_id':'fp01-ae99378e-76e8-4e89-91d5-65a17eb4ff78', 'api_access_token':'f119f9aad9baa62d85e09dbb247d5312bcab115bd48418d480e2167ba286ce19', 'sessionid':'ohfkkeg03d6ziam76bg1c88n6e86684g', 'sent_device_data':'1'}
r = requests.get('https://venmo.com/api/v5/users/13179759/feed', cookies=cookies)
for transaction in r.json()['data']:
	payer = transaction['actor']['username']
	paid = transaction['transactions'][0]['target']['username']
	g.add_edge(payer, paid)
while('paging' in r.json()):
	r = requests.get(r.json()['paging']['next'], cookies=cookies)
	for transaction in r.json()['data']:
		payer = transaction['actor']['username']
		paid = transaction['transactions'][0]['target']['username']
		g.add_edge(payer, paid)
nx.draw(g)