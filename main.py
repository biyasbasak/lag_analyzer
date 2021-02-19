import matplotlib.pyplot as plt
import numpy as np
import re
from enum import Enum


plt.style.use("ggplot")
FILE_NAME = "test_data/test1.txt"


class Search(Enum):
    LatencyOverview = re.compile("^L.*")
    LatencyDistribution = re.compile("Latency.*Distribution")
    Time = re.compile("[a-z]")
    TimeInSec = re.compile("[0-9]+s")
    ReqRate = re.compile("^Req/Sec")


def plotLatencyOverview(avg, std, nn):
    plt.figure(figsize=(10, 10))
    plt.xlabel("Percentile")
    plt.ylabel("Response Time in ms")
    # plt.xticks(np.arange(0, max(self.latency), 10))
    plt.yticks(np.arange(0, max(self.time), step=500))
    # plt.grid(True)
    plt.title("Latency Distribution")
    plt.plot(self.latency, self.time)
    plt.savefig("overview.png")


class LatencyDist:
    def __init__(self) -> None:
        self.percentile = []
        self.time = []
        self.size = 0

    def add(self, percentile, time) -> None:
        self.percentile.append(percentile)
        self.time.append(time)
        self.size = self.size+1
    def plot(self) -> None:
        plt.figure(figsize=(12,8))
        plt.xlabel("Percentile")
        plt.ylabel("Response Time in ms")
        # plt.xticks(np.arange(0, max(self.latency), 10))
        plt.yticks(np.arange(0, max(self.time), step=500))
        # plt.grid(True)
        plt.title("Latency Distribution")
        plt.plot(self.percentile, self.time)
        plt.savefig("latencydist.png")


if __name__ == "__main__":
    with open(FILE_NAME, 'r') as f:
        i = 0
        avg_latency = 0
        std_dev = 0
        nn_percentile = 0
        
        latency_dist = LatencyDist()
        
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
                while True:
                    tokens = f.readline().strip().split()
                    if len(tokens) == 0:
                        break
                    l = tokens[0]
                    t = tokens[-1]
                    l = l.strip("%")
                    if re.findall(Search.TimeInSec.value, t):
                        t = re.sub(Search.Time.value, "", t)
                        t = float(t) * 1000
                    else:
                        t = float(re.sub(Search.Time.value, "", t))
                    latency_dist.add(l, t)
                
                latency_dist.plot()
