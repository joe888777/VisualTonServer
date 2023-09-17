import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from getData import getData
from pyvis.network import Network




def html_to_text():
    data = create_graph()
    with open('simple_graph.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
        return html_content,data

def create_graph():

    data = getData()
    # 缩短 sender 和 receiver 地址
    for tx in data:
        tx['Sender_address'] = tx['Sender_address'][:6]
        tx['Receiver_address'] = tx['Receiver_address'][:6]
    df = pd.DataFrame(data)

    G = nx.DiGraph()
    for index, row in df.iterrows():
        sender_address = row["Sender_address"]
        receiver_address = row["Receiver_address"]
        amount = row["Amount"]
        node_type = row["Type"]
        node_color = "#B3C7D6"
        if node_type:
            node_color = node_type
        if amount >= 10000:
            node_size = 50
        elif amount >= 1000:
            node_size = 30
        else:
            node_size = 10
        G.add_node(
            sender_address,
            label=sender_address,
            color=node_color,
            size=node_size,
            borderWidth=2)
        G.add_node(
            receiver_address,
            label=receiver_address,
            color=node_color,
            size=node_size,
            borderWidth=2)
        G.add_edge(
            sender_address,
            receiver_address,
            label=amount,
            color="black",
            arrows="to",
            length=400,
            width=2)
        net = Network(
            notebook=True,
            width="1000px",
            height="700px",
            bgcolor='white',
            font_color='black',
            directed=True,
            cdn_resources='in_line')
        net.from_nx(G)
        
        net.save_graph("transaction_graph.html")


        # Old version
    # G = nx.from_pandas_edgelist(df,source='Sender_address',target='Receiver_address',edge_attr='Amount',create_using=nx.Graph())
    # print(list(G))
    # plt.figure(figsize=(10,10))
    # pos = nx.draw_kamada_kawai(G)
    # nx.draw(G,with_labels=True,node_color='purple',edge_cmap=plt.cm.Reds,pos=pos,arrows =True)


    net = Network(notebook=True,width="1000px",height="700px",bgcolor='#222222',font_color='white',cdn_resources='remote')
    net.from_nx(G)
    # net.save_graph("simple_graph.html")

    return data

create_graph()

