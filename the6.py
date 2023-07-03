# for thelow epochs values outputs differs (it is converting outputs between 00 02 22 but generally gives 02)but for bigger epoch values it generally gives the correct output.
# I think the reason of this error is convergency. I think back_pass function has some bugs but I cannot find it.
# Sometimes this is causing very similar output layer z values and giving same output.
# So I assing epoch 250 as defualt instead of 250 it is giving generally 02 output but sometimes it can be give 22 or 00 output
import random
import numpy as np


class NeuralNetwork:  # class that includes layers' node counts waight array, z valueses' value array, and for delta biases array
    def __init__(self, num_inputs, hidden_layer_sizes, num_outputs):
        self.num_inputs = num_inputs
        self.hidden_layer_sizes = hidden_layer_sizes
        self.num_outputs = num_outputs
        self.total_layer = 2 + len(hidden_layer_sizes)
        self.weights = []
        self.biases = []
        self.value = []
        self.layers = [self.num_inputs] + self.hidden_layer_sizes + [self.num_outputs]

        # initialize the weights and biases
        self.initialize_weights_deltas()

    def initialize_weights_deltas(
            self):  # initially assign a random value to weights between -0.5,0.5 and fill all deltas with 0.0

        for i in range(len(self.layers) - 1):
            weight = np.random.uniform(-0.5, 0.5, (self.layers[i + 1], self.layers[i]))
            self.weights.append(weight)
        for i in range(1, len(self.layers)):
            bias = np.random.uniform(0.0, 0.0, self.layers[i])
            self.biases.append(bias)

    def set_z_values(self, x):  # initilize the z values with given X datasets ith values
        self.value = []
        for i in range(len(x)):
            self.value.append(x[i])

    def insert_z_values(self, x):  # add new hidden layers or output layers z value to values array
        self.value.append(x)

    def calculate_layers_first_val(self,
                                   layer_idx):  # since I am keeping values as a 1D array I am finding ith layers first nodes value index
        if (layer_idx >= len(self.layers)):
            return -1
        result = 0
        for i in range(layer_idx):
            result += self.layers[i]
        return result

    def sigmoid(self, x):  # sigmoid function
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):  # derivative of sigmoid function
        a = self.sigmoid(x)
        return a * (1 - a)

    def forward_pass(self):
        """
        Perform a forward pass through the network
        """
        # for all nodes in layers starting from hidden layer to output layer(which is included) calculates z value and assing it
        for i in range(1, len(self.layers)):
            for j in range(self.layers[i]):
                # add 0 value to z value array
                self.insert_z_values(0.0)
                # get the weight of node that is coming to this node from left layer
                w = self.weights[i - 1][j]
                # take the value position of left layer
                first_val_idx = self.calculate_layers_first_val(i - 1)
                # get all the left layer z values as a list
                v = self.value[first_val_idx:(first_val_idx + self.layers[i - 1])]
                # calculate the w_(i,j)*v_i
                total = np.dot(w, v)
                # assign the value
                self.value[-1] = self.sigmoid(total)

    def get_weights_of_node(self, layer, node):  # to find the nodes all outgoing weight vaalues as an array
        w = []
        for j in range(self.layers[layer + 1]):
            w.append(self.weights[layer][j][node])
        return w

    def backward_pass(self, learning_rate):
        """
        Perform a backward pass through the network to update the weights
        """

        # Backpropagate the error through the hidden layers
        # since I calculate the delta values of output layer starting from last hidden layer to 1 calculate the delta value using the current layers node value weight calue and next layers bias value
        for i in range(len(self.layers) - 2, 0, -1):
            for j in range(self.layers[i]):
                a_j = self.value[self.calculate_layers_first_val(i) + j]
                g_prime = self.sigmoid_derivative(a_j)
                # current nodes weight value
                w = self.get_weights_of_node(i, j)
                # next layers bias value
                b = self.biases[i]
                total = np.dot(w, b)
                self.biases[i - 1][j] = total * g_prime


def update_weight(net, learning_rate):
    # updates the weight values
    for i in range(len(net.weights)):  # for all layers including weights (all layers except output layer)
        for j in range(net.layers[i]):  # all nodes of this layer
            for k in range(len(net.weights[i])):  # all nodes of next layer
                net.weights[i][k][j] += learning_rate * net.value[net.calculate_layers_first_val(i) + j] * \
                                        net.biases[i][k]  # calculate the new weight and assing it
                # biases[i] includes next layers delta


def BackPropagationLearner(X, y, net, learning_rate, epochs):
    # initialize each weight with the values min_value=-0.5, max_value=0.5,

    for epoch in range(epochs):
        # Iterate over each example
        for i in range(X.shape[0]):

            # Activate input layer in forward_pass
            net.set_z_values(X[i])
            # Forward pass
            net.forward_pass()
            # Error for the MSE cost function

            # The activation function used is sigmoid function

            # init the delta values of output layer
            for j in range(net.layers[-1]):
                a_j = net.value[-net.layers[-1] + j]
                g_prime = net.sigmoid_derivative(a_j)
                # if y= 0 for 0th output layers node error needs to be calculated as 1- calculated value(same as other unigue q values)
                if (j == y[i]):
                    y_j = 1
                else:
                    y_j = 0
                net.biases[-1][j] = g_prime * (y_j - a_j)
            # Backward pass
            net.backward_pass(learning_rate)
            #  Update weights
            update_weight(net, learning_rate)

    return net


def NeuralNetLearner(X, y, hidden_layer_sizes=None, learning_rate=0.01, epochs=1250):
    """50
    Layered feed-forward network.
    hidden_layer_sizes: List of number of hidden units per hidden layer if None set 3
    learning_rate: Learning rate of gradient descent
    epochs: Number of passes over the dataset
    activation:sigmoid
	"""
    # default hidden layer assign
    if hidden_layer_sizes is None:
        hidden_layer_sizes = [3]
    # to calculate input layer node size
    input_length = X.shape[1]
    # to calculate output layer node size
    outputh_len = len(np.unique(y))
    # iinit NeuralNetwork the class with calculated values above
    net = NeuralNetwork(input_length, hidden_layer_sizes, outputh_len)

    new_net = BackPropagationLearner(X, y, net, learning_rate, epochs)

    def predict(example):
        # activate input layer
        new_net.set_z_values(example)
        # forward pass
        new_net.forward_pass()

        # find the max node from output nodes
        prediction = np.argmax(new_net.value[-new_net.layers[-1]:])
        return prediction

    return predict


from sklearn import datasets

random.seed(0)
iris = datasets.load_iris()
X = iris.data
y = iris.target

nNL = NeuralNetLearner(X, y, hidden_layer_sizes=[3,5,2,5])
print(nNL([4.6, 3.1, 1.5, 0.2]))  # 0
print(nNL([6.5, 3., 5.2, 2.]))  # 2