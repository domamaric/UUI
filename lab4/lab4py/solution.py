import math
import random
import sys


args = sys.argv

class Population:
    def __init__(self, inputLen, nn):
        dangling = []
        dangling.append(inputLen)
        dangling.extend(nn)
        dangling.append(1)

        weightsNpArr = []
        b = []

        for i in range(1, len(dangling)):  # 1 5 1
            connections = [[random.normalvariate(0, 0.01) for _ in range(int(dangling[i - 1]))] for _ in range(int(dangling[i]))]
            weightsNpArr.append(connections)
            b.append([random.normalvariate(0, 0.01) for _ in range(int(dangling[i]))])

        self.weights = weightsNpArr
        self.b = b
        self.diffSquared = float('inf')

    def __str__(self):
        return str(self.weights)

    def __repr__(self):
        return str(self.weights)


def readFromFile(path):
    file1 = open(path, 'r', encoding='utf-8')
    linesTemp = file1.readlines()
    file1.close()
    return linesTemp


def createMatrix(fileName):
    linesMat = readFromFile(fileName)

    mat = []

    for line in linesMat:
        splited = line.strip().split(',')
        if splited != ['']:
            mat.append(splited)
    return mat


def sigCalc(x):
    return 1 / (1 + math.exp(-x))


def propagate(data, populations):
    for pop in populations:
        difSquared = 0
        for i in range(1, len(data)):
            row = trainData[i]
            y = float(row[-1])
            x = [float(num) for num in row[:-1]]

            for j, layer in enumerate(pop.weights):
                result = [sum([layer[k][l] * x[l] for l in range(len(x))]) + pop.b[j][k] for k in range(len(layer))]

                if j != len(pop.weights) - 1:
                    result = [sigCalc(val) for val in result]

                x = result

            difSquared += (y - result[0]) ** 2

        difSquared /= (len(trainData) - 1)
        pop.diffSquared = difSquared


trainInputTxt = ''
testInputTxt = ''
nn = []
popsize = 0
elitism = 0
k = 0.0
iter = 0
probabiltyForChromosomeMutation = 0.0

for count, arg in enumerate(args, 0):
    if arg == "--train":
        trainInputTxt = args[count + 1]
    elif arg == "--test":
        testInputTxt = args[count + 1]
    elif arg == "--nn":
        n = args[count + 1]

        if n == "5s":
            nn.append(5)
        elif n == "20s":
            nn.append(20)
        elif n == "5s5s":
            nn.append(5)
            nn.append(5)

    elif arg == "--popsize":
        popsize = int(args[count + 1])
    elif arg == "--elitism":
        elitism = int(args[count + 1])
    elif arg == "--p":
        probabiltyForChromosomeMutation = float(args[count + 1])
    elif arg == "--K":
        k = float(args[count + 1])
    elif arg == "--iter":
        iter = int(args[count + 1])

trainData = createMatrix(trainInputTxt)
testData = createMatrix(testInputTxt)

inputLen = len(trainData[0]) - 1
populations = []

for _ in range(popsize):
    populations.append(Population(inputLen, nn))

for c in range(iter):
    propagate(trainData, populations)

    # elitism, selection
    sortedPopulation = sorted(populations, key=lambda x: x.diffSquared)
    sortedPopulation = sortedPopulation[:elitism]

    if c % 2000 == 1999:
        print("[Train error @" + str(c + 1) + "]: " + str(sortedPopulation[0].diffSquared))

    # crossing
    newPopulation = []

    while len(newPopulation) < popsize:
        neuralNetwork1 = random.sample(sortedPopulation, 1)[0]
        neuralNetwork2 = random.sample(sortedPopulation, 1)[0] if len(newPopulation) == 0 else random.sample(newPopulation, 1)[0]

        newWeights = []
        for n1, n2 in zip(neuralNetwork1.weights, neuralNetwork2.weights):
            newWeight = [[(w1 + w2) / 2 for w1, w2 in zip(row1, row2)] for row1, row2 in zip(n1, n2)]
            newWeights.append(newWeight)

        newB = []
        for n1, n2 in zip(neuralNetwork1.b, neuralNetwork2.b):
            currentB = [(b1 + b2) / 2 for b1, b2 in zip(n1, n2)]
            newB.append(currentB)

        newPop = Population(inputLen, nn)
        newPop.weights = newWeights.copy()
        newPop.b = newB.copy()
        newPopulation.append(newPop)

    # mutation
    for currentPop in newPopulation:
        for w in currentPop.weights:
            for i in range(len(w)):
                for j in range(len(w[i])):
                    w[i][j] += random.normalvariate(0, k) * (random.random() < probabiltyForChromosomeMutation)

        for b in currentPop.b:
            for i in range(len(b)):
                b[i] += random.normalvariate(0, k) * (random.random() < probabiltyForChromosomeMutation)

    populations = newPopulation.copy()

getFirst = sorted(populations, key=lambda x: x.diffSquared)[0]
tempArr = [getFirst]
propagate(testData, tempArr)
print("[Test error]: " + str(getFirst.diffSquared))
