import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('./csv/mix.csv')
    plt.style.use("ggplot")
    fig, ax = plt.subplots(figsize=(16/2, 9/2))
    df.set_index("SNR[dB]").plot.line(ax=ax, style=['bs-.', 'bo-.', 'gs-.', 'go-.', 'rs-.', 'ro-.'])
    ax.set_title('タイトル')
    ax.set_xlabel('SNR[dB]', fontsize=14)
    ax.set_ylabel('BER[]', fontsize=14)
    ax.set_yscale('log')
    plt.show()
