
import math
import streamlit as st
import pandas as pd
import pydeck as pdk
import math
import ast
import pandas as pd
import pydeck as pdk


# df = pd.DataFrame()

# Custom color scale
COLOR_RANGE = [
    [65, 182, 196],
    [127, 205, 187],
    [199, 233, 180],
    [237, 248, 177],
    [255, 255, 204],
    [255, 237, 160],
    [254, 217, 118],
    [254, 178, 76],
    [253, 141, 60],
    [252, 78, 42],
    [227, 26, 28],
    [189, 0, 38],
    [128, 0, 38],
]
import numpy as np

# Create the list of 13 numbers from 0 to 1
BREAKS = np.linspace(0, 1, 13).tolist()


def color_scale(val):
    for i, b in enumerate(BREAKS):
        if val < b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[i]


def calculate_elevation(val):
    return math.sqrt(val) * 10

st.title('Sedgwick County Demographics')

st.header('Working Age 18-64')


option = st.selectbox(
    "Choose a Race/Ethnicity:",
    ('WHITE',
     'BLACK OR AFRICAN AMERICAN',
     'AMERICAN INDIAN AND ALASKA NATIVE',
     'ASIAN',
     'NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER',
     'ETHNICITY UNKNOWN',
     'TWO OR MORE RACES',
     'HISPANIC OR LATINO')
)
col = option.replace(' ', '_')
st.write('Showing ', option, ' Demographic Information')
opacity = st.slider('Choose Opacity', 0.0, 1.0, 0.5)
df = pd.read_csv('z:/Jon/Python/Census/sedgwick_st.csv')
df['coordinates'] = df['coordinates'].apply(ast.literal_eval)


df['ratio'] = round(df[col]/df['total'], 4)

df["fill_color"] = df["ratio"].apply(color_scale)
df[col] = df[col]*1

view_state = pdk.ViewState(
    **{"latitude": 37.68, "longitude": -97.5, "zoom": 9, "maxZoom": 16, "pitch": 45, "bearing": 0}
    )

polygon_layer = pdk.Layer(
    "PolygonLayer",
    df,
    id="geojson",
    opacity=opacity,
    stroked=False,
    get_polygon="coordinates",
    filled=True,
    extruded=True,
    # wireframe=True,
    get_elevation=col,
    get_fill_color="fill_color",
    get_line_color=[255, 255, 255],
    auto_highlight=True,
    pickable=True,
)

tooltip = {"html": "<b>Ratio of "+option+" population to total:</b> {ratio} <br /><b>"+option+" population:</b> {"+col+"}"}
r = pdk.Deck(
    polygon_layer,
    initial_view_state=view_state,
    # effects=[lighting_effect],
    map_style=pdk.map_styles.LIGHT,
    tooltip=tooltip
)

st.write('Darker shades of red represent higher ratios. Taller objects represent higher population counts')
st.write('Interact with the map to view more of the data')

map = st.pydeck_chart(r)


st.write('Summary demographic information for Sedgwick County')

st.table(pd.read_csv('z:/Jon/Python/Census/working_demographics_sedgwick.csv'))


