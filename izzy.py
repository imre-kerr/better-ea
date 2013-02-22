from __future__ import division

def spiketrain(a, b, c, d, k, tau, ext_input, thresh, steps):
    '''Compute a spike train according to the Izhikevich model'''
    v = -60
    u = 0
    train = []
    for i in xrange(steps):
        train += [v]
        if v >= thresh:
            v = c
            u = u + d
        dv = 1/tau * (k * v**2 + 5*v + 140 - u + ext_input[i])
        du = a/tau * (b*v - u)
        v += dv
        u += du
    return train

def detect_spikes(spike_train):
    '''Detect spikes in a spike train using a sliding window of size k'''
    thresh = 0
    k = 5
    spikes = []
    for i in xrange(len(spike_train) - k + 1):
        window = spike_train[i:i+k]
        if window[k/2] == max(window) and window[k/2] > thresh:
            spikes += [window[k/2]]
    return spikes

    
