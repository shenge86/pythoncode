# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 22:30:02 2026

@author: sheng
@name: Network Social Chart
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def build_social_diagram_static(nodes_list, connections, description="", title="Shen's Social Network"):
    """
    Builds and displays a social diagram.
    
    :param nodes_list: List of tuples (Name, Group) -> [("Alice", "Admin"), ...]
    :param connections: List of tuples (Name1, Name2) -> [("Alice", "Bob"), ...]
    :param title: The title of the plot
    """
    G = nx.Graph()

    # 1. Add nodes with a 'group' attribute
    for name, group in nodes_list:
        G.add_node(name, group=group)
    
    # 2. Add edges
    G.add_edges_from(connections)
    
    # 3. Define the color palette
    # You can add more groups and colors here
    palette = {
        "Unique"   : "#ff6666",   # Soft Red
        "Spiritual": "#66b3ff",   # Soft Blue
        "Creative" : "#99ff99",   # Soft Green
        "Technical": "#964B00",   # Brown
        "Default": "#d9d9d9"      # Grey
    }
    
    # 4. Map colors to nodes based on their group
    # We iterate through G.nodes to ensure the color list matches the graph order
    node_colors = []
    for node in G.nodes():
        group = G.nodes[node].get('group', 'Default')
        node_colors.append(palette.get(group, palette["Default"]))
    
    # 5. Create the legend
    # We create a "dummy" marker for each unique group in the palette
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=group,
               markerfacecolor=color, markersize=12)
        for group, color in palette.items() if group != "Default"
    ]
    
    
    # 6. Visualization
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, k=0.5, iterations=50) # k adjusts spacing
    
    nx.draw(
        G, pos, 
        with_labels=True, 
        node_color=node_colors, 
        node_size=2000, 
        font_size=3, 
        font_weight='bold', 
        edge_color="#cccccc",
        width=1.5
    )
    
    plt.legend(handles=legend_elements, title="People Types", loc='upper left', bbox_to_anchor=(1, 1))
    
    plt.title(title, pad=20)
    plt.savefig('shen_socialdiagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

#%%
def build_social_diagram_full(nodes_list, connections, description="", title="Social Network"):
    G = nx.Graph()
    G.add_nodes_from([n[0] for n in nodes_list])
    G.add_edges_from(connections)
    
    # 1. Setup colors
    palette = {
        "Unique"   : "#ff6666",   # Soft Red
        "Spiritual": "#66b3ff",   # Soft Blue
        "Creative" : "#99ff99",   # Soft Green
        "Technical": "#964B00",   # Brown
        "Default": "#d9d9d9"      # Grey
    }
    node_groups = {name: group for name, group in nodes_list}
    node_colors = [palette.get(node_groups.get(n, "Default"), palette["Default"]) for n in G.nodes()]

    # 2. Visualization setup
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5)
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, 
            node_size=1500, font_size=8, font_weight='bold', edge_color="#cccccc", ax=ax)

    # 3. ADD THE TEXT BOX
    if description:
        # Define box style
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        
        # ax.text(x, y, text, ...)
        # transform=ax.transAxes makes (0,0) bottom-left and (1,1) top-right (if using horizontalalignment='right')
        ax.text(0.01, 0.01, description, transform=ax.transAxes, fontsize=10,
                verticalalignment='bottom', horizontalalignment='left', bbox=props)

    # 4. Legend
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
        ('Natalia', 'Creative'),
        ('Adrienne', 'Creative'),
        ('Jenny B.', 'Creative'),
        ('Bucky R.', 'Creative'),
        ('Yolanda M.', 'Creative'),
        ('Jenny', 'Creative'),
        ('Zack W.', 'Creative'),
        ('Kathy', 'Creative'),
        ('Eddie', 'Creative'),
        ('Dominique', 'Creative'),
        ('DJ B.', 'Unique'),
        ('Justin E.', 'Spiritual'),
        ('Eduardo C.', 'Spiritual'),
        ('Geraldo O.', 'Spiritual'),
        ('Alex O.', 'Unique'),
        ('Eric C.', 'Spiritual'),
        ('Joe H.', 'Spiritual'),
        ('Gina L.', 'Unique'),
        ('Walter L.', 'Technical'),
        ('Daniela L.', 'Creative'),
        ('Ania', 'Unique'),
        ('Druck', 'Technical'),
        ('Tony C.', 'Technical'),
        ('Rafael T.', 'Technical'),
        ('Ryan F.', 'Technical'),
        ('Sam W.', 'Technical'),
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
        ('Shen Ge', 'Jenny'),
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
        ('Rose', 'Natalia'),
        ('Rose', 'Adrienne'),
        ('Rose', 'Jenny B.'),
        ('Natalia', 'Adrienne'),
        ('Natalia', 'Jenny B.'),
        ('Rose', 'Bucky R.'),
        ('Adrienne', 'Bucky R.'),
        ('Jenny B.', 'Bucky R.'),
        ('Jenny B.', 'Adrienne'),
        ('Yolanda M.', 'Bucky R.'),
        ('Yolanda M.', 'Jenny B.'),
        ('Shen Ge', 'Eddie'),
        ('Shen Ge', 'Dominique'),
        ('Eddie', 'Dominique'),
    ]
    
    # Run the function (basic one without description)
    # build_social_diagram_static(nodes, social_connections)
    
    desc = "Groups Notes:\nUnique means our conversations cannot be easily classified.\nSpiritual means we mainly talk about faith, God or emotional feelings. \
        \nCreative means we mainly talk about literature, art, music or upcoming creative events.\
        \nTechnical means we mainly talk on aerospace, science, or business."
    build_social_diagram_full(nodes, social_connections, description=desc)