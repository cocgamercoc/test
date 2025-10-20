import matplotlib.pyplot as plt

def plot_iv_smile(strikes,iv_mkt,iv_model,title="Implied Volatility Smile"):
    fig=plt.figure(figsize=(7,4.5))
    plt.plot(strikes,iv_mkt,"o-",label="Market IV")
    plt.plot(strikes,iv_model,"--",label="Heston IV")
    plt.xlabel("Strike"); plt.ylabel("Implied Volatility")
    plt.title(title); plt.legend(); plt.tight_layout()
    return fig
