import numpy as np
from scipy.optimize import least_squares
from .heston_model import heston_call_price
from .iv_helpers import implied_vol_call_bisect

def model_iv_for_strikes(S0,r,q,T,strikes,params):
    ivs=[]
    for K in strikes:
        p=heston_call_price(S0,K,T,r,q,params)
        iv=implied_vol_call_bisect(S0,K,T,r,q,p)
        ivs.append(iv)
    return np.array(ivs)

def fit_heston_iv(S0,r,q,T,strikes,iv_mkt,
                  x0=(1.0,0.04,0.5,-0.5,0.04),
                  bounds=([1e-3,1e-5,1e-3,-0.999,1e-5],
                          [5.0,0.5,3.0,0.0,0.5])):
    strikes=np.array(strikes); iv_mkt=np.array(iv_mkt)

    def residuals(x):
        kappa,theta,sigma,rho,v0=x
        penalty=max(0.0,sigma**2-2*kappa*theta)
        iv_model=model_iv_for_strikes(S0,r,q,T,strikes,x)
        mask=~np.isnan(iv_model)&~np.isnan(iv_mkt)
        res=(iv_model[mask]-iv_mkt[mask])
        return np.concatenate([res,[0.1*penalty]])

    sol=least_squares(residuals,x0=x0,bounds=bounds,
                      xtol=1e-6,ftol=1e-6,gtol=1e-6,max_nfev=200)
    return sol.x,sol.cost,sol
