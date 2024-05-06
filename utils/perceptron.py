import numpy as np

class Perceptron:
    def __init__(self, input_size, X, y, learning_rate=0.1, seed = 0):
        """
        Perceptron simple para clasificación binaria.

        Args:
            input_size (int): Tamaño de la entrada.
            learning_rate (float): Tasa de aprendizaje.
        """
        np.random.seed(seed)

        self.input_size = input_size
        self.learning_rate = learning_rate

        self.X = np.array(X)
        self.y = np.array(y)

        self.weights = np.random.rand(input_size)
        self.bias = np.array([0.5])

        self.errors = []
        
    def hardlim(self, x):
        """
        Función de activación hardlim o escalón.
        """
        return 1 if x >= 0 else 0

    def predict(self, x):
        """
        Predicción del perceptrón, mediante:
        a = hardlim(W*x + b)
        """
        x = np.array(x[0:self.input_size])
        return self.hardlim(np.matmul(self.weights, x.T) + self.bias)

    def train(self, x, y):
        a = self.predict(x)
        self.weights += self.learning_rate * (y - a) * np.array(x)
        self.bias += self.learning_rate * (y - a)

    def frontera_decision(self):
        """
        Retorna la frontera de decisión del perceptrón de 2 categorías.
        """
        # Intercepto con el eje x
        x2 = -self.bias/self.weights[0]
        y2 = 0

        # Intercepto con el eje y
        x1 = 0
        y1 = -self.bias/self.weights[1]

        return [x1, float(y1)], [float(x2), y2]
    
    def error(self):
        """
        Calcula el error del perceptrón.
        """
        error = 0
        for i in range(len(self.X)):
            error += (self.y[i] - self.predict(self.X[i]))**2
        
        self.errors.append(error/len(self.X))
        return error/len(self.X)
    