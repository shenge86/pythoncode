# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 22:30:02 2026

Build network social chart.

@author: sheng
@name: Network Social Chart
@version:
    
This module contains the following functions:
    
- `build_social_diagram_full` - Builds social diagram for people
    
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#%%
def build_social_diagram_full(nodes_list, connections, description="", title="Social Network"):
    """
    Builds and displays a social diagram.
    
    Args:
        nodes_list (List): contains 2-tuples (Name, Group) -> [("Alice", "Admin"), ...]
        connections (List): contains 2-tuples (Name1, Name2) -> [("Alice", "Bob"), ...]
        description (str): description of the legend
        title (str): title of the plot
        
    Returns:
        None
    """
    G = nx.Graph()
    G.add_nodes_from([n[0] for n in nodes_list])
    
    try:
        G.add_weighted_edges_from(connections)
    except:
        G.add_edges_from(connections)
    
    #%% 1. Setup colors
    palette = {
        "Unique"   : "#ff6666",   # Soft Red
        "Spiritual": "#66b3ff",   # Soft Blue
        "Creative" : "#99ff99",   # Soft Green
        "Technical": "#964B00",   # Brown
        "Default": "#d9d9d9"      # Grey
    }
    node_groups = {name: group for name, group in nodes_list}
    node_colors = [palette.get(node_groups.get(n, "Default"), palette["Default"]) for n in G.nodes()]

    #%% 2. Visualization setup
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # define the position of the nodes
    # k = optimal distance between nodes
    # pos = nx.spring_layout(G, k=0.5) 
    pos = nx.spring_layout(G, weight='weight') 
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, 
            node_size=1500, font_size=8, font_weight='bold', edge_color="#cccccc", ax=ax)

    #%% 3. ADD THE TEXT BOX
    if description:
        # Define box style
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        
        # ax.text(x, y, text, ...)
        # transform=ax.transAxes makes (0,0) bottom-left and (1,1) top-right (if using horizontalalignment='right')
        ax.text(0.01, 0.01, description, transform=ax.transAxes, fontsize=10,
                verticalalignment='bottom', horizontalalignment='left', bbox=props)

    #%% 4. Legend
    legend_elements = [Line2D([0],[0], marker='o', color='w', label=k, 
                              markerfacecolor=v, markersize=10) for k, v in palette.items()]
    ax.legend(handles=legend_elements, title="Groups", loc='upper left', bbox_to_anchor=(1, 1))
    
    plt.title(title, pad=20)
    plt.savefig('shen_socialdiagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

#%%
if __name__ == '__main__':
    # Nodes
    nodes = [
        ('Shen Ge', 'Unique'),
        ('Rose', 'Unique'),
        ('Natalia', 'Unique'),
        ('Adrienne', 'Creative'),
        ('Jenny B.', 'Creative'),
        ('Bucky R.', 'Creative'),
        ('Yolanda M.', 'Creative'),
        ('Jenny A.', 'Unique'),
        ('Zack W.', 'Creative'),
        ('Kathy', 'Creative'),
        ('Eddie', 'Creative'),
        ('Dominique', 'Creative'),
        ('DJ B.', 'Unique'),
        ('Justin E.', 'Spiritual'),
        ('Eduardo C.', 'Spiritual'),
        ('Geraldo O.', 'Spiritual'),
        ('Alex O.', 'Unique'),
        ('Eric C.', 'Unique'),
        ('Joe H.', 'Spiritual'),
        ('Gina L.', 'Unique'),
        ('Walter L.', 'Technical'),
        ('Daniela L.', 'Creative'),
        ('Ania', 'Unique'),
        ('Druck', 'Technical'),
        ('Tony C.', 'Technical'),
        ('Rafael T.', 'Technical'),
        ('Ryan F.', 'Technical'),
        ('Sam W.', 'Unique'),
        ('Sam M.', 'Technical'),
        ('Michelle T.', 'Technical'),
        ('Regina A.', 'Technical'),
        ('Glenn T.', 'Technical'),
        ('Leonard K.', 'Technical'),
        ('Xupeng', 'Technical'),
        ('Corey', 'Unique'),
        ('Justin Y.', 'Unique'),
        ('Michelle F.', 'Unique'),
        ('Alicia B.', 'Unique'),
        ('Mary C.', 'Unique'),
        ('Steve K.', 'Unique'),
        ('Youssouf D.', 'Unique'),
        ('Krista K.', 'Unique'),
        ('Joy', 'Unique'),
        ('Virgiliu P.', 'Technical'),
    ]
    
    # Each tuple is a link between two people (nodes)
    social_connections = [
        ('Shen Ge', 'Joy'),
        ('Shen Ge', 'Michelle F.'),
        ('Shen Ge', 'Rose'),
        ('Shen Ge', 'Alex O.'),
        ('Shen Ge', 'Eric C.'),
        ('Shen Ge', 'Druck'),
        ('Shen Ge', 'Michelle T.'),
        ('Shen Ge', 'Justin Y.'),
        ('Shen Ge', 'Alex O.'),
        ('Shen Ge', 'Eduardo C.'),
        ('Shen Ge', 'Geraldo O.'),
        ('Shen Ge', 'DJ B.'),
        ('Shen Ge', 'Justin E.'),
        ('Shen Ge', 'Joe H.'),
        ('Shen Ge', 'Ryan F.'),
        ('Shen Ge', 'Rafael T.'),
        ('Shen Ge', 'Tony C.'),
        ('Shen Ge', 'David C.'),
        ('Shen Ge', 'Corey'),
        ('Shen Ge', 'Ania'),
        ('Shen Ge', 'Natalia'),
        ('Shen Ge', 'Jenny B.'),
        ('Shen Ge', 'Bucky R.'),
        ('Shen Ge', 'Jenny A.'),
        ('Shen Ge', 'Adrienne'),
        ('Shen Ge', 'Yolanda M.'),
        ('Shen Ge', 'Alicia B.'),
        ('Shen Ge', 'Sam W.'),
        ('Shen Ge', 'Sam M.'),
        ('Shen Ge', 'Regina A.'),
        ('Shen Ge', 'Glenn T.'),
        ('Shen Ge', 'Leonard K.'),
        ('Shen Ge', 'Jeanette'),
        ('Shen Ge', 'Zack W.'),
        ('Shen Ge', 'Kathy'),
        ('Shen Ge', 'Mary C.'),
        ('Kathy', 'Mary C.'),
        ('Shen Ge', 'Xupeng'),
        ('Shen Ge', 'Steve K.'),
        ('Shen Ge', 'Youssouf D.'),
        ('Shen Ge', 'Krista K.'),
        ('Shen Ge', 'Julie P.'),
        ('Youssouf D.', 'Julie P.'),
        ('Youssouf D.', 'Krista K.'),
        ('Julie P.', 'Krista K.'),
        ('Shen Ge', 'Gina L.'),
        ('Shen Ge', 'Walter L.'),
        ('Shen Ge', 'Daniela L.'),
        ('Walter L.', 'Gina L.'),
        ('Daniela L.', 'Gina L.'),
        ('Daniela L.', 'Walter L.'),
        ('Jeanette', 'Leonard K.'),
        ('Corey', 'Ania'),
        ('Corey', 'Justin Y.'),
        ('Michelle T.', 'Justin Y.'),
        ('Michelle F.', 'Justin Y.'),
        ('Eduardo C.', 'Justin Y.'),
        ('Michelle F.', 'DJ B.'),
        ('Michelle F.', 'Rafael T.'),
        ('Michelle F.', 'Ryan F.'),
        ('Rafael T.', 'Ryan F.'),
        ('Rafael T.', 'Sam M.'),
        ('Sam M.', 'Ryan F.'),
        ('Tony C.', 'David C.'),
        ('Joe H.', 'Justin Y.'),
        ('Eric C.', 'Justin Y.'),
        ('Eric C.', 'Justin E.'),
        ('Eric C.', 'Druck'),
        ('Eric C.', 'Eduardo C.'),
        ('Eduardo C.', 'Geraldo O.'),
        ('Alex O.', 'Rose'),
        ('Alex O.', 'Eric C.'),
        ('Alex O.', 'Geraldo O.'),
        ('Alex O.', 'Eduardo C.'),
        ('Alex O.', 'Natalia'),
        ('Alex O.', 'Jenny A.'),
        ('Rose', 'Natalia'),
        ('Rose', 'Adrienne'),
        ('Rose', 'Jenny B.'),
        ('Natalia', 'Adrienne'),
        ('Natalia', 'Jenny B.'),
        ('Natalia', 'Jenny A.'),
        ('Rose', 'Bucky R.'),
        ('Adrienne', 'Bucky R.'),
        ('Jenny B.', 'Bucky R.'),
        ('Jenny B.', 'Adrienne'),
        ('Yolanda M.', 'Bucky R.'),
        ('Yolanda M.', 'Jenny B.'),
        ('Shen Ge', 'Eddie'),
        ('Shen Ge', 'Dominique'),
        ('Eddie', 'Dominique'),
        ('Shen Ge', 'Virgiliu P.'),
    ]
    
    social_connections_weighted = [
        ('Shen Ge', 'Jenny A.', 0.1),
        ('Shen Ge', 'Jenny B.', 0.1),
        ('Shen Ge', 'Alex O.', 0.2)
        ]
    
    
    desc = "Groups Notes:\nUnique means our conversations cannot be easily classified.\nSpiritual means we mainly talk about faith, God or emotional feelings. \
        \nCreative means we mainly talk about literature, art, music or upcoming creative events.\
        \nTechnical means we mainly talk on aerospace, science, or business."
    build_social_diagram_full(nodes, social_connections, description=desc)