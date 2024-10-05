# -*- coding: utf-8 -*-
"""GKHack24.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pT6rqzbd7BFhkOs7Se8oh3SPYcgJRsiv
"""

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from jupyter_dash import JupyterDash
import statsmodels.api as sm
from matplotlib import pyplot as plt

# Load the data from the CSV file (adjust header as necessary)
data = pd.read_csv("https://raw.githubusercontent.com/Awonke03/GKHACK24/main/Water_Leakages.csv")

# Display the first few rows of the updated DataFrame
data.head()

#shape of data
data.shape

data.columns

#data info
data.info()

#finding if there are missing data
data.isnull().sum()

#findingmissing value percentage
data.isnull().sum()/data.shape[0]*100

#finding the duplicates
data.duplicated().sum()

data.head(1)

"""We can observe that no data was recorded from 1960 to 1990, as there is only one unique value—a blank space—for nearly all, if not all, of the years in this range. Therefore, it is safe to conclude that these years should be dropped from our dataset."""

from plotly.subplots import make_subplots  # Import make_subplots
if data.isnull().values.any():
    missing_percentage = (data.isnull().sum() / len(data)) * 100
    columns_with_missing = missing_percentage[missing_percentage > 0]

    # Separate columns with 50% or greater missing values and those with less than 50%
    high_missing = columns_with_missing[columns_with_missing >= 50]
    low_missing = columns_with_missing[columns_with_missing < 50]

    # Creating subplots
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )

    # Donut plot for columns with 50% or greater missing values
    fig.add_trace(
        go.Pie(
            values=high_missing.values,
            labels=high_missing.index,
            hole=.3,
            textinfo='percent+label'
        ),
        row=1, col=1
    )

    # Donut plot for columns with less than 50% missing values
    fig.add_trace(
        go.Pie(
            values=low_missing.values,
            labels=low_missing.index,
            hole=.3,
            textinfo='percent+label'
        ),
        row=1, col=2
    )

    fig.update_layout(
        title_text="Percentage of Missing Values by Column",
        width=1350,
        height=600,
        annotations=[
            dict(
                text="Columns with ≥50% Missing Values",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.25, y=-0.15,
                xanchor="center", yanchor="top",
                font=dict(size=14)
            ),
            dict(
                text="Columns with <50% Missing Values",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.75, y=-0.15,
                xanchor="center", yanchor="top",
                font=dict(size=14)
            )
        ]
    )

    fig.show()
else:
    print("No missing values in the dataset.")

"""We can observed that from 1960 to 1990 no data was acquired, there are no obeservations at all in the years in this range. Therefore With the knowledge that all columns with more than 50% missing data are to be dropped since any imputions would be regarded as in accurate."""

#droping the cols
df1= data.drop(['1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
       '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
       '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
       '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
       '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
       '2005', '2006', '2007',], axis= 1 )

df1.head(2)

"""Understanding that the data represents Waker leakage by Percentage, measured as a percentage, we can now remove the two columns, Indicator Name and Indicator Code"""

df = df1.drop(columns=['Indicator Name', 'Indicator Code'])

df.dtypes

# Delete the last column from the dataset
df = df.iloc[:, :-1]

# Reset the index of the DataFrame
df = df.reset_index(drop=True)

# Display the first few rows of the updated DataFrame
df.head()

# Extract the columns to check first, all but "Country Name" and "Country Code"
cols_2_see = df.columns.difference(['Country Name', 'Country Code'])

NaNs = df[cols_2_see].isna().all(axis=1)
df[NaNs]

# Remove these rows from the dataset
df = df[~NaNs]
df.head(2)

df.shape

#importing the continents dataset
data2=pd.read_csv("https://raw.githubusercontent.com/Awonke03/GKHACK24/main/continents-according-to-our-world-in-data.csv")
data2.sample(n=5)

# Merge the DataFrames based on 'Country Name' and 'Country Code'
df_merged = df.merge(data2[['Entity', 'Continent', 'Code']],
                     left_on=['Country Name', 'Country Code'],
                     right_on=['Entity', 'Code'],
                     how='left')

# Move the 'Continent' column to position 3
continent_col = df_merged.pop('Continent')
df_merged.insert(2, continent_col.name, continent_col)

# Drop the redundant columns 'Entity' and 'Code'
df_merged = df_merged.drop(['Entity', 'Code'], axis=1)

# Display the first few rows of the updated DataFrame
df_merged.head(2)

# Select the columns from 1991 to 2022
columns_to_check = df_merged.loc[:, '2008':'2022']

# Find columns with NaN values
columns_with_na = columns_to_check.columns[columns_to_check.isnull().any()]

# Display the columns with NaN values
print("Columns with NaN values from 1991 to 2022:")
print(columns_with_na)

#Filter rows where '2021' or '2022' have NaN values
nan_rows = df_merged[df_merged[['2021', '2022']].isna().any(axis=1)]

# Select the 'Country Name' column along with '2021' and '2022' columns
result = nan_rows[['Country Name', '2021', '2022']]

result

# Updating the values for Afghanistan and the Russian Federation in the df_merged DataFrame
df_merged.loc[df_merged['Country Name'] == 'Afghanistan', '2021'] = 16.39
df_merged.loc[df_merged['Country Name'] == 'Afghanistan', '2022'] = 17.75
df_merged.loc[df_merged['Country Name'] == 'Russian Federation', '2022'] = 14.37

# Verify the changes for Afghanistan and the Russian Federation
print(df_merged[df_merged['Country Name'].isin(['Afghanistan', 'Russian Federation'])][['Country Name', '2021', '2022']])

# Fill NaN values with the mean of each column
df_merged[['2021', '2022']] = df_merged[['2021', '2022']].apply(lambda col: col.fillna(col.mean()))

df_merged.head(3)

# Get the sum of na values in the continent col
df_merged['Continent'].isna().sum()

# Filter rows where 'Continent' has NaN values
rows_with_na = df_merged[df_merged['Continent'].isna()]
rows_with_na

"""Here we notice that there are 75 rows, or rather 75 countries that are not 'continent classifies'. Maybe the issue is with the naming of the countries, that is to say 'South Africa', 'Suid Afrika' and 'South Africa ' are all different with the same country code. So we try matching using the country code alone"""

# Merge the DataFrames based only on 'Country Code'
merged_data1 = df.merge(data2[['Code', 'Continent']],
                              left_on='Country Code',
                              right_on='Code',
                              how='left')

# Drop the redundant column 'Code'
merged_data1 = merged_data1.drop(['Code'], axis=1)

# Move column "Continent" to position 3
col = merged_data1.pop('Continent')
merged_data1.insert(2, col.name, col)

merged_data1['Continent'].isna().sum()

rows_with_na.shape

# Check if the column 'Continent' exists and has NaN values
countries_without_continent = df_merged[df_merged['Continent'].isna()]

# Display the countries that do not have a continent assigned
print("Countries without a continent assigned:")
print(countries_without_continent[['Country Name', 'Continent','Country Code']])

# Display the list of country codes without continents
print("Country codes of countries without a continent assigned:")
print(countries_without_continent['Country Code'].tolist())

df_merged.head(2)

# clean dataset
df4 = pd.read_csv("https://raw.githubusercontent.com/Awonke03/GKHACK24/main/country_continent.csv")

# Merge df3 with df_merged on the 'Country Code' column
data = pd.merge(df4, df_merged, on='Country Code', how='inner')

# Display the first few rows of the merged DataFrame
data.head()



"""we can see that we have redundent rows and columns and so we are going to keep Country Name_y, Continent_y which is from df3 and drop Country Name_x , Continent_x which are coming from the pd.merge."""

# Drop the 'Country Name_y' and 'Continent_y' columns from the DataFrame 'data'
data = data.drop(columns=['Country Name_y', 'Continent_y'])

data.head(5)

# Transform the DataFrame to long format
data_long = pd.melt(data, id_vars=['Country Code', 'Country Name_x', 'Continent_x'],
                    var_name='Year', value_name='Water Leakage')

# Ensure 'Year' is a string
data_long['Year'] = data_long['Year'].astype(str)

# Filter data to include all countries
filtered_data = data_long

# Plotting the animated choropleth map
fig1 = px.choropleth(
    filtered_data,
    locations='Country Code',
    color='Water Leakage',  # Corrected from 'Water Leakage Rate' to 'Water Leakage'
    hover_name='Country Name_x',
    animation_frame='Year',
    color_continuous_scale='Viridis',
    title='Water Leakage Rate Over Time [2008-2022]',
    projection='natural earth'
)

# Customize layout and increase size of the map
fig1.update_layout(
    geo=dict(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="LightGray",
        showocean=True,
        oceancolor="LightBlue",
        showlakes=True,
        lakecolor="LightBlue"
    ),
    coloraxis_colorbar_title='Water Leakage Rate',
    title_font_size=24,
    title_font_family='Arial',
    width=1250,  # Increase the width of the map
    height=450   # Increase the height of the map
)

# Show the plot
fig1.show()

# Load the data
data_long = pd.melt(data, id_vars=['Country Code', 'Country Name_x', 'Continent_x'],
                    var_name='Year', value_name='Water Leakage')

# Ensure 'Year' is a string
data_long['Year'] = data_long['Year'].astype(str)

# Filter data for specific countries
selected_countries = [
    'South Africa',
    'Namibia',
    'Botswana',
    'Zimbabwe',
    'Mozambique'
]

# Filter data to include only selected countries
filtered_data = data_long[data_long['Country Name_x'].isin(selected_countries)]

# Create the animated bar plot
fig2 = px.bar(
    filtered_data,
    x='Country Name_x',  # X-axis represents the countries
    y='Water Leakage',  # Y-axis represents water leakage values
    color='Country Name_x',  # Different colors for different countries
    animation_frame='Year',  # Animation over the years
    animation_group='Country Name_x',  # Group animation by country
    title='Water Leakage by Country (2008-2022)',
    labels={'Country Name_x': 'Country', 'Water Leakage': 'Water Leakage'},
)

# Customize layout with specified height and width
fig2.update_layout(
    xaxis_title='Country',
    yaxis_title='Water Leakage',
    title_font_size=24,
    title_font_family='Arial',
    showlegend=False,  # Hide the legend as colors represent countries already
    width=1250,  # Set the width of the plot
    height=550   # Set the height of the plot
)

# Show the plot
fig2.show()

# Filter data for South Africa only
sa_data = data[data['Country Name_x'] == 'South Africa']

# List of yearly columns for 2008 to 2023
yearly_columns = [str(year) for year in range(2008, 2023)]  # Adjusted to include 2023

# Calculate the average water leakage for South Africa for each year
annual_averages_sa = sa_data[yearly_columns].mean()

# Convert the result to a DataFrame for plotting
trend_data_sa = pd.DataFrame({
    'Year': annual_averages_sa.index,
    'Average Water Leakage': annual_averages_sa.values
})

# Plotting the trend line graph for South Africa's water leakage
fig3 = px.line(trend_data_sa, x='Year', y='Average Water Leakage',
                title='Average Water Leakage for South Africa (2008-2023)',
                labels={'Average Water Leakage': 'Average Water Leakage (%)'},
                markers=True,  # Add markers to the line
                line_shape='spline',  # Use smooth curves
                color_discrete_sequence=['#1f77b4'])  # Custom color

# Customize layout with grid lines
fig3.update_layout(
    xaxis_title='Year',
    yaxis_title='Average Water Leakage (%)',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(255,255,255,0.8)',
    title_font_size=24,
    title_font_family='Arial',
    xaxis=dict(
        tickmode='linear',
        dtick=1,
        showgrid=True,  # Add grid lines for the x-axis
        gridcolor='LightGray'  # Color of the grid lines
    ),
    yaxis=dict(
        showgrid=True,  # Add grid lines for the y-axis
        gridcolor='LightGray'  # Color of the grid lines
    )
)

# Show the plot
fig3.show()

df5 = pd.read_excel("https://raw.githubusercontent.com/Awonke03/GKHACK24/main/NCData.xlsx")

# Sort the DataFrame by 'Agricultural Potential'
northern_cape_df_sorted = df5.sort_values(by='Agricultural Potential', ascending=False)

# Create the bar chart
fig4 = go.Figure(data=[
    go.Bar(name='Agricultural Potential', x=northern_cape_df_sorted['City/Town in the NC'], y=northern_cape_df_sorted['Agricultural Potential']),
    go.Bar(name='Size of Economy', x=northern_cape_df_sorted['City/Town in the NC'], y=northern_cape_df_sorted['Size of Economy'])
])

# Update layout of the figure
fig4.update_layout(
    barmode='group',
    title='Agricultural Potential and Size of Economy of Towns in the Northern Cape'
)

# Show the plot
fig4.show()

# Read data from the Excel file
df = pd.read_excel("https://raw.githubusercontent.com/Awonke03/GKHACK24/main/Leakage_Costs.xlsx")

df.columns = ['Year', 'Water Leakage (%)', 'Water Leakage Cost (Million R)']

# Create a bar plot for Water Leakage Cost
fig5 = px.bar(
    df,
    x='Year',
    y='Water Leakage Cost (Million R)',
    color='Water Leakage Cost (Million R)',
    color_continuous_scale='Viridis',
    title='Water Leakage Cost by Year (2008-2022)',
    labels={'Water Leakage Cost (Million R)': 'Water Leakage Cost (Million R)'},
    template='plotly_white'
)

# Update layout for the figure
fig5.update_layout(
    xaxis=dict(title='Year'),
    yaxis=dict(title='Water Leakage Cost (Million R)'),
    width=1250,  # Set the height to 1250
    height=500     # Set the width to 550
)

# Show the plot
fig5.show()

# Load the data from the Excel file
file_path = "https://raw.githubusercontent.com/Awonke03/GKHACK24/main/Economic_Effect.xlsx"
df = pd.read_excel(file_path)

# Filter the data for the relevant years (2018-2022)
data_filtered = df[df['Year'].isin([2018, 2019, 2020, 2021, 2022])]

# Create the Sunburst Chart
sunburst_fig = px.sunburst(
    data_filtered,
    path=['Year', 'Sector'],  # Define the hierarchy for the sunburst chart
    values='Water Leakage Cost (%)',  # Use 'Water Leakage Cost (%)' as the values
    title='Water Leakage Costs by Sector in South Africa (2018-2022)',
    color='Water Leakage Cost (%)',  # Color by Water Leakage Cost
    color_continuous_scale='Greens',  # Change this to a green color scale
    branchvalues='total',  # Calculate branch values as total
    template='plotly_white'
)

# Update layout for the figure
sunburst_fig.update_layout(
    title_font_size=24,
    title_font_family='Arial',
    height=450,  # Set the height to 450
    width=1250   # Set the width to 1250
)

# Show the plot
sunburst_fig.show()


import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from jupyter_dash import JupyterDash

# Create the app
# Create the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

# Sidebar layout with full height and centered buttons
sidebar = html.Div(
    [
        html.Hr(),
        html.H6("Investing in Infrastructure: Building a Sustainable Water Future", style={'color': 'white', 'text-align': 'center', 'margin-bottom': '10px'}),
        dbc.Button("Water Analysis", href="/visuals1", id="visuals1-button", color="primary", className="mb-2", style={'border-radius': '25px', 'width': '150px'}),
        dbc.Button("Water Impact", href="/visuals2", id="visuals2-button", color="secondary", className="mb-2", style={'border-radius': '25px', 'width': '150px'}),
        html.H6("Every Drop Saved: Cutting Costs Through Smart Leak Management", style={'color': 'white', 'text-align': 'center', 'margin-bottom': '10px'}),
    ],
    style={
        'width': '15%',
        'position': 'fixed',
        'top': '0',
        'right': '0',
        'height': '100%',
        'backgroundColor': '#343a40',
        'padding': '10px',
        'z-index': '10',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'alignItems': 'center'
    }
)

# Title of the dashboard
title = html.H1("Print('Alpha')", style={
    'text-align': 'center',
    'position': 'fixed',
    'top': '10px',
    'left': '50%',
    'transform': 'translateX(-50%)',
    'width': '100%',
    'z-index': '999'
})

# Content layout with fixed height, adjusted for the sidebar
content = html.Div(id="page-content", style={
    'margin-right': '15%',
    'margin-left': '0',
    'margin-top': '60px',
    'height': 'calc(100vh - 100px)',
    'overflowY': 'auto',
    'padding': '10px',
    'z-index': '1',
})

# Define the first page visuals with proper spacing and centering
first = dbc.Container([
    dbc.Row(
        dbc.Col(dcc.Graph(figure=fig1, style={'width': '100%', 'height': '400px'}), width=12),
        justify="center",  # Center the graph
        style={'margin-bottom': '40px'}  # Space below fig1
    ),
    dbc.Row(
        dbc.Col(html.Hr(style={'border': '1px solid #ccc', 'margin-bottom': '20px'})),  # Divider
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(figure=fig2, style={'width': '100%', 'height': '500px'}), width=12),
        justify="center",  # Center the graph
        style={'margin-bottom': '40px'}  # Space below fig2
    ),
    dbc.Row(
        dbc.Col(html.Hr(style={'border': '1px solid #ccc', 'margin-bottom': '20px'})),  # Divider
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(figure=fig3, style={'width': '100%', 'height': '450px'}), width=12),
        justify="center",  # Center the graph
        style={'margin-bottom': '40px'}  # Space below fig3
    ),
], fluid=True)

# Define the second page visuals with proper spacing and centering
second = dbc.Container([
    dbc.Row(
        dbc.Col(dcc.Graph(figure=sunburst_fig, style={'width': '100%', 'height': '400px'}), width=12),
        justify="center",  # Center the graph
        style={'margin-bottom': '40px'}  # Space below fig6
    ),
    dbc.Row(
        dbc.Col(html.Hr(style={'border': '1px solid #ccc', 'margin-bottom': '20px'})),  # Divider
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(figure=fig5, style={'width': '100%', 'height': '450px'}), width=12),
        justify="center",  # Center the graph
        style={'margin-bottom': '40px'}  # Space below fig5
    ),
    dbc.Row(
        dbc.Col(html.Hr(style={'border': '1px solid #ccc', 'margin-bottom': '20px'})),  # Divider
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(figure=fig4, style={'width': '100%', 'height': '500px'}), width=12),
        justify="center",  # Center the graph
        style={'margin-bottom': '40px'}  # Space below fig4
    ),
], fluid=True)

# App layout
app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    title,
    content
])

# Callback to control navigation
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/visuals1" or pathname == "/":
        return first
    elif pathname == "/visuals2":
        return second
    else:
        return first

# Run the app on a different port
if __name__ == "__main__":
    app.run_server(debug=True, port=8009)



