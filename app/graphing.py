import plotly.graph_objects as go
import plotly.io as pio
import networkx as nx

pio.templates.default = "simple_white"


def build_network(
    graph: nx.Graph,
    layout: nx.layout,
) -> tuple[go.Scatter, go.Scatter]:
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
        line=dict(width=0.25, color="#D3D3D3"),
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
        node_name.append(node)

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(graph.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f"# of connections: {str(len(adjacencies[1]))}")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        hovertext=node_name,
        customdata=node_text,
        hovertemplate="%{hovertext}<br>%{customdata}<extra></extra>",
        marker=dict(
            showscale=True,
            colorscale="ice",
            reversescale=True,
            color=[],
            size=5,
            colorbar=dict(
                thickness=10,
                title="Node Connections",
                xanchor="left",
                titleside="right",
            ),
            line_width=0.5,
        ),
    )
    node_trace.marker.color = node_adjacencies
    return node_trace, edge_trace


def draw_network(
    node_trace: go.Scatter, edge_trace: go.Scatter, title: str
) -> go.Figure:
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            annotations=[
                dict(showarrow=True, xref="paper", yref="paper", x=0.005, y=-0.002)
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )

    return fig