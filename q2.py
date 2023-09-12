import numpy as np
import math
import csv
import random
from datetime import datetime
import all_questions

#q2 main code

def q2_count(kills_ls, account_cheaters, cheater_dic, match_dic):
    """
    Assumes kills_ls is a list of lists where each list has 4 values
    Assumes account_cheaters is a set where account ids correspond to teams_ls
    Assumes cheater_dic is a dictionary to lookup when a cheater starts cheating
    Assumes match_dic is a nested dictionary, populated with various variables about each match in kills_ls
    Returns an int count of the number of cheaters who started cheating after being killed by a cheater
    """
    
    count = 0
    for i in range(len(kills_ls)):
        match_id = kills_ls[i][0]
        killer = kills_ls[i][1]
        victim = kills_ls[i][2]
        timekill = kills_ls[i][3]
        match_start = match_dic[match_id]['match start']

        #do both parties ever cheat
        if killer in account_cheaters and victim in account_cheaters:
            #need if statement because otherwise these will cause an error
            killer_start = cheater_dic[killer]
            victim_start = cheater_dic[victim]

            #is the killer a cheater at the time, does the killed become a cheater after
            if killer_start < match_start and victim_start > timekill:
                count += 1
            
    return(count)

#q2 shuffle

def q2_shuffle(match_dic, account_cheaters, cheater_dic):
    """
    Assumes match_dic is a nested dictionary, populated with various variables about each match in kills_ls
    Assumes account_cheaters is a set where account ids correspond to match_dic
    Assumes cheater_dic is a dictionary to lookup when a cheater starts cheating
    Returns an int count of the number of cheaters who started cheating after being killed by a cheater
        where the killer and victim have been randomized.
    """
    count = 0
    for key in match_dic:
        
        if match_dic[key]['cheat bool'] == True:
            
            #generate the shuffled players list for this match
            players_ls = match_dic[key]['players list']
            num_ls = all_questions.match_shuffle(players_ls)
            event_list = match_dic[key]['event list']
            match_start = match_dic[key]['match start']
            
            #go through the match events in chronological order
            for event in event_list:
                timekill = event[0]
                killer = event[1]
                victim = event[2]
                
                #reassign the killer and victim to their random counterparts
                killer_shuffle = all_questions.shuffle_player(num_ls, players_ls, killer)
                victim_shuffle = all_questions.shuffle_player(num_ls,players_ls, victim)

                #are both the killer and the victim ever cheaters?
                if killer_shuffle in account_cheaters and victim_shuffle in account_cheaters:
                    killer_start = cheater_dic[killer_shuffle]
                    victim_start = cheater_dic[victim_shuffle]

                    #is the killer a cheater at the time, does the killed become a cheater after
                    if killer_start < match_start and victim_start > timekill:
                        count += 1
            
    return(count)

#q2 output

def q2_shuffle_output(match_dic, account_cheaters, cheater_dic, n):
    """
    Assumes match_dic a nested dictionary, populated with various variables about each match in kills_ls
    Assumes account_cheaters is a set where account ids correspond to match_dic
    Assumes cheater_dic is a dictionary to lookup when a cheater starts cheating
    Assumes n is an integer with the number of times you want to shuffle
    Returns print statements with the mean and 95% confidence interval of the random shuffling
    """
    
    n_list = []
    
    #shuffle the data n times
    for i in range(n):
        #keep track of each repitition
        n_list.append(q2_shuffle(match_dic, account_cheaters, cheater_dic))
        
    n_array = np.array(n_list)
    sd = np.std(n_array)
    mean = np.mean(n_array)
    
    #calculate confidence intervals and format output
    minus_ci =  format(mean - (1.96*sd), '.2f')
    plus_ci = format(mean + (1.96*sd), '.2f')
    
    print("The mean number of players who start cheating after being killed by a cheater when players are randomized is: ", mean, "The mean has a 95% confidence interval of", minus_ci, 'to', plus_ci)
    return