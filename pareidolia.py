import signal
import pyev
import getface

def sig_cb(watcher, revents):
    print("got SIGINT")
    loop = watcher.loop
    # unloop all nested loop
    loop.stop(pyev.EVBREAK_ALL)

def timer_cb(watcher, revents):
    loop.data.look_for_faces()    

if __name__ == "__main__":
    get_face = getface.GetFace()
    loop = pyev.default_loop(data=get_face)
    # initialise and start a repeating timer
    timer = loop.timer(0, 2.0, timer_cb, 0)
    timer.start()
    # initialise and start a Signal watcher
    sig = loop.signal(signal.SIGINT, sig_cb)
    sig.start()
    # now wait for events to arrive
    loop.start()
