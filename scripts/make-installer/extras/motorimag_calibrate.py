import uuid
import time
import matplotlib
import matplotlib.pyplot as plt
import random
from pylsl import StreamInfo, StreamOutlet

num_trials = 120
warmup_trials = 20
pause_every = 30
fontsize = 30
matplotlib.rcParams.update({'font.size': fontsize})

labels = ['L', 'R']
markers = ['left', 'right']

info = StreamInfo(name='MotorImag-Markers', type='Markers', channel_count=1,
                  nominal_srate=0, channel_format='string',
                  source_id='t8u43t98u')
outlet = StreamOutlet(info)

hFigure, ax = plt.subplots()
ax.set_yticklabels([''])
ax.set_xticklabels([''])
t = plt.text(0.5, 0.5, '', horizontalalignment='center')
plt.xlim(xmin=0, xmax=1)
plt.ylim(ymin=0, ymax=1)
plt.ion()
plt.draw()
plt.show()
try:
    for trial in range(1, warmup_trials+num_trials+1):
        if not plt.fignum_exists(hFigure.number):
            break
        choice = random.choice([0, 1])
        t.set_text(labels[choice])
        if trial > warmup_trials:
            outlet.push_sample([markers[choice]])
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
        time.sleep(3)
        t.set_text('')
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
        time.sleep(1)
        if trial % pause_every == 0:
            t.set_text('Pause')
            hFigure.canvas.draw()
            hFigure.canvas.flush_events()
            time.sleep(10)
            t.set_text('')
        hFigure.canvas.draw()
        hFigure.canvas.flush_events()
except Exception as e:
    print(e)
