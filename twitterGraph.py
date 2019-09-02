import plotly.graph_objects as go
import random
import networkx as nx
import os
from twitterRequests import *

def get_user_list(username):
    file_path = 'data/user_list/' + username + '.json'
    data = []
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
    else:
        data = get_list(username, 'friends')
        if len(data) > 0:
            with open(file_path, 'w') as outfile:
                json.dump(data, outfile)
    
    return data

def get_ids_list(username):
    file_path = 'data/ids/' + username + '.json'
    data = []
    if os.path.isfile(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
    else:
        data, rate_limit = get_ids(username, 'friends')
        print(rate_limit)
        if not rate_limit:
            with open(file_path, 'w') as outfile:
                json.dump(data, outfile)
    
    return data

def mount_graph():
    username = input('Whats your Twitter username? ')
    friends = get_user_list(username)
    for friend in friends:
        if friend['verified']:
            friends.remove(friend)
    create_graph(friends)


def create_graph(vec):
    G = nx.Graph()

    for i in range(0,len(vec)):
        G.add_node(i, name=vec[i]['name'], id=vec[i]['id'], username=vec[i]['screen_name'])

    nodes = G.nodes(data=True)
    for out_node in nodes:
        username = str(out_node[1]['username'])
        print(username)
        related_friends = get_ids_list(username)
        for node in nodes:
            for friend_id in related_friends:
                if(friend_id == node[1]['id']):
                    print('here')
                    G.add_edge(out_node[0], node[0])


    pos = nx.fruchterman_reingold_layout(G)

    edge_x = []
    edge_y = []
    for e in G.edges():
        edge_x.extend([pos[e[0]][0], pos[e[1]][0], None])
        edge_y.extend([pos[e[0]][1], pos[e[1]][1], None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x =[pos[k][0] for k in range(len(pos))]
    node_y=[pos[k][1] for k in range(len(pos))]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(G.nodes[node]['name'])

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                title='<b>Projeto e Análise de Algoritimos - Grafos 1</b>',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="Feito por Alexandre Miguel e Gabriela Guedes",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002)],
                    xaxis=dict(showgrid=False, zeroline=False,
                            showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()



if __name__ == "__main__":
    create_barear_token()
    mount_graph()
