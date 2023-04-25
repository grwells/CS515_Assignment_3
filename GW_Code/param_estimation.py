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
        header_str = header_str + '{:^4}'.format(i)

    border = '-' * len(header_str)

    print(header_str)
    print(border)
        

    for i in range(side_len):
        print(i, '|', end='')
        for k in range(side_len):
            print('{:^4}'.format(transition_table[i][k]), end='')

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
        header_str = header_str + '{:^4}'.format(i)

    border = '-' * len(header_str)

    print(header_str)
    print(border)

    for key in sorted(emission_table[0].keys()):
        print(key, '|', end='')        

        for i in range(state_len):
            print('{:^4}'.format(emission_table[i][key]), end='')

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

        prev_state = state_path[0]

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


            # check for transition from state to state
            if prev_state != curr_state:
                #print('\ttransition from', prev_state, 'to', curr_state)
                transition_matrix[int(prev_state)][int(curr_state)] += 1

            prev_state = curr_state

    print('emission table\n', emission_table)
    print('transition matrix\n', transition_matrix)
    print('TRANSITIONS')
    pretty_print_transitions(transition_matrix)
    print()
    print('EMISSIONS')
    pretty_print_emissions(emission_table)


if __name__ == '__main__':
    print('readng emission file')
    paired_line_list = read_emission_file('../data/DataFile2.txt')

    count_observations(paired_line_list, 3)