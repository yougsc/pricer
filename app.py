from src.monte_carlo import monte_carlo, monte_carlo_anti
from src.black_scholes import call, put, greeks_op, greeks_val
import streamlit as st
import matplotlib.pyplot as plt

if __name__ == "__main__":
    st.header("Option Pricer")
    st.subheader("Analytical Method")

    if "latest_result" not in st.session_state:
        st.session_state.latest_result = None

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        S = st.number_input("Spot (S)", value=100.0)
    with col2:
        K = st.number_input("Strike (K)", value=100.0)
    with col3:
        T = st.number_input("Maturity (T)", value=1.0)
    with col4:
        r = st.number_input("Risk-free rate (r)", value=0.05)
    with col5:
        q = st.number_input("Dividend yield", value=0.0)
    with col6:
        sigma = st.number_input("Volatility (σ)", value=0.20)

    show_call = st.toggle("Call")
    show_put = st.toggle("Put")

    if st.button("Add"):
        st.session_state.latest_result = {
            "S": S, "K": K, "T": T, "r": r, "q": q, "sigma": sigma
        }

    if st.session_state.latest_result is not None:
        p = st.session_state.latest_result
        fig, ax = plt.subplots()

        if show_call:
            resultc = call(p["S"], p["K"], p["T"], p["r"], p["q"], p["sigma"])
            ax.scatter(p["S"], resultc, c="b", label="Call")

        if show_put:
            resultp = put(p["S"], p["K"], p["T"], p["r"], p["q"], p["sigma"])
            ax.scatter(p["S"], resultp, c="r", label="Put")

        ax.set_xlabel("Spot Price")
        ax.set_ylabel("Option Price")
        if show_call or show_put:
            ax.legend()

        st.pyplot(fig)