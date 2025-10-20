# Calibration Plan

1. Load single-maturity SPX calls (20–45 DTE)
2. Compute mid prices + implied vols
3. For each strike, compute Heston call → implied vol
4. Minimize SSE between market and model vols
5. Report parameters + RMSE + smile plot

Initial guess:
(κ,θ,σ,ρ,v₀) = (1.0, 0.04, 0.5, −0.5, 0.04)

Bounds:
κ∈[1e-3,5], θ∈[1e-5,0.5], σ∈[1e-3,3],
ρ∈[−0.999,0], v₀∈[1e-5,0.5]
