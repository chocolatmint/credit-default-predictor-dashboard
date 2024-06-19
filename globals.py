import streamlit as st
import pickle

@st.cache_data
def load_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def init_session_state():
    st.session_state.data = load_data('credit_default_datasets.pkl')