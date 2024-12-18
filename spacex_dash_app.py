# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv( "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    
    html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    html.Br(),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        searchable=True,
        value='ALL',
        placeholder='Select a Launch Site here',
        style = {
            'padding' : '3px',
            'text-align-last' : 'center'
        }
    ),


    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range

    dcc.RangeSlider(id='payload-slider',
        min=0,
        max=10000,
        step=100,
        marks={i: '{}'.format(i) for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':

        data = spacex_df.groupby('Launch Site')['class'].sum().reset_index() 
        names = 'Launch Site'
        title = 'Total Success Launches By Site'         

    else :
        filtered_df = spacex_df[ spacex_df['Launch Site'] == entered_site ]
        filtered_df['class_name'] = np.where(filtered_df['class'] == 1, 'Success', 'Failure')

        data = filtered_df.groupby('class_name')['class'].count().reset_index()
        names = 'class_name'
        title = f'Total Success Launches For Site {entered_site}'


    fig = px.pie(data, 
        values='class',
        names=names,
        title=title
    )     
    
    return fig    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( 
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider',component_property='value'),
    ]
)
def get_payload_chart(entered_site, entered_payload_mass):
    if entered_site == 'ALL':

        filtered_df = spacex_df
        title = 'Correlation Between Payload and Success for All Sites'
    else:
        filtered_df = spacex_df[ spacex_df['Launch Site'] == entered_site ]
        title = f'Correlation Between Payload and Success for Site {entered_site}'


    data = filtered_df[ filtered_df['Payload Mass (kg)'].between(entered_payload_mass[0], entered_payload_mass[1]) ]

    fig = px.scatter(data, 
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=['Launch Site'],
        title=title
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()


# 1. Which site has the largest successful launches?
# KSC LC-39A with 10
 
# 2. Which site has the highest launch success rate?
# KSC LC-39A with 76.9%

# 3. Which payload range(s) has the highest launch success rate?
# [360, 380] => 100 %
# Around 5000 => 100%

# 4. Which payload range(s) has the lowest launch success rate?
# [500, 1800] => 0%
# [5400, 9500] => 0%

# 5. Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
# B5, with 100%