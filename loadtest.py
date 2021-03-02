import matplotlib.pyplot as plt
import re
import argparse
import numpy as np

plt.style.use("ggplot")

# pass one or more log files
FILE_NAME = ["loadtest_data/sample.log"]


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--format", default="png",
                    help="Output format of the chart")

args = parser.parse_args()


def plot_pdf(distributions, name, output_format="png") -> None:
    plt.figure(figsize=(20,8))
    distributions = [np.log(val) for val in distributions]
    plt.title(name)
    plt.xlabel("Response Time in ms", size=20)
    plt.title(name, size=20)
    plt.hist(distributions, bins='auto', density=True)
    plt.savefig(name+"."+output_format)


def plot_cdf(distributions, name, output_format="png") -> None:
    plt.figure(figsize=(20,8))
    plt.title(name)
    plt.xlabel("Response Time in ms", size=20)
    plt.ylabel("Percentile", size=20)
    plt.title(name, size=20)
    plt.hist(distributions, bins='auto', cumulative=True,
             density=True, histtype='step')
    plt.savefig(name+"."+output_format)


if __name__ == "__main__":
    distributions = []

    for file in FILE_NAME:
        with open(file, 'r') as f:
            latency_values = []
            for line in f:
                line = line.strip()
                if re.search(re.compile("MULogs:.*elapsed.*time", re.IGNORECASE), line):
                    tokens = line.split(":")
                    if len(tokens) == 0:
                        break
                    value = float(tokens[-1])
                    latency_values.append(value)
            distributions.append(latency_values)

    plot_pdf(distributions, name="PDF", output_format=args.format)
    plot_cdf(distributions, name="CDF", output_format=args.format)
