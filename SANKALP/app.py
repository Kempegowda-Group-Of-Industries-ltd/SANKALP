import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Utility Functions
def calculate_emissions_industry(data):
    """
    Calculate total CO₂ emissions for industry-level data.
    """
    emissions = data['emission'].sum()  # Sum emissions column
    credits_required = emissions / 10  # Example: 1 credit offsets 10 kg of CO₂
    return emissions, credits_required

def calculate_emissions_common(activity_data):
    """
    Calculate emissions for common use cases.
    """
    emissions = 0
    if "transport" in activity_data:
        if activity_data["transport"]["type"] == "car":
            emissions += activity_data["transport"]["miles"] * 0.21  # CO₂ per mile
    if "energy" in activity_data:
        emissions += activity_data["energy"]["usage"] * 0.85  # CO₂ per kWh
    return emissions

def generate_sample_file():
    """
    Generate a sample CSV file for industry-level emissions input.
    """
    data = {
        "source": ["Factory A", "Factory B", "Factory C"],
        "emission": [1500, 2300, 1200]  # CO₂ in kg
    }
    df = pd.DataFrame(data)
    df.to_csv("sample_emissions.csv", index=False)
    return df

# Streamlit App
def main():
    st.title("SANKALP: Sustainability Actions for Nature")
    user_type = st.sidebar.radio("Select User Type", ["Industry Level", "Common Use"])
    
    if user_type == "Industry Level":
        st.header("Industry-Level Emission Tracking")
        st.write("Choose to input emissions data manually or upload a file.")
        
        option = st.selectbox("How would you like to input data?", ["Manual Input", "Upload File"])
        
        if option == "Manual Input":
            num_sources = st.number_input("Number of Emission Sources", min_value=1, max_value=10, step=1)
            emissions_data = []
            for i in range(num_sources):
                source = st.text_input(f"Source {i+1} Name", f"Source {i+1}")
                emission = st.number_input(f"CO₂ Emission for {source} (in kg)", min_value=0.0)
                emissions_data.append({"source": source, "emission": emission})
            if st.button("Calculate Total Emissions"):
                df = pd.DataFrame(emissions_data)
                total_emissions, credits_required = calculate_emissions_industry(df)
                st.write(f"Total Emissions: {total_emissions} kg")
                st.write(f"Carbon Credits Required: {credits_required} credits")
                st.bar_chart(df.set_index("source"))
        
        elif option == "Upload File":
            uploaded_file = st.file_uploader("Upload Emission Data File (CSV)", type=["csv"])
            if uploaded_file:
                data = pd.read_csv(uploaded_file)
                st.write("Uploaded Data:")
                st.write(data)
                total_emissions, credits_required = calculate_emissions_industry(data)
                st.write(f"Total Emissions: {total_emissions} kg")
                st.write(f"Carbon Credits Required: {credits_required} credits")
                st.bar_chart(data.set_index("source"))
        
        st.download_button("Download Sample File", data=generate_sample_file().to_csv(index=False), file_name="sample_emissions.csv")
    
    elif user_type == "Common Use":
        st.header("Common Use Carbon Footprint Tracker")
        st.subheader("Transportation Emissions")
        transport_type = st.selectbox("Transport Type", ["Car", "Bus", "Train"])
        miles = st.number_input("Miles traveled", min_value=0)
        
        st.subheader("Energy Usage")
        energy_usage = st.number_input("Energy Usage (kWh)", min_value=0)
        
        activity_data = {
            "transport": {"type": transport_type, "miles": miles},
            "energy": {"usage": energy_usage}
        }
        
        if st.button("Calculate CO₂ Emissions"):
            emissions = calculate_emissions_common(activity_data)
            credits_required = emissions / 10  # Example: 1 credit offsets 10 kg of CO₂
            st.write(f"Total CO₂ Emissions: {emissions} kg")
            st.write(f"Carbon Credits Required: {credits_required} credits")
            
            # Visualization
            chart_data = pd.DataFrame({
                "Activity": ["Transport", "Energy"],
                "CO₂ Emissions (kg)": [miles * 0.21, energy_usage * 0.85]
            })
            st.altair_chart(alt.Chart(chart_data).mark_bar().encode(
                x="Activity",
                y="CO₂ Emissions (kg)",
                color="Activity"
            ), use_container_width=True)

if __name__ == "__main__":
    main()
