import numpy as np
import matplotlib.pyplot as plt
x = np.arange(0, 5, 0.1);
y = np.sin(x)
fig= plt.plot(x, y)
plt.ylabel( 'some numbers' )
plt.savefig(r'C:\Users\Avner\SkyDrive\NLP\BiblicalNLPworks\Graphs\1st.png')





