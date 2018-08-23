import numpy as np
import matplotlib.pyplot as plt


def outer(vecA, vecB):
    return np.outer(vecA, vecB)
    

def inner(matrix, vec):
    return matrix.dot(vec)
    


class NN:

    def __init__(self, layerSizes):
        nrLayers = len(layerSizes) - 1
        self.L = nrLayers - 1 # we count from 0
        self.x = [0] * nrLayers
        self.W = [0] * nrLayers
        self.b = [0] * nrLayers
        self.y = [0] * nrLayers
        self.dEdx = [0] * nrLayers
        self.dEdW = [0] * nrLayers
        self.dEdb = [0] * nrLayers
        for l in range(0, self.L+1): # range is exclusive last value
            f = layerSizes[l]
            t = layerSizes[l+1]
            self.W[l] =  np.random.rand(t, f)
            self.b[l] = np.random.rand(t)



    def actFct(self, x):
        return 1. / (1. + np.exp(x))


    def diffAct(self, x):
        return np.exp(-x) / (1. + np.exp(-x))**2


    def predict(self, inpt):
        # 1.1.  First Layer
        self.x[0] = inner(self.W[0], inpt) + self.b[0]
        self.y[0] = self.actFct(self.x[0])

        # 1.2.  Higher layers
        for l in range(1, self.L+1): # range is exclusive last value
            self.x[l] = inner( self.W[l], self.y[l-1] ) + self.b[l]
            self.y[l] = self.actFct(self.x[l])
        
        return self.y[self.L]


    def backprop(self, target):
        # 2.1.  Top Layer
        self.dEdx[self.L] = (target - self.y[self.L]) * self.diffAct(self.x[self.L])
        self.dEdW[self.L] = outer( self.dEdx[self.L], self.y[self.L-1])
        self.dEdb[self.L] = self.dEdx[self.L]

        # 2.2.  Lower layers
        for l in range(self.L-1, -1, -1): # range is exclusive last value
            self.dEdx[l] = inner(self.dEdx[l+1], self.W[l+1]) * self.diffAct(self.x[l])
            self.dEdW[l] = outer( self.dEdx[l], self.y[l-1] )
            self.dEdb[l] = self.dEdx[l]
        
        return (self.dEdW, self.dEdb)

        
    def training(self, inputs, targets, decay):

        alpha = 1
        outs = []
        offBy = []
        alphas = []

        for s in range(len(inputs)):
            print "now training on {}th sample with alpha = {}".format(s, alpha)

            inpt = inputs[s]
            target = targets[s]

            output = self.predict(inpt)
            (dEdW, dEdb) = self.backprop(target)

            for l in range(self.L + 1): # range is eclusive last value
                self.W[l] -= alpha * dEdW[l]
                self.b[l] -= alpha * dEdb[l]
            
            alpha = decay(alpha)

            print "Training result: should be {}, is {}".format(target, output)
            outs.append(output[0])
            offBy.append(abs(target - output))
            alphas.append(alpha)
        
        plt.plot(outs)
        plt.plot(offBy)
        plt.plot(alphas)
        plt.show()





inputs = []
targets = []
for i in range(10000):
    a = np.random.randint(2)
    b = np.random.randint(2)
    o = [(a+b)%2]
    inputs.append([a, b])
    targets.append(o)

nn = NN([2, 4, 1])
nn.training(inputs, targets, lambda a  : a*0.999)
print nn.predict([1,0])