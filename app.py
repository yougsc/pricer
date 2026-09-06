from src.monte_carlo import monte_carlo,monte_carlo_anti
import streamlit as st
from src.black_scholes import call,put,greeks_op,greeks_val
if __name__ == "__main__":
    st.header("Option Pricer") 
    st.subheader("Analytical Method")