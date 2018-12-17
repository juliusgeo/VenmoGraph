import requests
import networkx as nx


g = nx.Graph()
cookies = {'api_access_token':''}
headers = {'Accept':'application/json', 'Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive', 'content-type':'application/x-www-form-urlencoded', 'DNT':'1', 'Host':'venmo.com', 'origin':'https://venmo.com', 'Referer':'https://venmo.com/'}
username = raw_input("What venmo username do you want to graph? ")
r = requests.get("https://venmo.com/api/v5/users/me", cookies=cookies)
print(r.json())
if(username == r.json()['username']):
	start_id = r.json()['id']
else:
	r = requests.get("https://venmo.com/api/v5/search?q="+username, cookies=cookies)
	start_id = r.json()['data'][0]['id']
stack = set()
stack.add(start_id)
transaction_log = []
def parse_transaction(transaction, recurse):
	if 'payment_id' in transaction.keys():
		if transaction['payment_id'] in transaction_log:
			return
	if(transaction['transactions'][0]['target']=='a phone number'):
		return
	payer = transaction['actor']['username']
	paid = transaction['transactions'][0]['target']['username']
	payer_id = transaction['actor']['id']
	paid_id = transaction['transactions'][0]['target']['id']
	if(recurse == True):
		if len(stack) <= 20:
			stack.add(payer_id)
			stack.add(paid_id)
			#add_person_to_graph(payer_id)
			#add_person_to_graph(paid_id)
	if(g.has_edge(payer, paid)):
		g[payer][paid]['weight'] +=1
	else:
		if 'payment_id' in transaction.keys():
			transaction_log.append(transaction['payment_id'])
		g.add_edge(payer, paid, weight=1)

def add_person_to_graph(id, recurse = True):
	print('added to stack')
	r = requests.get('https://venmo.com/api/v5/users/'+id+'/feed', cookies=cookies)
	if 'data' not in r.json():
		return;
	for transaction in r.json()['data']:
		parse_transaction(transaction, recurse)
	while('paging' in r.json()):
		r = requests.get(r.json()['paging']['next'], cookies=cookies)
		if 'data' not in r.json():
			return;
		for transaction in r.json()['data']:
			parse_transaction(transaction, recurse)

add_person_to_graph(start_id)
others = list(stack)
for i in others:
	add_person_to_graph(i, recurse = False)
import matplotlib.pyplot as plt
edge_list=sorted(g.edges(data=True), key=lambda x: x[2]['weight'])
pos=nx.spring_layout(g)
edgewidth = [ d['weight']/3+1 for (u,v,d) in edge_list]
edgecolors = [ float(d['weight']+1) for (u,v,d) in edge_list]
node_colors = [plt.cm.Blues(i) for i in edgecolors]
#edgecolors = [math.log(i) for i in edgecolors]
print(edgecolors)
nx.draw_networkx(g,pos, node_color='#A0CBE2', cmap=plt.cm.Blues, edgelist=[], font_size=6, node_size=100)
nx.draw_networkx_edges(g,pos, width=3, edgelist=edge_list,edge_width=edgewidth, edge_color=edgecolors, edge_cmap=plt.cm.Blues)
plt.show()


