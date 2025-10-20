import numpy as np
from math import sqrt, log, exp
from scipy.stats import norm

def bs_price_call(S,K,T,r,q,sigma):
    if T<=0 or sigma<=0: return max(S*exp(-q*T)-K*exp(-r*T),0.0)
    d1=(log(S/K)+(r-q+0.5*sigma**2)*T)/(sigma*sqrt(T))
    d2=d1-sigma*sqrt(T)
    return S*exp(-q*T)*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)

def implied_vol_call_bisect(S,K,T,r,q,price,lo=1e-6,hi=5.0,tol=1e-6,max_iter=100):
    if T<=0 or price<=0: return np.nan
    plo,phi=bs_price_call(S,K,T,r,q,lo),bs_price_call(S,K,T,r,q,hi)
    if price<plo or price>phi: return np.nan
    for _ in range(max_iter):
        mid=0.5*(lo+hi); pm=bs_price_call(S,K,T,r,q,mid)
        if abs(pm-price)<tol: return mid
        if pm>price: hi=mid
        else: lo=mid
    return 0.5*(lo+hi)
