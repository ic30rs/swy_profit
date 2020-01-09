import linecache
from itertools import islice

import frozen_dir


class Food:

    def __init__(self, name, price, time, consumption):
        self.name = name
        self.price = price
        self.time = time
        self.consumption = consumption

    def getConsumption(self, i) -> int:
        return self.consumption[i]


def readFood() -> list:
    ret = list()
    with open(frozen_dir.app_path() + '\\data\\foods.csv', 'r') as f:
        for line in islice(f, 1, None):
            split = line.split(',')
            name = split[0]
            # consumption = [int('0'+split[1]), int('0'+split[2]), int('0'+split[3]),
            #                int('0'+split[4]), int('0'+split[5]), int('0'+split[6])]
            consumption = [int('0' + split[i]) for i in range(1, 7)]
            price = float(split[7])
            timeStr = split[8]
            minute = int(timeStr.split("m")[0])
            second = int(timeStr.split("m")[1])
            time = minute * 60 + second
            ret.append(Food(name, price, time, consumption))
    return ret


def readFarm() -> list:
    with open(frozen_dir.app_path() + '\\data\\farm.csv', 'r') as f:
        lines = f.readlines()

        yieldLine = lines[1]
        farmYield = [int(yieldLine.split(",")[i]) for i in range(len(yieldLine.split(",")))]

        buffLine = lines[2]
        farmerBuff = [float(buffLine.split(",")[i].strip().strip('%')) / 100 for i in range(len(buffLine.split(",")))]

        return [farmYield[i] * (1+farmerBuff[i]) * 24 for i in range(len(farmYield))]

def readTime() -> int:
    with open(frozen_dir.app_path() + '\\data\\cook.csv', 'r') as f:
        lines = f.readlines()

        buffLine = lines[1]
        cookBuff = [float(buffLine.split(",")[i].strip().strip('%')) / 100 for i in range(len(buffLine.split(",")))]

        return sum([ 24 * 60 * 60 / (1-cookBuff[i]) for i in range(len(cookBuff))])


if __name__ == '__main__':
    print(readTime())