import argparse
import numpy as np
import numpy.random
import plotly.subplots
import plotly.graph_objs as go

colors = ["red", "green", "blue", "orange", "gray"]

def generate_distributions(means, stds, n_samples):
    return [numpy.random.normal(mean, std, ns)
            for (mean, std, ns) in zip(means, stds, n_samples)]


def visualize_distributions(data, dist_names, norm=False):
    fig = plotly.subplots.make_subplots(rows=1, cols=2)
    for i, x in enumerate(data): # for each distribution
        # (1) compute (and normalize) histogram
        h, bins = np.histogram(x)
        if norm:
            h = h / h.sum()
        # get histogram bin centers from the endpoinds:
        bins_centers = (bins[0:-1] + bins[1:]) / 2

        # (2) Plot
        marker_style1 = dict(color=colors[i], size=2,
                             line=dict(color=colors[i], width=2))
        # append data to 1st subplot:
        fig.append_trace(go.Scatter(y=x, name=dist_names[i],
                                    marker=marker_style1), 1, 1)
        # append histogram to 2nd subplot:
        fig.append_trace(go.Scatter(x=bins_centers, y=h,
                                    name="hist " + dist_names[i],
                                    marker=marker_style1), 1, 2)
    plotly.offline.iplot(fig)


def parse_arguments():
    """Parse/check input arguments."""
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('-m', '--means', type=int, nargs="+", required=True,
                        help="Mean value(s) of the distribution(s)")
    parser.add_argument('-s', '--stds', type=int, nargs="+", required=True,
                        help="Standard deviation(s) of the distribution(s)")
    parser.add_argument('-n', '--num_of_samples', type=int, nargs="+",
                        required=True,
                        help="Number of samples of the distribution(s)")
    parser.add_argument('--names', nargs="+",
                        help="Distribution names")
    parser.add_argument('--normalize', action='store_true',
                        help="Set true if histograms are to be normalized")
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
    args = parse_arguments()
    m, s, n, norm = args.means, args.stds, args.num_of_samples, args.normalize
    if not(len(m) == len(s) == len(n)):
        print("Distribution parameters must be of the same length!")
        exit(1)
    if len(m) > 5:
        print("Maximum number of distributions is 5!")
        exit(1)
    names = args.names
    if not names or len(names) != len(m):
        names = [f"var_{i}" for i in range(len(m))]

    d = generate_distributions(m, s, n)
    visualize_distributions(d, names, norm)
