import matplotlib.pyplot as plt
import pylab

from rtchange import Finder


ar_data = []
with open('./ar.tsv') as fp:
    for l in fp:
        l = l.strip()
        if l:
            ar_data.append(float(l))
ar_data = ar_data

f = Finder(discounting_param=0.1, order=2, smoothing=10)
scores = list(f.score(ar_data))

plt.figure(1)
plt.subplot(211)
plt.title("Jumping means")
plt.plot(ar_data, color='#4DB6AC')

plt.subplot(212)
plt.title("Change scores")
plt.plot(scores, color='#FF5252')

plt.show()

pylab.show()
