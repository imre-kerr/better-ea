import ctrnn
import min_cog_game

if __name__ == "__main__":
    gtype = input()

    num_input = 5
    num_hidden = 2
    num_output = 2

    num_weights = num_hidden*(num_input + num_hidden) + num_output*(num_hidden + num_output)
    num_biases = num_hidden + num_output
    num_gains = num_hidden + num_output
    num_taus = num_hidden + num_output
    
    i = 0
    weight_list = gtype[i:i+num_weights]
    i += num_weights
    bias_list = gtype[i:i+num_biases]
    i += num_biases
    gain_list = gtype[i:i+num_gains]
    i += num_gains
    tau_list = gtype[i:i+num_taus]
    
    agent = ctrnn.CTRNN(num_input, num_hidden, num_output, 
                            weight_list, bias_list, gain_list, tau_list)
    
    game = min_cog_game.Game()
    game.play(agent, True)
