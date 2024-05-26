

import plotly.express as px
import pickle
import streamlit as st
from streamlit_plotly_events import plotly_events
import geopandas as gpd
import geojson
px.set_mapbox_access_token("pk.eyJ1IjoiYW1hbnp5MTIzNCIsImEiOiJjbG9land0NjcwazR6MmtvMjgycTJ2bHp2In0.wEKHMlZHua7rHUV0Av03UQ")
st.set_page_config(layout="wide") 
st.image("wcs.png", width=100)
# Add title to your Streamlit app
st.title("Pakistan Glacier Dashboard")

@st.cache_resource
def get_glacier_df():
    print("Getting glacier df ")
    glaciers_df = gpd.read_file("intersection.geojson")
    glaciers_df = glaciers_df.rename({"RGIId": "RGI Glacier ID", "Name": "Glacier Name", "BgnDate":"Begin Date" , "EndDate" : "End Date", "Area" : "Total Area, km2", "Zmin": "Minimum Elevevation", "Zmed": "Median Elevation", "Zmax":"Maximum Elevation"}, axis = 1)
    return glaciers_df[["Glacier Name", "RGI Glacier ID", "Begin Date", "End Date", "Total Area, km2", "Minimum Elevevation", "Median Elevation", "Maximum Elevation", "CenLat", "CenLon"]]

@st.cache_resource
def create_scatter_plot(df):
    print("creating scatter figure")
    # fig = pickle.load(open('fig1.pkl','rb'))
    # return fig
    with open('intersection.geojson') as f:
        glaciers_gj = geojson.load(f)
    with open('pakistan.geojson') as f:
        pakistan_gj = geojson.load(f)
    fig = px.scatter_mapbox(df, lat = "CenLat", lon = "CenLon", height =800, hover_data=["Glacier Name", "RGI Glacier ID"])
    fig.update_layout(mapbox_layers=[{
                "below": 'traces',
                "sourcetype": "geojson",
                "type": "fill",
                "color": "#16c9cc",
                "source": glaciers_gj
            },
            {
                "below": 'traces',
                "sourcetype": "geojson",
                "type": "line",
                "color": "black",
                "source": pakistan_gj
            }])

    return fig


glaciers_df = get_glacier_df()
glaciers_df.loc[glaciers_df["Glacier Name"].isna(), "Glacier Name"] = " "
fig = create_scatter_plot(glaciers_df)
fig.update_layout(margin=dict(l=20, r=20, t=20, b=20),)
print("running selected points")
selected_points = plotly_events(fig)

print("done")
# selected_points = plotly_events(fig)

if len(selected_points)>0:
    selected_glacier = glaciers_df.iloc[[selected_points[0]["pointIndex"]]]
    st.write(tuple(selected_glacier[["CenLat", "CenLon"]].values))
    st.dataframe(selected_glacier[["Glacier Name", "RGI Glacier ID", "Begin Date", "End Date", "Total Area, km2", "Minimum Elevevation", "Median Elevation", "Maximum Elevation"]])

st.text("")
    # Provide references
st.subheader("Data References")
st.markdown(
        """
https://nsidc.org/data/nsidc-0770/versions/6
    """
    )
st.text("")
st.markdown("Developed by Haris Mushtaq")
