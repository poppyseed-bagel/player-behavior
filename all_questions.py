import numpy as np
import math
import csv
import random
from datetime import datetime

#import cheaters.txt
def import_cheater_data(file):
    """
    Assumes file is a text file with a similar makeup to cheaters.txt
    Returns a list of lists where each list has a cheater's account id, datetime object when they started cheating,
    and datetime object when they were banned.
    """
    with open(str(file)) as data:
        cheaters_ls = []
        for line in data:
            split = line.strip().split('\t')

            #create datetime objects
            start_cheat = datetime.strptime(split[1], '%Y-%m-%d')
            ban = datetime.strptime(split[2], '%Y-%m-%d')

            cheaters_ls.append([split[0], start_cheat, ban])
        
    return(cheaters_ls)

#import teams.txt

def import_team_data(file):
    """
    Assumes file is a text file with a similar makeup to teams.txt
    Returns a list of lists where each list has a match id, player account id, and their team id match
    """
    with open(str(file)) as team_ids:
        team_ls = []
        for line in team_ids:
            split = line.strip().split('\t')

            team_ls.append(split)

    return(team_ls)

#import kills.txt
def import_kills_data(file):
    """
    Assumes file is a text file with a similar makeup to kills.txt
    Returns a list of lists where each list is a match id, killer account id, victim account id, and 
    a datetime object of when the kill happened
    """
    with open(str(file)) as kills:
        
        kills_ls = []
        for line in kills:
            split = line.strip().split('\t')

            #create datetime objects
            kill_time = datetime.strptime(split[3], '%Y-%m-%d %H:%M:%S.%f')

            kills_ls.append([split[0], split[1], split[2], kill_time])

    return(kills_ls)


#create data structure
def create_match_dic(kills_ls, account_cheaters):
    """
    Assumes kills_ls is a kills_ls of lists with each list having 4 entries. 
    Assumes account cheaters is a set with match ids and account players to correspond to those in kills_ls
    Returns a nested dictionary, populated with various variables about each match in kills_ls
    """
    #create the structure for the nested dictionary
    match_dic = {x[0]:{'observe bool':False, 'cheat bool': False, 'observable killers':[], 
                   'match start': None, 'victims':[], 'third kill': None, 
                   'killers': [], 'list of times': [],
                   'players list': [], 'event list': [], 'killer victims':{}} for x in kills_ls};
    
    #updates the dictionary with a for loop that goes through each event 
    match_dic = simple_populate_match_dic(kills_ls, match_dic)
    
    #updates the dictionary with values that required the whole dataset to be loaded (i.e. sets and min values)
    match_dic = advanced_populate_match_dic(kills_ls, match_dic, account_cheaters)
                
    return(match_dic)

#create data structure
def simple_populate_match_dic(kills_ls, match_dic):
    """
    Assumes kills_ls is a kills_ls of lists with each list having 4 entries.
    Assumes match_dic is a nested dictionary with match ids to correspond to those in kills_ls
    Returns match_dic populated with the values in kills list
    """
    
    for i in range(len(kills_ls)):

        match_id = kills_ls[i][0]
        killer_id = kills_ls[i][1]
        victim_id = kills_ls[i][2]
        time_kill = kills_ls[i][3]

        #in order to find min time for match start later
        match_dic[match_id]['list of times'].append(time_kill)

        match_dic[match_id]['victims'].append(victim_id)

        match_dic[match_id]['killers'].append(killer_id)

        match_dic[match_id]['event list'].append([time_kill, killer_id, victim_id])
        
    return(match_dic)    

#create data structure

def advanced_populate_match_dic(kills_ls, match_dic, account_cheaters):
    """
    Assumes kills_ls is a kills_ls of lists with each list having 4 entries.
    Assumes match_dic is a nested dictionary with match ids to correspond to those in kills_ls
    Assumes account cheaters is a set with match ids and account players to correspond to those in kills_ls
    Returns match_dic populated with the values that required the whole dataset to be grouped by match 
    """
    
    for key in match_dic:
    
        temp_ls = []
        
        match_dic[key]['event list'] = sorted(match_dic[key]['event list'])
        
        match_dic[key]['match start'] = min(match_dic[key]['list of times'])

        #get unique values
        match_dic[key]['victims'] = list(set(match_dic[key]['victims']))
        match_dic[key]['killers'] = list(set(match_dic[key]['killers']))

        temp_ls = (match_dic[key]['victims'] + match_dic[key]['killers'])
        match_dic[key]['players list'] = list(set(temp_ls))

        #future questions only require a match to be analyzed if at least one player in the match was even a cheater
        if any(player in set(match_dic[key]['players list']) for player in account_cheaters):
             match_dic[key]['cheat bool'] = True
                
    return(match_dic)

#for shuffling match players

def match_shuffle(players_ls):
    """
    Assumes player_ls is a list of a non-zero length
    Returns a list, the length of players list with shuffled index number
    """
    index_ls = [x for x in range(len(players_ls))]
    random.shuffle(index_ls)
    return(index_ls)

#for shuffling match players

def shuffle_player(rdm_ls, og_ls, player):
    """
    Assumes rdm_ls is a list of shuffled indexes and og_ls is the original list of player account ids
    Assumes player is a string value in og_ls
    Returns the player's shuffled counterpart according to the random index list
    """
    
    #find the player's original index
    index_player = og_ls.index(player)
    #find what number has been assigned to that index
    index_shuffle = rdm_ls[index_player]
    #find what player is in that number index in the original list
    player_shuffle = og_ls[index_shuffle]
    
    return(player_shuffle)


