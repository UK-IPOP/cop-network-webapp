from functools import lru_cache
from typing import Union

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import networkx as nx
import csv
import dash_bootstrap_components as dbc
import scholar_network

from app import graphing, utils


# TODO: performance improvements


def load_scholar_names_from_file() -> list[str]:
    with open("data/COPscholars.csv", "r") as f:
        csvreader = csv.DictReader(f)
        authors = []
        for row in csvreader:
            authors.append(row.get("Name"))
    return authors

def create_cop_network_graph_figure():
    graph, positions = utils.load_graph_from_files()
    node_trace, edge_trace = graphing.build_network(graph, positions)
    fig = graphing.draw_network(node_trace, edge_trace, title="COP Network Graph")
    return fig


def pair_graph(author1, author2):
    custom_graph = scholar_network.build_graph(author1, author2)

    # ! time consuming, re-looping over nodes
    G = nx.Graph()
    G.add_edges_from(custom_graph.node_pairs())

    positions = nx.spring_layout(G)
    node_trace, edge_trace = graphing.build_network(G, positions)
    fig = graphing.draw_network(
        node_trace,
        edge_trace,
        title=f"{author1.title() if author1 else '...'} x {author2.title() if author2 else '...'} Network Graph",
    )
    return fig

def parse_name(name: str) -> str:
    parts = name.split()
    parsed = f"{parts[0]} {parts[-1]}"
    return parsed


theme = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sketchy/bootstrap.min.css"
app = dash.Dash(__name__, title="COP Scholar Network Dashboard", external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

scholar_names = load_scholar_names_from_file()
cop_network_graph = create_cop_network_graph_figure()


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/IPOP-logo.png",
                            style={'width': '100px'},
                        )
                    ],
                    align="center",
                    width=2,
                ),
                dbc.Col([html.H1(children="UK COP Network", className="text-info", style={'text-align': 'center'})], width=4),
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/UK-COP-logo.jpg",
                            style={'width': '250px', 'height': '200px'},
                        )
                    ],
                    align="center",
                    width=2,
                ),
            ],
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Author 1 Select:", className="text-info"),
                        dcc.Dropdown(
                            id="author-dropdown1",
                            options=[],
                            value="",
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("Author 2 Select:", className="text-info"),
                        dcc.Dropdown(
                            id="author-dropdown2",
                            options=[],
                            value="",
                        ),
                    ],
                    width=4,
                ),
            ],
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Card(
                    dbc.Spinner(
                        dcc.Graph(id="network-graph"),
                        type="grow",
                        color="primary",
                        size="lg",
                    ),
                    className="p-3 m-3",
                    body=True,
                    style={'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)'},
                )
            ],
            className="px-5",
            justify="center",
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output(component_id="author-dropdown2", component_property="options"),
    Input(component_id="author-dropdown1", component_property="value"),
)
def update_options1(input_value: str) -> list[dict[str, str]]:
    return [
        {"label": parse_name(person), "value": person}
        for person in scholar_names
        if person != input_value
    ]


@app.callback(
    Output(component_id="author-dropdown1", component_property="options"),
    Input(component_id="author-dropdown2", component_property="value"),
)
def update_options2(input_value: str) -> list[dict[str, str]]:
    return [
        {"label": parse_name(person), "value": person}
        for person in scholar_names
        if person != input_value
    ]


@app.callback(
    Output("network-graph", "figure"),
    [
        Input(component_id="author-dropdown1", component_property="value"),
        Input(component_id="author-dropdown2", component_property="value"),
    ],
)
def on_author_select(author1: Union[str, None], author2: Union[str, None]) -> go.Figure:
    if author1 or author2:
        return pair_graph(author1, author2)
    return cop_network_graph


if __name__ == "__main__":
    app.run_server(debug=True)
