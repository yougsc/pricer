import numpy as np
import scipy


def call(S, K, T, r,q, sigma):
    if K <= 0 or S <= 0 or T <0 or sigma <0:
        raise ValueError("error: nonsensical values for K,T,sigma or S")
    if T<=0:
        return max(S - K, 0)  
    if sigma == 0:
        # deterministic forward payoff
        F = S * np.exp((r - q) * T)
        return np.exp(-r * T) * max(F - K, 0)
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))

    d2 = d1 - sigma*np.sqrt(T)
    return S*np.exp(-q*T)*scipy.stats.norm.cdf(d1)-K*np.exp(-r*T)*scipy.stats.norm.cdf(d2)

def put(S, K, T, r,q,sigma ):
    if K <= 0 or S <= 0 or T <0 or sigma <0:
        raise ValueError("error: nonsensical values for K,T,sigma or S")

    if T<=0:
        return max(K-S, 0) 
    if sigma == 0:
        # deterministic forward payoff
        F = S * np.exp((r - q) * T)
        return np.exp(-r * T) * max(K-F, 0)
    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))

    d2 = d1 - sigma*np.sqrt(T)
    return K*np.exp(-r*T)*scipy.stats.norm.cdf(-d2)-S*np.exp(-q*T)*scipy.stats.norm.cdf(-d1)

def parity_check(call,put,S,K,T,r,q):
    return call-put,S*np.exp(-q*T)-K*np.exp(-r*T)
def greeks_op(S, K, T, r,q, sigma):
    if K <= 0 or S <= 0 or T <=0 or sigma <=0:
        raise ValueError("error: nonsensical values for K,T,sigma or S")

    d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    delta_c=np.exp(-q*T)*scipy.stats.norm.cdf(d1)
    delta_p=np.exp(-q*T)*(scipy.stats.norm.cdf(d1)-1)
    gamma=np.exp(-q*T)*scipy.stats.norm.pdf(d1)/(S*sigma*np.sqrt(T))
    vega= S*np.exp(-q*T)*scipy.stats.norm.pdf(d1)*np.sqrt(T)
    rho_c=K*T*np.exp(-r*T)*scipy.stats.norm.cdf(d2)
    rho_p=-K*T*np.exp(-r*T)*scipy.stats.norm.cdf(-d2)
    return {"delta_c":delta_c,"delta_p":delta_p,"gamma":gamma,"vega":vega,"rho_c":rho_c,"rho_p":rho_p}
def greeks_val(S,K, T, r,q,sigma ,h,func):
    delta = (func(S+h,K, T, r,q,sigma )-func(S-h,K, T, r,q,sigma ))/(2*h)
    gamma= (func(S+h,K, T, r,q,sigma )-2*func(S,K,T,r,q,sigma)-func(S-h,K, T, r,q,sigma ))/(h**2)
    vega= (func(S,K, T, r,q,sigma+h )-func(S,K, T, r,q,sigma-h ))/(2*h)
    return {"delta":delta,"gamma":gamma,"vega":vega}
    
    
