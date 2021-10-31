import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import polyline
import numpy as np
import sys
sys.path.append("src")
from get_data import get_activity_data
sys.path.append(".")
from api_key import mapbox_token
from app_utilities import apply_selection


# get data from strava
df = get_activity_data()

####################### APP ###############################
st.title('Dora The Strava Explorer')

## Selection side bar
st.sidebar.title("Select activities")
# activity type selector
activity_type_all = list(df['type'].unique())
type_selected = st.sidebar.multiselect("Select activity type(s)", activity_type_all, activity_type_all)
if not type_selected:
    st.error("Please select at least one activity type.")
# time range selector
start_date = st.sidebar.date_input('Start date', df.start_date_local.min().date())
end_date = st.sidebar.date_input('End date', df.start_date_local.max().date())
if start_date > end_date:
    st.error('Error: End date must fall after start date.')

# apply filters
df_selected = apply_selection(df, type_selected, start_date, end_date)
st.success(f'Number of selected activities: {df_selected.shape[0]}')

# plot ride on map
fig = go.Figure()
col_scale = px.colors.qualitative.Alphabet
colors = col_scale*int(np.ceil(df_selected.shape[0]/len(col_scale)))
# loop over selected rides
for idx, row in df_selected.iterrows():
    # skip activities without gps
    if row['map.summary_polyline'] is None:
        continue
        
    coordinates = polyline.decode(row['map.summary_polyline'])
    ride_longitudes = [coordinate[1] for coordinate in coordinates]
    ride_latitudes = [coordinate[0] for coordinate in coordinates]

    fig.add_trace(
        go.Scattermapbox(
            lat = ride_latitudes, 
            lon = ride_longitudes,
            mode = "lines", # is it possible to add direction arrow?
            line= go.scattermapbox.Line(
                color=colors[idx]
            ),
            name=f"{row['start_date_local'].date()} - {row['name']}"
        )
    )

fig.update_layout(
        mapbox = go.layout.Mapbox(
            accesstoken=mapbox_token,
            style='light',
            zoom=9,
            center=go.layout.mapbox.Center(
                lat=np.median(ride_latitudes),
                lon=np.median(ride_longitudes)
            ),
        ),
        showlegend=False,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

st.plotly_chart(fig)