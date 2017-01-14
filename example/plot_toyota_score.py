import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pylab

from rtchange import Finder


toyota_date_data = []
toyota_closing_price_data = []
with open('./toyota.csv') as fp:
    for l in fp:
        l = l.strip()
        if l:
            splitted = l.split(',')
            toyota_date_data.append(
                dt.datetime.strptime(splitted[0], '%Y-%m-%d').date())
            toyota_closing_price_data.append(float(splitted[1]))

f = Finder(discounting_param=0.2, order=3, smoothing=3)
scores = list(f.score(toyota_closing_price_data))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.figure(1)
plt.subplot(211)
plt.title("TOYOTA stock prices")
plt.plot(toyota_date_data, toyota_closing_price_data, color='#4DB6AC')

plt.subplot(212)
plt.title("Change scores")
plt.plot(toyota_date_data, scores, color='#FF5252')

plt.show()

pylab.show()
