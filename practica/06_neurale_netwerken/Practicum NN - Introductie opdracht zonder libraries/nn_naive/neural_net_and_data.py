# ====== Legal notices
#
# Copyright 2017 Jacques de Hooge, GEATEC engineering, www.geatec.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

# Define dimensions

nrOfRows = 3
nrOfColumns = 3
nrOfSymbols = 2

# Define general constants

weightGain = 0.005
costThreshold = 0.1

# Define relevant functions

def softMax (inVec):
    # Apply non-linear function to individual components and normalize, i.e. make the sum of the actual outputs == 1
    # By normalizing the outputs they can be compared to the desired outputs in a scale-invariant way by the cost function
    # Note that the sum of the reference outputs also == 1
    # Combined with a sum-of-squares cost function, a cost threshold between 0 and 1 will be the right order of magnitude
    expVec = [math.exp (inScal) for inScal in inVec]
    aSum = sum (expVec)
    return [expScal / aSum for expScal in expVec]

def costFunc (outVec, modelVec):
    # Compute sum of squared component errors
    # This can in many cases be interpreted as error energy, which is in many fields a popular error measure
    return sum ([(lambda x: x * x) (zipped [0] - zipped [1]) for zipped in zip (outVec, modelVec)])
    
# Define flow graph elements    
    
class Node:
    def __init__ (self):
        self.inLinks = []
        self.value = None
    
    def __call__ (self):
        if self.inLinks:
            # Compute value if there are input links, if there aren't assume it's an input node, whose value is explicitly set
            self.value = sum ([inLink () for inLink in self.inLinks])
            
        return self.value
    
class Link:
    def __init__ (self, inNode = None, outNode = None):
        self.inNode = inNode
        outNode.inLinks.append (self)
        
        self.weight = 1
        
    def adaptWeight (self, cost):
        self.weight += weightGain * cost * self.weight
    
    def __call__ (self):
        return self.weight * self.inNode ()

# Instantiate 2 layers of nodes        
    
inNodes = [[Node () for iColumn in range (nrOfColumns)] for iRow in range (nrOfRows)]  
outNodes = [Node () for iSymbol in range (nrOfSymbols)]

# Build dataflow graph by connecting the nodes with links

links = []
for inRow in inNodes:
    for inNode in inRow:
        for outNode in outNodes:
            links.append (Link (inNode, outNode))

# Define symbols

symbolVecs = {'O': (1, 0), 'X': (0, 1)}
symbolChars = dict ((value, key) for key, value in symbolVecs.items ())           
          
# Define datasets (training set should normally be much larger than test set for best results)
          
trainingSet = (
    ((
        (1, 1, 1),
        (1, 0, 1),
        (1, 1, 1)
    ), 'O'),
    ((
        (0, 1, 0),
        (1, 0, 1),
        (0, 1, 0)
    ), 'O'),
    ((
        (0, 1, 0),
        (1, 1, 1),
        (0, 1, 0)
    ), 'X'),
    ((
        (1, 0, 1),
        (0, 1, 0),
        (1, 0, 1)
    ), 'X')
)

testSet = (
    ((
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0)
    ), 'O'),
    ((
        (1, 0, 1),
        (1, 0, 1),
        (1, 1, 0)
    ), 'O'),
    ((
        (1, 0, 0),
        (1, 1, 1),
        (0, 0, 1)
    ), 'X'),
    ((
        (0, 0, 1),
        (1, 1, 1),
        (1, 0, 0)
    ), 'X')
)

# Compute average cost over all training items, with current weights

def computeAverageCost ():
    # Init accumulated cost
    accumulatedCost = 0
   
    # Accumulate cost over all training items
    for trainingItem in trainingSet:
    
        # Set input values for current trainingItem       
        for iRow in range (nrOfRows):
            for iColumn in range (nrOfColumns):
                inNodes [iRow][iColumn] .value = trainingItem [0][iRow][iColumn]
                
        # Accumulate cost, so compute sum of "error energy" over whole training set
        accumulatedCost += costFunc (softMax ([outNode () for outNode in outNodes]), symbolVecs [trainingItem [1]])
        
    # Divide accumulated cost by nr of training items to obtain average cost per training item
    # This makes the accumulated cost scale invariant with respect to the size of the training
    # Since the cost per training item <= 1, the average cost will be <= 1 
    return accumulatedCost / len (trainingSet)
    
# Learn with the aid of training set
    
averageCost = computeAverageCost ()
iterationIndex = 0
while averageCost > costThreshold:
    bestCostIncrease = 0
    bestLink = None
    
    # Try to adjust the most effective link weight (so no steepest descent, but just most 'sensitive' weight)
    for link in links:
        # Vary one weight
        link.adaptWeight (averageCost)
        
        newAverageCost = computeAverageCost ()
        costIncrease = newAverageCost - averageCost
       
        if abs (costIncrease) > abs (bestCostIncrease):
            bestCostIncrease = costIncrease
            bestLink = link
            
        # Undo weight variation (and go on varying next weight)          
        link.adaptWeight (-averageCost)
      
    # Apply most effective weight variation, but in the right direction
    bestLink.adaptWeight (-averageCost if bestCostIncrease > 0 else averageCost)
    averageCost = computeAverageCost ()
    print ('Iteration:', iterationIndex + 1, 'Average cost:', averageCost)
    
    iterationIndex += 1
    
# Apply what has been learned to test set
    
for testItem in testSet:
    # Set input values for current testItem       
    for iRow in range (nrOfRows):
        for iColumn in range (nrOfColumns):
            inNodes [iRow][iColumn] .value = testItem [0][iRow][iColumn]

    outVec = softMax ([outNode () for outNode in outNodes])
    print ('Offered as:', testItem [1], 'Reconstructed as:', symbolChars [(round (outVec [0]), round (outVec [1]))], ', probabilities : ', outVec)