import pandas as pd
import dash
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash
import dash_html_components as html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

url = "https://drive.google.com/file/d/13S43h2FWUvsQvOdVgr2u-bEIE2UdAJUw/view?usp=sharing"
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]

spacex_df=pd.read_csv(url)

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                   id='site-dropdown',
                                   options=[
                                       {'label':'All Sites', 'value':'All'},
                                       {'label':launch_sites[0], 'value':launch_sites[0]},
                                       {'label':launch_sites[1], 'value':launch_sites[1]},
                                       {'label':launch_sites[2], 'value':launch_sites[2]},
                                       {'label':launch_sites[3], 'value':launch_sites[3]}
                                       ],
                                    placeholder="Select Launch Site",
                                    value='All',
                                    searchable=True),
                            
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=9600,
                                    step=1000,
                                    value=[min_payload, max_payload],
                                    marks={
                                        0: '0 kg',
                                        1000: '1000 kg',
                                        5000: '5000 kg',
                                        9600: 'MAX'
                                        }
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    pie_df = spacex_df
    if entered_site == 'All':
        fig = px.pie(
            pie_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Site')
        return fig

    else:
        pie_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        title = f"Successful Launches per site {entered_site}"
        fig = px.pie(pie_df, values='class count', names='class', title=title)
        return fig

# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_chart(site, payload):
    scatter_df = spacex_df[(spacex_df['Payload Mass (kg)'] > payload[0]) & (spacex_df['Payload Mass (kg)'] < payload[1])]

    if site == 'All':
        fig= px.scatter(
            scatter_df,
            x='Payload Mass (kg)',
            y='class',
            labels = {'class':'Success'},
            color='Booster Version Category',
            title='Correlation between Payload and Success for All sites')
        return fig
    else :
        scatter_df=scatter_df[scatter_df['Launch Site'] == site]
        fig= px.scatter(
            scatter_df,
            x='Payload Mass (kg)',
            y='class',
            labels = {'class':'Success'},
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {site}')
        return fig

if __name__ == '__main__':
    app.run_server()
