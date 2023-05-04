import streamlit as st


def get_secret(key, default=None, is_optional=False):
    if st.secrets.has_key(key):
        return st.secrets[key]
    if is_optional:
        return default
    raise Exception(f"Secret {key} not configured in '.streamlit/secrets.toml'")
