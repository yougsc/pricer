import numpy as np
def monte_carlo(S,K, T, r,q, sigma,N,seed):
    np.random.seed(seed)
    Z=np.random.normal(0,1,N)
    S_T= S*np.exp((r-q-0.5*sigma**2)*T+sigma*np.sqrt(T)*Z)
    disc_call = np.exp(-r*T) * np.maximum(S_T - K, 0)
    disc_put = np.exp(-r*T) * np.maximum(K-S_T, 0)
    m_c= np.mean(disc_call)
    m_p=np.mean(disc_put)
    std_err_c= np.sqrt(np.var(disc_call, ddof=1)/N)
    std_err_p=np.sqrt(np.var(disc_put, ddof=1)/N)

    return {"std_err_c":std_err_c,"std_err_p":std_err_p,"m_c":m_c,"m_p":m_p}
def monte_carlo_anti(S,K, T, r,q, sigma,N,seed):
    np.random.seed(seed)
    Z=np.random.normal(0,1,N//2)
    S_T= S*np.exp((r-q-0.5*sigma**2)*T+sigma*np.sqrt(T)*Z)
    S_T_n=S*np.exp((r-q-0.5*sigma**2)*T+sigma*np.sqrt(T)*-Z)
    disc_call = (np.exp(-r*T) * np.maximum(S_T - K, 0)+np.exp(-r*T) * np.maximum(S_T_n - K, 0))/2
    disc_put = (np.exp(-r*T) * np.maximum(K-S_T, 0)+np.exp(-r*T) * np.maximum(K-S_T_n, 0))/2
    m_c= np.mean(disc_call)
    m_p=np.mean(disc_put)
    std_err_c= np.sqrt(np.var(disc_call, ddof=1)/(N//2))
    std_err_p=np.sqrt(np.var(disc_put, ddof=1)/(N//2))   
    return {"std_err_c":std_err_c,"std_err_p":std_err_p,"m_c":m_c,"m_p":m_p}
    
