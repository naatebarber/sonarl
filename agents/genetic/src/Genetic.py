import numpy as np

class Genetic:
    def __init__(self, n_states, n_actions, depth, width, noise=None, layers=None, logits=None):
        self.n_states = n_states
        self.n_actions = n_actions
        self.width = width
        self.depth = depth
        self.noise = noise
        self.layers = layers
        self.logits = logits

    def sigmoid(self, x):
        return 1. / (1 + np.exp(-x))

    def softmax(self, x):
        e = np.exp(x - np.max(x))
        if e.ndim == 1:
            return e / np.sum(e, axis=0)
        else:
            return e / np.array([np.sum(e, axis=1)]).T

    def relu(self, x):
        return x * (x > 0)

    def tanh(self, x):
        return np.tanh(x)

    def null_activation(self, x):
        return x

    def pick_random_activation(self):
        activations = [self.sigmoid, self.softmax, self.relu, self.tanh]
        return activations[np.random.randint(0, len(activations))]

    def predict(self, state):
        if self.layers is None:
            self.layers = []
            for i in range(self.depth):
                weight_shape = None
                activ = None
                if i is 0:
                    weight_shape = [self.n_states, self.width]
                    activ = self.pick_random_activation()
                elif i is self.depth - 1:
                    weight_shape = [self.width, self.n_actions]
                    activ = self.pick_random_activation()
                else:
                    weight_shape = [self.width, self.width]
                    activ = self.pick_random_activation()

                self.layers.append({
                    "activation": activ,
                    "weight": np.random.normal(size=weight_shape),
                    "bias": None
                })         

        if self.logits is None:
            self.logits = np.random.normal(size=[1, self.width])

        prediction = state
        for i in range(self.depth):
            # print(self.layers[i]['weight'].shape)
            weighted = np.matmul(prediction, self.layers[i]['weight'])
            if self.layers[i]['bias'] is None:
                self.layers[i]['bias'] = np.random.normal(size=weighted.shape)
            prediction = self.layers[i]['activation'](np.add(weighted, self.layers[i]['bias']))
            
        # print(prediction, self.softmax(prediction))
        return self.sigmoid(prediction)

    def mutate_with_noise(self):
        for i in range(self.depth):
            layer_shape = self.layers[i]['weight'].shape
            w_mess = np.random.normal(size=layer_shape, scale=np.amax(self.layers[i]['weight']) * self.noise)
            b_mess = np.random.normal(size=layer_shape, scale=np.amax(self.layers[i]['bias']) * self.noise)
            self.layers[i]['weight'] = np.add(self.layers[i]['weight'], w_mess)
            self.layers[i]['bias'] = np.add(self.layers[i]['bias'], b_mess)
        return Genetic(self.n_states, self.n_actions, self.depth, self.width, self.noise, self.layers, self.logits)