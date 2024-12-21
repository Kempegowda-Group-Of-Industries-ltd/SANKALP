import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# --- Utility Functions ---
def calculate_emissions_common(activity_data):
    emissions = 0
    if "transport" in activity_data:
        if activity_data["transport"]["type"] == "car":
            emissions += activity_data["transport"]["miles"] * 0.21  # CO₂ per mile
    if "energy" in activity_data:
        emissions += activity_data["energy"]["usage"] * 0.85  # CO₂ per kWh
    return emissions

def calculate_emissions_industry(data):
    emissions = data['emission'].sum()  # Sum emissions column
    credits_required = emissions / 10  # Example: 1 credit offsets 10 kg of CO₂
    return emissions, credits_required

def generate_sample_file():
    data = {
        "source": ["Factory A", "Factory B", "Factory C"],
        "emission": [1500, 2300, 1200]  # CO₂ in kg
    }
    df = pd.DataFrame(data)
    df.to_csv("sample_emissions.csv", index=False)
    return df

def trade_credits(user_id, farmer_id, credits, price):
    user_balance = get_user_balance(user_id)
    farmer_balance = get_farmer_balance(farmer_id)
    if user_balance >= credits * price:
        update_user_credits(user_id, -credits * price)
        update_farmer_credits(farmer_id, credits)
        return True
    return False

def get_user_balance(user_id):
    return 100  # Mock user balance

def get_farmer_balance(farmer_id):
    return 50  # Mock farmer balance

def update_user_credits(user_id, amount):
    pass  # Placeholder for database update

def update_farmer_credits(farmer_id, amount):
    pass  # Placeholder for database update

# --- Streamlit App ---
def main():
    st.title("SANKALP: Sustainability Actions for Nature")
    nav = st.sidebar.radio("Navigate", ["Home", "Tracker", "Marketplace", "Dashboard", "Education"])

    if nav == "Home":
        st.image("https://via.placeholder.com/800x400.png", use_container_width=True)
        st.write("Welcome to SANKALP, your one-stop solution for sustainability actions!")

    elif nav == "Tracker":
        st.header("Log Your Sustainability Actions")
        user_type = st.radio("Select User Type", ["Industry Level", "Common Use"])

        if user_type == "Industry Level":
            st.subheader("Industry-Level Emission Tracking")
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
            st.subheader("Common Use Carbon Footprint Tracker")
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
                
                chart_data = pd.DataFrame({
                    "Activity": ["Transport", "Energy"],
                    "CO₂ Emissions (kg)": [miles * 0.21, energy_usage * 0.85]
                })
                st.altair_chart(alt.Chart(chart_data).mark_bar().encode(
                    x="Activity",
                    y="CO₂ Emissions (kg)",
                    color="Activity"
                ), use_container_width=True)

    elif nav == "Marketplace":
        st.header("Carbon Credit Marketplace")
        try:
            farmers = pd.read_csv("farmers_data.csv")  # Ensure this file exists
        except FileNotFoundError:
            st.error("Farmers data file not found.")
            return
        farmer_id = st.selectbox("Select Farmer", farmers['farmer_name'])
        credits_available = farmers.loc[farmers['farmer_name'] == farmer_id, 'credits'].values[0]
        price_per_credit = farmers.loc[farmers['farmer_name'] == farmer_id, 'price_per_credit'].values[0]
        st.write(f"Credits available: {credits_available}")
        st.write(f"Price per credit: ₹{price_per_credit}")
        
        credits_to_trade = st.number_input("Credits to purchase", min_value=1, max_value=credits_available)
        if st.button("Trade Carbon Credits"):
            user_id = 1  # Mock user ID
            if trade_credits(user_id, farmer_id, credits_to_trade, price_per_credit):
                st.success("Credits successfully traded!")
            else:
                st.error("Insufficient balance or invalid trade.")

    elif nav == "Dashboard":
        st.header("Your Impact Dashboard")
        st.write("Total CO₂ Saved: 1000 kg")  # Mock data
        st.write("Total Carbon Credits Purchased: 20 credits")  # Mock data

    elif nav == "Education":
        st.header("Learn and Act")
        st.write("Explore articles, videos, and resources on sustainability.")
        st.write("- Renewable Energy")
        st.write("- Waste Management")
        st.write("- Sustainable Agriculture")
        st.write("- Climate Change Awareness")

if __name__ == "__main__":
    main()
