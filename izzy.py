from __future__ import division

def spiketrain(a, b, c, d, k, tau, ext_input, thresh, steps):
    '''Compute a spike train according to the Izhikevich model'''
    v = -60
    u = 0
    train = [v]
    for i in xrange(steps):
        dv = 1/tau * (k * v**2 + 5*v + 140 - u + ext_input[i])
        du = a/tau * (b*v - u)
        v += dv
        u += du
        train += [v]
        if v >= thresh:
            v = c
            u = u + d
    return train

def detect_spikes(spike_train, thresh, k):
    '''Detect spikes in a spike train using a sliding window of size k'''
    spikes = []
    for i in xrange(len(spike_train) - k + 1):
        window = spike_train[i:i+k]
        if window[k/2] == max(window) and window[k/2] > thresh:
            spikes += [k/2]
    return spikes
