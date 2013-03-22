from __future__ import division
import math

class CTRNNNode:
    def __init__(self, gain=0, tau=0):
        self.parents = []
        self.weights = []
        self.gain = gain
        self.tau = tau
        self.output = 0
        self.next_output = 0
        self.y = 0
        
    def add_parent(self, parent, weight):
        '''Add a parent, duh.'''
        self.parents.append(parent)
        self.weights.append(weight)
        
    def reset(self):
        '''Reset all internal state'''
        self.output = 0
        self.next_output = 0
        self.y = 0

    def timestep(self):
        '''Compute next output level, and update internal state.
        
        Should not be used for input nodes.'''
        s = sum([self.weights[i] * self.parents[i].output for i in xrange(len(self.parents))])
        self.y += (s - self.y) / self.tau
        self.next_output = 1/(1 + math.exp(self.y*self.gain))
        
    def update_output(self):
        '''Actually update output levels. Makes sure all nodes see output from the same timestep.'''
        self.output = self.next_output
        
class CTRNN:
    '''Implements a single instance of a Beer-type Continuous-Time Recurrent Neural Network'''
    def __init__(self, num_input, num_hidden, num_output, 
                 weight_list, bias_list, gain_list, tau_list):
        '''CTRNN constructor.
        
        Order of the weight list is complicated. Check the code.'''
        # Create all the nodes 
        
        self.bias_node = CTRNNNode()
        self.bias_node.output = 1
        
        self.input_nodes = [CTRNNNode() for i in xrange(num_input)]
        
        self.hidden_nodes = []
        for i in xrange(num_hidden):
            print "Hidden node " + str(i) + " has gain " + str(gain_list[i]) + " and tau " + str(tau_list[i])
            self.hidden_nodes.append(CTRNNNode(gain_list[i], tau_list[i]))
        
        self.output_nodes = []
        for i in xrange(num_output):
            print "Output node " + str(i) + " has gain " + str(gain_list[num_hidden+i]) + " and tau " + str(tau_list[num_hidden+i])
            self.output_nodes.append(CTRNNNode(gain_list[num_hidden+i], tau_list[num_hidden+i]))
        
        # Create connections between them  
        i = 0
        for node in self.hidden_nodes:
            j = 0
            for parent in self.input_nodes:
                w = weight_list.pop()
                node.add_parent(parent, w)
                print "Hidden node " + str(i) + " has parent input node " + str(j) + " with weight " + str(w)
                j += 1
            j = 0
            for parent in self.hidden_nodes:
                w = weight_list.pop()
                node.add_parent(parent, w)
                print "Hidden node " + str(i) + " has parent hidden node " + str(j) + " with weight " + str(w)
                j += 1
            w = bias_list.pop()
            node.add_parent(self.bias_node, w)
            print "Hidden node " + str(i) + " has bias " + str(w)
            i += 1

        i = 0            
        for node in self.output_nodes:
            j = 0
            for parent in self.hidden_nodes:
                w = weight_list.pop()
                node.add_parent(parent, w)
                print "Output node " + str(i) + " has parent hidden node " + str(j) + " with weight " + str(w)
                j += 1
            j = 0
            for parent in self.output_nodes:
                w = weight_list.pop()
                node.add_parent(parent, w)
                print "Output node " + str(i) + " has parent output node " + str(j) + " with weight " + str(w)
                j += 1
            w = bias_list.pop()
            node.add_parent(self.bias_node, w)
            print "Output node " + str(i) + " has bias " + str(w)
            i += 1
            
    def reset(self):
        '''Reset internal state of each node'''
        for node in self.hidden_nodes:
            node.reset()            
        for node in self.output_nodes:
            node.reset()            
    
    def timestep(self, sensor_input):
        '''Compute new output levels for all nodes, and return output from output nodes.'''
        for i in xrange(len(sensor_input)):
            self.input_nodes[i].output = sensor_input[i]
            
        for node in self.hidden_nodes:
            node.timestep()
        for node in self.hidden_nodes:
            node.update_output()            

        for node in self.output_nodes:
            node.timestep()
        for node in self.output_nodes:
            node.update_output()
            
        return [node.output for node in self.output_nodes]