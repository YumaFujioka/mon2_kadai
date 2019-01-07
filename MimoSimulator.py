# estimator = EstimationModules.Estimator()



import numpy as np
import EstimationModules
import argparse

parser = argparse.ArgumentParser(
            prog="MimoSimulator",
            usage="MIMOシミュレータです。",
            description="推定方式など実験設定を指定して実行して下さい。",
            add_help=True
            )
# 推定方式、入力アンテナ数、出力アンテナ数、イテレーション数、ビット数
parser.add_argument("-m", "--Method", action="store", default="zf")
parser.add_argument("-s", "--SigNum", action="store", default=4)
parser.add_argument("-o", "--ObsNum", action="store", default=4)
parser.add_argument("-i", "--IterNum", action="store", default=50000)
parser.add_argument("-b", "--BitsNum", action="store", default=256)
args = parser.parse_args()

if __name__ == "__main__":
    # 入力アンテナ数、出力アンテナ数
    M = args.SigNum
    N = args.ObsNum
    # ループ数、シンボルビット数
    IterNum = args.IterNum
    BitsNum = args.BitsNum

    # 0〜40dBでシミュレート
    for SNR_dB in np.linspace(0, 40.0, 11):
        # デシベル・ノイズ処理
        SNR = 10.0**(SNR_dB/10.0)   # SNRを真値に変換
        N_0 = M / SNR               # 雑音の複素分散。シンボル辺りのエネルギーを1.0としている
        sigma = np.sqrt(N_0/2.0)    # 雑音の振幅値

        num_of_error_bit = 0        # 誤りビット数

        #####ctはappendで処理？

        for 
