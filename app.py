from src.monte_carlo import monte_carlo, monte_carlo_anti
from src.black_scholes import call, put, greeks_op, greeks_val
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    st.header("Option Pricer")
    st.subheader("Analytical Method")
    if "all_res_c" not in st.session_state:
        st.session_state.all_res_c = []
    if "all_res_p" not in st.session_state:
        st.session_state.all_res_p = []
    if "prev_plot" not in st.session_state:
        st.session_state.prev_plot = None
    if "x_axis" not in st.session_state:
        st.session_state.x_axis = "S"
    if "res_mc" not in st.session_state:
        st.session_state.res_mc = None
    if "latest_result" not in st.session_state:
        st.session_state.latest_result = None
    if "calc_result" not in st.session_state:
        st.session_state.calc_result = None
    if "y_axis_greeks" not in st.session_state:
        st.session_state.y_axis_greeks=["gamma"]


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
    x_axis_choice = st.radio(
    "X-axis variable",
    options=["S", "K", "T", "r", "q", "sigma"],
    horizontal=True,
)
    st.session_state.x_axis = x_axis_choice
    col7, col8, col9, col10 = st.columns(4)
    with col7:
        show_call = st.toggle("Call")
    with col8:
        show_put = st.toggle("Put")
    with col9:
        show_greeks = st.toggle("Greeks")
    with col10:
        if st.button("Add"):
            st.session_state.latest_result = {
            "S": S, "K": K, "T": T, "r": r, "q": q, "sigma": sigma,"call": show_call, "put": show_put
        }

    st.session_state.y_axis_greeks = st.multiselect(
    "Greek",
    options=["delta", "gamma","vega"],
    default=["gamma"],
)
    if st.button("Clear"):
        st.session_state.all_res_c=[]
        st.session_state.all_res_p=[]
        st.session_state.prev_plot=None
        st.session_state.latest_result = None
        
    if st.session_state.latest_result is not None:
        if st.session_state.latest_result!=st.session_state.prev_plot:
            p = st.session_state.latest_result
            

            if show_call:
                resultc = call(p["S"], p["K"], p["T"], p["r"], p["q"], p["sigma"])
                st.session_state.all_res_c.append({"result":resultc,"S":p["S"],"K": p["K"],"T": p["T"],"r": p["r"],"q": p["q"],"sigma": p["sigma"]})
                

            if show_put:
                resultp = put(p["S"], p["K"], p["T"], p["r"], p["q"], p["sigma"])
                st.session_state.all_res_p.append({"result":resultp,"S":p["S"],"K": p["K"],"T": p["T"],"r": p["r"],"q": p["q"],"sigma": p["sigma"]})
                
            st.session_state.prev_plot=p 
        fig, ax = plt.subplots()
        if show_call :
            ax.scatter([d[st.session_state.x_axis] for d in st.session_state.all_res_c],
                       [d["result"] for d in st.session_state.all_res_c],
                       c="b", label="Call")
        if show_put :
            ax.scatter([d[st.session_state.x_axis] for d in st.session_state.all_res_p],
                       [d["result"] for d in st.session_state.all_res_p],
                       c="r", label="Put")
        ax.set_xlabel(st.session_state.x_axis)
        ax.set_ylabel("Option Price")
        if show_call or show_put:
            ax.legend()
            
            
        st.pyplot(fig)

        if show_greeks:
        
                p = st.session_state.latest_result
                X = np.arange(1,2*p["K"],1)
                Y= [greeks_op(x, p["K"], p["T"], p["r"], p["q"], p["sigma"])for x in X]
                fig3,ax3 = plt.subplots()
                if "delta" in st.session_state.y_axis_greeks:
                    if show_call:
                        ax3.scatter(X,
                       [y["delta_c"] for y in Y],
                       c="b", label="Call Delta")
                    if show_put:
                        ax3.scatter(X,
                       [y["delta_p"] for y in Y],
                       c="r", label="Put Delta")
                if "gamma" in st.session_state.y_axis_greeks:
                    ax3.scatter(X,
                       [y["gamma"] for y in Y],
                       c="y", label="Gamma")
                if "vega" in st.session_state.y_axis_greeks:
                    ax3.scatter(X,
                       [y["vega"] for y in Y],
                       c="g", label="vega")
        
                ax3.set_xlabel("S")
                ax3.set_ylabel("Greek")
                ax3.legend()
            
                st.pyplot(fig3)


        N= st.slider(label="Number of Paths for Monte Carlo estimation", min_value=1000,max_value=3000000, value =300000)
        anti = st.toggle("Antithetic variates")
    if st.button("Run Monte Carlo Estimation"):
        current_state = [p, N, anti, show_call, show_put]
        if st.session_state.calc_result != current_state:
            if anti:
                res_mc = monte_carlo_anti(p["S"], p["K"], p["T"], p["r"], p["q"], p["sigma"], N, 54)
            else:
                res_mc = monte_carlo(p["S"], p["K"], p["T"], p["r"], p["q"], p["sigma"], N, 54)
            st.session_state.calc_result = current_state
            st.session_state.res_mc = res_mc

    # Display OUTSIDE the button block, so it persists across reruns
    if st.session_state.res_mc is not None:
        res_mc = st.session_state.res_mc
        f, ax2 = plt.subplots(figsize=(5, 5))
        labels, values, errors, colors = [], [], [], []

        if show_call:
            labels.append("Call (MC)")
            values.append(res_mc["m_c"])
            errors.append(res_mc["std_err_c"] * 1.96)
            colors.append("b")
        if show_put:
            labels.append("Put (MC)")
            values.append(res_mc["m_p"])
            errors.append(res_mc["std_err_p"] * 1.96)
            colors.append("r")

        if labels:
            ax2.bar(labels, values, color=colors)
            ax2.errorbar(labels, values, yerr=errors, fmt='none', color='black', capsize=6)
            if show_call:
                ax2.axhline(resultc, color='b', linestyle='--', label="Call (analytical)")
            if show_put:
                ax2.axhline(resultp, color='r', linestyle='--', label="Put (analytical)")
            ax2.set_ylabel("Estimated price")
            ax2.legend()
            st.pyplot(f)
        