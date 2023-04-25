import streamlit as st
import streamlit_authenticator as stauth
import streamlit.components.v1 as components
from  authenticate import Authenticate
import yaml
from yaml.loader import SafeLoader

# Set form title and configuration for page title
st.set_page_config(page_title="Kwin Stationers - The sky is a podium",
                   page_icon=":pencil2:",
                   layout="wide")

st.title("Welcome to Kwin Stationers!")
st.markdown("""
          We are a small business that provides high-quality products and services to our customers. Our goal is to make your life easier and more enjoyable by providing you with the tools and resources you need to succeed.
        """)

# Add page footer
st.markdown("---")
st.write("© 2023 Kwin Stationers")
