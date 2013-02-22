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

def dist_spike_time(train1, train2):
    '''Compute distance between two spike trains using the spike time distance metric'''
    spikes1 = detect_spikes(train1)
    spikes2 = detect_spikes(train2)
    
    n = min(len(spikes1), len(spikes2))
    p = 2
    
    dist = 1/n * sum(abs(spikes1[i] - spikes2[i])**p for i in xrange(n)) ** (1/p)
    
    # Note that m and n are reversed in relation to their names in izzy-evo.pdf
    m = max(len(train1), len(train2))
    penalty = (m - n) * len(train1) / (2 * n)
    
    return dist + penalty

def dist_spike_interval(train1, train2):
    '''Compute distance between two spike trains using the spike interval distance metric'''
    spikes1 = detect_spikes(train1)
    spikes2 = detect_spikes(train2)
    
    n = min(len(spikes1), len(spikes2))
    p = 2
    
    dist = 1/(n-1) * sum(abs((spikes1[i] - spikes1[i-1])-(spikes2[i] - spikes2[i-1]))**p for i in xrange(1,n)) ** (1/p)
    
    # Note that m and n are reversed in relation to their names in izzy-evo.pdf
    m = max(len(train1), len(train2))
    penalty = (m - n) * len(train1) / (2 * n)
    
    return dist + penalty

