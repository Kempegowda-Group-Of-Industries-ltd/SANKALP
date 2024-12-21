import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud
import io

# --- Utility Functions ---
def calculate_emissions_industry(data):
    emissions = data['emission'].sum()  # Sum emissions column
    credits_required = emissions / 10  # Example: 1 credit offsets 10 kg of CO₂
    return emissions, credits_required

def calculate_emissions_common(activity_data):
    emissions = 0
    if "transport" in activity_data:
        if activity_data["transport"]["type"] == "car":
            emissions += activity_data["transport"]["miles"] * 0.21  # CO₂ per mile
    if "energy" in activity_data:
        emissions += activity_data["energy"]["usage"] * 0.85  # CO₂ per kWh
    return emissions

def generate_sample_file():
    data = {"source": ["Factory A", "Factory B", "Factory C"], "emission": [1500, 2300, 1200]}
    df = pd.DataFrame(data)
    return df

def display_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    buffer = io.BytesIO()
    wordcloud.to_image().save(buffer, format="PNG")
    st.image(buffer.getvalue(), use_column_width=True)

# --- Streamlit App ---
def main():
    st.title("🌍 SANSRA SANKALP: Sustainability Actions for Nature 🌱")
    st.sidebar.title("Menu")
    user_type = st.sidebar.radio("Select User Type", ["Industry Level", "Common Use"])

    if user_type == "Industry Level":
        st.header("🏭 Industry-Level Emission Tracking")
        st.write("Choose to input emissions data manually or upload a file.")
        option = st.selectbox("Input Method", ["Manual Input", "Upload File"])

        if option == "Manual Input":
            num_sources = st.number_input("Number of Sources", min_value=1, max_value=10, step=1)
            emissions_data = [{"source": f"Source {i+1}", "emission": st.number_input(f"CO₂ Emission for Source {i+1} (in kg)", min_value=0.0)} for i in range(num_sources)]

            if st.button("Calculate Emissions"):
                df = pd.DataFrame(emissions_data)
                total_emissions, credits_required = calculate_emissions_industry(df)
                st.write(f"🌟 Total Emissions: **{total_emissions} kg**")
                st.write(f"🌟 Carbon Credits Required: **{credits_required} credits**")

                chart = alt.Chart(df).mark_bar().encode(x='source', y='emission', color='source')
                st.altair_chart(chart, use_container_width=True)

        elif option == "Upload File":
            uploaded_file = st.file_uploader("Upload Emission Data File (CSV)", type=["csv"])
            if uploaded_file:
                data = pd.read_csv(uploaded_file)
                st.write("### Uploaded Data:")
                st.write(data)
                total_emissions, credits_required = calculate_emissions_industry(data)
                st.write(f"🌟 Total Emissions: **{total_emissions} kg**")
                st.write(f"🌟 Carbon Credits Required: **{credits_required} credits**")

                chart = alt.Chart(data).mark_bar().encode(x='source', y='emission', color='source')
                st.altair_chart(chart, use_container_width=True)

        sample_file = generate_sample_file()
        st.download_button("📥 Download Sample File", data=sample_file.to_csv(index=False), file_name="sample_emissions.csv")

    elif user_type == "Common Use":
        st.header("🏡 Common Use Carbon Footprint Tracker")
        transport_type = st.selectbox("Transport Type", ["Car", "Bus", "Train"])
        miles = st.number_input("Miles Traveled", min_value=0)
        energy_usage = st.number_input("Energy Usage (kWh)", min_value=0)

        activity_data = {"transport": {"type": transport_type, "miles": miles}, "energy": {"usage": energy_usage}}

        if st.button("Calculate CO₂ Emissions"):
            emissions = calculate_emissions_common(activity_data)
            credits_required = emissions / 10
            st.write(f"🌟 Total CO₂ Emissions: **{emissions} kg**")
            st.write(f"🌟 Carbon Credits Required: **{credits_required} credits**")

            chart_data = pd.DataFrame({"Activity": ["Transport", "Energy"], "CO₂ Emissions (kg)": [miles * 0.21, energy_usage * 0.85]})
            chart = alt.Chart(chart_data).mark_bar().encode(x='Activity', y='CO₂ Emissions (kg)', color='Activity')
            st.altair_chart(chart, use_container_width=True)

        st.write("### Word Cloud of Sustainable Actions")
        display_wordcloud("Transportation Energy Recycling Sustainability Climate Change Green")

if __name__ == "__main__":
    main()
