# Draw y = x ^ 2 - 2 in [-1, 1] 
import matplotlib.pyplot as plt
import numpy as np
x = np.arange(-5, 5, 0.01)
y = np.cos(x * x)
plt.plot(x, y, 'g')
plt.show()