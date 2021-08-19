import argparse
import numpy as np
import numpy.random


def generate_data(m, s, n_samples):
    x = numpy.random.normal(m, s, n_samples)
    m_est = x.mean()
    s_est = x.std()
    # z = (x - m) / s
    x_norm = (x - m_est) / s_est
    return x_norm


def visualize_data(x):
    # get and normalize histograms
    h, bins = np.histogram(x)
    h = h / h.sum()
    # get histogram bin center from the endpoinds returned by np.histogram():
    bins_centers = (bins[0:-1] + bins[1:]) / 2
    h_norm, bins_norm = np.histogram(x_norm)
    h_norm = h_norm / h_norm.sum()
    bins_centers_norm = (bins_norm[0:-1] + bins_norm[1:]) / 2


def parse_arguments():
    """Parse/check input arguments."""

    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-m', '--means',
                        help="Mean value(s) of the distribution(s)")
    parser.add_argument('-s', '--stds',
                        help="Standard deviation(s) of the "
                             "distribution(s)")
    parser.add_argument('-n', '--num_of_samples',
                        help="Number of samples of the distributions")


    arguments = parser.parse_args()
    return arguments

if __name__ == "__main__":
    args = parse_arguments()
    m = args.means
    s = args.stds
    n = args.num_of_samples
    data = generate_data(10, 2, 100)
    print(data)