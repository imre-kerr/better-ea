from __future__ import division
import math

class CTRNNNode:
    def __init__(self, gain=0, tau=0):
        self.parents = []
        self.weights = []
        self.gain = gain
        self.tau = tau
        self.internal_state = 0
        self.output = 0
        self.next_output = 0
        self.y = 0
        
    def add_parent(self, parent, weight):
        '''Add a parent, duh.'''
        self.parents.append(parent)
        self.weights.append(weight)

    def timestep(self):
        '''Compute next output level, and update internal state.
        
        Should not be used for input nodes.'''
        s = 0
        for i, parent in enumerate(self.parents):
            s += self.weights[i] * parent.output
        self.y += (-self.y + s) / self.tau
        self.next_output = 1/(1 + math.e**(self.y*self.gain))
        
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
            self.hidden_nodes.append(CTRNNNode(gain_list[i], tau_list[i]))
        
        self.output_nodes = []
        for i in xrange(num_output):
            self.output_nodes.append(CTRNNNode(gain_list[num_hidden+i], tau_list[num_hidden+i]))
        
        # Create connections between them  
        
        for node in self.hidden_nodes:
            for parent in self.input_nodes:
                node.add_parent(parent, weight_list.pop())
            for parent in self.hidden_nodes:
                node.add_parent(parent, weight_list.pop())
            node.add_parent(self.bias_node, bias_list.pop())
                
        for node in self.output_nodes:
            for parent in self.hidden_nodes:
                node.add_parent(parent, weight_list.pop())
            for parent in self.output_nodes:
                node.add_parent(parent, weight_list.pop())
            node.add_parent(self.bias_node, bias_list.pop())
            
            
    def timestep(self, sensor_input):
        '''Compute new output levels for all nodes, and return output from output nodes.'''
        for i, value in enumerate(sensor_input):
            self.input_nodes[i].output = value
            
        for node in self.hidden_nodes:
            node.timestep()
        for node in self.hidden_nodes:
            node.update_output()            

        for node in self.output_nodes:
            node.timestep()
        for node in self.output_nodes:
            node.update_output()
            
        return [node.output for node in self.output_nodes]