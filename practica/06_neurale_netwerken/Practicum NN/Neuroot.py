import numpy as np
import math
import random
import logging
from icecream import ic

# logging.basicConfig(level=logging.INFO)

# Create a neural network that can see the difference between a + or a 0

# Class
class Neuroot:
    """A model to check if the given shape is a cross or a circle"""

    # init
    def __init__(self):
        pass

    # Initialize bias between 0 and 1
    def initialize_bias(self):
        self.bias = random.uniform(0, 1)
        
        return self.bias

    # Initialize weight between 0 and 1
    def initialize_weightMatrix(self, size):
        self.weights = [round(random.uniform(0, 1),2) for i in range(size)]
        
        # As 1*9
        return self.weights

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
            weighted_sum += (input_matrix[j][0] * weight_matrix[j])
            weighted_sum02 += (input_matrix[j][0] * weight_matrix02[j])
            
            # The + bias part
            weighted_sum += self.bias
            weighted_sum02 += self.bias02

        # Apply softmax function and put in a list
        output_list = self.softmax([weighted_sum, weighted_sum02])
        # self.softmax()
        return output_list
    
    # Train function
    def train(self, x, y, epochs=100, learning_rate=0.1):
        y_train = y

        # Create x_train
        self.x_train = []

        # Flatten matrix + append into x_train
        for i in range(len(x)):
            logging.info(len(x))
            self.x_train.append(self.flatten(x[i]))
        logging.debug(f'Flattened: {self.x_train}')
        
        # Initialize Bias
        self.bias = self.initialize_bias()
        self.bias02 = self.initialize_bias()
        logging.debug(f'Bias: {self.bias}')
        logging.debug(f'Bias 2: {self.bias02}')

        # Initialize Weight matrix
        self.weight_matrix = self.initialize_weightMatrix(len(self.x_train[0]))
        self.weight_matrix02 = self.initialize_weightMatrix(len(self.x_train[0]))
        logging.debug(f'Weight: {self.weight_matrix}')
        logging.debug(f'Weight 2: {self.weight_matrix02}')

        # Epochs
        epochs = range(0, epochs)
        # Starting point error
        lowest_error = 9e9

        # Create error starting point
        error = 0
        counter = 0
        # Start training
        for epoch in epochs:
            counter += 1
            logging.info(f"epoch : {epoch}")

            if error < lowest_error:
                
                print(f"runs at try {counter} -> {error} < {lowest_error}")
                if error != 0:
                    lowest_error = error
                random_index = random.randrange(0,9)
                
                self.weight_matrix[random_index] = round(random.uniform(0, 1),2)
                self.previous_weight =  self.weight_matrix

                
         

                self.weight_matrix02[random_index] = round(random.uniform(0, 1),2)
                self.previous_weight02 =  self.weight_matrix02

                # self.bias = self.initialize_bias()
                # self.previous_bias = self.bias
                # self.bias02 = self.initialize_bias()
                # self.previous_bias02 = self.bias02


            else:

                self.weight_matrix = self.previous_weight
                self.weight_matrix02 = self.previous_weight02

                # self.bias = self.previous_bias
                # self.bias02 = self.previous_bias02

                random_index = random.randrange(0,9)
                
                self.weight_matrix[random_index] = round(random.uniform(0, 1),2)
                self.previous_weight =  self.weight_matrix

                self.weight_matrix02[random_index] = round(random.uniform(0, 1),2)
                self.previous_weight02 =  self.weight_matrix02

                # self.bias = self.initialize_bias()
                # self.previous_bias = self.bias
                # self.bias02 = self.initialize_bias()
                # self.previous_bias02 = self.bias02

    

            # For each inputVector
            for inputVector, label in zip(self.x_train, y_train):
                logging.debug(f"inputVector : {inputVector}")

                # Labeled output
                logging.debug(f"label : {label}")

                # Predict output
                classification = self.classify(inputVector)
                logging.debug(f"Classify : {classification}")

                # Reset error
                error = 0

                # Determine error
                for i in range(len(label)):
                    error += (-math.log2(classification[i]) * label[i])

            logging.debug(f"Weight 1 : {self.weight_matrix}")
            logging.debug(f"Weight 2 : {self.weight_matrix02}")
            logging.debug(f"Error : {error}")
            logging.debug(f'Lowest error : {lowest_error}')
    
                # update weight and b
        logging.info(f'Lowest error : {lowest_error}')        
        return self.previous_weight, self.previous_weight02

    # Input: 3x3 matrix
    # Output: 2x1 matrix
    def classify(self, input_matrix):
        
        self.input_matrix = input_matrix
        # Multiply and show outcome
        self.prediction_matrix = self.multiply(self.input_matrix, self.weight_matrix, self.weight_matrix02)
        return self.prediction_matrix
    
    # Prediction function
    def predict(self, input):
        self.weight_matrix = self.previous_weight
        self.weight_matrix02 = self.previous_weight02

        # self.bias = self.previous_bias
        # self.bias02 = self.previous_bias02

        prediction = self.classify(input)

        if prediction[0] >= 0.5:

            print(f"This is a circle! Prediction outcome: {prediction}")
        
        else:
            print(f"This is a cross! Prediction outcome: {prediction}")
        
