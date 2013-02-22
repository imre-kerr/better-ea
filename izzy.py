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
