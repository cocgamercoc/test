# Heston Calibration (SPX, Single Maturity)

**Goal:** Fit the Heston stochastic-volatility parameters \(\kappa,\theta,\sigma,\rho,v_0\)
to a single SPX option-chain maturity by minimizing the squared error between
market and Heston-model implied volatilities.

**Motivation:** Black–Scholes assumes constant volatility and fails to reproduce
the observed volatility smile. Heston introduces mean-reverting stochastic
variance and correlation between price and variance, capturing skew and smile.

**Pipeline**
1. Fetch SPX options via Yahoo Finance (`data_loader_yahoo.py`)
2. Compute mid prices + implied vols
3. Calibrate Heston params using least squares (`calibration.py`)
4. Plot Market vs Heston smiles (`plot_smile.py`)

**Outputs**
- `iv_smile_market_vs_heston.png`
- Calibrated parameters: \(\kappa,\theta,\sigma,\rho,v_0\)
- RMSE between market and model implied vols
