import streamlit as st
import pandas as pd
import os

st.title("Redbus Data Dashboard")

# ----------- 1. Path to Redbus_data folder -----------
data_folder = r"C:\Users\USER\OneDrive\Desktop\red bus\Redbus_data\Redbus_data"

# ----------- 2. Load all CSV files -----------
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

if not csv_files:
    st.error(" No CSV files found in Redbus_data folder")
else:
    # Load and combine CSV files
    df_list = [pd.read_csv(os.path.join(data_folder, f)) for f in csv_files]
    df = pd.concat(df_list, ignore_index=True)

    # ----------- 3. Clean Column Names -----------
    df.columns = df.columns.str.strip().str.replace("_", " ").str.title()

    # ----------- 4. Ensure numeric columns are numeric -----------
    numeric_cols = ["Price", "Star Rating", "Seats Available"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ----------- 5. Ensure State column exists -----------
    if "State" not in df.columns:
        df["State"] = "Unknown"  # default placeholder; you can update later with correct values

    st.subheader("All Bus Details")
    st.dataframe(df)

    # ----------- 6. Filters -----------

    # Route Name Filter
    if "Route Name" in df.columns:
        route_options = df["Route Name"].dropna().unique().tolist()
        selected_route = st.multiselect("Select Route(s):", route_options, default=route_options)
    else:
        selected_route = []

    # Bus Type Filter
    if "Bus Type" in df.columns:
        bus_type_options = df["Bus Type"].dropna().unique().tolist()
        selected_bus_type = st.multiselect("Select Bus Type(s):", bus_type_options, default=bus_type_options)
    else:
        selected_bus_type = []

    # State Filter
    state_options = df["State"].dropna().unique().tolist()
    selected_state = st.multiselect("Select State(s):", state_options, default=state_options)

    # Price Range Filter
    if "Price" in df.columns:
        min_price = int(df["Price"].min())
        max_price = int(df["Price"].max())
        selected_price = st.slider("Price Range:", min_price, max_price, (min_price, max_price))
    else:
        selected_price = (0, 999999)

    # Star Rating Filter
    if "Star Rating" in df.columns:
        min_rating = float(df["Star Rating"].min())
        max_rating = float(df["Star Rating"].max())
        selected_rating = st.slider("Star Rating:", min_rating, max_rating, (min_rating, max_rating))
    else:
        selected_rating = (0, 5)

    # Seats Available Filter
    if "Seats Available" in df.columns:
        min_seats = int(df["Seats Available"].min())
        max_seats = int(df["Seats Available"].max())
        selected_seats = st.slider("Seats Available:", min_seats, max_seats, (min_seats, max_seats))
    else:
        selected_seats = (0, 60)

    # ----------- 7. Apply Filter Logic Safely -----------

    filtered_df = df.copy()

    if "Route Name" in df.columns and selected_route:
        filtered_df = filtered_df[filtered_df["Route Name"].isin(selected_route)]

    if "Bus Type" in df.columns and selected_bus_type:
        filtered_df = filtered_df[filtered_df["Bus Type"].isin(selected_bus_type)]

    if selected_state:
        filtered_df = filtered_df[filtered_df["State"].isin(selected_state)]

    if "Price" in df.columns:
        filtered_df = filtered_df[filtered_df["Price"].between(selected_price[0], selected_price[1])]

    if "Star Rating" in df.columns:
        filtered_df = filtered_df[filtered_df["Star Rating"].between(selected_rating[0], selected_rating[1])]

    if "Seats Available" in df.columns:
        filtered_df = filtered_df[filtered_df["Seats Available"].between(selected_seats[0], selected_seats[1])]

    # ----------- 8. Display Filtered Results -----------
    st.subheader(f"Filtered Buses ({len(filtered_df)} results)")
    st.dataframe(filtered_df)





