# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
from PIL import Image

# layout
st.set_page_config(layout="wide")

st.markdown(""" 
<style>
    /* above the header */
    [data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
    }
    
    /* central part */
    [data-testid="stAppViewContainer"] {
    background-color: white;
    }

    /* sidebar*/
    [data-testid="stSidebar"] {
    background-color: #B01AA7;
    }

    /* streamlit buttons*/
        /* arrow + 3 lines*/
    .css-fblp2m{
        color:#B01AA7 !important;
    }
    .css-fblp2m:hover{
        color:#31333F !important;
    }
        /* cross*/
    section[data-testid="stSidebar"] .css-fblp2m{
        color:white !important;
    }
    section[data-testid="stSidebar"] .css-fblp2m:hover{
        color:#31333F !important;
    }

    /* Titles*/
    .css-10trblm {
    color:#B04AA7;
    }
    /* Streamlit link*/
    .css-1vbd788 {
    color:#31333F !important;
    text-decoration-line:underline;
    }
    .css-1vbd788:hover {
    color:#B04AA7 !important;
    }

    /* Links*/
    a {
    color:white !important;
    }
    a:hover {
    color:#46B1C9 !important;
    }

    /* buttons */
    .css-10y5sf6 {
    color: rgb(176, 26, 167);
    }
    
    .css-1vzeuhh {
    background-color: rgb(176, 26, 167);
    }
    
</style>       
""",unsafe_allow_html=True)

# banner
image = Image.open("https://github.com/delphinecesar/Bloc-5/blob/main/DASHBOARD/banner.png")    
st.image(image)

# load dataset
dataset_clean = pd.read_csv('dataset_clean.csv')
dataset_join = pd.read_csv('dataset_join.csv')
dataset_join_clean = pd.read_csv('dataset_join_clean.csv')

# Title
st.title("🚙 Dashboard")

st.markdown("""
Welcome to the getaround Streamlit dashboard, designed to provide valuable data insights and help making informed decisions for this car rental platform. 
With this tool, the team can analyze key metrics, understand the impact of rental delays for both car owners and renters.
""")

# General analysis
st.subheader("General analysis")

st.markdown("""
Let's start by reviewing the basic information of the dataset.
""")
_, col1, col2, _= st.columns([1,2,2,1])
with col1:
    rentals_nb = len(dataset_clean)
    st.metric("Number of car rentals:", rentals_nb)

with col2:
    cars_nb = str(dataset_clean['car_id'].nunique())
    st.metric("Number of cars rented:", cars_nb)

col1, col2, col3 = st.columns(3)
with col1:
    fig = px.pie(dataset_clean, 
        names='checkin_type', 
        title= 'Repartition by checkin type', 
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4)
    fig.update_traces(
        textposition = 'inside',
        textfont_size = 14,
        textinfo = 'percent+label',
        showlegend = False)
    st.plotly_chart(fig, theme=None, use_container_width=True) 

with col2:
    fig = px.pie(dataset_clean[dataset_clean['checkin_type'] == 'mobile'],
        names='state', 
        title= 'Mobile checkin', 
        color_discrete_sequence=px.colors.qualitative.Set2[2:],
        hole=.4)
    fig.update_traces(
        textposition = 'inside', 
        textfont_size = 14,
        textinfo = 'percent+label',
        showlegend = False)
    st.plotly_chart(fig, theme=None, use_container_width=True)

with col3:
    fig = px.pie(dataset_clean[dataset_clean['checkin_type'] == 'connect'],
        names='state', 
        title= 'Connect checkin',
        color_discrete_sequence=px.colors.qualitative.Set2[2:], 
        hole=.4)
    fig.update_traces(
        textposition = 'inside', 
        textfont_size = 14,
        textinfo = 'percent+label',
        showlegend = False)
    st.plotly_chart(fig, theme=None, use_container_width=True)

st.write("""
There are far more "mobile" than "connect" cars, and only a few are equipped with the connect system. 
We can see that there is a relatively higher proportion of canceled rentals for "connect" cars.
""")
         
st.markdown("""
    ------------------------
    """)
         
# Delay analysis
st.subheader("Delay analysis")

st.write("""
Now let's see how many cars are returned late.
""")

col1, col2 = st.columns(2)
with col1:
    fig = px.pie(dataset_clean, 
        names='delay', 
        title= 'Check-out timing', 
        color_discrete_sequence=px.colors.qualitative.Set2[3:],
        hole=.4)
    fig.update_traces(
        textposition = 'inside', 
        textfont_size = 14,
        textinfo = 'percent+label',
        showlegend = False)
    st.plotly_chart(fig, theme=None, use_container_width=True) 

with col2:
    dataset_delay = dataset_clean[(dataset_clean["delay_range"] != "On time") & (dataset_clean["delay_range"] != "Unknown")]
        
    cat_order = ["Up to 30min late", "30min to 1h late", "1h to 1h30 late",
             "1h30 to 2h late", "2h to 2h30 late", "2h30 to 3h late", "Above 3h late"]

    delay = dataset_delay["delay_range"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delay.index, y=delay.values))
    fig.update_layout(title="Delay analysis", 
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[3:])
    st.plotly_chart(fig, theme=None, use_container_width=True)

_, col1, col2, _= st.columns([1,2,2,1])
with col1:
    median_all_cars = dataset_delay["delay_at_checkout_in_minutes"].median()
    st.metric("Median delay for all late cars (in min):", median_all_cars)

with col2:
    median_connect_cars = dataset_delay[dataset_delay["checkin_type"] == "connect"]["delay_at_checkout_in_minutes"].median()
    st.metric('Median delay for late "connect" cars (in min):', median_connect_cars)

st.write("""
Almost half of all rentals are returned late by their drivers. The majority of delays are less than 1 hour.
""")

st.markdown("""
    ------------------------
    """)

# Successive rentals
st.subheader("Focus on successive rentals")

st.write("""
Now that we've seen that many cars are returned late, let's take a look at successive rentals. 
This means rentals involving cars that were rented less than 12 hours previously.
""")
         
_, col1, col2, _= st.columns([1,2,2,1])
with col1:
    successive_rentals = len(dataset_join)    
    st.metric("Number of successive rentals:", successive_rentals)

with col2:
    successive_rentals_part = round((successive_rentals*100)/rentals_nb,2)
    st.metric("% of succesive rentals:", successive_rentals_part)


col1, col2 = st.columns(2)  
with col1:
    labels = ["Unique", "Successive"]
    values = [19469, 1841]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)]) 
    fig.update_layout(
        title="Type of rentals",
        colorway=px.colors.qualitative.Set2,
        )
    fig.update_traces(
        textposition='inside', 
        textfont_size = 14,
        insidetextorientation='radial',
        textinfo='percent+label',
        showlegend=False
        )
    st.plotly_chart(fig, theme=None, use_container_width=True) 

with col2:
    cat_order = ["Up to 30min", "30min to 1h", "1h to 1h30", "1h30 to 2h", "2h to 2h30", "2h30 to 3h", "Above 3h"]

    delta = dataset_join_clean["time_delta_with_previous_rental_in_minutes_t"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delta.index, y=delta.values))
    fig.update_layout(title="Time delta with previous rental", 
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[1:])
    st.plotly_chart(fig, theme=None, use_container_width=True)

st.markdown("""
    ------------------------
    """)

# Late checkout impact
st.subheader("Late checkout impact on the rental process")

st.markdown("""In order to ensure data integrity, a total of 112 rentals were excluded from the analysis due to missing data. 
            These rentals were removed because it was not possible to determine whether they were impacted or not.
              \n
            "Impacted" means that the car was returned late by the previous driver.""")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1: 
    cat_order = ["Impacted", "Not impacted"]

    delta1 = dataset_join_clean[dataset_join_clean["time_delta_with_previous_rental_in_minutes_t"] == "Up to 30min"]
    delta1_repart = delta1["delay_status"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delta1_repart.index, y=delta1_repart.values))
    fig.update_layout(title="Up to 30min delta",
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[2:])
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        showlegend=False
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)

with col2:
    delta2 = dataset_join_clean[dataset_join_clean["time_delta_with_previous_rental_in_minutes_t"] == "30min to 1h"]
    delta2_repart = delta2["delay_status"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delta2_repart.index, y=delta2_repart.values))
    fig.update_layout(title="30min to 1h delta",
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[3:])
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        showlegend=False
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)

with col3:
    delta3 = dataset_join_clean[dataset_join_clean["time_delta_with_previous_rental_in_minutes_t"] == "1h to 1h30"]
    delta3_repart = delta3["delay_status"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delta3_repart.index, y=delta3_repart.values))
    fig.update_layout(title="1h to 1h30 delta",
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[4:])
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        showlegend=False
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)

with col4:
    delta4 = dataset_join_clean[dataset_join_clean["time_delta_with_previous_rental_in_minutes_t"] == "1h30 to 2h"]
    delta4_repart = delta4["delay_status"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delta4_repart.index, y=delta4_repart.values))
    fig.update_layout(title="1h30 to 2h delta",
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[5:])
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        showlegend=False
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)

with col5:
    delta5 = dataset_join_clean[dataset_join_clean["time_delta_with_previous_rental_in_minutes_t"] == "2h to 2h30"]
    delta5_repart = delta5["delay_status"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delta5_repart.index, y=delta5_repart.values))
    fig.update_layout(title="2h to 2h30 delta",
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[6:])
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        showlegend=False
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)

with col6:
    delta6 = dataset_join_clean[dataset_join_clean["time_delta_with_previous_rental_in_minutes_t"] == "2h30 to 3h"]
    delta6_repart = delta6["delay_status"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delta6_repart.index, y=delta6_repart.values))
    fig.update_layout(title="2h30 to 3h delta",
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[7:])
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        showlegend=False
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)

with col7:
    delta7 = dataset_join_clean[dataset_join_clean["time_delta_with_previous_rental_in_minutes_t"] == "Above 3h"]
    delta7_repart = delta7["delay_status"].value_counts().loc[cat_order]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=delta7_repart.index, y=delta7_repart.values))
    fig.update_layout(title="Above 3h delta",
                      title_x =0.5,
                      colorway=px.colors.qualitative.Set2[8:])
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(title=""),
        showlegend=False
    )
    st.plotly_chart(fig, theme=None, use_container_width=True)

_, col1, col2, col3, _ = st.columns([1,2,2,2,1])

with col1:
    impacted_rentals = dataset_join_clean["delay_status"].value_counts()["Impacted"]
    st.metric("Number of impacted successive rentals:", impacted_rentals)

with col2:
    impacted_rentals_percentage = round((impacted_rentals*100)/successive_rentals,2)
    st.metric("% of impacted successive rentals:", impacted_rentals_percentage)

with col3:
    impacted_all_rentals_percentage = round((impacted_rentals*100)/rentals_nb,2)
    st.metric("% of impacted rentals (among all rentals):", impacted_all_rentals_percentage)

st.markdown("""
    ------------------------
    """)

# Focus on impacted successive rentals
st.subheader("Focus on impacted successive rentals")

_, col1, col2, _ = st.columns([1,2,2,1])
with col1:
    fig = px.pie(dataset_join_clean[dataset_join_clean["delay_status"] == "Not impacted"], 
        names='state', 
        title= 'Rental state for impacted cars', 
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4)
    fig.update_traces(
        textposition = 'inside',
        textfont_size = 14,
        textinfo = 'percent+label',
        showlegend = False)
    st.plotly_chart(fig, theme=None, use_container_width=True)

with col2:
    fig = px.pie(dataset_join_clean[dataset_join_clean["delay_status"] == "Impacted"], 
        names='state', 
        title= 'Rental state for impacted cars', 
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4)
    fig.update_traces(
        textposition = 'inside',
        textfont_size = 14,
        textinfo = 'percent+label',
        showlegend = False)
    st.plotly_chart(fig, theme=None, use_container_width=True)

_, col1, _, col2, _ = st.columns([3,2,1,2,2])
with col1:
    dataset_join_clean_notimpacted = dataset_join_clean[dataset_join_clean["delay_status"] == "Not impacted"]
    not_impacted_cancel = dataset_join_clean_notimpacted["state"].value_counts()["canceled"]
    st.metric("Number of canceled rentals:", not_impacted_cancel)

with col2:
    dataset_join_clean_impacted = dataset_join_clean[dataset_join_clean["delay_status"] == "Impacted"]
    impacted_cancel = dataset_join_clean_impacted["state"].value_counts()["canceled"]
    st.metric("Number of canceled rentals:", impacted_cancel)

st.markdown("""We can see that a higher proportion of rentals affected by delays have been canceled. 
            However, to know whether these rentals were really cancelled because of this, we would need more 
            information, such as the time of cancelation.
            """)

st.markdown("""
    ------------------------
    """)

# Decision-making tool
st.subheader("Decision-making tool")

st.markdown("""In conclusion, for the time being, the number of successive rentals remains fairly low, 
            so it may not be worth setting a threshold between two rentals. However, if the business grows in the future, 
            it could be worthwhile. The tool below will help the Product Manager to make the best decision.
            """)

def resolved_rentals(threshold, scope):
    if scope == "connect":
        connect_late_rentals = dataset_clean[(dataset_clean["delay_at_checkout_in_minutes"] > 0) & (dataset_clean["checkin_type"] == "connect")]
        connect_solved_rentals = connect_late_rentals[connect_late_rentals["delay_at_checkout_in_minutes"] <= threshold] 
        percentage = round((len(connect_solved_rentals) / len(connect_late_rentals)) * 100, 2)
        return percentage
    else:
        late_rentals = dataset_clean[dataset_clean["delay_at_checkout_in_minutes"] > 0]
        solved_rentals = late_rentals[late_rentals["delay_at_checkout_in_minutes"] <= threshold]
        percentage = round((len(solved_rentals) / len(late_rentals)) * 100, 2)
        return percentage
    
_, col1, _, col2, _  = st.columns([1,2,1,2,1])

with col1:
    threshold = st.slider(
        'Select a threshold (in minutes):',
        min_value=0,
        max_value=720, 
        step=30)

with col2:
    scope = st.radio(
        'On which cars do you want to apply the feature?',
        ('connect', 'all'))

result = resolved_rentals(threshold, scope)
st.markdown(f"<p style='text-align: center; font-size: 18px'>If a <strong>{threshold}-minute</strong> threshold is set, <strong>{result}%</strong> of <strong>{scope}</strong> problematic rentals will be solved</p>", unsafe_allow_html=True)
