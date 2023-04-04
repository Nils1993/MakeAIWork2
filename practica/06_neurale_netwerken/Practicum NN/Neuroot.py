import numpy as np
import random


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
        return [round(random.uniform(0, 1), 2) for i in range(size)]

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


    # Apply the math
    def multiply(self, input_matrix, weight_matrix):
        weighted_sum = 0
        for i in range(len(input_matrix)):
            weighted_sum = weighted_sum + (input_matrix[i][0] * weight_matrix[i])
        return weighted_sum
    
    def train(self, epochs=100, learning_rate=0.1):
        pass

    # Input: 3x3 matrix
    # Output: 2x1 matrix
    def classify(self, input_matrix):
            
        # Flatten input matrix
        flat_matrix = self.flatten(input_matrix)

        # Initialize bias
        bias = self.initialize_bias()
        print(f'Bias: {bias}')
        
        # Initialize weight
        weight_matrix = self.initialize_weightMatrix(len(flat_matrix))
        print(f'Weight: {weight_matrix}')
        
        # Multiply and show outcome
        prediction_matrix = self.multiply(flat_matrix, weight_matrix) + bias
        print(f'Outcome: {prediction_matrix}')
        return prediction_matrix