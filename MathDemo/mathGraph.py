import numpy as np

import matplotlib.pyplot as plt

x1 = np.arange(0, 2*np.pi, 0.01)
x2 = np.arange(0+0.001, np.pi/2-0.0001, 0.0001)
x3 = np.linspace(-4,4,100,endpoint=True)
y1 = np.sin(x1)
y2 = np.cos(x1)
y3 = np.tan(x2)
plt.plot(x1, y1)
plt.plot(x1, y2)
# plt.plot(x2, y3)
plt.plot(x3, (x3**2/9), color="black", linewidth= "5")
plt.show()