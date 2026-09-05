import numpy as np
import scipy


def call(S, K, T, r,q, sigma):
    if S or K <= 0 or T or sigma<0:
        "error: nonsensical values for K,T,sigma or S"
        return 0,0 
    if T>0:
        d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    else:
        d1=max(S-K,0)
    d2 = d1 - sigma*np.sqrt(T)
    return S*np.exp(-q*T)*scipy.stats.norm.cdf(d1)-K*np.exp(-r*T)*scipy.stats.norm.cdf(d2)

def put(S, K, T, r,q,sigma ):
    if S or K <= 0 or T or sigma<0:
        "error: nonsensical values for K,T,sigma or S"
        return 0,0 
    if T>0:
        d1 = (np.log(S/K) + (r - q + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    else:
        d1=max(K-S,0)
    d2 = d1 - sigma*np.sqrt(T)
    return K*np.exp(-r*T)*scipy.stats.norm.cdf(-d2)-S*np.exp(-q*T)*scipy.stats.norm.cdf(-d1)

def parity_check(put,call,S,q,T,K,r):
    return call-put,S*np.exp(-q*T)-K*np.exp(-r*T)