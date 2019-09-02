import plotly.graph_objects as go
import random
import networkx as nx
from twitterRequests import *

def get_pos():
    return [random.random() for i in range(0, 2)]

def mount_graph():
    # username = input('Whats your Twitter username? ')
    # friends = get_list(username, 'friends')
    friends = [
        {
            'name':'gabi',
            'verified': False
        },
        {
            'name':'mamis',
            'verified': False
        },
        {
            'name':'papis',
            'verified': False
        },
        {
            'name':'blabla',
            'verified': False
        }
    ]
    edges = [(0,1),(0,2),(0,3)]
    # for friend in friends:
    #     if friend['verified']:
    #         friends.remove(friend)
    #     else:
    #         f_edges = get_friends_edges(friend, friends)
    #         edges = [*edges, *f_edges]
        
    create_graph(friends, edges)


def get_friends_edges(friend, initial_list):
    friend_list = get_list(friend['screen_name'], 'friends')
    edges = []
    for person in friend_list:
        if person in initial_list:
            index1 = initial_list.index(friend)
            index2 = initial_list.index(person)
            edges.append((index1, index2))
    return edges


def create_graph(vec, edges):
    G = nx.Graph()

    for i in range(0,len(vec)):
        G.add_node(i, name=vec[i]['name'])
    
    G.add_edges_from(edges)
    pos = nx.fruchterman_reingold_layout(G)
    print(pos)

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
    # create_barear_token()
    mount_graph()
