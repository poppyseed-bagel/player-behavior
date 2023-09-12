import numpy as np
import math
import csv
import random
from datetime import datetime
import all_questions


#q3 main setup

def q3_count(match_dic, account_cheaters, cheater_dic):
    """
    Assumes match_dic is a nested dictionary, populated with various variables about each match in kills_ls
    Assumes account_cheaters is a set where account ids correspond to match_dic
    Assumes cheater_dic is a dictionary to lookup when a cheater starts cheating
    Returns how many players observed an active cheater on at least one occasion and then started cheating.
    """
    
    q3_list = []
    
    #for each match
    for key in match_dic:
    
        #if there is ever a cheater in that match
        if match_dic[key]['cheat bool'] == True:

            observe = []
            event_list = match_dic[key]['event list']
            match_start = match_dic[key]['match start']
            third_kill = None

            #go through all events chronologically
            for event in event_list:

                timekill = event[0]
                killer = event[1]
                victim = event[2]

                #if the killer was an active cheater in that match
                if killer in account_cheaters:
                    killer_start = cheater_dic[killer]

                    if killer_start <= match_start:
                        
                        #create a dictionary entry for the killer and their victims in this match
                        if killer not in match_dic[key]['killer victims']:
                            match_dic[key]['killer victims'][killer] = [[timekill, victim]]
                        
                        #add onto an existing dictionary entry for the killer and their victims in this match
                        else:
                            match_dic[key]['killer victims'][killer].append([timekill, victim])

                            #the first cheating killer to kill three people
                            if len(match_dic[key]['killer victims'][killer]) == 3:
                                third_kill = match_dic[key]['killer victims'][killer][2][0]

                #if a victim died after the third kill in a match with an observable cheater
                if third_kill != None and timekill > third_kill:
                    observe.append(victim)
                    
            #check if that victim becomes a cheater after the match 
            for player in observe: 
                if player in account_cheaters:
                    player_start = cheater_dic[player]

                    if player_start > match_start:
                        q3_list.append(player)
                        
    #find the unique number of players who observed an active cheater and then started cheating.
    q3_counter = len(set(q3_list))
                
    return(q3_counter)

#q3 shuffle

def q3_shuffle(kills_ls, match_dic, account_cheaters, cheater_dic):
    """
    Assumes kills_ls is a list of lists where each list has four values
    Assumes match_dic match_dic is a nested dictionary, populated with various variables about each match in kills_ls
    Assumes account_cheaters is a set where account ids correspond to match_dic
    Assumes cheater_dic is a dictionary to lookup when a cheater starts cheating
    Returns how many players observed an active cheater on at least one occasion and then started cheating
        where the killer and victim have been randomized.
    """
    #create a dictionary to store killer/victim counts based off of randomized shuffling
    killer_victim_dic = {x[0]:{'killer victims':{}} for x in kills_ls}
    count_list = []
    counter = 0
    
    #for each match
    for key in match_dic:
        
        #if there is ever a cheater in that match
        if match_dic[key]['cheat bool'] == True:
            
            #generate the shuffled players list for this match
            players_ls = match_dic[key]['players list']
            num_ls = all_questions.match_shuffle(players_ls)
            
            observe = []
            event_list = match_dic[key]['event list']
            match_start = match_dic[key]['match start']
            third_kill = None
            
            #go through all events chronologically
            for event in event_list:

                timekill = event[0]
                killer = event[1]
                victim = event[2]
                
                #assign the killer / victim their shuffled player
                killer_shuffle = all_questions.shuffle_player(num_ls, players_ls, killer)
                victim_shuffle = all_questions.shuffle_player(num_ls,players_ls, victim)
                
                #if the killer was an active cheater in that match
                if killer_shuffle in account_cheaters:
                    killer_start = cheater_dic[killer_shuffle]

                    if killer_start <= match_start:
                        
                        #create a dictionary entry for the killer and their victims in this match
                        if killer_shuffle not in killer_victim_dic[key]['killer victims']:
                            killer_victim_dic[key]['killer victims'][killer_shuffle] = [[timekill, victim_shuffle]]
                        
                        #add onto an existing dictionary entry for the killer and their victims in this match
                        else:
                            killer_victim_dic[key]['killer victims'][killer_shuffle].append([timekill, victim_shuffle])

                            #the first cheating killer to kill three people
                            if len(killer_victim_dic[key]['killer victims'][killer_shuffle]) == 3:
                                third_kill = killer_victim_dic[key]['killer victims'][killer_shuffle][2][0]

                #if a victim died after the third kill in a match with an observable cheater
                if third_kill != None and timekill > third_kill:
                    observe.append(victim_shuffle)
            
            #check if that victim becomes a cheater after the match
            for player in observe: 
                if player in account_cheaters:
                    player_start = cheater_dic[player]

                    if player_start > match_start:
                        count_list.append(player) 
                       
    counter = len(set(count_list))
                    
    return(counter)

#q3 shuffle output
def q3_shuffle_output(kills_ls, match_dic, account_cheaters, cheater_dic, n):
    """
    Assumes kills_ls is a list of lists where each list has four values
    Assumes match_dic a nested dictionary, populated with various variables about each match in kills_ls
    Assumes account_cheaters is a set where account ids correspond to match_dic
    Assumes cheater_dic is a dictionary to lookup when a cheater starts cheating
    Assumes n is an integer with the number of times you want to shuffle
    Returns print statements with the mean and 95% confidence interval of the random shuffling
    """
    #shuffle the data n times
    n_list = []
    for i in range(n):
        #keep track of each repitition
        n_list.append(q3_shuffle(kills_ls, match_dic, account_cheaters, cheater_dic))
        
    n_array = np.array(n_list)
    sd = np.std(n_array)
    mean = np.mean(n_array)
    
    #calculate confidence intervals and format output
    minus_ci = format(mean - (1.96*sd), '.2f')
    plus_ci = format(mean + (1.96*sd), '.2f')
    
    print("The mean number of players who start cheating after observing an active cheater on at least one occasion when players are randomized is: " + str(mean) + " The mean has a 95% confidence interval of " + str(minus_ci) + ' to ' + str(plus_ci))
    
    return 