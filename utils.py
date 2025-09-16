import streamlit as st
import pandas as pd


@st.cache_data(ttl=86400)
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"{file_path} file not found. Please make sure the file exists in the same directory.")
        return None
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        return None


@st.cache_data(ttl=86400)
def load_prompt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"{file_path} file not found. Please make sure the file exists in the same directory.")
        return None
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        return None