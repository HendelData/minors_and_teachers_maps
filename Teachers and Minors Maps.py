import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

filepath = 'C:/Users/marce/Documents/Python/'

# GET DATA
df = pd.read_csv("https://drive.google.com/uc?export=download&id=18ypmtAmSX3azLTEggzVp5juo4oVZkHJx")
df = df.drop(df.index[-3:])

df.rename(columns={'MINOR POPULATION': 'minors'}, inplace=True)

# DICTIONARY TO REPLACE STATE NAME WITH TWO-LETTER ABBREVIATION
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

df['state_abbr'] = df['STATE'].replace(us_state_to_abbrev)

# CREATE TEXT FIELDS TO BE DISPLAYED
df['minors_text'] = df['minors'].map('{:,.0f}'.format).astype(str)
df['teachers_text'] = df['TEACHERS'].map('{:,.0f}'.format).astype(str)

# CREATE SUBPLOT CANVAS
rows = 1
cols = 2
fig = make_subplots(rows=rows, cols=cols,
                    specs=[[{'type': 'choropleth'} for c in np.arange(cols)] for r in np.arange(rows)],
                    subplot_titles=['Minors by State', 'Teachers by State'])

# MAP OF MINORS
fig.add_trace(go.Choropleth(
    locations=df['state_abbr'],
    z=df['minors'],
    zmin=0,
    zmax=8000000,
    locationmode='USA-states',
    colorscale='fall',
    colorbar=dict(title='Minors', x=0.41, y=0.50, len=0.55, tickformat=',')), row=1, col=1)

# MAP OF TEACHERS
fig.add_trace(go.Choropleth(
    locations=df['state_abbr'],
    z=df['TEACHERS'],
    locationmode='USA-states',
    colorscale='fall',
    colorbar=dict(title='Teachers', x=0.96, y=0.50, len=0.55, tickformat=',')), row=1, col=2)

for i in range(0, 1):
    fig.update_layout(
        title_text='Minor and Teacher Count by State 2018',
        title_x=0.5,
        title_y=0.95,
        margin=dict(t=0),
        **{'geo' + str(i) + '_scope': 'usa' for i in [''] + np.arange(2, rows * cols + 1).tolist()})

for index, trace in enumerate(fig.data):
    fig.data[index].hovertemplate = '%{location} <br> %{z:,} <extra></extra>'

# ADJUST DISTANCE BETWEEN TITLE AND MAP
fig.layout.annotations[0].update(y=0.75)
fig.layout.annotations[1].update(y=0.75)

fig.write_html(filepath + 'Teachers and Minors Small Multiples Map.html')
