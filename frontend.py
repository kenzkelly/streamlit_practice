import streamlit as st
import json
import numpy as np
import plotly.graph_objects as go
import requests

def generate_json(personality_traits_values):
    data = {
        "Openness": personality_traits_values[0],
        "Conscientious": personality_traits_values[1],
        "Extraversion": personality_traits_values[2],
        "Agreeable": personality_traits_values[3],
        "Neuroticism": personality_traits_values[4]
    }
    return json.dumps(data)

@st.cache(allow_output_mutation=True)
def make_radar_chart(json_data, n_clusters):
    fig = go.Figure()
    cmap = [(31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40), (148, 103, 189)]  # List of RGB tuples
    angles = list(json_data.keys())
    angles.append(angles[0])
    
    data = list(json_data.values())
    data.append(data[0])
    for i in range(n_clusters):
        fig.add_trace(go.Scatterpolar(
            r=data,
            theta=angles,
            mode='lines',
            line_color=f'rgba{tuple(cmap[i % len(cmap)] + (255,))}',
            name="User Input"))

    fig.update_layout(
        yaxis_range = [0,5],
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[1, 5])  # Adjusted range to match the sliders (1-5)
            ),
        showlegend=True
    )
    fig.update_traces()
    return fig

def main():
    st.title("O.C.E.A.N.S. Job Finder")

    # Initialize slider values
    personality_traits_values = [0, 0, 0, 0, 0]

    # Create sliders for each personality trait
    for i, trait in enumerate(["Openness", "Conscientious", "Extraversion", "Agreeable", "Neuroticism"]):
        personality_traits_values[i] = st.slider(f"{trait}", 0, 5, 0)  # Adjusted range to match sliders (1-5)

    # Generate and display JSON based on slider values
    json_data = generate_json(personality_traits_values)
    st.subheader("Generated JSON:")
    st.code(json_data, language="json")

    # Plot radar chart based on user input
    st.subheader("User Input Visualization:")
    radar_chart = make_radar_chart(json.loads(json_data), 1)  # Assuming 1 cluster for user input
    st.plotly_chart(radar_chart)

    if st.button("Submit"):
        api_endpoint = "https://kenzkelly.pythonanywhere.com/"
        response = requests.post(api_endpoint, json=json_data)
        
        if response.status_code == 200: 
            response_json = response.json()
            # Assuming the output is a list of dictionaries
            
            if isinstance(response_json, list):
                st.subheader("Output as Bar Chart:")
                similarity_scores = [d[1] for d in response_json]
                job_titles = [d[0] for d in response_json]
                
                # Create a Plotly bar chart
                fig = go.Figure([go.Bar(x=job_titles, y=similarity_scores)])
                fig.update_layout(
                    xaxis_title="Job Titles",
                    yaxis_title="Similarity Score",
                    title="Job Recommendations Based on Similarity"
                )
                st.plotly_chart(fig)
            else:
                st.error("The output format is not a list of dictionaries.")
            
        else: 
            st.error(f"Request failed with status code: {response.status_code}")

if __name__ == "__main__":
    main()
