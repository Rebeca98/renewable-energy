import pandas as pd
#  herramienta de visualización de datos geoespaciales en Python
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

from params import *


def obtain_growth_rates(dataframe):
    continents = ['Africa', 'Europe', 'South America', 'North America', 'Oceania', 'Asia']

    growth_rates = {}
    for continent in continents:
        continent_data = dataframe[dataframe['Entity'] == continent]
        growth_rate = continent_data['Renewables (% equivalent primary energy)'].pct_change(
        ).mean() * 100
        growth_rates[continent] = growth_rate

    return growth_rates


def bar_plot_annual_renewable_rates(dataframe):
    fig_bar = go.Figure()

    growth_rates = obtain_growth_rates(dataframe)
    fig_bar.add_trace(go.Bar(x=list(growth_rates.keys()),
                             y=list(growth_rates.values()),
                             marker_color=['skyblue', 'lightgreen', 'lightcoral', 'orange', 'purple', 'pink']))

    fig_bar.update_layout(title='Average Annual Renewable Energy Growth Rates by Continent (%)',
                          xaxis_title='Continent',
                          yaxis_title='Average Growth Rate (%)',
                          plot_bgcolor='whitesmoke',
                          font=dict(size=12, color='black'),
                          bargap=0.3)

    for continent, growth_rate in growth_rates.items():
        fig_bar.add_annotation(x=continent, y=growth_rate + 0.1,
                               text=f'{growth_rate:.2f}%',
                               showarrow=False,
                               font=dict(size=12, color='black'))
    return fig_bar


def plot_lineplot(entities, dataframe):
    if not isinstance(entities, list):
        entities = [entities]
    data_copy = dataframe.copy()
    df = data_copy[data_copy['Entity'].isin(entities)]

    lineplot = px.line(df, x='Year', y='Renewables (% equivalent primary energy)', color='Entity',
                       title='Renewable Energy Share Over Time (% equivalent primary energy)',
                       labels={
                           'Year': 'Year', 'Renewables (% equivalent primary energy)': 'Renewable Share (%)', 'Entity': 'Entity'},
                       width=1000, height=400)
    lineplot.update_xaxes(title_font=dict(size=TITLE_FONT_SIZE))
    lineplot.update_yaxes(title_font=dict(size=LABEL_FONT_SIZE))
    lineplot.update_traces(line=dict(width=LINE_WIDTH))

    return lineplot


def get_pivot_table(dataframe, value):
    latest_n_years = dataframe['Year'].unique()[-value:]
    filtered_data = dataframe[dataframe['Year'].isin(latest_n_years)]
    top_20_per_year = filtered_data.groupby('Year').apply(
        lambda x: x.nlargest(20, 'Renewables (% equivalent primary energy)'))

    # reorganizamos los datos en el DataFrame, de este forma tenemos una serie de tiempo
    pivot_data = top_20_per_year.pivot(
        index='Entity', columns='Year', values='Renewables (% equivalent primary energy)').fillna(0)

    # suma a lo largo del eje 1 (columnas)
    sortes_pivote_cumsum = pivot_data.sum(axis=1).sort_values(ascending=False)

    # utilizamos el orden que obtuvimos en la suma acumulado,i.e. los países con mayor proporcion de Renewable (%)
    sorted_pivot_data = pivot_data.loc[sortes_pivote_cumsum.index]
    return sorted_pivot_data


def plot_barplot(value, dataframe):

    sorted_pivot_data = get_pivot_table(dataframe, value)
    barplot = px.bar(sorted_pivot_data, barmode='stack',
                     color_discrete_sequence=px.colors.sequential.Viridis,
                     width=800, height=500)

    # Configurar el título y etiquetas de los ejes
    barplot.update_layout(title=f"Top 20 Entities for Renewable Energy Share in the Last {value} Years",
                          xaxis_title='Entity', yaxis_title='Renewable Energy Share (%)',
                          )

    # Rotar etiquetas del eje x
    barplot.update_xaxes(tickangle=90)

    return barplot


def lowest_renewable_share(value, dataframe):
    latest_n_years = dataframe['Year'].unique()[-value:]

    heatmap_data = pd.DataFrame()

    for year in latest_n_years:
        specific_year_data = dataframe[dataframe['Year'] == year]
        bottom_countries_year = specific_year_data.nsmallest(
            10, 'Renewables (% equivalent primary energy)')
        heatmap_data[year] = bottom_countries_year.set_index(
            'Entity')['Renewables (% equivalent primary energy)']
    return heatmap_data, latest_n_years


def plot_heatmap(value, dataframe):
    heatmap_data, latest_n_years = lowest_renewable_share(value, dataframe)
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values.tolist(),
        x=latest_n_years,
        y=heatmap_data.index.tolist(),
        colorscale='YlOrRd',  # Los colores rojos indican valores más bajos
        reversescale=True,  # Invierte la escala de colores
        colorbar=dict(title='Renewable Energy Share (%)')
    ))

    # Configurar el diseño y las etiquetas del gráfico
    heatmap_fig.update_layout(
        title='Renewable Energy Share in Bottom 10 Countries/Regions',
        xaxis=dict(title='Year', tickfont=dict(size=14)),
        yaxis=dict(title='Country/Region', tickfont=dict(size=14)),
        font=dict(size=16),
        height=600,
        width=900,
        margin=dict(l=80, r=80, t=100, b=80),
    )
    return heatmap_fig


def plot_scatterplot(entity, dataframe):
    entity_data = dataframe[dataframe['Entity'] == entity]

    fig_scatter = go.Figure(go.Scatter(
        x=entity_data['Year'],
        y=entity_data['Renewables (% electricity)'],
        mode='lines+markers',
        name='Renewable Energy'
    ))

    fig_scatter.update_layout(
        title=f"Renewable Energy Usage Rate in {entity} Over the Years",
        xaxis_title='Year',
        yaxis_title='Renewable Energy Rate (%)',
        hovermode='x'
    )

    fig_scatter.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=5, label="Last 5 years", step="year", stepmode="backward"),
                    dict(count=10, label="Last 10 years", step="year", stepmode="backward"),
                    dict(count=20, label="Last 20 years", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig_scatter


def scatterplot_multiple(dataframes):
    interest_countries = ['Germany', 'France', 'United Kingdom', 'Denmark', 'Spain', 'Mexico']

    selected_data = dataframes[dataframes['Entity'].isin(interest_countries)]

    fig_scatter = go.Figure()

    for country in interest_countries:
        country_data = selected_data[selected_data['Entity'] == country]
        fig_scatter.add_trace(go.Scatter(
            x=country_data['Year'],
            y=country_data['Renewables (% electricity)'],
            mode='lines+markers',
            name=country
        ))

    fig_scatter.update_layout(
        title='Top 5 European Countries and Turkey: Renewable Energy Usage Rates',
        xaxis_title='Year',
        yaxis_title='Renewable Energy Rate (%)',
        legend_title='Countries',
        hovermode='x unified'
    )

    return fig_scatter


def map_plot(dataframe):
    sorted_dataframe = dataframe.sort_values('Year')
    fig = px.choropleth(
        sorted_dataframe,
        locations="Entity",
        locationmode="country names",
        color="Renewables (% electricity)",
        animation_frame="Year",
        color_continuous_scale="Viridis",
        range_color=(0, 100)
    )

    fig.update_geos(projection_type="natural earth")

    fig.update_layout(
        title="Renewable Energy Usage World Map",
        coloraxis_colorbar={"title": "Renewable Energy Usage (%)"}
    )
    return fig
