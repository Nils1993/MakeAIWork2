import torch
from torch import nn

class LidarBrain(nn.Module):
    
    def __init__(self, inputs, hidden1_size, hidden2_size, outputs):
        super().__init__()

        layers = [hidden1_size, hidden2_size]

        self.model = nn.Sequential(
            nn.Linear(inputs, hidden1_size),
            nn.Linear(hidden1_size, hidden2_size),
            nn.Linear(hidden2_size, outputs)
        )


    def forward(self, x):

        return self.model(x)

