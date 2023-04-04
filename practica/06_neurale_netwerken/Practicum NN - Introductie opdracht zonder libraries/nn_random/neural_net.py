import data as dt
import numpy as np
import itertools as it

gain = 2

def sigmoid (x):
    return 1 / (1 + np.exp (-x))

class NeuralNet:
    def __init__(self, outputDict):
        self.outputDict = outputDict
        self.labelDict = {value: key for key, value in self.outputDict.items ()}
        self.weights0 = np.random.rand (dt.hiddenDim, dt.inputDim)
        self.weights1 = np.random.rand (dt.outputDim, dt.hiddenDim)             

    def cost (self):
        return np.sum ((self.refOutputs - self.outputs) ** 2) / len (self.outputs)

    def read (self, dataSet):
        self.dataSet = dataSet
        self.inputs = np.array ([list (it.chain (*item [0])) for item in self.dataSet]) .T
        self.refOutputs = np.array ([self.outputDict[item [1]] for item in self.dataSet]) .T

    def report (self, caption):
        print ()
        print (caption, '- cost:', self.cost ())
        for itemIndex, item in enumerate (self.dataSet):
            output = self.outputs.T [itemIndex]
            print (
                item [1],
                self.refOutputs.T [itemIndex],
                self.labelDict [tuple (np.rint (output) .astype (int) .tolist ())],
                output
            )
        print ()

    def classify (self):
        self.outputs0 = sigmoid (self.weights0 @ self.inputs)
        self.outputs = sigmoid (self.weights1 @ self.outputs0)

    def correct (self):
        weightsTensor = (self.weights0, self.weights1)
        bestWeightsIndex = 0
        bestRowIndex = 0
        bestColumnIndex = 0
        bestFactor = 1
        currentCost = self.cost ()
        lowestCost = currentCost
        for weightsIndex, weights in enumerate (weightsTensor):
            for rowIndex in range (weights.shape [0]):
                for columnIndex in range (weights.shape [1]):
                    for signedGain in (-gain, gain):
                        originalWeight = weights [rowIndex, columnIndex]
                        factor = 1 + signedGain * currentCost
                        weightsTensor [weightsIndex][rowIndex, columnIndex] *= factor
                        self.classify ()
                        cost = self.cost ()
                        if cost < lowestCost:
                            lowestCost = cost
                            bestWeightsIndex = weightsIndex
                            bestRowIndex = rowIndex
                            bestColumnIndex = columnIndex
                            bestFactor = factor
                        weightsTensor [weightsIndex][rowIndex, columnIndex] = originalWeight
        weightsTensor [bestWeightsIndex][bestRowIndex, bestColumnIndex] *= bestFactor

    def train (self, trainingSet, maxCost):
        self.read (trainingSet)
        while True:
            self.classify ()
            print (int (self.cost () * 100) * '*')
            if self.cost () < maxCost:
                break
            self.correct ()
        self.report ('Training set')

    def test (self, testSet):
        self.read (testSet)
        self.classify ()
        self.report ('Test set')

neuralNet = NeuralNet (dt.outputDict)
neuralNet.train (dt.trainingSet, dt.maxCost)
neuralNet.test (dt.testSet)
