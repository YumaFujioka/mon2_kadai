import numpy as np
import EstimationModules
import argparse
from tqdm import tqdm
import csv
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# パーサ設定
parser = argparse.ArgumentParser(
            prog="MimoSimulator",
            usage="MIMOシミュレータです。",
            description="推定方式など実験設定を指定して実行して下さい。",
            add_help=True
            )
# 推定方式、入力アンテナ数、出力アンテナ数、イテレーション数、ビット数
parser.add_argument("-m", "--Method", action="store", default="zf")
parser.add_argument("-t", "--TransNum", action="store", default=4)
parser.add_argument("-o", "--ObsNum", action="store", default=4)
parser.add_argument("-i", "--IterNum", action="store", default=50000)
parser.add_argument("-s", "--SymNum", action="store", default=256)
args = parser.parse_args()

# エンコーダ
def bits2QPSK(bits):
    BPSK_T = 2.0 * bits.T - 1.0
    QPSK_T = (BPSK_T[0::2] + 1j * BPSK_T[1::2]) / np.sqrt(2)
    QPSK = QPSK_T.T # ただの転置。書きやすくするために転置してるだけ。
    return QPSK
# デコーダ
def QPSK2bits(QPSK):
    re_bits = np.where(QPSK.real > 0, 1, 0)
    im_bits = np.where(QPSK.imag > 0, 1, 0)
    bits = np.insert(re_bits, np.arange(1, len(re_bits[0])+1), im_bits, axis=1)
    return bits
# 設定表示
def show_settings(Method, TransNum, ObsNum, IterNum, SymNum, PSK):
    print(
        "==========\n",
        "Settings\n",
        "\tMethod=\t\t", args.Method,
        "\n\tSigNum=\t\t", TransNum,
        "\n\tObsNum=\t\t", ObsNum,
        "\n\tIteration=\t", IterNum,
        "\n\tSigSymNum=\t", SymNum,
        "\n\tPSK=\t\t", PSK,
        )

if __name__ == "__main__":
    # 送信アンテナ数、受信アンテナ数
    M = int(args.TransNum)
    N = int(args.ObsNum)
    # ループ数、送信機あたりのシンボル数
    IterNum = int(args.IterNum)
    SymNum_per_Trans = args.SymNum / M
    # 推測器
    estimator = EstimationModules.Estimator(M, N, SymNum_per_Trans)
    # ログ表示
    show_settings(args.Method, M, N, IterNum, args.SymNum, "QPSK")

    print("==========\n", "Simulation Phase.")
    SNR_dB_list = np.linspace(0, 40.0, 11) # 0〜40dBでシミュレート
    BER_list = []
    for SNR_dB in SNR_dB_list:
        # デシベル・ノイズ処理
        SNR = 10.0**(SNR_dB/10.0)   # SNRを真値に変換
        N_0 = M / SNR               # 雑音の複素分散。シンボル辺りのエネルギーを1.0としている
        sigma = np.sqrt(N_0/2.0)    # 雑音の振幅値

        num_of_error_bit = 0        # 誤りビット数

        #####ctはappendで処理？
        for i in tqdm(range(IterNum), ncols=100, leave=False, desc="SNR_dB=\t"+str(SNR_dB)):
            data_bits = np.where(np.random.rand(M, int(SymNum_per_Trans * 2)) > 0.5, 1, 0)  # M個の(SymNum_per_Trans*2)bit列を作成
            tx_syms = bits2QPSK(data_bits)                                                  # シンボル系列。QPSKなのでSymNum_per_Trans個のシンボル系列が出来る
            H_mat = (np.random.randn(N, M) + 1j * np.random.randn(N, M)) / np.sqrt(2)       # 通信路行列
            noise_syms = (np.random.randn(N, int(SymNum_per_Trans)) + 1j * np.random.randn(N, int(SymNum_per_Trans))) * sigma   # 雑音シンボル

            rx_syms = H_mat @ tx_syms + noise_syms                                  # 通信路通過
            tx_syms_hat = eval("estimator." + args.Method)(H_mat, rx_syms, N_0)     # 推定
            est_bits = QPSK2bits(tx_syms_hat)                                       # 推定シンボル(QPSK)をビットに変換

            num_of_error_bit += np.sum( np.sum( np.abs(data_bits - est_bits)))      # 誤りビット数をカウント

        BER = num_of_error_bit / (IterNum * SymNum_per_Trans * 2 * M)   # BER計算
        BER_list.append(BER)                                            # BER格納
        print("\t| SNR[dB]= {0:>6} BER= {1:<10}".format(SNR_dB, BER))

    print(" Simulation Completed.\n", "==========")

    result = [[SNR_dB_list[i], BER_list[i]] for i in range(len(SNR_dB_list))]
    with open("./csv/method="+str(args.Method)+"_M="+str(M)+"_N="+str(N)+'.csv', "w") as csvfile:
        field = ["SNR[dB]", "BER"]
        writer = csv.DictWriter(csvfile, fieldnames=field)
        writer.writeheader()
        for i in range(len(SNR_dB_list)):
            writer.writerow({'SNR[dB]': SNR_dB_list[i], 'BER': BER_list[i]})

    print("saved csv.")

    plt.figure()
    plt.title("method="+str(args.Method)+" M="+str(M)+" N="+str(N), fontsize=20)
    plt.xlabel("SNR[dB]", fontsize=16)
    plt.ylabel("BER", fontsize=16)
    mpl.style.use("seaborn-whitegrid")
    plt.grid()
    plt.xlim([0, 40])
    plt.ylim([0, 0.35])
    plt.plot(SNR_dB_list, BER_list, marker="o", ls=":", color="green")

    plt.savefig("./graph/method="+str(args.Method)+"_M="+str(M)+"_N="+str(N)+'.png')
    print("saved graph.")
