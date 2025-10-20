# Heston Model (Theory Overview)

\[
\begin{aligned}
dS_t &= (\mu-q)S_t\,dt + \sqrt{v_t}S_t\,dW_t^{(1)},\\
dv_t &= \kappa(\theta-v_t)\,dt + \sigma\sqrt{v_t}\,dW_t^{(2)},\\
\text{corr}(dW_t^{(1)},dW_t^{(2)}) &= \rho.
\end{aligned}
\]

Under risk-neutral measure \(dS_t=(r-q)S_t\,dt+\sqrt{v_t}S_t\,dW_t^{(1)}\).

European call (Heston 1993):
\[
C = S_0e^{-qT}P_1 - Ke^{-rT}P_2,
\quad
P_j = \tfrac12+\tfrac1\pi\int_0^\infty
\Re\!\left[\frac{e^{-iu\ln K}\phi_j(u)}{iu}\right]du.
\]

Calibration target:
\[
\min_{\kappa,\theta,\sigma,\rho,v_0}\sum_i
(\sigma^{mkt}_i-\sigma^{hes}_i)^2.
\]

Soft Feller condition: \(2\kappa\theta\ge\sigma^2\).
