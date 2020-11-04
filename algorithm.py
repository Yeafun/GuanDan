handCards = ['H2', 'H2', 'H3']
actionList = [['Single',2,['H2']], ['Single',3,['H3']],['Pair',2,['H2',"H2"]],['Pair',3,['H2',"H3"]],['Trip',3,['H2','H2','H3']]]




import collections
from random import shuffle

from typing_extensions import final

min_count = 10000
save_action = []
best_action=[]
i = 100
while(i>0):
    temp = []
    count = 0
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

   
    min_count = min(min_count, count)
    if min_count == count:
        best_action = []
        for _ in save_action:
            best_action.append(_)
    
    save_action = []
    
    i -= 1

print(best_action)
print(min_count)