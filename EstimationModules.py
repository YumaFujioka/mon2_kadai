import numpy as np
from itertools import product

class Estimator():
    def __init__(self, M, N, BitsNum):
        self.M = M
        self.N = N
        self.BitsNum = BitsNum  # データシンボル長の修正で連鎖的に修正がいるかも

        # MLD用の候補リスト。先に作っておく。
        # QPSKを仮定
        syms_candi_list = []
        QPSK_candi = np.array([-1-1j, -1+1j, 1-1j, 1+1j]) / np.sqrt(2)
        for candi in product(QPSK_candi, repeat=self.M):
            syms_candi_list.append(list(candi))
        self.syms_candi_mat = np.array(syms_candi_list).T # M*Q^M行列

    def zf(self, H, rx_syms, N_0):
        if self.M == self.N:
            Weight = np.linalg.inv(H)
        else:
            Weight = np.linalg.pinv(H)
        tx_syms_hat = Weight @ rx_syms
        return tx_syms_hat

    def mmse(self, H, rx_syms, N_0):
        Weight = np.linalg.inv(H @ np.conjugate(H.T) + N_0 * np.eye(self.N)) @ H
        tx_syms_hat = np.conjugate(Weight.T) @ rx_syms
        return tx_syms_hat

    def mld(self, H, rx_syms, N_0):
        # np.tile...はシンボル長の数だけ候補シンボルを並べただけの行列。やってることは|y - Hx|でしかない。
        # 4^M：QのM乗が候補数
        diff_mat = np.array([rx_syms - H @ np.tile(self.syms_candi_mat[:, i].reshape(self.M, 1), int(self.BitsNum/2) ) for i in range(4**self.M)])
        argmin_index = np.argmin(np.linalg.norm(diff_mat, axis=1), axis=0)
        rx_syms = np.array([self.syms_candi_mat[:, index] for index in argmin_index]).T
        return rx_syms
