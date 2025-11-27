import io
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Redbus Data Dashboard", layout='wide')
st.title("Redbus Data Dashboard")

# ----------- 1. Path to inner Redbus_data folder -----------
data_folder = r"C:\Users\USER\OneDrive\Desktop\red bus\Redbus_data\Redbus_data"

# ----------- 2. Load all CSV files -----------
@st.cache_data(ttl=60*60)
def load_all_csvs(dir_path: str) -> pd.DataFrame:
    if not os.path.isdir(dir_path):
        return pd.DataFrame()
    csv_files = [f for f in os.listdir(dir_path) if f.lower().endswith('.csv')]
    if not csv_files:
        return pd.DataFrame()
    dfs = []
    for f in csv_files:
        p = os.path.join(dir_path, f)
        try:
            df_local = pd.read_csv(p)
        except Exception:
            df_local = pd.read_csv(p, encoding='latin-1')
        dfs.append(df_local)
    return pd.concat(dfs, ignore_index=True)


df = load_all_csvs(data_folder)

if df.empty:
    st.error("No CSV files found or no data loaded in Redbus_data folder")
else:
    st.sidebar.header("Filters")
    # Refresh button to clear cached data and reload
    if st.sidebar.button('Refresh data'):
        st.cache_data.clear()
        st.experimental_rerun()

    st.subheader("All Bus Details")

    # ----------- 4. Filters -----------

    # Filter by Route Name (sidebar)
    if 'Route Name' in df.columns:
        route_options = sorted(df['Route Name'].dropna().unique().tolist())
        selected_route = st.sidebar.multiselect("Select Route(s):", options=route_options, default=route_options)
    else:
        route_options = []
        selected_route = []

    # Filter by Bus Type (sidebar)
    if 'Bus Type' in df.columns:
        bus_type_options = sorted(df['Bus Type'].dropna().unique().tolist())
        selected_bus_type = st.sidebar.multiselect("Select Bus Type(s):", options=bus_type_options, default=bus_type_options)
    else:
        bus_type_options = []
        selected_bus_type = []

    # Filter by Price Range (convert to numeric safely)
    if 'Price' in df.columns:
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        valid_prices = df['Price'].dropna()
        if not valid_prices.empty:
            min_price = int(valid_prices.min())
            max_price = int(valid_prices.max())
            selected_price = st.sidebar.slider("Select Price Range", min_price, max_price, (min_price, max_price))
        else:
            selected_price = (0, 0)
    else:
        selected_price = (0, 0)

    # ----------- 5. Apply all filters together -----------
    filtered_df = df.copy()
    if selected_route:
        filtered_df = filtered_df[filtered_df['Route Name'].isin(selected_route)]
    if selected_bus_type:
        filtered_df = filtered_df[filtered_df['Bus Type'].isin(selected_bus_type)]
    if 'Price' in filtered_df.columns and filtered_df['Price'].dtype.kind in 'biufc':
        filtered_df = filtered_df[filtered_df['Price'].between(selected_price[0], selected_price[1])]

    # KPI cards (showing overall and filtered stats)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    total_routes = df['Route Name'].nunique() if 'Route Name' in df.columns else 0
    total_buses = len(df)
    avg_price = float(df['Price'].mean()) if 'Price' in df.columns and not df['Price'].dropna().empty else 0
    total_bus_types = df['Bus Type'].nunique() if 'Bus Type' in df.columns else 0
    kpi1.metric('Total Routes', total_routes)
    kpi2.metric('Total Buses', total_buses)
    kpi3.metric('Avg Price', f"{avg_price:.2f}")
    kpi4.metric('Bus Types', total_bus_types)

    st.subheader(f"Filtered Buses ({len(filtered_df)} results)")
    # Download filtered results as CSV
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Filtered Results', csv_bytes, file_name='filtered_buses.csv', mime='text/csv')
    st.dataframe(filtered_df)

    # Sidebar options for visuals
    show_visuals = st.sidebar.checkbox('Show visuals', value=True)
    remove_duplicates = st.sidebar.checkbox('Remove duplicate rows (Route + Bus + Link)', value=True)

    display_df = filtered_df.copy()
    if remove_duplicates:
        if all(c in display_df.columns for c in ['Route Name', 'Bus Name', 'Route Link']):
            display_df = display_df.drop_duplicates(subset=['Route Name', 'Bus Name', 'Route Link'])

    # Optional visualizations
    if show_visuals:
        # Price Distribution
        if 'Price' in display_df.columns and display_df['Price'].dtype.kind in 'biufc':
            st.subheader('Price Distribution')
            fig, ax = plt.subplots()
            sns.histplot(display_df['Price'].dropna(), bins=30, ax=ax)
            ax.set_xlabel('Price')
            st.pyplot(fig)

        # Top 10 Routes by number of buses
        if 'Route Name' in display_df.columns:
            st.subheader('Top 10 Routes')
            top_routes = display_df['Route Name'].value_counts().nlargest(10)
            fig2, ax2 = plt.subplots()
            sns.barplot(x=top_routes.values, y=top_routes.index, ax=ax2)
            ax2.set_xlabel('Number of entries')
            ax2.set_ylabel('Route Name')
            st.pyplot(fig2)

        # Boxplot of Price by Bus Type
        if 'Price' in display_df.columns and 'Bus Type' in display_df.columns:
            st.subheader('Price by Bus Type')
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=display_df, x='Bus Type', y='Price', ax=ax3)
            ax3.set_xlabel('Bus Type')
            ax3.set_ylabel('Price')
            plt.xticks(rotation=45)
            st.pyplot(fig3)
