import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime
import os

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
dataset_name = "sales"
table_name = "sales_data"

# Set page title and configuration
st.set_page_config(page_title="Kwin Stationers - Sales",
                   page_icon=":round-point-of-sale:",
                   layout="wide")

st.markdown("<h1 style='text-align: center;'> Kwin Stationers </h1>", unsafe_allow_html=True)
st.title("Sales Input ")
with st.form("form 4", clear_on_submit=True):
    # Input fields
    date = st.date_input("Date")
    product_name = st.text_input("Product Name")
    salesperson = st.text_input("Salesperson")
    quantity = st.number_input("Quantity", min_value=1)
    price = st.number_input("Price", min_value=0.01, step=0.01, format="%.2f")
    
    notes = st.text_area("Notes")
    
    # Define submit button
    if st.form_submit_button("Submit"):
        # Calculate total amount charged
        amount_charged = quantity * price

        # Check if dataset exists, and create it if it doesn't
        dataset_ref = client.dataset(dataset_name)
        try:
            dataset = client.get_dataset(dataset_ref)
        except:
            dataset = bigquery.Dataset(dataset_ref)
            dataset = client.create_dataset(dataset)
            
        # Create table if it doesn't exist
        table_ref = dataset_ref.table(table_name)
        try:
            table = client.get_table(table_ref)
        except:
            table_schema = [
                bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
                bigquery.SchemaField("product_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("salesperson", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("quantity", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("price", "FLOAT", mode="REQUIRED"),
                bigquery.SchemaField("amount_charged", "FLOAT", mode="REQUIRED"),
                bigquery.SchemaField("notes", "STRING", mode="NULLABLE")
            ]
            table = bigquery.Table(table_ref, schema=table_schema)
            table = client.create_table(table)

        # Define form fields
        form_data = {
            "date": date,
            "product_name": product_name,
            "salesperson": salesperson,
            "quantity": quantity,
            "price": price,
            "amount_charged": quantity * price,  # Calculate total amount charged
            "notes": notes
        }

        # Insert form data into BigQuery table
        errors = client.insert_rows(table, [form_data])

        # Check for errors
        if errors == []:
            st.success("Form data inserted successfully.")
        else:
            st.error("Errors inserting form data: %s" % errors)

    # Add page footer
    st.markdown("---")
    st.write("© 2023 Kwin Stationers")
