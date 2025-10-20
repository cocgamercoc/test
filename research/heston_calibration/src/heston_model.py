import numpy as np
from numpy import exp, log, sqrt

def _phi(u, params, S0, r, q, T, j):
    kappa, theta, sigma, rho, v0 = params
    u = np.asarray(u, dtype=np.complex128)
    i = 1j
    b = kappa - (rho*sigma if j==1 else 0)
    u_shift = u - i if j==1 else u
    d = np.sqrt((rho*sigma*u_shift*i - b)**2 - (sigma**2)*(-u_shift**2 - i*u_shift))
    g = (b - rho*sigma*u_shift*i - d)/(b - rho*sigma*u_shift*i + d)
    g = np.where(np.abs(g)<1-1e-12, g, (1-1e-12)*g/np.abs(g))
    C = (r-q)*u*i*T + (kappa*theta/(sigma**2))*((b - rho*sigma*u_shift*i - d)*T - 
        2*np.log((1 - g*np.exp(-d*T))/(1 - g)))
    D = ((b - rho*sigma*u_shift*i - d)/(sigma**2))*((1 - np.exp(-d*T))/(1 - g*np.exp(-d*T)))
    return np.exp(C + D*v0 + i*u*np.log(S0*np.exp((r-q)*T)))

def heston_call_price(S0,K,T,r,q,params,n=1600,umax=100.0):
    u=np.linspace(1e-8,umax,n); du=u[1]-u[0]; i=1j
    phi1=_phi(u-1j,params,S0,r,q,T,1)
    phi2=_phi(u,params,S0,r,q,T,2)
    lnK=np.log(K)
    integrand1=np.real(np.exp(-i*u*lnK)*phi1/(i*u))
    integrand2=np.real(np.exp(-i*u*lnK)*phi2/(i*u))
    P1=0.5+(1/np.pi)*np.trapz(integrand1,dx=du)
    P2=0.5+(1/np.pi)*np.trapz(integrand2,dx=du)
    return S0*np.exp(-q*T)*P1 - K*np.exp(-r*T)*P2
