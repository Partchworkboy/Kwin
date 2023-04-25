import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime
import os

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

# Set up BigQuery dataset and table names
dataset_name = "inventory"
table_name = "incoming_inventory"

# Check if dataset exists, and create it if it doesn't
dataset_ref = client.dataset(dataset_name)
try:
    dataset = client.get_dataset(dataset_ref)
except:
    dataset = bigquery.Dataset(dataset_ref)
    dataset = client.create_dataset(dataset)

# Check if table exists, and create it if it doesn't
table_ref = dataset_ref.table(table_name)
try:
    table = client.get_table(table_ref)
except:
    table_schema = [
        bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("product_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("quantity", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("unit_cost", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("total_cost", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("supplier", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("notes", "STRING", mode="NULLABLE")
    ]
    table = bigquery.Table(table_ref, schema=table_schema)
    table = client.create_table(table)

# Define form fields
st.markdown("<h1 style='text-align: center;'> Kwin Stationers </h1>", unsafe_allow_html=True)
st.title("Incoming Inventory")
date = st.date_input("Date")
product_name = st.text_input("Product Name")
quantity = st.number_input("Quantity", min_value=1)
unit_cost = st.number_input("Unit Cost", min_value=0.0, step=0.01)
supplier = st.text_input("Supplier")
notes = st.text_input("Notes")

# Define submit button
if st.button("Submit"):
    # Calculate total cost
    total_cost = quantity * unit_cost

    # Insert form data into BigQuery table
    form_data = {
        "date": date,
        "product_name": product_name,
        "quantity": quantity,
        "unit_cost": unit_cost,
        "total_cost": total_cost,
        "supplier": supplier,
        "notes": notes
    }
    rows_to_insert = [form_data]
    errors = client.insert_rows(table, rows_to_insert)

    # Check for errors
    if errors == []:
        st.success("Form data inserted successfully.")
    else:
        st.error("Errors inserting form data: %s" % errors)


# Add page footer
st.markdown("---")
st.write("© 2023 Kwin Stationers")
