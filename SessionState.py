import streamlit as st
import hashlib

# SessionState defined

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)


# Function to get or create a session state
def get_session_state(**kwargs):
    # Create a new hash object
    hasher = hashlib.sha256()

    # Generate a hash key based on the kwargs
    for key, value in kwargs.items():
        # Convert the key-value pair to string and encode as UTF-8
        key_str = str(key).encode("utf-8")
        value_str = str(value).encode("utf-8")
        # Update the hash object with the key and value
        hasher.update(key_str + value_str)

    # Get the hexadecimal representation of the hash digest
    hash_key = hasher.hexdigest()

    # Create a new session state if one doesn't exist
    if not hasattr(st.session, "_session_state"):
        st.session._session_state = {}

    # Create a new state for the hash key if it doesn't exist
    if hash_key not in st.session._session_state:
        st.session._session_state[hash_key] = kwargs

    # Return the session state for the hash key
    return st.session._session_state[hash_key]

