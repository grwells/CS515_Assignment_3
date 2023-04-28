from itertools import chain
from math import log10, copysign
import pandas as pd


aminoDictionary = {'a': 0, 'r': 1, 'n': 2, 'd': 3, 'c': 4, 'q': 5, 'e': 6, 'g': 7, 'h': 8, 'i': 9,
                       'l': 10, 'k': 11, 'm': 12, 'f': 13, 'p': 14, 's': 15, 't': 16, 'w': 17, 'y': 18, 'v': 19}

#returns the number of pairs over a list of sequences as defined as P_ab and P_ba
def number_of_character_pairs_in_sequences(letterA: str, letterB: str, sequenceList: list) -> int:
    
    pairs = 0
    for i in range(0,len(sequenceList[0])):
        col = [col[i] for col in sequenceList]
        #print(col)

        if (letterA == letterB):
            # if calculate_pairs(col.count(letterA)) > 0:
            #     print("found pair in col:",i) 
            pairs += calculate_pairs(col.count(letterA))     
        else:
            # if(col.count(letterA) * col.count(letterB) > 0):
            #     print("found pair in col:",i) 

            pairs += col.count(letterA) * col.count(letterB)
    
    return pairs

#pairs are characterized by the Σ(k) from 1 to n - 1 which is characterized by (n-1^2 + n-1) / 2) 
def calculate_pairs(n : int) -> int:
    return (pow(n-1,2) + n-1 ) // 2

def round_up(x):
    return int(x + copysign(0.5, x))

def generate_scoring_matrix(filename: str) -> list:
    sequence_list = []
    sequence_length = 0
    number_of_sequences = 0
    #20x20 list filled with 0's so i can manually index.
    score_matrix = [[0 for _ in range(20)] for _ in range(20)]
    # all sequences must be the same length
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            sequence_list.append(list(line))
    #rows
    number_of_sequences = len(sequence_list)
    #Columns
    sequence_length = len(sequence_list[0])

    #pairs are characterized by the Σ(n) from 1 to the len(col) - 1 which is characterized by (n^2 + n) / 2) 
    possible_pairs = calculate_pairs(number_of_sequences)
    #possible pairs for a column multiplied by the number of columns which is the length of the sequence.
    total_possible_pairs = possible_pairs * (sequence_length)
    
    #fill the scoring matrix
    for rowKey, rowValue in aminoDictionary.items():
        for colKey, colValue, in aminoDictionary.items():
            
            #print("probability of:",rowKey, rowValue,end=" ")
            #print(colKey, colValue)

            pairs = number_of_character_pairs_in_sequences(rowKey,colKey, sequence_list)
            probability_of_pair = pairs/ total_possible_pairs

            chain_list = list(chain.from_iterable(sequence_list))

            background_freq_a = chain_list.count(rowKey)/ len(chain_list)
            background_freq_b = chain_list.count(colKey)/ len(chain_list)

            # print("probability of pair:",probability_of_pair)
            # print("background freq A:",background_freq_a)
            # print("background freq B:",background_freq_b)

            #prevent math errors. 
            if(probability_of_pair == 0 or background_freq_a == 0 or background_freq_b == 0):
                score_matrix[rowValue][colValue] = 0
            else:
                #6.25 scaling
                result = 1/0.16 * log10(probability_of_pair/(background_freq_a * background_freq_b))

                rounded = round_up(result)

                score_matrix[rowValue][colValue] = rounded 

    return score_matrix    




def main():

    score_matrix = generate_scoring_matrix("DataFile1-1.txt")
    
    #print(score_matrix)
    
    #pretty print
    df = pd.DataFrame(score_matrix,columns=list(aminoDictionary.keys()),index=list(aminoDictionary.keys()))

    print(df)

if __name__ == "__main__":
    main()
