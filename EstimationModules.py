import numpy as np

class Estimator():
    def __init__(self, M, N):
        self.M = M
        self.N = N

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
        pass
