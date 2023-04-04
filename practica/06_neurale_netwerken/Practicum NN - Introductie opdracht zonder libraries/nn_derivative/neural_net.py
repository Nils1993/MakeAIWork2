import data as dt
import numpy as np
import itertools as it
import time as tm

def sigmoid (x):
    return 1 / (1 + np.exp (-x))

def sigmoidDeriv (s):  # d sigmoid (x) / d x with s == sigmoid (x)
    return s * (1 - s)

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
            outputList = np.rint (output) .astype (int) .tolist ()
            try:
                print (
                    item [1],
                    self.refOutputs.T [itemIndex],
                    self.labelDict [tuple (outputList)],
                    output
                )
            except:
                print (f'Key {outputList} not found')
        print ()

    def classify (self):
        self.outputs0 = sigmoid (self.weights0 @ self.inputs)
        self.outputs = sigmoid (self.weights1 @ self.outputs0)

    def correct (self): # For each layer: weights += d sum_of_squared_corrections / d weights
        commonFactor = 2  * sigmoidDeriv (self.outputs) * (self.refOutputs - self.outputs)
        self.weights0 += sigmoidDeriv (self.outputs0) * (self.weights1.T @ commonFactor) @ self.inputs.T  
        self.weights1 += commonFactor @ self.outputs0.T  

    def train (self, trainingSet, maxCost):
        self.read (trainingSet)
        while True:
            self.classify ()
            print (int (self.cost () * 100) * '*')
            if self.cost () < maxCost:
                break
            self.correct ()
            tm.sleep (0.1)
        self.report ('Training set')

    def test (self, testSet):
        self.read (testSet)
        self.classify ()
        self.report ('Test set')

neuralNet = NeuralNet (dt.outputDict)
neuralNet.train (dt.trainingSet, dt.maxCost)
neuralNet.test (dt.testSet)
