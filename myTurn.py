import collections
from random import shuffle

from typing_extensions import final



def myTurn(handCards,actionList):
    min_count = 10000
    max_bomb = 0
    save_action = []
    best_action=[]
    i = 100
    while(i>0):
        temp = []
        count = 0
        bomb_counter = 0
        for _ in handCards:
            temp.append(_)
        while(temp!=[]):
            shuffle(actionList)
            for action in actionList:
                flag = True
                action_counter = collections.Counter(action[2])
                temp_counter = collections.Counter(temp)
                for card in action[2]:
                    if card not in temp or action_counter[card] > temp_counter[card]:
                        flag = False
                if flag == True:
                    # print(action)
                    save_action.append(action)
                    for card in action[2]:
                        # print(card)
                        temp.remove(card)
                    count += 1
                    if action[0] == 'Bomb':
                        bomb_counter += 1


        min_count = min(min_count, count)
        max_bomb = max(max_bomb, bomb_counter)
        if min_count == count and max_bomb == bomb_counter:

            best_action = []
            for _ in save_action:
                best_action.append(_)
        
        save_action = []
        
        i -= 1

    return best_action