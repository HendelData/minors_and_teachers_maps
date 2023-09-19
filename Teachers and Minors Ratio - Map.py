import pandas as pd
import plotly.express as px

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
df['Ratio'] = round(df['minors'] / df['TEACHERS'], ndigits=0)

df['ratio_text'] = df['Ratio'].map('{:,.0f}'.format).astype(str) + ":1"

pd.set_option('display.width', 600)
pd.set_option("display.max_columns", len(df.columns))

fig = px.choropleth(df, locationmode="USA-states", locations='state_abbr', color='Ratio',
                    color_continuous_scale="fall",
                    range_color=(min(df['Ratio']), max(df['Ratio'])),
                    scope="usa",
                    hover_data={'ratio_text': True}
                    )

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                  title="Ratio of Minors to Teachers 2018",
                  legend=dict(entrywidth=10),
                  title_x=0.5,
                  title_y=0.95,
                  hoverlabel=dict(bgcolor="white", font=dict(size=12, family="Arial", color="black"), align="left"))

fig.update_traces(hovertemplate="%{customdata[0]}<extra>%{location}</extra>")

fig.update_coloraxes(colorbar_showticksuffix="all", colorbar_ticksuffix=":1")

fig.write_html(filepath + 'Teachers and Minors Ratio Map.html')
