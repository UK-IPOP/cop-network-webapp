from typing import Union

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import networkx as nx
import csv
import pandas as pd
from dash import dash_table
import dash_bootstrap_components as dbc
import scholar_network
import pickle

from utils import graphing, utils
from dotenv import load_dotenv
import os

load_dotenv()


def load_scholar_names_from_file() -> list[str]:
    """Loads scholars from file.

    Returns:
        list[str]: A list of scholar names.
    """
    with open("data/COPscholars.csv", "r") as f:
        csvreader = csv.DictReader(f)
        authors = []
        for row in csvreader:
            authors.append(row.get("Name"))
        return authors


def load_ipop_scholar_names_from_file() -> list[str]:
    """Loads, specifically, IPOP scholars from file.

    Returns:
        list[str]: List of IPOP scholar names.
    """
    with open("data/IPOP-Scholars.csv", "r") as f:
        csvreader = csv.DictReader(f)
        authors = []
        for row in csvreader:
            authors.append(row.get("Name"))
        return authors


def load_sure_scholar_names_from_file() -> list[str]:
    """Loads, specifically, SURE scholars from file.

    Returns:
        list[str]: List of SURE scholar names.
    """
    with open("data/SUREscholars.csv", "r") as f:
        csvreader = csv.DictReader(f)
        authors = []
        for row in csvreader:
            authors.append(
                row.get("First", "").strip() + " " + row.get("Last", "").strip()
            )
        return authors


def create_cop_network_graph_figure():
    """Creates entire network graph.

    This function calls our utility and graphing functions
    to generate the entire network once on page load.

    Returns:
        [go.Figure]: plotly figure representing drawn network.
    """
    graph, positions = utils.load_graph_from_files()
    node_trace, edge_trace = graphing.build_network(graph, positions)
    fig = graphing.draw_network(node_trace, edge_trace, title="COP Network Graph")
    return fig


def create_ipop_network_graph_figure():
    """Creates entire network graph for IPOP scholars only.

    This function calls our utility and graphing functions
    to generate the entire network once on page load.

    Returns:
        [go.Figure]: plotly figure representing drawn network.
    """
    graph, positions = utils.load_ipop_graph_from_files()
    node_trace, edge_trace = graphing.build_network(graph, positions)
    fig = graphing.draw_network(node_trace, edge_trace, title="IPOP Network Graph")
    return fig


def create_sure_graph_figure():
    """Creates entire network graph for POC scholars only.

    This function calls our utility and graphing functions
    to generate the entire network once on page load.

    Returns:
        [go.Figure]: plotly figure representing drawn network.
    """
    with open("data/sure-graph.pkl", "rb") as f:
        graph = pickle.load(f)
    with open("data/sure-pos.pkl", "rb") as f:
        positions = pickle.load(f)
    node_trace, edge_trace = graphing.build_network(graph, positions)
    fig = graphing.draw_network(node_trace, edge_trace, title="SURE Network Graph")
    return fig


def parse_name(name: str) -> str:
    """Extracts first and last parts of a name.

    This could be first and last name or any variation.

    Args:
        name (str): String name to be parsed

    Returns:
        str: Extracted 2-part name.
    """
    parts = name.split()
    parsed = f"{parts[0][0]} {parts[-1]}".title()
    if parsed == "J Mcginty":
        return "J McGinty"
    return parsed


def pair_graph(name1: str, name2: str) -> go.Figure:
    """Draws a graph, given two scholars to filter the network on.

    Args:
        author1 (str): first scholar name to filter on
        author2 (str): second scholar name to filter on

    Returns:
        go.Figure: drawn network graph
    """
    a1 = parse_name(name1) if name1 else None
    a2 = parse_name(name2) if name2 else None
    graph = scholar_network.build_graph(a1, a2)
    print(name1, "--0-", name2)
    print(graph.node_pairs())
    # ! time consuming, re-looping over nodes
    # ! also, try to just filter the pickled graph instead of recreating a new one
    G = nx.Graph()
    print(name1, "--1-", name2)
    G.add_edges_from(graph.node_pairs())
    print(name1, "--2-", name2)

    positions = nx.spring_layout(G)
    print(name1, "--3-", name2)

    node_trace, edge_trace = graphing.build_network(G, positions, a1, a2)
    fig = graphing.draw_network(
        node_trace,
        edge_trace,
        title=f"{name1.title() if name1 else '...'} x {name2.title() if name2 else '...'} Network Graph",
    )
    return fig


def pair_graph_sure(name1: str, name2: str) -> go.Figure:
    """Draws a graph, given two scholars to filter the network on.

    Args:
        author1 (str): first scholar name to filter on
        author2 (str): second scholar name to filter on

    Returns:
        go.Figure: drawn network graph
    """
    a1 = parse_name(name1) if name1 else None
    a2 = parse_name(name2) if name2 else None
    graph = scholar_network.build_graph(a1, a2, fpath="data/scraped_sure.json")
    print(a1, "--0-", a2)
    # ! time consuming, re-looping over nodes
    # ! also, try to just filter the pickled graph instead of recreating a new one
    G = nx.Graph()
    print(a1, "--1-", a2)
    G.add_edges_from(graph.node_pairs())
    print(a1, "--2-", a2)

    positions = nx.spring_layout(G)
    print(a1, "--3-", a2)

    node_trace, edge_trace = graphing.build_network(G, positions, a1, a2)
    fig = graphing.draw_network(
        node_trace,
        edge_trace,
        title=f"{name1.title() if name1 else '...'} x {name2.title() if name2 else '...'} Network Graph",
    )
    print(a1, "--4-", a2)
    return fig


def make_datatable(df: pd.DataFrame) -> dash_table.DataTable:
    """Creates a datatable of all scholars."""
    table = dash_table.DataTable(
        id="datatable",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_cell={"textAlign": "left"},
        style_header={"backgroundColor": "rgb(3, 60, 115)", "color": "white"},
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        page_size=20,
    )
    return table


# dash globals
theme = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sketchy/bootstrap.min.css"
app = dash.Dash(
    __name__,
    title="COP Scholar Network Dashboard",
    external_stylesheets=[dbc.themes.CERULEAN],
)
server = app.server
app.config["suppress_callback_exceptions"] = True


# call these once here, in global state, at application startup, then reuse
scholar_names = load_scholar_names_from_file()
ipop_names = load_ipop_scholar_names_from_file()
all_names = set(scholar_names) | set(ipop_names)
sure_names = load_sure_scholar_names_from_file()

sure_graph = create_sure_graph_figure()
cop_network_graph = create_cop_network_graph_figure()
ipop_network_graph = create_ipop_network_graph_figure()


counts_df = pd.read_csv("data/coauthor_counts.csv")
table = make_datatable(counts_df)

# tab for entire COP
tab1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Description:", className="text-center text-info"),
                        html.Hr(),
                        html.P(
                            [
                                "This network graph shows authors and their direct coauthors. "
                                "When an author is selected you are able to see the author's entire network graph. "
                                "When you select two authors, you are able to see their combined network(s) and any "
                                "shared connections they may have. Note that only full graphs for the selected authors "
                                "are shown, and any other authors are only showcasing a sub-graph or sub-network of their "
                                "entire network. To see their entire network, selected them from the dropdown. If they "
                                "are not in the dropdown, then you can request to add them, although at this time only "
                                "COP scholars are included. There are: ",
                                html.Span(
                                    f"{len(scholar_names)} COP ",
                                    className="strong text-primary",
                                ),
                                "scholars/authors available to choose from.",
                            ]
                        ),
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
                )
            ],
            className="px-5",
            justify="center",
            align="center",
        ),
    ],
    fluid=True,
)


# tab for IPOP only
tab2 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Description:", className="text-center text-info"),
                        html.Hr(),
                        html.P(
                            [
                                "This network graph shows authors and their direct coauthors. "
                                "When an author is selected you are able to see the author's entire network graph. "
                                "When you select two authors, you are able to see their combined network(s) and any "
                                "shared connections they may have. Note that only full graphs for the selected authors "
                                "are shown, and any other authors are only showcasing a sub-graph or sub-network of their "
                                "entire network. To see their entire network, selected them from the dropdown. If they "
                                "are not in the dropdown, then you can request to add them, although at this time only "
                                "COP scholars are included. There are: ",
                                html.Span(
                                    f"{len(ipop_names)} IPOP ",
                                    className="strong text-primary",
                                ),
                                "scholars/authors available to choose from.",
                            ]
                        ),
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
                        dcc.Graph(figure=ipop_network_graph, id="ipop-graph"),
                        type="grow",
                        color="primary",
                        size="lg",
                    ),
                    className="p-3 m-3",
                    body=True,
                )
            ],
            className="px-5",
            justify="center",
            align="center",
        ),
    ],
    fluid=True,
)

# tab for SURE conference only
tab3 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/sure_logo.PNG",
                            style={
                                "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto",
                                "width": "30%",
                            },
                            className="text-center",
                        ),
                        html.P(
                            [
                                "There are: ",
                                html.Span(
                                    f"{len(sure_names)} SURE ",
                                    className="strong text-primary",
                                ),
                                "scholars/authors available to choose from.",
                            ]
                        ),
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
                            id="author-dropdown5",
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
                            id="author-dropdown6",
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
                        dcc.Graph(figure=sure_graph, id="poc-graph"),
                        type="grow",
                        color="primary",
                        size="lg",
                    ),
                    className="p-3 m-3",
                    body=True,
                )
            ],
            className="px-5",
            justify="center",
            align="center",
        ),
    ],
    fluid=True,
)


# tabe 4 for datatabel
tab4 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Description:", className="text-center text-info"),
                        html.Hr(),
                        html.P(
                            [
                                "This page showcases UK COP authors and their co-authors. "
                                "Use the dropdown to select an author and see their co-author specifically. "
                            ]
                        ),
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
                        html.Label("Author Select:", className="text-info"),
                        dcc.Dropdown(
                            id="author-dropdown4",
                            options=[
                                {"label": person, "value": person}
                                for person in sorted(scholar_names)
                            ],
                            value="",
                        ),
                    ],
                    width=6,
                ),
            ],
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Card(
                    children=table,
                    className="p-3 m-3",
                    id="table-card",
                    body=True,
                )
            ],
            className="px-5",
            justify="center",
            align="center",
        ),
    ],
    fluid=True,
)

# content for main card area
main_content = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="COP", tab_id="tab-1", tabClassName="mx-auto"),
                    dbc.Tab(label="IPOP", tab_id="tab-2", tabClassName="mx-auto"),
                    dbc.Tab(label="SURE", tab_id="tab-3", tabClassName="mx-auto"),
                    dbc.Tab(label="Data Table", tab_id="tab-4", tabClassName="mx-auto"),
                ],
                id="card-tabs",
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(id="main_content_body"),
    ]
)

# layout for entire application
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/IPOP-logo.png",
                            style={"width": "100px"},
                        )
                    ],
                    align="center",
                    width=2,
                ),
                dbc.Col(
                    [
                        html.H1(
                            children="UK COP Scholarship Network",
                            className="text-info",
                            style={"text-align": "center"},
                        )
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Img(
                            src="/assets/UK-COP-logo.jpg",
                            style={"width": "250px", "height": "200px"},
                        )
                    ],
                    align="center",
                    width=2,
                ),
            ],
            justify="center",
            align="center",
        ),
        main_content,
    ],
    fluid=True,
)


@app.callback(
    Output(component_id="table-card", component_property="children"),
    Input(component_id="author-dropdown4", component_property="value"),
)
def update_options_table(input_value: str) -> dash_table.DataTable:
    """Dynamically adjust datatable to selected author."""
    if input_value:
        first, last = input_value.split(" ")
        return make_datatable(counts_df[counts_df["Author 1"] == f"{first[0]} {last}"])

    return make_datatable(df=counts_df)


@app.callback(
    Output(component_id="author-dropdown2", component_property="options"),
    Input(component_id="author-dropdown1", component_property="value"),
)
def update_options1(input_value: str) -> list[dict[str, str]]:
    """Dynamically adjust dropdown options to not include selected."""
    return [
        {"label": person, "value": person}
        for person in sorted(scholar_names)
        if person != input_value
    ]


@app.callback(
    Output(component_id="author-dropdown1", component_property="options"),
    Input(component_id="author-dropdown2", component_property="value"),
)
def update_options2(input_value: str) -> list[dict[str, str]]:
    """Dynamically adjust dropdown options to not include selected."""
    return [
        {"label": person, "value": person}
        for person in sorted(scholar_names)
        if person != input_value
    ]


@app.callback(
    Output(component_id="author-dropdown4", component_property="options"),
    Input(component_id="author-dropdown3", component_property="value"),
)
def update_options3(input_value: str) -> list[dict[str, str]]:
    """Dynamically adjust dropdown options to not include selected."""
    return [
        {"label": person, "value": person}
        for person in sorted(ipop_names)
        if person != input_value
    ]


@app.callback(
    Output(component_id="author-dropdown3", component_property="options"),
    Input(component_id="author-dropdown4", component_property="value"),
)
def update_options4(input_value: str) -> list[dict[str, str]]:
    """Dynamically adjust dropdown options to not include selected."""
    return [
        {"label": person, "value": person}
        for person in sorted(ipop_names)
        if person != input_value
    ]


@app.callback(
    Output(component_id="author-dropdown6", component_property="options"),
    Input(component_id="author-dropdown5", component_property="value"),
)
def update_options5(input_value: str) -> list[dict[str, str]]:
    """Dynamically adjust dropdown options to not include selected."""
    return [
        {"label": person, "value": person}
        for person in sorted(sure_names)
        if person != input_value
    ]


@app.callback(
    Output(component_id="author-dropdown5", component_property="options"),
    Input(component_id="author-dropdown6", component_property="value"),
)
def update_options6(input_value: str) -> list[dict[str, str]]:
    """Dynamically adjust dropdown options to not include selected."""
    return [
        {"label": person, "value": person}
        for person in sorted(sure_names)
        if person != input_value
    ]


@app.callback(
    Output("network-graph", "figure"),
    [
        Input(component_id="author-dropdown1", component_property="value"),
        Input(component_id="author-dropdown2", component_property="value"),
    ],
)
def draw_cop_graph(author1: Union[str, None], author2: Union[str, None]) -> go.Figure:
    """Generate new visualization given author filters or load default."""
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
    """Generate new visualization given author filters or load default."""
    if author1 or author2:
        return pair_graph(author1, author2)
    return ipop_network_graph


@app.callback(
    Output("poc-graph", "figure"),
    [
        Input(component_id="author-dropdown5", component_property="value"),
        Input(component_id="author-dropdown6", component_property="value"),
    ],
)
def draw_poc_graph(author1: Union[str, None], author2: Union[str, None]) -> go.Figure:
    """Generate new visualization given author filters or load default."""
    if author1 or author2:
        return pair_graph_sure(author1, author2)
    return sure_graph


@app.callback(
    Output("main_content_body", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    """Control tab navigation."""
    if active_tab == "tab-2":
        return tab2
    elif active_tab == "tab-3":
        return tab3
    elif active_tab == "tab-4":
        return tab4
    else:
        return tab1


# run main application
if __name__ == "__main__":
    app.run_server(debug=os.getenv("DEBUG", False))
