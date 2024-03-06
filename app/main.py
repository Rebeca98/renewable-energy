from params import *
import pandas as pd
import plotly.express as px


import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, html, Input, Output
import dash

from utils_dashboard import bar_plot_annual_renewable_rates as bar_plot_annual_renewable_rates_db
from utils_dashboard import plot_lineplot as plot_lineplot_db
from utils_dashboard import plot_barplot as plot_barplot_db
from utils_dashboard import plot_heatmap as plot_heatmap_db
from utils_dashboard import plot_scatterplot as plot_scatterplot_db
from utils_dashboard import scatterplot_multiple as scatterplot_multiple_db
from utils_dashboard import map_plot as map_plot_db


renewable_share_energy = pd.read_csv("../data/01 renewable-share-energy.csv")
share_electricity_renewables = pd.read_csv("../data/04 share-electricity-renewables.csv")


renewable_share_energy['Entity'].unique()
ENTITIES = list(renewable_share_energy['Entity'].unique())


dash_app = dash.Dash(name=__name__,
                     title='Images & Video Dashboard',
                     external_stylesheets=[dbc.themes.BOOTSTRAP],
                     suppress_callback_exceptions=True)

# Definimos el layout de la aplicación
dash_app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.H2(f'Análisis de Energías Renovables')
                            ),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    style={"textDecoration": "none"},
                ),
            ]
        ),
        color="#E5E4E2",
        dark=False
    ),
    dbc.Container([
        html.Hr(),
        dbc.Tabs([
            dbc.Tab(label="Gráfico de Líneas", tab_id="line-plot-tab"),
            dbc.Tab(label="Gráfico de Barras", tab_id="bar-plot-tab"),
            dbc.Tab(label="Gráfico de Barras", tab_id="map-plot"),
        ], id="tabs", active_tab="line-plot-tab"),
        html.Div(id="tabs-content")
    ])
])


@dash_app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    if active_tab == "line-plot-tab":
        return html.Div([
            html.H2(f'Seleccionar entidad o región'),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Label('Entidad/Región:'),
                        dcc.Dropdown(
                            id='drop-entity',
                            options=[{'label': entity, 'value': entity} for entity in ENTITIES],
                            value=DEFAULT_ENTITY,
                            multi=True
                        )
                    ]),
                )
            ], align="center", style={'margin-bottom': '25px', 'margin-top': '25px', 'text-align': 'center'}),

            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Graph(
                            id='line-plot'
                        )
                    ]),
                )
            ], align="center", style={'padding-left': '30px', 'padding-right': '30px'}),

            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Graph(id='heatmap-plot'),
                        dcc.Slider(0, 20, 5,
                                   value=6,
                                   id='slider-heatmap'),
                        html.Div(id='slider-output-container-heatmap')
                    ])


                )
            ], align="center", style={'padding-left': '30px', 'padding-right': '30px'}),

            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H2('Información General'),
                        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed accumsan libero sit amet purus eleifend, id ullamcorper eros vehicula. Nam at augue consequat, tempus velit vitae, commodo arcu. Aliquam erat volutpat. Integer interdum nibh non felis tristique, ut vulputate nulla laoreet. Mauris ultrices ligula id arcu commodo, non euismod enim accumsan. Duis vitae ligula ut justo malesuada gravida. Maecenas dapibus ipsum sed magna convallis, eget finibus odio fermentum. Quisque tincidunt, risus id fermentum venenatis, libero ex suscipit nisi, ut varius est nisl vel sem. Aenean sed semper risus. Vivamus sed arcu vitae ex pellentesque ultrices a non velit. Integer auctor, quam in commodo scelerisque, purus lectus egestas nulla, vel suscipit nisi sem nec elit. Suspendisse potenti. Sed in risus nec mauris vehicula faucibus. Etiam nec purus pretium, accumsan orci eu, dictum orci. Sed gravida eget nisi nec congue."),
                    ], style={'background-color': '#65bdd0', 'color': 'white', 'border-radius': '5px', 'padding': '10px', 'margin': '20px'})
                )
            ], align="center", style={'padding-left': '30px', 'padding-right': '30px'})

        ])
    elif active_tab == "bar-plot-tab":
        return html.Div([

            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Graph(id='bar-plot'),
                        dcc.Slider(0, 20, 5,
                                   value=10,
                                   id='my-slider'),
                        html.Div(id='slider-output-container')
                    ]))
            ], align="center", style={'padding-left': '30px', 'padding-right': '30px'}),

            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Interval(
                            id='interval-component',
                            interval=60*1000,  # en milisegundos
                            n_intervals=0),
                        html.Div(id='bar-plot-annual-rates')
                    ])
                )
            ], align="center", style={'padding-left': '30px', 'padding-right': '30px'})
        ])

    elif active_tab == "map-plot":
        return html.Div([
            html.H2(f'Seleccionar entidad o región'),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Label('Entidad/Región:'),
                        dcc.Dropdown(
                            id='drop-entity',
                            options=[{'label': entity, 'value': entity} for entity in ENTITIES],
                            value=DEFAULT_ENTITY,
                            multi=False
                        )
                    ]),
                )
            ], align="center", style={'margin-bottom': '25px', 'margin-top': '25px', 'text-align': 'center'}),

            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Graph(
                            id='scatter-plot'
                        )
                    ]),
                )
            ], align="center", style={'padding-left': '30px', 'padding-right': '30px'}),
            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Interval(
                            id='interval-component-2',
                            interval=60*1000,  # en milisegundos
                            n_intervals=0),
                        html.Div(id='scatter-plot-line')
                    ])
                )
            ], align="center", style={'padding-left': '30px', 'padding-right': '30px'}),
            html.Hr(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Interval(
                            id='interval-component-3',
                            interval=60*1000,  # en milisegundos
                            n_intervals=0),
                        html.Div(id='map-plots')
                    ])
                )
            ], align="center", style={'padding-left': '30px', 'padding-right': '30px'})
        ])


@dash_app.callback(
    Output('line-plot', 'figure'),
    Input('drop-entity', 'value')
)
def plot_lineplot(entities):
    lineplot = plot_lineplot_db(entities, renewable_share_energy)
    return lineplot


@dash_app.callback(
    Output('scatter-plot', 'figure'),
    Input('drop-entity', 'value')
)
def plot_scatterplot(entity):
    scatterplot = plot_scatterplot_db(entity=entity, dataframe=share_electricity_renewables)
    return scatterplot


@dash_app.callback(
    [Output('slider-output-container', 'children'),
     Output('bar-plot', 'figure')],
    [Input('my-slider', 'value')]
)
def plot_barplot(value):
    barplot = plot_barplot_db(value, renewable_share_energy)
    return [f'Selected value: {value}'], barplot


@dash_app.callback(
    [Output('slider-output-container-heatmap', 'children'),
     Output('heatmap-plot', 'figure')],
    [Input('slider-heatmap', 'value')]
)
def plot_heatmap(value):
    barplot = plot_heatmap_db(value, renewable_share_energy)
    return [f'Selected value: {value}'], barplot


@dash_app.callback(
    Output('scatter-plot-line', 'children'),
    [Input('interval-component-2', 'n_intervals')]
)
def scatterplot_multiple(n):
    fig = scatterplot_multiple_db(share_electricity_renewables)
    return dcc.Graph(figure=fig)


@dash_app.callback(
    Output('map-plots', 'children'),
    [Input('interval-component-3', 'n_intervals')]
)
def update_bar_plot_annual_renewable_rates(n):
    fig = bar_plot_annual_renewable_rates_db(renewable_share_energy)
    return dcc.Graph(figure=fig)


@dash_app.callback(
    Output('bar-plot-annual-rates', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def map_plot(n):
    fig = map_plot_db(share_electricity_renewables)
    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8001, host="0.0.0.0")
