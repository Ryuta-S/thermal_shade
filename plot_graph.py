import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def main():

    load_path_1 = "input/plot_graph/sun_vals.npy"
    load_path_2 = "input/plot_graph/non_sun_vals.npy"

    output_path = 'output/plot_graph/Boson_Capture_3.png'


    sun_vals = np.load( load_path_1 )
    non_sun_vals = np.load( load_path_2 )


    plt.plot(range(len(sun_vals)), sun_vals, label='sun')
    plt.plot(range(len(non_sun_vals)), non_sun_vals, label='non sun')
    plt.legend()
    plt.savefig( output_path )
    plt.show()




if __name__ == "__main__":
    main()
