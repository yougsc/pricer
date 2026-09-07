from src.monte_carlo import monte_carlo,monte_carlo_anti
import streamlit as st
from src.black_scholes import call,put,greeks_op,greeks_val
import matplotlib.pyplot as plt
if __name__ == "__main__":
    st.header("Option Pricer") 
    st.subheader("Analytical Method")
    if "latest_result" not in st.session_state:
        st.session_state.latest_result = None
    if "last_plotted" not in st.session_state:
        st.session_state.last_plotted = None
    if "fig" not in st.session_state:
        st.session_state.fig = None

    col1, col2, col3, col4,col5,col6 = st.columns(6)
    with col1:
        S = st.number_input("Spot (S)", value=100.0)
    with col2:
        K = st.number_input("Strike (K)", value=100.0)
    with col3:
        T = st.number_input("Maturity (T)", value=1.0)
    with col4:
        r = st.number_input("Risk-free rate (r)", value=0.05)
    with col5:
        t = st.number_input("Dividend yield", value=0.0)
    with col6:
        sigma = st.number_input("Volatility (σ)", value=0.20)

    if st.button("Add"):
        st.session_state.latest_result = {"S": S, "K": K, "T":T,"r":r,"t":t,"sigma":sigma}

    # Only redraw the figure if the data actually changed
    if st.session_state.latest_result is not None:

        if st.session_state.latest_result != st.session_state.last_plotted:
            fig, ax = plt.subplots()

            if st.toggle("Call"):
                resultc = call(st.session_state.latest_result["S": S],st.session_state.latest_result["K": K],st.session_state.latest_result["T":T],st.session_state.latest_result["r":r],st.session_state.latest_result["t":t],st.session_state.latest_result["sigma":sigma])
                ax.scatter(st.session_state.latest_result["S": S],resultc,c="b")

            if st.toggle("Put"):
                resultp = call(st.session_state.latest_result["S": S],st.session_state.latest_result["K": K],st.session_state.latest_result["T":T],st.session_state.latest_result["r":r],st.session_state.latest_result["t":t],st.session_state.latest_result["sigma":sigma])
                ax.scatter(st.session_state.latest_result["S": S],resultp,c="r")
            ax.set_xlabel("Spot Price")
            ax.set_ylabel("Option Price ")
            st.session_state.fig = fig
            st.session_state.last_plotted = st.session_state.latest_result

        st.pyplot(st.session_state.fig)