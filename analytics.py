import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stat

class Analytics:


    def __init__(self):
        self.f = list(open("scores.txt", "r"))
        self.t = [i for i in range(0, len(self.f))] 

        self.wpm = []
        self.acc = []
        self.scores = []
        self.streak = 0
        h = 0

        for s in self.f:
            s = s[20:]

            e = s.replace('\n', '').split(' ')

            self.wpm.append(float(e[0]))
            self.acc.append(float(e[1]))
            self.scores.append(float(e[2]))
            if float(e[1]) == 100:
                h += 1
            else:
                if h > self.streak:
                    self.streak = h
                h = 0
        
    def computeReport(self):
        self.avgWpm = int(stat.mean(self.wpm))
        self.maxWpm = int(max(self.wpm))
        self.avgAcc = int(stat.mean(self.acc))
        self.avgScore = int(stat.mean(self.scores))
        self.maxScore = int(max(self.scores))

    def report(self):
        self.computeReport()
        print(f'Average wpm {self.avgWpm}')
        print(f'Max wpm {self.maxWpm}')
        print(f'Average accuracy {self.avgAcc}')
        print(f'Average score {self.avgScore}')
        print(f'Max score {self.maxScore}')
        print(f'longest 100% streak: {self.streak}')

    def feedback(self, data):
        self.computeReport()
        data = data.split(' ')

        if int(float(data[0])) > self.avgWpm:
            print(f'Your speed was {int(float(data[0]))-self.avgWpm} wpm faster than your average.')
        if int(float(data[1])) > self.avgAcc:
            print(f'You were {int(float(data[1]))-self.avgAcc} % more accurate than your average.')
        if int(float(data[2])) > self.avgScore:
            print(f'You were {int(float(data[2]))-self.avgScore} higher score than usual..')

        if int(float(data[0])) > self.maxWpm:
            print(f'New speed record! {int(float(data[1]))-self.maxWpm} wpm faster.')
        if int(float(data[2])) > self.maxScore:
            print(f'New high score {data[2]}! That is {int(float(data[2]))-self.maxScore} better than before.')

        if int(float(data[0])) > self.avgWpm and int(float(data[1])) < self.avgAcc:
            print('You should go a bit slower and keep you focus on accuracy.')

        if int(float(data[1])) == 100:
            print('Very good! Now start getting faster!')

    def graph(self):
        wpmP = plt.subplots()
        accP = plt.subplots()
        scrP = plt.subplots()

        wpmP[1].plot(self.t, self.wpm, color='red')
        accP[1].plot(self.t, self.acc, color='green')
        scrP[1].plot(self.t, self.scores, color='blue')

        poly1d_fn = np.poly1d(np.polyfit(self.t, self.wpm, 1))
        wpmP[1].plot(self.t, self.wpm, self.t, poly1d_fn(self.t), '--r')

        poly1d_fn = np.poly1d(np.polyfit(self.t, self.acc, 1))
        accP[1].plot(self.t, self.acc, self.t, poly1d_fn(self.t), '--g')

        poly1d_fn = np.poly1d(np.polyfit(self.t, self.scores, 1))
        scrP[1].plot(self.t, self.scores, self.t, poly1d_fn(self.t), '--b')

        wpmP[1].set_title('wpm')
        accP[1].set_title('accuracy')
        scrP[1].set_title('scores')

        # plt.legend()
        plt.show()
