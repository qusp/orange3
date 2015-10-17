import time
import matplotlib.pyplot as plt
from pylsl import ContinuousResolver, StreamInlet
width = 0.25
wait_for = 0.25
print('Resolving a Control stream...')
resolver = ContinuousResolver(prop='name', value='Control')
while len(resolver.results()) == 0:
    resolver = ContinuousResolver(prop='name', value='Control')
    time.sleep(wait_for)
info = resolver.results()[0]
inlet = StreamInlet(info)

hFigure, ax = plt.subplots()
plt.plot([0,0],[-1,1],linestyle='--',color='k')
plt.hold(True)
hbar = plt.barh([0.5, .5],[0,0], color='kk',height=0.25, align='center')[::]
plt.xlim(xmin=-1.5, xmax=1.5)
plt.ylim(ymin=0, ymax=1)
plt.ion()
plt.draw()
plt.show()
while True:
    try:
        if not plt.fignum_exists(hFigure.number):
            break
        sample, timestamp = inlet.pull_sample()
        if not timestamp:
            continue
        values = [0, 1] if sample[0] else [-1, 0]
        for vi,hi in zip(values, hbar):
            hi.set_width(vi)
            hi.axes.xaxis.get_major_locator().refresh()
        plt.xlim(xmin=-1.5, xmax=1.5)
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
    except Exception as e:
        print(str(e))
