from typing import Union
import plotly.graph_objects as go
import plotly.io as pio
import networkx as nx

pio.templates.default = "plotly_white"


def build_network(
    graph: nx.Graph,
    layout: nx.layout,
    focus1: Union[str, None] = None,
    focus2: Union[str, None] = None,
) -> tuple[go.Scatter, go.Scatter]:
    """Generates a network scatterplot's data structure.

    Args:
        graph (nx.Graph): networkx graph to be drawn
        layout (nx.layout): layout in which to visualize the graph
        focus1 (Union[str, None], optional): author to highlight. Defaults to None.
        focus2 (Union[str, None], optional): author to highlight. Defaults to None.

    Returns:
        tuple[go.Scatter, go.Scatter]: Plotly Scatter graph object traces.
    """
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = layout[edge[0]]
        x1, y1 = layout[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.25, color="#999999"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = []
    node_y = []
    node_name = []
    for node in graph.nodes():
        x, y = layout[node]
        node_x.append(x)
        node_y.append(y)
        if node == focus1 or node == focus2:
            node_name.append(f"**{node}**")
        else:
            node_name.append(node)

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(graph.adjacency()):
        n_info = len(adjacencies[1])
        node_adjacencies.append(n_info)
        node_text.append(f"# of connections: {str(n_info)}")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        hovertext=node_name,
        customdata=node_text,
        hovertemplate="<b>%{hovertext}</b><br>%{customdata}<extra></extra>",
        marker=dict(
            showscale=True,
            colorscale="thermal",
            color=[],
            size=5,
            colorbar=dict(
                thickness=20,
                title="Co-authors",
                xanchor="left",
                titleside="top",
            ),
            line_width=0.5,
        ),
    )
    node_trace.marker.color = node_adjacencies
    return node_trace, edge_trace


def draw_network(
    node_trace: go.Scatter, edge_trace: go.Scatter, title: str
) -> go.Figure:
    """Draws network.

    Args:
        node_trace (go.Scatter): traces for where to draw nodes (points).
        edge_trace (go.Scatter): traces for where to draw edges (lines).
        title (str): Title for the chart.

    Returns:
        go.Figure: plotly figure of drawn graph.
    """
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            titlefont_size=20,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                    text="** denotes focus of the network when filtered",
                    font=dict(size=14),
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    fig.update_traces()

    return fig
