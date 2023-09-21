import streamlit as st
from workout import main

def main():
    if st.button('Open the app by clicking here: '):
        st.expander('Here is Workout Planner 💪')
