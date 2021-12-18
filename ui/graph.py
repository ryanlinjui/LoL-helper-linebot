import matplotlib.pyplot as plt
from matplotlib.axes import (
    Axes
)
from ui import req_keys

graph_nodes = (
    # x axies
    [ 1, 1,-1,-1],
    # y axies
    [ 1,-1,-1, 1],
)
def draw_subtitle(ax:Axes, b_x:float, b_y:float, num:float, title:str):
    ax.text(b_x, b_y+0.08, "{:.1f}".format(num*10), color='white', fontsize=18, horizontalalignment='center', bbox=dict(fc='firebrick', ec='none', alpha=0.5))
    ax.text(b_x, b_y-0.08, title, fontsize=14, horizontalalignment='center')
    
def draw_background(ax:Axes):
    x,y = graph_nodes
    graph_stage = 5

    for i in range(1, graph_stage+1):
        ax.fill(
            [ p*((1/graph_stage)*i) for p in x ],
            [ p*((1/graph_stage)*i) for p in y ],
            facecolor='none',
            edgecolor='firebrick', linewidth=1
        )
    
    for i in range(len(x)):
        ax.plot(
            [0, x[i]],
            [0, y[i]],
            color='firebrick', linewidth=1
        )


def export_graph(scale:list, filename:str):
    fig, ax = plt.subplots()
    x,y = graph_nodes

    # base of graph
    draw_background(ax)
    # user performance
    ax.fill(
        [ p*scale[i] for i, p in enumerate(x) ],
        [ p*scale[i] for i, p in enumerate(y) ],
        facecolor='purple',
        alpha=.5
    )

    # subtitle
    for i, k in enumerate(req_keys):
        draw_subtitle(ax, x[i]*1.2, y[i]*1.1, scale[i], k)
    ax.axis("off")
    ax.axis('equal')

    fig.savefig(filename)
