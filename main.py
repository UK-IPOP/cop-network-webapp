from typing import Union

import dash
from dash_bootstrap_components._components.Col import Col
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.H2 import H2
from dash_html_components.Hr import Hr
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import networkx as nx
import csv
import dash_bootstrap_components as dbc
import scholar_network

from app import graphing, utils


# TODO: performance improvements


def load_scholar_names_from_file(ipop_only: bool = False) -> list[str]:
    with open("data/COPscholars.csv", "r") as f:
        csvreader = csv.DictReader(f)
        authors = []
        if ipop_only:
            for row in csvreader:
                if row.get('Group') == 'Pharmacy Practice and Science':
                    authors.append(row.get("Name"))
            return authors
        else:
            for row in csvreader:
                authors.append(row.get("Name"))
            return authors

def create_cop_network_graph_figure():
    graph, positions = utils.load_graph_from_files()
    node_trace, edge_trace = graphing.build_network(graph, positions)
    fig = graphing.draw_network(node_trace, edge_trace, title="COP Network Graph")
    return fig


def create_ipop_network_graph_figure():
    graph, positions = utils.load_ipop_graph_from_files()
    node_trace, edge_trace = graphing.build_network(graph, positions)
    fig = graphing.draw_network(node_trace, edge_trace, title="IPOP Network Graph")
    return fig


def pair_graph(author1, author2):
    custom_graph = scholar_network.build_graph(author1, author2)

    # ! time consuming, re-looping over nodes
    G = nx.Graph()
    G.add_edges_from(custom_graph.node_pairs())

    positions = nx.spring_layout(G)
    node_trace, edge_trace = graphing.build_network(G, positions, author1, author2)
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
ipop_names = load_scholar_names_from_file(ipop_only=True)
cop_network_graph = create_cop_network_graph_figure()
ipop_network_graph = create_ipop_network_graph_figure()


tab1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2('Description:', className='text-center text-info'),
                        html.Hr(),
                        html.P([
                            "This network graph shows authors and their direct coauthors. "
                            "When an author is selected you are able to see the author's entire network graph. "
                            "When you select two authors, you are able to see their combined network(s) and any "
                            "shared connections they may have. Note that only full graphs for the selected authors "
                            "are shown, and any other authors are only showcasing a sub-graph or sub-network of their "
                            "entire network. To see their entire network, selected them from the dropdown. If they "
                            "are not in the dropdown, then you can request to add them, although at this time only "
                            "COP scholars are included. There are: ",
                            html.Span(f"{len(scholar_names)} COP ", className='strong text-primary'),
                            "scholars/authors available to choose from."
                        ]),
                    ],
                    width=9,
                )
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
    fluid=True
)


tab2 = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.H2('Description:', className='text-center text-info'),
                    html.Hr(),
                    html.P([
                        "This network graph shows authors and their direct coauthors. "
                        "When an author is selected you are able to see the author's entire network graph. "
                        "When you select two authors, you are able to see their combined network(s) and any "
                        "shared connections they may have. Note that only full graphs for the selected authors "
                        "are shown, and any other authors are only showcasing a sub-graph or sub-network of their "
                        "entire network. To see their entire network, selected them from the dropdown. If they "
                        "are not in the dropdown, then you can request to add them, although at this time only "
                        "COP scholars are included. There are: ",
                        html.Span(f"{len(ipop_names)} IPOP ", className='strong text-primary'),
                        "scholars/authors available to choose from."
                    ]),
                ],
                width=9,
                )
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
                            id="author-dropdown3",
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
                            id="author-dropdown4",
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
                        dcc.Graph(figure=ipop_network_graph, id='ipop-graph'),
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
    fluid=True
)

main_content = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="COP", tab_id="tab-1", tabClassName='ml-auto'),
                    dbc.Tab(label="IPOP", tab_id="tab-2", tabClassName='mr-auto'),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(id='main_content_body'),
    ]
)

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
                dbc.Col([html.H1(children="UK COP Scholarship Network", className="text-info", style={'text-align': 'center'})], width=4),
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
        main_content

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
    Output(component_id="author-dropdown4", component_property="options"),
    Input(component_id="author-dropdown3", component_property="value"),
)
def update_options3(input_value: str) -> list[dict[str, str]]:
    return [
        {"label": parse_name(person), "value": person}
        for person in ipop_names
        if person != input_value
    ]


@app.callback(
    Output(component_id="author-dropdown3", component_property="options"),
    Input(component_id="author-dropdown4", component_property="value"),
)
def update_options4(input_value: str) -> list[dict[str, str]]:
    return [
        {"label": parse_name(person), "value": person}
        for person in ipop_names
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


@app.callback(
    Output("ipop-graph", "figure"),
    [
        Input(component_id="author-dropdown3", component_property="value"),
        Input(component_id="author-dropdown4", component_property="value"),
    ],
)
def draw_ipop_graph(author1: Union[str, None], author2: Union[str, None]) -> go.Figure:
    if author1 or author2:
        return pair_graph(author1, author2)
    return ipop_network_graph


@app.callback(
    Output("main_content_body", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    if active_tab == "tab-2":
        return tab2
    else:
        return tab1


if __name__ == "__main__":
    app.run_server(debug=True)
