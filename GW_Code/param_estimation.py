import os
import json

def pretty_print_transitions(transition_table):
    '''
    Print the transition counts for each symbol in
    an easily readable format
    '''
    side_len = len(transition_table[0])

    header_str = '  |'
    for i in range(len(transition_table[0])):
        header_str = header_str + '{:^10}'.format(i)

    border = '-' * len(header_str)

    print(header_str)
    print(border)
        

    for i in range(side_len):
        print(i, '|', end='')
        for k in range(side_len):
            print('{:10.4f}'.format(transition_table[i][k]), end='')

        print()


def pretty_print_emissions(emission_table):
    '''
    Print the emission counts for each symbol in an
    easily readable table.
    '''
    emission_len = 20
    state_len = len(emission_table)

    header_str = '  |'
    for i in range(state_len):
        header_str = header_str + '{:^10}'.format(i)

    border = '-' * len(header_str)

    print(header_str)
    print(border)

    for key in sorted(emission_table[0].keys()):
        print(key, '|', end='')        

        for i in range(state_len):
            print('{:10.4f}'.format(emission_table[i][key]), end='')

        print()
    


def read_emission_file(filename):
    '''
    Read a data file with the format

        <genome>\n
        <state_path>\n
        \n

    into a list of tuples (<genome>, <state_path>)
    '''

    paired_lines = []

    with open(filename, 'r') as f:
        i = 0
        line_pair_a = None
        line_pair_b = None


        for line in f:
            line = line.strip()
            if i == 0:
                line_pair_a = line
                i = i + 1

            elif i == 1:
                line_pair_b = line
                i += 1

            else:
                paired_lines.append((line_pair_a, line_pair_b))
                i = 0

        return paired_lines 


def count_observations(paired_lines, num_states):
    '''
    Estimate the emission probabilities and the transition
    probabilities for the vocabulary and state-to-state 
    transitions.
    '''
    # create a list of dictionaries, one dict for each state
    #   emissions will be counted in each table
    emission_table = [{} for i in range(num_states)]
    # make a num_states^2 matrix with the transitions
    #   set to 0
    transition_matrix = [[0] * num_states for i in range(num_states)]
    
    for pair in paired_lines:
        genome = pair[0]
        state_path = pair[1]

        for i in range(len(genome)):
            # count number of emissions and transitions
            curr_state = state_path[i]

            # count emission for state
            #print('\temitted', genome[i], 'from state', curr_state)
            symbol_in_keys = genome[i] in emission_table[int(curr_state)].keys()

            if symbol_in_keys:
                # increment count
                emission_table[int(curr_state)][genome[i]] += 1

            else:
                # initialize count
                emission_table[int(curr_state)][genome[i]] = 1


        prev_state = state_path[0]

        for i in range(1, len(state_path)):
            # check for transition from state to state
            curr_state = state_path[i]
            transition_matrix[int(prev_state)][int(curr_state)] += 1

            prev_state = curr_state

    #print('emission table\n', emission_table)
    #print('transition matrix\n', transition_matrix)

    return emission_table, transition_matrix


def calculate_emission_probabilities(emissions):
    # calculate probabilities for emission
    #   sum all observations for each state
    #   then divide every observation by total observations
    num_states = len(emissions)
    total_observations = [0 for i in range(num_states)]

    for i in range(num_states):
        keys = emissions[i].keys()
        emissions[i]['sum'] = 0

        for symbol in keys:
            total_observations[i] += emissions[i][symbol]

        # calculate probability
        for symbol in keys:
            if symbol is 'sum':
               continue 

            emissions[i][symbol] = (emissions[i][symbol])/total_observations[i]
            emissions[i]['sum'] += emissions[i][symbol]
            print(f'sum[{i}] +=', emissions[i][symbol], f'{symbol}=', emissions[i]['sum'])
        

    return emissions


def calculate_transition_probabilities(transitions):
    # calculate probabilities for emission
    #   sum all observations for each state
    #   then divide every observation by total observations
    num_states = len(transitions)
    total_observations = [0 for i in range(len(transitions))]

    for i in range(num_states):
        for k in range(num_states):
            total_observations[i] += transitions[i][k]

    # calculate probability
    for i in range(num_states):
        for k in range(num_states):
            #print(transitions[i][k], '/', total_observations[i], '=', end='', sep='')
            transitions[i][k] = (transitions[i][k])/total_observations[i]
            #print(transitions[i][k])
        
    return transitions


if __name__ == '__main__':
    print('readng emission file')
    paired_line_list = read_emission_file('../data/DataFile2.txt')

    emissions, transitions = count_observations(paired_line_list, 3)
    '''
    print('EMISSIONS')
    pretty_print_emissions(emissions)
    print()
    print('TRANSITIONS')
    pretty_print_transitions(transitions)
    '''
    em_prob = calculate_emission_probabilities(emissions)
    tran_prob = calculate_transition_probabilities(transitions)

    print()
    print('EMISSIONS')
    pretty_print_emissions(em_prob)
    print()
    print('TRANSITIONS')
    pretty_print_transitions(tran_prob)
