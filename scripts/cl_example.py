import argparse
import numpy as np
import numpy.random
import plotly.subplots
import plotly.graph_objs as go


def generate_data(mean, std, n_samples):
    x = numpy.random.normal(mean, std, n_samples)
    return x


def visualize_data(x):
    h, bins = np.histogram(x)
    h = h / h.sum()
    # get histogram bin centers from the endpoinds returned by np.histogram():
    bins_centers = (bins[0:-1] + bins[1:]) / 2
    marker_style1 = dict(color='red', size=2, line=dict(color='red', width=2))
    fig = plotly.subplots.make_subplots(rows=1, cols=2)
    p1 = go.Scatter(y=x, name='random variable', marker=marker_style1)
    #p2 = go.Scatter(y=x_norm, name='normalized random variable', marker=marker_style2)
    fig.append_trace(p1, 1, 1)
    #fig.append_trace(p2, 1, 1)
    hp1 = go.Scatter(x=bins_centers, y=h, name='random variable histogram', marker=marker_style1)
    #hp2 = go.Scatter(x=bins_centers_norm, y=h_norm, name='normalized random variable histogram', marker=marker_style2)
    fig.append_trace(hp1, 1, 2)
    #fig.append_trace(hp2, 1, 2)
    plotly.offline.iplot(fig)



def parse_arguments():
    """Parse/check input arguments."""

    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-m', '--means',
                        type=int,
                        help="Mean value(s) of the distribution(s)")
    parser.add_argument('-s', '--stds',
                        type=int,
                        help="Standard deviation(s) of the "
                             "distribution(s)")
    parser.add_argument('-n', '--num_of_samples',
                        type=int,
                        help="Number of samples of the distributions")


    arguments = parser.parse_args()
    return arguments

if __name__ == "__main__":
    args = parse_arguments()
    m = args.means
    s = args.stds
    n = args.num_of_samples
    data = generate_data(m, s, n)
    visualize_data(data)