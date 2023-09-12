import numpy as np
import math
import csv
import random
from datetime import datetime
import all_questions

#set up q1
def create_unique_match_teams(team_ls):
    """
    Assumes teams_ls is a list of lists where each list has 3 values
    Returns a list of tuples with the unique value of match, team pairs
    """
    match_teams = [(x[0], x[2]) for x in team_ls]
    unique_match_teams = list(set(match_teams))
    
    return(unique_match_teams)

def populate_dict(team_ls, tuple_ls, account_cheaters):
    """
    Assumes teams_ls is a list of lists where each list has 3 values
    Assumes tuple_ls is a list of tuples where each tuple is a unique match, team pair
    Assumes account_cheaters is a set where account ids correspond to teams_ls
    Returns a dictionary where the keys are the tuples from tuples_ls, populated with cheating player ids
    """
    
    team_match_dic = {x:[] for x in tuple_ls}
    
    for i in range(len(team_ls)):
    
        match_id = team_ls[i][0]
        player_id = team_ls[i][1]
        team_id = team_ls[i][2]

        if player_id in account_cheaters:

            #create dictionary of all cheaters in a team in a specific match
            team_match_dic[(match_id, team_id)].append(player_id)

    return(team_match_dic)

def populate_cheater_dic(team_ls, tuple_ls, account_cheaters):
    """
    Assumes teams_ls is a list of lists where each list has 3 values
    Assumes tuple_ls is a list of tuples where each tuple is a unique match, team pair
    Assumes account_cheaters is a set where account ids correspond to teams_ls
    Returns a dictionary where the keys are match_ids, populated with the team id and player of cheaters in a match
    """
    match_cheater_team_dic = {x[0]:[] for x in tuple_ls}
    
    for i in range(len(team_ls)):
    
        match_id = team_ls[i][0]
        player_id = team_ls[i][1]
        team_id = team_ls[i][2]

        if player_id in account_cheaters:
            match_cheater_team_dic[match_id].append([team_id, player_id])
            
    return(match_cheater_team_dic)

#count cheaters
def q1_count(counter_dic, team_match_dic):
    """
    Assumes counter dic is a dictionary with int keys and zero/none values
    Assumes team_match_dic has been populated by the function populate_dic
    Returns a dictionary with estimate how often cheaters end up on the same team
    """
    
    for value in team_match_dic.values():
        
        #count how many cheaters are on a team in a match
        num_cheaters = len(value)
        counter_dic[num_cheaters] +=1
        
    return(counter_dic)

#print output
def q1_output(counter_dic):
    """
    Assumes counter_dic is a dictionary with estimate how often cheaters end up on the same team
    Returns print statements for each count value pair
    """
    for key in counter_dic:
        print(counter_dic[key], 'amount of teams have', key, 'cheaters on the team.')
    return

#set up shuffle
def create_shuffle_dic(team_ls, tuple_ls):
    """
    Assumes teams_ls is a list of lists where each list has 3 values
    Assumes tuple_ls is a list of tuples where each tuple is a unique match, team pair
    Returns a dictionary where the key is the match id and the values are all teams in that match ever
    in order to randomly assign teams in a match later on.
    """
    
    match_shuffle_dic = {x[0]:[] for x in tuple_ls}
    
    for i in range(len(team_ls)):

        match_id = team_ls[i][0]
        player_id = team_ls[i][1]
        team_id = team_ls[i][2]

        match_shuffle_dic[match_id].append(team_id)
    
    return(match_shuffle_dic)

#do shuffle
def q1_shuffle(shuffle_dic, counter_dic, match_cheater_team_dic, tuple_ls):
    """
    Assumes shuffle_dic is the output of the shuffle_dic function
    Assumes counter_dic is a dictionary with int keys and zero/none values
    Assumes match_dic is the output of the populate_cheater_dic function
    Assumes tuple_ls is a list of tuples where each tuple is a unique match, team pair
    Returns a dictionary with estimate how often cheaters end up on the same team when teams are randomized
    """
    team_match_dic = {x:[] for x in tuple_ls}

    for match in match_cheater_team_dic:

        shuffle_ls = list(set(shuffle_dic[match]))

        for i in range(len(match_cheater_team_dic[match])):

            player_id = match_cheater_team_dic[match][i][1]
            #give every cheater a random team
            random_team = random.choice(shuffle_ls)

            team_match_dic[(match, random_team)].append(player_id)

    counter_dic = q1_count(counter_dic, team_match_dic)
            
    return(counter_dic)

#repeat shuffle and retain info
def repeat_n(counter_dic, match_cheater_team_dic, tuple_ls, team_ls,  n):
    """
    Assumes counter_dic is a dictionary with int keys and zero/none values
    Assumes a dictionary where the keys are match_ids, populated with the team id and player of cheaters in a match
    Assumes tuple_ls is a list of tuples where each tuple is a unique match, team pair
    Assumes teams_ls is a list of lists where each list has 3 values
    Assumes n is an integer with the number of times you want to shuffle
    Returns 3 lists of length(counter_dic) with the mean of the repeated trials, and each mean's 95% confidence interval
    lower and upper bounds.
    """
    shuffled_dic = create_shuffle_dic(team_ls, tuple_ls)
    
    ls = []
    
    #shuffle the data n times
    for i in range(n):
        #reset dictionary each time for mean count
        counter_dic = {x:0 for x in counter_dic.keys()}
        output = list(q1_shuffle(shuffled_dic, counter_dic, match_cheater_team_dic, tuple_ls).values())
        
        #keep track of each repitition
        ls.append(output)
        
    arr = np.array(ls)
    mean_arr = np.mean(arr, axis = 0)
    sd = np.std(arr, axis = 0)
    
    minus_int = []
    plus_int = []
    mean = []
    
    #calculate confidence intervals and format output
    for i in range(len(mean_arr)):
        
        mean.append(format(mean_arr[i], '.2f'))
        
        minus = mean_arr[i] - (1.96*sd[i])
        minus_int.append(format(minus, '.2f'))
        
        plus = mean_arr[i] + (1.96*sd[i])
        plus_int.append(format(plus, '.2f'))
    
    return(mean, minus_int, plus_int)

#shuffle output
def q1_shuffle_output(counter_dic, mean_ls, minus_ls, plus_ls):
    """
    Assumes counter_dic is a dictionary with positive ints in increasing order
    Returns print statements for each count value pair and the 95% confidence interval of the random shuffling
    """
    print("When players are randomized: ")
    for key in counter_dic:
        print(mean_ls[key], 'amount of teams have', key, 'cheaters on the team.')
        print("The 95% confidence interval for this stat is from" , minus_ls[key] , "to" , plus_ls[key])
        
    return
