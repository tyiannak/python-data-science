import argparse
import numpy as np
import numpy.random
import plotly.subplots
import plotly.graph_objs as go


def generate_distributions(means, stds, n_samples):
    return [numpy.random.normal(mean, std, ns)
            for (mean, std, ns) in zip(means, stds, n_samples)]


def visualize_distributions(data, norm=False):
    fig = plotly.subplots.make_subplots(rows=1, cols=2)
    for x in data: # for each distribution
        # (1) compute (and normalize) histogram
        h, bins = np.histogram(x)
        if norm:
            h = h / h.sum()
        # get histogram bin centers from the endpoinds:
        bins_centers = (bins[0:-1] + bins[1:]) / 2

        # (2) Plot
        marker_style1 = dict(color='red', size=2,
                             line=dict(color='red', width=2))
        # append data to 1st subplot:
        fig.append_trace(go.Scatter(y=x, name='random variable',
                                    marker=marker_style1), 1, 1)
        # append histogram to 2nd subplot:
        fig.append_trace(go.Scatter(x=bins_centers, y=h,
                                    name='random variable histogram',
                                    marker=marker_style1), 1, 2)
    plotly.offline.iplot(fig)


def parse_arguments():
    """Parse/check input arguments."""
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-m', '--means', type=int, nargs="+",
                        help="Mean value(s) of the distribution(s)")
    parser.add_argument('-s', '--stds', type=int, nargs="+",
                        help="Standard deviation(s) of the "
                             "distribution(s)")
    parser.add_argument('-n', '--num_of_samples', type=int, nargs="+",
                        help="Number of samples of the distribution(s)")
    parser.add_argument('--normalize', action='store_true',
                        help="Set true if histograms are to be normalized")
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
    args = parse_arguments()
    m = args.means
    s = args.stds
    n = args.num_of_samples
    normalize = args.normalize
    d = generate_distributions(m, s, n)
    visualize_distributions(d, normalize)
