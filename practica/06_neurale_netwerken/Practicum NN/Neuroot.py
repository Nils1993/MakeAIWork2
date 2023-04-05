import numpy as np
import math
import random
import logging

logging.basicConfig(level=logging.DEBUG)

# Create a neural network that can see the difference between a + or a 0

# Class
class Neuroot:
    """A model to check if the given shape is a cross or a circle"""

    # init
    def __init__(self):
        pass

    # Initialize bias between 0 and 1
    def initialize_bias(self):      
        return random.uniform(0, 1)

    # Initialize weight between 0 and 1
    def initialize_weightMatrix(self, size):
        
        # As 1*9
        return [round(random.uniform(0, 1),2) for i in range(size)]

    # transform
    def flatten(self, matrix):    
        
        # Create empty matrix
        flat_matrix = []
        # trainsform to 1*9
        prep_matrix = matrix[0] + matrix[1] + matrix[2]

        # convert to floats
        for i in range(len(prep_matrix)):
            prep_matrix[i] = float(prep_matrix[i])

        # Transform to 9*1
        for i in range(len(prep_matrix)):
            flat_matrix.append([prep_matrix[i]])

        return flat_matrix
    
    # Create softmax function
    def softmax(self, inputs):
        # MATHS
        temp = [math.exp(v) for v in inputs]
        total = sum(temp)
        return [t / total for t in temp]


    # Apply the math
    def multiply(self, input_matrix, weight_matrix, weight_matrix02):
        
        # Create variables with value 0
        weighted_sum02 = 0
        weighted_sum = 0
        for j in range(len(input_matrix)):

            # (x1*w1 + x2*w2....) + bias 
            weighted_sum = weighted_sum + (input_matrix[j][0] * weight_matrix[j])
            weighted_sum02 = weighted_sum02 + (input_matrix[j][0] * weight_matrix02[j])
            
            # The + bias part
            weighted_sum = weighted_sum + self.bias
            weighted_sum02 = weighted_sum02 + self.bias

        # Apply softmax function and put in a list
        output_list = self.softmax([weighted_sum, weighted_sum02])
        return output_list
    
    # Train function
    def train(self, x, y, epochs=100, learning_rate=0.1):
        y_train = y

        # Create x_train
        self.x_train = []

        # Flatten matrix + append into x_train
        for i in range(len(x)):
            self.x_train.append(self.flatten(x[i]))
        logging.debug(f'Flattened: {self.x_train}')
        
        # Initialize Bias
        self.bias = self.initialize_bias()
        logging.debug(f'Bias: {self.bias}')

        # Initialize Weight matrix
        self.weight_matrix = self.initialize_weightMatrix(len(self.x_train[0]))
        self.weight_matrix02 = self.initialize_weightMatrix(len(self.x_train[0]))
        logging.debug(f'Weight: {self.weight_matrix}')
        logging.debug(f'Weight 2: {self.weight_matrix02}')

        
        epochs = range(0, epochs)

        for epoch in epochs:
            logging.info(f"epoch : {epoch}")

            # For each inputVector
            for inputVector, label in zip(self.x_train, y_train):
                logging.debug(f"inputVector : {inputVector}")

                # Labeled output
                logging.debug(f"label : {label}")

                # Predict output
                prediction = self.classify(inputVector)
                logging.debug(f"prediction : {prediction}")

                # Determine error
                error = label - prediction
                logging.debug(f"error : {error}")
                # update weight and b
                if error != 0:
                    for j in inputVector:

                        deltaWeight = learning_rate * (self.weightVector + (error * j))
                        self.weightVector = self.weightVector + deltaWeight
                        logging.debug(f"deltaWeight : {deltaWeight}")
                        logging.debug(f"learning_rate : {learning_rate}")

                        deltaBias = learning_rate * (self.bias + error)
                        self.bias = self.bias + deltaBias
                        logging.debug(f"deltaBias : {deltaBias}")

    # Input: 3x3 matrix
    # Output: 2x1 matrix
    def classify(self, input_matrix):
        
        self.input_matrix = input_matrix
        # Multiply and show outcome
        self.prediction_matrix = self.multiply(self.input_matrix, self.weight_matrix, self.weight_matrix02)
        return self.prediction_matrix