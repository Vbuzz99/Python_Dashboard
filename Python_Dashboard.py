import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.colors as colors
from dash import Dash, html, dcc, Input, Output
import random
import plotly.graph_objects as go



houses=pd.read_csv("data_House_prices.csv")
st.dataframe(houses)


frequency_table = houses['city'].value_counts().reset_index()
frequency_table.columns = ['City', 'Frequency']

frequency_table1 = houses['bedrooms'].value_counts().reset_index()
frequency_table1.columns = ['Bedrooms', 'Frequency']




random_color_sequence = random.sample(colors.qualitative.Plotly,7)


app1=Dash()



city_dropdown = dcc.Dropdown(options=houses['city'].unique(),
                            value='Algona',style={'border': '1px solid #888888','borderRadius': '5px',
                                                  'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.3)','backgroundColor': '#B5F1B5','width': '150px', 'display': 'inline-block'})
color_dropdown = dcc.Dropdown(
    id='color-dropdown',
    options=[{'label': 'Blue', 'value': 'blue'},{'label': 'Yellow', 'value': 'yellow'},{'label': 'Green', 'value': 'Green'},],
    value='Green',
    style={'border': '1px solid #888888','borderRadius': '5px',
                          'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.3)','backgroundColor': '#B5F1B5','width': '150px', 'display': 'inline-block'})


app1.layout = html.Div(children=[
    html.Div(
        children=[
            html.H1(
                children='House Prices Dashboard',
                style={'textAlign': 'center','backgroundColor': '#023E02','color': '#06F206','fontFamily': 'Arial, sans-serif','fontSize': '48px',
                       'textShadow': '2px 2px 4px rgba(0, 0, 0, 0.3)','padding': '20px','borderRadius': '10px','boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)'})]),
    html.Div(children=[
        html.Div(children=[html.H2(children='House Price Difference With Number of Bedrooms in Each City',style={'color': '#025602', 'padding': '20px'}),
                           html.P(children='Click on the dropdown',style={'fontSize': '14px', 'color': '#035003', 'padding': '10px'}),
                           city_dropdown,
                           color_dropdown, 
                           dcc.Graph(id='price-graph')],style={'background-color': '#111', 'border-radius': '10px', 'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'grid-column': '1', 'grid-row': '1', 'margin': '10px'}),
        html.Div(children=[
            html.H2(children='House Price vs Waterfront [Yes/No]',style={'color': '#025602', 'padding': '20px'}),
            dcc.Graph(id='price-graph1')],style={'background-color': '#111', 'border-radius': '10px', 'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'grid-column': '2', 'grid-row': '1', 'margin': '10px'}),
        html.Div(children=[
            html.H2(children='Percentage of Houses in Each City',style={'color': '#025602', 'padding': '20px'}),
            dcc.Graph(id='price-graph2')],style={'background-color': '#111', 'border-radius': '10px', 'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'grid-column': '1', 'grid-row': '2', 'margin': '10px'}),
        html.Div(children=[
            html.H2(children='Percentage of Houses with No. of Bathrooms They Have',style={'color': '#025602', 'padding': '20px'}),
            dcc.Graph(id='graph3')],style={'background-color': '#111', 'border-radius': '10px', 'box-shadow': '0px 4px 10px rgba(0, 0, 0, 0.2)', 'grid-column': '2', 'grid-row': '2', 'margin': '10px'})],
        style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-template-rows': '1fr 1fr', 'grid-gap': '20px', 'background-color':'#202120'})
    ])






@app1.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id=city_dropdown, component_property='value'),
    Input(component_id='color-dropdown', component_property='value')  
)
def update_graph1(selected_city, selected_color):
    filtered_houses = houses[houses['city'] == selected_city]
    box_fig = px.box(filtered_houses, x='bedrooms', y='price', title=f'House Prices in {selected_city}')
    box_fig.update_traces(marker_color=selected_color)  
    box_fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
    return box_fig


@app1.callback(
    Output(component_id='price-graph1', component_property='figure'),
    Input(component_id=city_dropdown, component_property='value')
)
def update_graph2(selected_city):
    Box_fig1 = px.box(houses, x='waterfront', y='price',title='House Prices Difference with waterfont')
    Box_fig1.update_traces(marker_color='#3EF03E')
    Box_fig1.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
    
    
    return Box_fig1

@app1.callback(
    Output(component_id='price-graph2', component_property='figure'),
    Input(component_id=city_dropdown, component_property='value')
)
def update_graph3(selected_city):
    Pie_fig = px.pie(frequency_table, values='Frequency', names='City',color_discrete_sequence=random_color_sequence)
    Pie_fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
    return Pie_fig

@app1.callback(
    Output(component_id='graph3', component_property='figure'),
    Input(component_id=city_dropdown, component_property='value')
)


def update_graph4(selected_city):
    Pie_fig1 = go.Figure(data=[go.Pie(values=frequency_table1['Frequency'],labels=frequency_table1['Bedrooms'],
                                      marker=dict(colors=['#5BFA00', '#40A405', '#51D105', '#60F607', '#0AE30A', '#9FF26F', '#43503B', '#1F5103', '#143402']),hole=0.5)]
    )
    Pie_fig1.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
    
    return Pie_fig1

if __name__ == '__main__':
    app1.run_server(debug=True)