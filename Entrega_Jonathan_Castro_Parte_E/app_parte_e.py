"""Modulo individual - Parte E (Jonathan Castro). Rodar: streamlit run app_parte_e.py"""
import streamlit as st

from secoes import parte_e

st.set_page_config(page_title="Parte E - Afazeres Domesticos", page_icon="🏠", layout="wide")
parte_e.render()
