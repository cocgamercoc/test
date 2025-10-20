import yfinance as yf, numpy as np, pandas as pd
from datetime import datetime
from scipy.stats import norm

def bs_price_call(S,K,T,r,q,sigma):
    if T<=0 or sigma<=0: return max(S*np.exp(-q*T)-K*np.exp(-r*T),0.0)
    d1=(np.log(S/K)+(r-q+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    return S*np.exp(-q*T)*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)

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

def load_spx_option_slice(window=(20,45),r=0.0,q=0.015,min_quotes=12):
    print("📈 Fetching SPX chain via Yahoo Finance...")
    tkr=yf.Ticker("^SPX"); S0=tkr.history(period="1d")["Close"].iloc[-1]
    today=datetime.utcnow().date()
    valid=[(e,(datetime.strptime(e,"%Y-%m-%d").date()-today).days)
           for e in tkr.options if window[0]<=
           (datetime.strptime(e,"%Y-%m-%d").date()-today).days<=window[1]]
    if not valid: raise ValueError("No expirations 20–45 DTE.")
    expiry,dte=valid[0]; chain=tkr.option_chain(expiry).calls
    chain["mid"]=0.5*(chain["bid"]+chain["ask"])
    chain=chain.dropna(subset=["mid","strike"]); chain=chain[chain["mid"]>0]
    print(f"Selected {expiry} ({dte} DTE), quotes={len(chain)}")
    T=dte/365.0
    chain["implied_vol"]=[implied_vol_call_bisect(S0,k,T,r,q,m)
                          for k,m in zip(chain["strike"],chain["mid"])]
    df=chain.dropna(subset=["implied_vol"])[["strike","mid","implied_vol"]]\
            .sort_values("strike").reset_index(drop=True)
    if len(df)<min_quotes: raise ValueError("Too few valid IVs.")
    print(f"✅ Loaded {len(df)} strikes for calibration.")
    return df,S0,r,q,T
