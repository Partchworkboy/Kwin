import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import plotly.express as px
import db_dtypes 

# Set form title and configuration for page title
st.set_page_config(page_title="Kwin Stationers - The sky is a podium",
                   page_icon=":pencil2:",
                   layout="wide")

# Load Google Cloud Platform credentials from secrets.toml
secrets = st.secrets["gcp_service_account"]
project_id = secrets["project_id"]
credentials_dict = {
    "type": secrets["type"],
    "project_id": secrets["project_id"],
    "private_key_id": secrets["private_key_id"],
    "private_key": secrets["private_key"],
    "client_email": secrets["client_email"],
    "client_id": secrets["client_id"],
    "auth_uri": secrets["auth_uri"],
    "token_uri": secrets["token_uri"],
    "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["client_x509_cert_url"]
}

# Authenticate BigQuery client with GCP credentials
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
client = bigquery.Client(project=project_id, credentials=credentials)

# Define function to refresh tables
@st.cache(ttl=60*60)  # Set time-to-live to 1 hour
def refresh_tables():
    # Initialize tables
    sales_data = pd.DataFrame()
    incoming_inventory = pd.DataFrame()
    
    # Refresh tables every hour
    while True:
        query_sales = f"SELECT * FROM `{project_id}.sales.sales_data`"
        sales_data = client.query(query_sales).to_dataframe()
        
        query_inventory = f"SELECT * FROM `{project_id}.inventory.incoming_inventory`"
        incoming_inventory = client.query(query_inventory).to_dataframe()

        # Wait for an hour before refreshing tables
        time.sleep(3600)

# Set up BigQuery dataset and table names
dataset_name = "sales"
table_name = "sales_data"

# Query BigQuery table and display data in tabular format
query = f"SELECT * FROM `{project_id}.{dataset_name}.{table_name}`"
df = client.query(query).to_dataframe()
st.header("Sales Data")
st.table(df.style.set_table_styles([{'selector': 'th', 'props': [('background-color', '#4287f5'),('color','white')]}]))

# Set up BigQuery dataset and table names
dataset_name = "inventory"
table_name = "incoming_inventory"

# Query BigQuery table and display data in tabular format
query = f"SELECT * FROM `{project_id}.{dataset_name}.{table_name}`"
df = client.query(query).to_dataframe()
st.header("Purchase Data")
st.table(df.style.set_table_styles([{'selector': 'th', 'props': [('background-color', '#4287f5'),('color','white')]}]))

def generate_summary_statistics(df):
    summary = df.agg({
        "amount_charged": ["sum", "mean", "median", "max", "min"],
        "quantity": ["sum", "mean", "median", "max", "min"]
    })
    summary.columns = ["Total sales", "Average sale", "Median sale", "Highest sale", "Lowest sale",
                       "Total quantity sold", "Average quantity sold", "Median quantity sold",
                       "Highest quantity sold", "Lowest quantity sold"]
    summary = summary.T
    summary["Total sales"] = summary["Total sales"].apply(lambda x: f"${x:,.2f}")
    summary["Average sale"] = summary["Average sale"].apply(lambda x: f"${x:,.2f}")
    summary["Median sale"] = summary["Median sale"].apply(lambda x: f"${x:,.2f}")
    summary = summary.round(2)
    return summary

# Define function to generate summary table
def generate_summary_table(df):
    summary = generate_summary_statistics(df)
    st.write("## Summary Statistics")
    st.table(summary.style.format({"Total sales": "${:,.2f}", "Average sale": "${:,.2f}", "Median sale": "${:,.2f}"}))

# Define function to generate sales table
def generate_sales_table(df):
    st.write("## Sales Data")
    st.dataframe(df.style.format({"amount_charged": "${:,.2f}"}))

    
# Define function to generate purchase table
def generate_purchase_table(df):
    st.write("## Purchase Data")
    st.write(df)


# Add page footer
st.markdown("---")
st.write("© 2023 Kwin Stationers")

