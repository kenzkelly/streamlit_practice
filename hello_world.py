import streamlit as st
import json
import numpy as np
import requests

def generate_json(personality_traits_values):
    data = {"Openness": personality_traits_values[0],
            "Conscientious": personality_traits_values[1],
            "Extraversion": personality_traits_values[2],
            "Agreeable": personality_traits_values[3],
            "Neuroticism": personality_traits_values[4]
            }
    return json.dumps(data)


def main():
    st.title("O.C.E.A.N.S. Job Finder")

    # Initialize slider values
    personality_traits_values = [0, 0, 0, 0, 0]

    # Create sliders for each personality trait
    for i, trait in enumerate(["Openness", "Conscientious", "Extraversion", "Agreeable", "Neuroticism"]):
        personality_traits_values[i] = st.slider(f"{trait}", 0, 5, 0)

    # Generate and display JSON based on slider values
    json_data = generate_json(personality_traits_values)
    st.subheader("Generated JSON:")
    st.code(json_data, language="json")

    # Plot bar chart based on user input
    #st.subheader("User Input Visualization:")
    #plot_bar_chart(personality_traits_values)
    # send to chalice 
    #st.json(json_data)


    if st.button("Submit"):
        api_endpoint = "https://kenzkelly.pythonanywhere.com"
        response = requests.post(api_endpoint,json = json_data)
        if response.status_code == 200: 
            st.success(response.content)
        else: 
            st.error(str(response.status_code))

if __name__ == "__main__":
    main()