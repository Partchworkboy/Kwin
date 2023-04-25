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
_RELEASE = True

if not _RELEASE:
    
    # Create a login widget
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    # Creating the authenticator object
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    # Render the login widget and authenticate users
    authentication_status, name = authenticator.authenticate()
    if authentication_status:
        st.session_state['authenticated'] = True
        st.session_state['name'] = name
        st.write(f'welcome *{name}*')
        st.title('Kwin Stationers')

    elif not authentication_status:
        st.error('Username/Password is incorrect')

    elif authentication_status is None:
        st.warning('Please enter your username and password')

    # Set up the sidebar
    st.sidebar.header("Navigation")
    menu = ["Home", "Dashboard", "Sales", "Purchases", "Blog"]
    selected_menu = st.sidebar.radio("", menu)
    # Show logout button
    show_logout()

    # Set up the pages
    if selected_menu == "Home":
        st.title("Welcome to Kwin Stationers!")
        st.markdown("""
            We are a small business that provides high-quality products and services to our customers. Our goal is to make your life easier and more enjoyable by providing you with the tools and resources you need to succeed.
        """)

    elif selected_menu == "Dashboard":
        st.title("Dashboard")
        st.markdown("""
            This is the dashboard.
        """)

    elif selected_menu == "Sales":
        st.title("Sales")
        st.markdown("""
            This is the sales page.
        """)

    elif selected_menu == "Purchases":
        st.title("Purchases")
        st.markdown("""
            This is the purchases page.
        """)

    elif selected_menu == "Blog":
        st.title("Blog")
        st.markdown("""
            This is the blog page.
        """)
    # Add page footer
    st.markdown("---")
    st.write("© 2023 Kwin Stationers")

    # Run the app
    if __name__ == "__main__":
        main()
