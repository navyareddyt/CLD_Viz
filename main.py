import streamlit as st
import json
import plotly.graph_objects as go
import pandas as pd

# Load the precomputed dictionaries from JSON files
with open('gender_dict.json') as json_file:
    gender_dict = json.load(json_file)

with open('religion_dict.json') as json_file:
    religion_dict = json.load(json_file)

# Load the traffic data from a CSV file
df_traffic = pd.read_csv('traffic_df.csv', index_col='year')

# Ensure the 'year' column is the DataFrame index if it's not already
if 'year' in df_traffic.columns:
    df_traffic.set_index('year', inplace=True)

# Read the social media presence data from the JSON file
with open('social_media_dict.json', 'r') as json_file:
    social_media_dict = json.load(json_file)

# Create a DataFrame from the social_media_dict
df_social_media = pd.DataFrame.from_dict(social_media_dict, orient='index')


st.set_page_config(layout="wide")

# Sidebar for entity selection
selected_entities = st.sidebar.multiselect("Select Country", sorted(list(set(gender_dict.keys()) & set(religion_dict.keys()))))

# Expandable Gender Selection
gender_expander_selection = st.sidebar.expander("Gender")
gender_selection = [
    gender_expander_selection.checkbox('Male', value=True, key='male'),
    gender_expander_selection.checkbox('Female', value=True, key='female')
]
# Define colors for gender distribution
gender_colors = ['#1f77b4', '#d62728']

# Expandable Religion Selection
religion_expander_selection = st.sidebar.expander("Religion")
religions = ['Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Judaism', 'Others']
religion_selection = [religion_expander_selection.checkbox(religion, value=True, key=religion) for religion in religions]

# Define custom colors for religion distribution
religion_colors = ['#2ca02c', '#9467bd', '#8c564b', '#ff7f0e', '#6b6ecf', '#17becf'] 


# Expandable Social Media Presence Selection
social_media_expander_selection = st.sidebar.expander("Social Media Presence")
social_media_platforms = ['twitter', 'facebook', 'youtube', 'instagram', 'website', 'linkedin']
social_media_selection = [social_media_expander_selection.checkbox(platform, value=True, key=platform) for platform in social_media_platforms]

# Define custom colors for each social media platform
social_media_colors = ['#FF5733', '#FFD700', '#7FFF00', '#4169E1', '#9400D3', '#FF1493']


# Expandable Gender Distribution Plot
if selected_entities and any(gender_selection):
    with st.expander("Gender Distribution for Selected Entities", expanded=True):
        gender_fig = go.Figure()

        for gender, selected, color in zip(['Male', 'Female'], gender_selection, gender_colors):
            if selected:
                idx = 0 if gender == 'Male' else 1
                gender_fig.add_trace(go.Bar(x=list(selected_entities), y=[gender_dict[entity][idx] for entity in selected_entities], name=gender, marker_color=color))

        gender_fig.update_layout(barmode='group', xaxis_tickangle=-45)
        st.plotly_chart(gender_fig, use_container_width=True)

# Expandable Religion Distribution Plot
if selected_entities and any(religion_selection):
    with st.expander("Religion Distribution for Selected Entities", expanded=True):
        religion_fig = go.Figure()

        for religion, selected, color in zip(religions, religion_selection, religion_colors):
            if selected:
                idx = religions.index(religion)
                religion_fig.add_trace(go.Bar(x=selected_entities, y=[religion_dict[entity][idx] for entity in selected_entities], name=religion, marker_color=color))

        religion_fig.update_layout(barmode='group', xaxis_tickangle=-45)
        st.plotly_chart(religion_fig, use_container_width=True)

# Expandable Social Media Distribution Plot
if selected_entities and any(social_media_selection):
    with st.expander("Social Media Distribution for Selected Countries", expanded=True):
        social_media_fig = go.Figure()

        for platform, selected, color in zip(social_media_platforms, social_media_selection, social_media_colors):
            if selected:
                idx = social_media_platforms.index(platform)
                social_media_fig.add_trace(go.Bar(x=selected_entities, y=[social_media_dict[country][idx] for country in selected_entities], name=platform, marker_color=color))

        social_media_fig.update_layout(barmode='group', xaxis_tickangle=-45)
        st.plotly_chart(social_media_fig, use_container_width=True)

        
# Expandable Traffic Plot
if selected_entities:
    with st.expander("Traffic Information for Selected Entities", expanded=True):
        traffic_fig = go.Figure()

        # Iterate over each selected entity and add a line trace for each
        for entity in selected_entities:
            # Check if the entity is in the columns of the DataFrame
            if entity in df_traffic.columns:
                # Extracting yearly traffic data for the current entity
                yearly_traffic = df_traffic[entity]
                
                # Add a line trace for the selected entity's traffic data
                traffic_fig.add_trace(go.Scatter(x=yearly_traffic.index, y=yearly_traffic, mode='lines+markers', name=entity))

        # Setting the title and axis labels
        traffic_fig.update_layout(title='Traffic Volume Trend for Selected Entities',
                                  xaxis_title='Year',
                                  yaxis_title='Traffic Volume',
                                  )

        # Display the figure in the Streamlit app
        st.plotly_chart(traffic_fig, use_container_width=True)