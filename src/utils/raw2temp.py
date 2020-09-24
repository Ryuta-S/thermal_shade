import numpy as np
import sys, os
import matplotlib as mpl
import matplotlib.pyplot as plt

def main():
    image = []
    raw2temp(image)


def raw2temp(image,camera_temp):
    """
    カメラのアウトプットから温度を計算する関数
    @param image src画像 np.ndarray
    @param camera_temp カメラで画像を撮った時の本体温度 float
    @return temp 温度に変換した配列 np.ndarray

    """


    Bcal = 19.32029522054909
    Rcal = 1896.4810262642202
    Fcal = 1.0623746441660586
    Ocal = -142.5463107245369 * camera_temp + 25603.74739193574

    temp = Bcal / np.log((Rcal / (image - Ocal)) + Fcal)

    return temp

if __name__ == "__main__":
    main()