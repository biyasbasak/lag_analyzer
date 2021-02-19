import matplotlib.pyplot as plt
import numpy as np
import sys
import re
import argparse
from enum import Enum


plt.style.use("ggplot")
FILE_NAME = "test_data/test1.txt"


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--format", default="png",
                    help="Output format of the chart")
args = parser.parse_args()


class Search(Enum):
    LatencyOverview = re.compile("^L.*")
    LatencyDistribution = re.compile("Latency.*Distribution")
    Time = re.compile("[a-z]")
    TimeInSec = re.compile("[0-9]+s")
    ReqRate = re.compile("^Req/Sec")
    Detailed_Percentile = re.compile("^Detailed.*Percentile.*spectrum")


# def plotLatencyOverview(avg, std, nn):
#     plt.figure(figsize=(10, 10))
#     plt.xlabel("Percentile")
#     plt.ylabel("Response Time in ms")
#     # plt.xticks(np.arange(0, max(self.latency), 10))
#     plt.yticks(np.arange(0, max(self.time), step=500))
#     # plt.grid(True)
#     plt.title("Latency Distribution")
#     plt.plot(self.latency, self.time)
#     plt.savefig("overview.png")


class LatencyDist:
    def __init__(self) -> None:
        self.percentile = []
        self.time = []
        self.size = 0

    def add(self, percentile, time) -> None:
        self.percentile.append(percentile)
        self.time.append(time)
        self.size = self.size+1

    def plot(self, name, output_format, size=(12, 8)) -> None:
        plt.figure(figsize=size)
        plt.title(name)
        plt.xlabel("Response Time in ms", size=20)
        plt.ylabel("Percentile", size=20)
        # plt.xticks(np.arange(0, max(self.latency), 10))
        plt.xticks(np.arange(0, max(self.time), step=500))
        # plt.grid(True)
        plt.title(name, size=20)
        plt.plot(self.time, self.percentile)
        plt.savefig(name+"."+output_format)

# class PercentileSpectrum:
#     def __init__(self) -> None:
#         self.value = []
#         self.percentile = []
#         self.count = []
#         self.onebyone = []
#         self.size = 0
#     def add(self, percentile, value, count, onebyone) -> None:
#         self.percentile.append(percentile)
#         self.value.append(value)
#         self.count.append(count)
#         self.onebyone.append(onebyone)
#         self.size = self.size+1


if __name__ == "__main__":

    with open(FILE_NAME, 'r') as f:
        i = 0
        avg_latency = 0
        std_dev = 0
        nn_percentile = 0

        # percentile_spect = PercentileSpectrum()
        for line in f:
            line = line.strip()
            if re.match(Search.LatencyOverview.value, line) and not re.match(Search.LatencyDistribution.value, line):
                tokens = line.split()
                avg_latency = tokens[1]
                std_dev = tokens[2]
                nn_percentile = tokens[3]
                # plot.addOverview(avg_latency, std_dev, nn_percentile)
            if re.match(Search.LatencyDistribution.value, line):
                # loop until the next line is a space
                latency_dist = LatencyDist()
                while True:
                    tokens = f.readline().strip().split()
                    if len(tokens) == 0:
                        break
                    p = tokens[0]
                    t = tokens[-1]
                    p = p.strip("%")
                    if re.findall(Search.TimeInSec.value, t):
                        t = re.sub(Search.Time.value, "", t)
                        t = float(t) * 1000
                    else:
                        t = float(re.sub(Search.Time.value, "", t))
                    latency_dist.add(p, t)
                name_tokens = line.strip().split()
                name = name_tokens[0] + " " + name_tokens[1]
                latency_dist.plot(name, args.format)

            if re.match(Search.Detailed_Percentile.value, line):

                latency_dist = LatencyDist()
                next(f)
                next(f)
                while True:
                    tokens = f.readline().strip().split()
                    if re.match(re.compile("#"), tokens[0]):
                        break

                    v = float(tokens[0])
                    p = float(tokens[1])
                    # c = float(tokens[2])
                    # o = float(tokens[3])
                    latency_dist.add(p, v)
                name_tokens = line.strip().split()
                name = name_tokens[0] + " " + name_tokens[1]
                latency_dist.plot(name, args.format, size=(16, 8))
