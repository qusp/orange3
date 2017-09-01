import matplotlib.pyplot as plt
from pylsl import resolve_stream, StreamInlet

print('Resolving a Control stream...')
streams = resolve_stream('type', 'Control')
inlet = StreamInlet(streams[0])

hFigure, ax = plt.subplots()
plt.plot([0, 0], [-1, 1], linestyle='--', color='k')
plt.hold(True)
hbar = plt.barh(.5,0, color='kk', height=0.25, align='center')[0]
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
        hbar.set_width(sample[0]*2-1)
        hbar.axes.xaxis.get_major_locator().refresh()
        plt.xlim(xmin=-1.5, xmax=1.5)
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
    except Exception as e:
        print(e)
