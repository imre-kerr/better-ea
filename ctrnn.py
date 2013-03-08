class CTRNN:
    '''Implements a single instance of a Beer-type Continuous-Time Recurrent Neural Network'''
    def __init__(self, num_input, num_hidden, num_output, weight_list, bias_list, gain_list, tau_list):
        '''CTRNN constructor.

        each *_list: list of floats

        weight_list format: 
          input-hidden edges (num_input * num_hidden)
          intra-hidden edges (num_hidden**2)
          hidden-output edges (num_hidden * num_output)
          intra-output edges (num_output**2)

        biases in a separate list because different ranges -> easier for development function
        bias_list format: 
          hidden biases (num_hidden)
          output biases (num_output)
          
        gain_list format:
          hidden gains (num_hidden)
          output gains (num_output)
        
        tau_list format:
          hidden taus (num_hidden)
          output taus (num_output)'''

        
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output

        self.input_nodes = range(num_input)
        self.hidden_nodes = [i + num_input for i in xrange(num_hidden)]
        self.output_nodes = [i + num_input + num_hidden for i in xrange(num_output)]
        self.bias_node = num_input + num_hidden + num_output

        num_nodes = num_input + num_hidden + num_output + 1
        self.matrix = [[0]*(num_nodes) for i in xrange(num_nodes)]

        for i in xrange(num_input):
            for j in xrange(num_hidden):
                self.matrix[self.input_nodes[i]][self.hidden_nodes[j]] = weight_list.pop(0)

        for i in xrange(num_hidden):
            for j in xrange(num_hidden):
                self.matrix[self.hidden_nodes[i]][self.hidden_nodes[j]] = weight_list.pop(0)

        for i in xrange(num_hidden):
            for j in xrange(num_output):
                self.matrix[self.hidden_nodes[i]][self.output_nodes[j]] = weight_list.pop(0)

        for i in xrange(num_output):
            for j in xrange(num_output):
                self.matrix[self.output_nodes[i]][self.output_nodes[j]] = weight_list.pop(0)

        for i in xrange(num_hidden):
            self.matrix[self.bias_node][self.hidden_nodes[i]] = bias_list.pop(0)
        
        for i in xrange(num_output):
            self.matrix[self.bias_node][self.output_nodes[i]] = bias_list.pop(0)

        self.hidden_gains = gain_list[:num_hidden]
        self.output_gains = gain_list[-num_output:]

        self.hidden_taus = tau_list[:num_hidden]
        self.output_taus = tau_list[-num_output:]

        self.hidden_states = [0] * num_hidden
        self.output_states = [0] * num_output
