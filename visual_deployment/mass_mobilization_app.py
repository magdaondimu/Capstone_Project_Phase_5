import streamlit as st
import pandas as pd
import plotly.express as px

# Custom CSS for styling
st.markdown("""
    <style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .reportview-container .main{
        color: #000000;
        background-color: #FFFFFF;
    }
    .css-1d391kg { 
        display: flex; 
        justify-content: center; 
        padding: 0.5rem 0rem; 
    }
    .css-1d391kg div { 
        padding: 0.5rem 2rem; 
    }
    </style>
    """, unsafe_allow_html=True)

# Load the cleaned dataset
df = pd.read_csv('mass_mobilization_cleaned.csv')

# Top navigation
nav = st.radio("Navigation", ["Home", "World Trends", "Regional Trends", "Country Trends"], horizontal=True)

# Home Page
if nav == "Home":
    st.title("Mass Mobilization Analytics")
    st.write("""
        Welcome to the Mass Mobilization Analytics dashboard. This platform provides insights 
        into global, regional, and country-level protest trends. Use the navigation bar above to 
        explore different sections and delve into the data.
    """)
    
    # Add a slideshow of images with captions
    images = [
        {"path": "image(1).webp", "caption": "Supporters of Venezuelan opposition leader Juan Guaidó take part in a march in Caracas in February 2019."},
        {"path": "image(2).webp", "caption": "Iraqi protesters join hands after taking part in prayers during anti-government demonstrations in the Shiite holy city of Najaf, in November 2019."},
        {"path": "image(3).jpg", "caption": "#EndSars protests against police brutality is seen by analysts as a turning point in Nigerian politics and the youth vote is expected to be critical in the 2023 election."}
    ]
    
    current_image = st.session_state.get('current_image', 0)
    
    st.image(images[current_image]["path"], caption=images[current_image]["caption"], use_column_width=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        if st.button("Previous"):
            current_image = (current_image - 1) % len(images)
    
    with col3:
        if st.button("Next"):
            current_image = (current_image + 1) % len(images)
    
    st.session_state['current_image'] = current_image

# World Trends Page
elif nav == "World Trends":
    st.title("World Protests")
    st.write("""
        This section visualizes the global distribution and frequency of protests. 
        Select a year to see the number of protests in each country for that specific year.
    """)
    year = st.selectbox("Select Year", sorted(df['year'].unique()))
    
    # Filter data for the selected year
    filtered_data = df[df['year'] == year]
    
    # Count number of protests per country
    protest_counts = filtered_data['country'].value_counts().reset_index()
    protest_counts.columns = ['country', 'protests_count']
    
    # Create the map
    world_map = px.scatter_geo(protest_counts, locations="country", locationmode='country names',
                               color="protests_count", hover_name="country", size="protests_count",
                               projection="natural earth", title="World Protests",
                               color_continuous_scale=px.colors.sequential.Reds)
    # Add borders and remove lakes
    world_map.update_geos(showcoastlines=True, coastlinecolor="Black",
                          showland=True, landcolor="white",
                          showocean=True, oceancolor="LightBlue",
                          showcountries=True, countrycolor="Black")
    st.plotly_chart(world_map)

# Regional Trends Page
elif nav == "Regional Trends":
    st.title("Regional Analysis")
    st.write("""
        This page provides insights into protest activities at the regional level. 
        Select a region and a range of years to view the data on protest days, participants, demands, and violence.
    """)
    region = st.selectbox("Select Region", [r for r in df['region'].unique() if r != 'Canada'] + ['N.America(Canada)'])
    if region == 'N.America(Canada)':
        region = 'Canada'
    
    year_range = st.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (int(df['year'].min()), 2020))

    # Filter data for the selected region and year range
    regional_data = df[(df['region'] == region) & (df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

    # Tabs for data visualization
    tab = st.selectbox("Select Tab", ["Protest Days", "Participants", "Demands", "Violence"])

    # Chart type selection
    chart_type = st.radio("Select Chart Type", ["Barplot", "Line Graph"])

    # Friendly demand names mapping
    demand_mapping = {
        'demand_labor_wage_dispute': 'Labor/Wage Dispute',
        'demand_land_farm_issue': 'Land/Farm Issue',
        'demand_police_brutality': 'Police Brutality',
        'demand_political_behavior': 'Political Behavior',
        'demand_price_increases': 'Price Increases',
        'demand_removal_of_politician': 'Removal of Politician'
    }

    if tab == "Protest Days":
        protest_days = regional_data.groupby('year')['protest_duration'].sum().reset_index().sort_values(by='year')
        if chart_type == "Barplot":
            protest_days_chart = px.bar(protest_days, x="year", y="protest_duration", title="Cumulative Protest Days", labels={'protest_duration': 'Protest Days'})
        else:
            protest_days_chart = px.line(protest_days, x="year", y="protest_duration", title="Cumulative Protest Days", labels={'protest_duration': 'Protest Days'})
        st.plotly_chart(protest_days_chart)
        # Add download button for Protest Days data
        csv = protest_days.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Protest Days Data",
            data=csv,
            file_name='regional_protest_days.csv',
            mime='text/csv',
        )
    elif tab == "Participants":
        participants = regional_data.groupby('year')['participants_numeric'].sum().reset_index().sort_values(by='year')
        if chart_type == "Barplot":
            participants_chart = px.bar(participants, x="year", y="participants_numeric", title="Cumulative Number of Participants", labels={'participants_numeric': 'Participants'})
        else:
            participants_chart = px.line(participants, x="year", y="participants_numeric", title="Cumulative Number of Participants", labels={'participants_numeric': 'Participants'})
        participants_chart.update_layout(yaxis=dict(tickformat='.2s', title='Participants'))
        participants_chart.update_traces(hovertemplate='Year: %{x}<br>Participants: %{y:.0f}')
        st.plotly_chart(participants_chart)
        # Add download button for Participants data
        csv = participants.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Participants Data",
            data=csv,
            file_name='regional_participants.csv',
            mime='text/csv',
        )
    elif tab == "Demands":
        demand = st.selectbox("Select Demand", list(demand_mapping.values()))
        demand_column = [key for key, value in demand_mapping.items() if value == demand][0]
        demand_data = regional_data[regional_data[demand_column] == 1]
        demand_counts = demand_data['year'].value_counts().reset_index().sort_values(by='year')
        demand_counts.columns = ['year', 'protests_count']
        if chart_type == "Barplot":
            demand_chart = px.bar(demand_counts, x="year", y="protests_count", title=f"Protests with Demand: {demand}", labels={'protests_count': 'Protests Count'})
        else:
            demand_chart = px.line(demand_counts, x="year", y="protests_count", title=f"Protests with Demand: {demand}", labels={'protests_count': 'Protests Count'})
        st.plotly_chart(demand_chart)
        # Add download button for Demands data
        csv = demand_counts.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download Data for {demand}",
            data=csv,
            file_name=f'regional_{demand}.csv',
            mime='text/csv',
        )
    elif tab == "Violence":
        state_violence = ['response_beatings', 'response_shootings', 'response_killings']
        violence_mapping = {
            0: 'Non Violent',
            1: 'Protester Violence',
            2: 'State Violence',
            3: 'Both Violence'
        }
        violence = st.selectbox("Select Violence Type", list(violence_mapping.values()))

        if violence == 'Non Violent':
            violence_data = regional_data[regional_data['protesterviolence'] == 0]
            title = "Protests with Non-Violent Protesters"
        elif violence == 'Protester Violence':
            violence_data = regional_data[regional_data['protesterviolence'] == 1]
            title = "Protests with Protester Violence"
        elif violence == 'State Violence':
            violence_data = regional_data[regional_data[state_violence].sum(axis=1) > 0]
            title = "Protests with State Violence"
        elif violence == 'Both Violence':
            violence_data = regional_data[(regional_data['protesterviolence'] == 1) & (regional_data[state_violence].sum(axis=1) > 0)]
            title = "Protests with Both State and Protester Violence"

        violence_counts = violence_data.groupby('year').size().reset_index(name='protests_count').sort_values(by='year')
        if chart_type == "Barplot":
            violence_chart = px.bar(violence_counts, x="year", y="protests_count", title=title, labels={'protests_count': 'Protests Count'})
        else:
            violence_chart = px.line(violence_counts, x="year", y="protests_count", title=title, labels={'protests_count': 'Protests Count'})
        st.plotly_chart(violence_chart)
        # Add download button for Violence data
        csv = violence_counts.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download Data for {title}",
            data=csv,
            file_name=f'regional_{title.replace(" ", "_").lower()}.csv',
            mime='text/csv',
        )


# Country Trends Page
elif nav == "Country Trends":
    st.title("Country Analysis")
    st.write("""
        This page provides insights into protest activities at the country level. 
        Select a country and a range of years to view the data on protest days, participants, demands, and violence.
    """)
    country = st.selectbox("Select Country", df['country'].unique())
    
    year_range = st.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (int(df['year'].min()), 2020))
    
    # Filter data for the selected country and year range
    country_data = df[(df['country'] == country) & (df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

    # Tabs for data visualization
    tab = st.selectbox("Select Tab", ["Protest Days", "Participants", "Demands", "Violence"])

    # Chart type selection
    chart_type = st.radio("Select Chart Type", ["Barplot", "Line Graph"])

    # Friendly demand names mapping
    demand_mapping = {
        'demand_labor_wage_dispute': 'Labor/Wage Dispute',
        'demand_land_farm_issue': 'Land/Farm Issue',
        'demand_police_brutality': 'Police Brutality',
        'demand_political_behavior': 'Political Behavior',
        'demand_price_increases': 'Price Increases',
        'demand_removal_of_politician': 'Removal of Politician'
    }

    if tab == "Protest Days":
        protest_days = country_data.groupby('year')['protest_duration'].sum().reset_index().sort_values(by='year')
        if chart_type == "Barplot":
            protest_days_chart = px.bar(protest_days, x="year", y="protest_duration", title="Cumulative Protest Days", labels={'protest_duration': 'Protest Days'})
        else:
            protest_days_chart = px.line(protest_days, x="year", y="protest_duration", title="Cumulative Protest Days", labels={'protest_duration': 'Protest Days'})
        st.plotly_chart(protest_days_chart)
        # Add download button for Protest Days data
        csv = protest_days.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Protest Days Data",
            data=csv,
            file_name='country_protest_days.csv',
            mime='text/csv',
        )
    elif tab == "Participants":
        participants = country_data.groupby('year')['participants_numeric'].sum().reset_index().sort_values(by='year')
        if chart_type == "Barplot":
            participants_chart = px.bar(participants, x="year", y="participants_numeric", title="Cumulative Number of Participants", labels={'participants_numeric': 'Participants'})
        else:
            participants_chart = px.line(participants, x="year", y="participants_numeric", title="Cumulative Number of Participants", labels={'participants_numeric': 'Participants'})
        participants_chart.update_layout(yaxis=dict(tickformat='.2s', title='Participants'))
        participants_chart.update_traces(hovertemplate='Year: %{x}<br>Participants: %{y:.0f}')
        st.plotly_chart(participants_chart)
        # Add download button for Participants data
        csv = participants.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Participants Data",
            data=csv,
            file_name='country_participants.csv',
            mime='text/csv',
        )
    elif tab == "Demands":
        demand = st.selectbox("Select Demand", list(demand_mapping.values()))
        demand_column = [key for key, value in demand_mapping.items() if value == demand][0]
        demand_data = country_data[country_data[demand_column] == 1]
        demand_counts = demand_data['year'].value_counts().reset_index().sort_values(by='year')
        demand_counts.columns = ['year', 'protests_count']
        if chart_type == "Barplot":
            demand_chart = px.bar(demand_counts, x="year", y="protests_count", title=f"Protests with Demand: {demand}", labels={'protests_count': 'Protests Count'})
        else:
            demand_chart = px.line(demand_counts, x="year", y="protests_count", title=f"Protests with Demand: {demand}", labels={'protests_count': 'Protests Count'})
        st.plotly_chart(demand_chart)
        # Add download button for Demands data
        csv = demand_counts.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download Data for {demand}",
            data=csv,
            file_name=f'country_{demand}.csv',
            mime='text/csv',
        )
    elif tab == "Violence":
        state_violence = ['response_beatings', 'response_shootings', 'response_killings']
        violence_mapping = {
            0: 'Non Violent',
            1: 'Protester Violence',
            2: 'State Violence',
            3: 'Both Violence'
        }
        violence = st.selectbox("Select Violence Type", list(violence_mapping.values()))

        if violence == 'Non Violent':
            violence_data = country_data[country_data['protesterviolence'] == 0]
            title = "Protests with Non-Violent Protesters"
        elif violence == 'Protester Violence':
            violence_data = country_data[country_data['protesterviolence'] == 1]
            title = "Protests with Protester Violence"
        elif violence == 'State Violence':
            violence_data = country_data[country_data[state_violence].sum(axis=1) > 0]
            title = "Protests with State Violence"
        elif violence == 'Both Violence':
            violence_data = country_data[(country_data['protesterviolence'] == 1) & (country_data[state_violence].sum(axis=1) > 0)]
            title = "Protests with Both State and Protester Violence"

        violence_counts = violence_data.groupby('year').size().reset_index(name='protests_count').sort_values(by='year')
        if chart_type == "Barplot":
            violence_chart = px.bar(violence_counts, x="year", y="protests_count", title=title, labels={'protests_count': 'Protests Count'})
        else:
            violence_chart = px.line(violence_counts, x="year", y="protests_count", title=title, labels={'protests_count': 'Protests Count'})
        st.plotly_chart(violence_chart)
        # Add download button for Violence data
        csv = violence_counts.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download Data for {title}",
            data=csv,
            file_name=f'country_{title.replace(" ", "_").lower()}.csv',
            mime='text/csv',
        )
