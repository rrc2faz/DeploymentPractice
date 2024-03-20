# Rachel Cleal, Assignment 5, DS4003

# DS4003 | Spring 2024 | Rachel Cleal

# Objective: Practice adding callbacks to Dash apps. 

# TASK 1 is the same as ASSIGNMENT 4. You are welcome to update your code. 

# UI Components:
# A dropdown menu that allows the user to select `country`
# - The dropdown should allow the user to select multiple countries
# - The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# - The slider should allow the user to select a range of years
# - The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# - The graph should display the gdpPercap for each country as a line
# - Each country should have a unique color
# - The graph should have a title and axis labels in reader friendly format
 

# (2) Write Callback functions for the slider and dropdown to interact with the graph
# This means that when a user updates a widget the graph should update accordingly.
# The widgets should be independent of each other. 
# Layout:
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# Submission:
# - Deploy your app on Render. 
# - In Canvas, submit the URL to your public Github Repo (made specifically for this assignment)
# - The readme in your GitHub repo should contain the URL to your Render page. 

# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# Dependencies
import seaborn as sns
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

# Use pandas to read in data
# make sure to have the file in the same directory (e.g., folder) as the notebook
df = pd.read_csv("gdp_pcap.csv")
# df.info(verbose=True, show_counts=True)

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets) # initialize the app
server = app.server

all_columns = list(df)   # Create a list of all column headers
year_column = all_columns.pop(0)   # Get rid of country from the list so it's only country names
# print(all_columns)   # Got it

clean_df = df
for column in clean_df[all_columns]:   # This loops through each column and changes value to float
    #print('column name: ', column)   # So I know it's going through each column
    clean_df[column] = clean_df[column].replace({'k':'*1e3'}, regex=True).map(pd.eval).astype(float)

#sorted_df['1900'] = sorted_df['1900'].replace({'k':'*1e3'}, regex=True).map(pd.eval).astype(float)
# Alternatively, the above works for each column
    
# clean_df.info(verbose=True, show_counts=True)

# Define layout and elements
min_year = int(all_columns[0])  # get the minimum value of year in the dataset
max_year = int(all_columns[-1]) # maximum value of year

app.layout = html.Div([
    html.Div(children = [
        dcc.Markdown('''
            # Interactive GDP Per Country App
            ##### This app includes three components: a dropdown menu, slider, and graph. To begin, please select a country from the dropdown menu. Then, use the slider to select the date range you are interested in. The graph displays the GDP over the decades colored by country, and is not connected to the slider and dropdown. 
        '''),
    ], className = 'twelve columns' ),
    html.Div(children = [   # Dropdown 
        html.Label('Select Country'),
        dcc.Dropdown(
            options = [{'label':country, 'value':country} for country in df['country']],  # Options are all countries in dataset
            value = [],   # Making the default value an empty list of countries 
            #value = clean_df.loc[clean_df['country']=='USA'],
            multi = True,    # Can select more than one country
            id = 'country_dropdown',  
            )
               ], className = 'five columns'),
    html.Div(children = [   # Slider 
        html.Label('Select Year Range'),    # Label for slider 
        dcc.RangeSlider( 
            min = min_year,
            max = max_year,
            value = [min_year, max_year],   # Make default value the whole range of years in dataset
            step = 1,    # Can go up/down by 1 
            marks = None,   # I don't want marks
            id = 'range_slider',
            tooltip={"placement": "bottom", "always_visible": True},
            allowCross = False,     # Prevent slider points from crossing over each other 
        )
    ], className = 'five columns'),  # Take up half of screen 
    html.Div(children = [   # Graph, so it knows when to place it 
        dcc.Graph(
            id='indicator_graph',
        ), ],
        className = 'twelve columns'),   # Take up whole screen 
    ], className = 'row')   # Placement along row 
#], className = 'row' ) 
    #dcc.Graph(figure=fig)

# Every function must have its own callback operator...but must it really?
@callback(
    Output('indicator_graph', 'figure', allow_duplicate=True),   # Outputs
    Input('country_dropdown', 'value'),   # Dropdown input 
    Input('range_slider', 'value'),   # Slider input 
    prevent_initial_call=True)   # May not need this, but fixed an error at one point 


def update_graph(selected_country, year_range):   # update graph function 

    choices = clean_df[clean_df['country'].isin(selected_country)]
    choices = choices.melt(id_vars=['country'], value_vars=all_columns, var_name='Year', value_name='GDP Per Cap')   # Melt function 
    choices = choices[choices['Year'].astype(int).between(year_range[0], year_range[1])]
    # dff = df[df['Year'] == year_value]   The example in class10

    fig = px.line(choices,   # Make the graph 
                  x = 'Year',
                  y = 'GDP Per Cap',
                  color = 'country',
                  title = 'GDP Percap x Year by Country',
                  labels = {'GDP per Capita'})
                  #.update_layout(xaxis_title="Year", yaxis_title="GDP Per Capita")) 
    return fig


# Run app
if __name__ == '__main__':
    app.run_server(jupyter_mode='tab', debug=True)