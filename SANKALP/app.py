import streamlit as st
import pandas as pd
import numpy as np

# --- Utility Functions ---
# Carbon footprint calculator function
def calculate_emissions(activity_data):
    emissions = 0
    if "transport" in activity_data:
        if activity_data["transport"]["type"] == "car":
            emissions += activity_data["transport"]["miles"] * 0.21  # CO₂ per mile for car
    if "energy" in activity_data:
        emissions += activity_data["energy"]["usage"] * 0.85  # CO₂ per kWh for average household energy use
    return emissions

# Carbon credit trading function
def trade_credits(user_id, farmer_id, credits, price):
    # This is a simplified mock of trading carbon credits
    # In real use, this would involve database updates or API calls
    user_balance = get_user_balance(user_id)
    farmer_balance = get_farmer_balance(farmer_id)
    if user_balance >= credits * price:
        # Deduct user credits and add to farmer's balance
        update_user_credits(user_id, -credits * price)
        update_farmer_credits(farmer_id, credits)
        return True
    return False

def get_user_balance(user_id):
    # Mock balance for the user
    return 100  # Let's assume the user has 100 units of currency

def get_farmer_balance(farmer_id):
    # Mock balance for the farmer
    return 50  # Let's assume the farmer has 50 credits

def update_user_credits(user_id, amount):
    # Update user credits
    pass  # In real implementation, this would update the database

def update_farmer_credits(farmer_id, amount):
    # Update farmer credits
    pass  # In real implementation, this would update the database

# --- Streamlit App ---
def main():
    st.title("SANKALP: Sustainability Actions for Nature")
    
    nav = st.sidebar.radio("Navigate", ["Home", "Tracker", "Marketplace", "Dashboard", "Education"])
    
    # Home Page
    if nav == "Home":
        st.image("https://via.placeholder.com/800x400.png", use_column_width=True)
        st.write("Welcome to SANKALP, your one-stop solution for sustainability actions!")
    
    # Tracker Page
    elif nav == "Tracker":
        st.header("Log Your Sustainability Actions")
        st.subheader("Transport Emissions")
        
        transport_type = st.selectbox("Transport Type", ["Car", "Bus", "Train"])
        miles = st.number_input("Miles traveled", min_value=0)
        
        activity_data = {"transport": {"type": transport_type, "miles": miles}}
        if st.button("Calculate CO₂ Emissions"):
            emissions = calculate_emissions(activity_data)
            st.write(f"Total CO₂ Emissions: {emissions} kg")
        
        # Add energy, waste, and other categories similarly here

    # Marketplace Page
    elif nav == "Marketplace":
        st.header("Carbon Credit Marketplace")
        st.write("Here, you can buy carbon credits from local farmers.")
        
        # Display farmer data from a CSV or database
        farmers = pd.read_csv("farmers_data.csv")  # This is a placeholder file
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

    # Dashboard Page
    elif nav == "Dashboard":
        st.header("Your Impact Dashboard")
        st.write("Track your sustainability efforts here.")
        
        st.write("Total CO₂ Saved: 1000 kg")  # Mock data
        st.write("Total Carbon Credits Purchased: 20 credits")  # Mock data

    # Education Page
    elif nav == "Education":
        st.header("Learn and Act")
        st.write("Explore articles, videos, and resources on sustainability.")
        st.write("Here are some important topics you can learn about:")
        st.write("- Renewable Energy")
        st.write("- Waste Management")
        st.write("- Sustainable Agriculture")
        st.write("- Climate Change Awareness")

if __name__ == "__main__":
    main()
