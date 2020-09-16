import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def main():
    """ .npyファイルで保存されたデータから，グラフをプロットする．
    """

    #load_path_1 = "../data/0006_0915/sun_vals_0001.npy"
    #load_path_2 = "../data/0006_0915/non_sun_vals_0001.npy"   
    load_path_1 = os.path.join('..','data', '0006_0915','sun_vals_0000.npy')
    load_path_2 = os.path.join('..','data', '0006_0915','non_sun_vals_0000.npy')

    #output_path = '../data/0006_0915/plot_0001.png'
    output_path = os.path.join('..','data', '0006_0915','plot_0000.png')

    sun_vals = np.load( load_path_1 )
    non_sun_vals = np.load( load_path_2 )


    plt.plot(range(len(sun_vals)), sun_vals, label='sun')
    plt.plot(range(len(non_sun_vals)), non_sun_vals, label='non sun')
    plt.legend()
    plt.savefig( output_path )
    plt.show()




if __name__ == "__main__":
    main()
