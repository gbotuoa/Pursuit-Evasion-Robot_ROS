import numpy as np
import matplotlib.pyplot as plt
import math as m

#x=np.arange(-10,10)
x = np.linspace(-10,10,1000)
y=np.tanh(x)
yy=np.tanh(x*3)

plt.plot(x,y,label="tanh(x)")
plt.plot(x,yy,label="tanh(3x)")
#plt.xticks([1])
#plt.yticks([])
plt.grid(True, which='both')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.show()
