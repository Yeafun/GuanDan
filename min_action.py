

from random import randint
from time import sleep
# 中英文对照表
ENG2CH = {
    "Single": "单张",
    "Pair": "对子",
    "Trips": "三张",
    "ThreePair": "三连对",
    "ThreeWithTwo": "三带二",
    "TwoTrips": "钢板",
    "Straight": "顺子",
    "StraightFlush": "同花顺",
    "Bomb": "炸弹",
    "PASS": "过"
}


class Action(object):

    def __init__(self):
        self.action = []
        self.act_range = -1

    def parse(self, msg):
        self.action = msg["actionList"]
        self.act_range = msg["indexRange"]
        # print(self.action)
      
        # print("可选动作范围为：0至{}".format(self.act_range))

        # print("最大到你工作是{}".format(self.state._greaterAction))
        
        def countCard(card):
            '''
            数牌，看手牌中牌有多少张
            input: card -> String
            return: number -> int
            '''
            count = 0
            handCards = self.state._handCards
            for c in handCards:
                if c[-1] == card:
                    count += 1
            
            return count

        
        # 还贡给单张
        
        if msg["stage"] == "back" and msg["type"] == "act":
            # from myTurn import myTurn
            # best_action = myTurn(self.state._handCards, self.action)
            # for i,a in enumerate(self.action):
            #     for action in best_action:
            #         if action[0]=='Single':
                        
            #                 if a == action:
            #                     print(a)
            #                     return i
            # return 0



            for i,a in enumerate(self.action):
                if countCard(a[2][0][-1]) == 1:
                    return i
            return 0

        if self.act_range > 0:
            
            reserve_card = [] # 需要保留的牌
            for i,action in enumerate(self.action):
                # 记录炸弹的牌型
                if 'Bomb' in action:
             
                    reserve_card.append(self.action[i][1])
            
            # 逢人配
            heart_rank = []
            for card in self.state._handCards:
                if card == 'H'+self.state._curRank:
                    heart_rank.append(card)

            def partBomb(choose):
                # 当选出的牌型中用到了组成炸弹的牌
                for i in range(len(self.action[choose][2])):
                    if self.action[choose][2][i][-1] in reserve_card:
                        return True 
                return False

            def findSingle():
                '''
                return card ——> String
                '''
                # 找到最小的单张的牌
                for c in self.state._handCards:
                    if countCard(c[-1]) == 1:
                        return c[-1]
                return 0

            def findHeart(choose):
                if heart_rank:
                    for i in range(len(self.action[choose][2])):
                        if self.action[choose][2][i] == heart_rank[0]:
                            return True
                return False

            def allBomb(choose):
                if self.action[choose][0] == "Bomb":
                    cards_number = countCard(self.action[choose][1])
                    bomb_number  = len(self.action[choose][2])
                    if cards_number > bomb_number:
                        return False
                return True

            def bomb():
                # 选择一个合适的炸弹
                choose = 0
                for i,action in enumerate(self.action):
                    if action[0] == "Bomb":
                        if allBomb(i):
                            choose = i
                            break
                    
                return choose

            def countBomb():
                # 查询现在有几个炸弹
                counter = 0
                have_counted=[]
                for card in self.state._handCards:
                    if card[-1] not in have_counted:
                        if countCard(card[-1])>= 4:
                            counter += 1
                            have_counted.append(card[-1])
                return counter

            '''
            轮到你出牌时
            '''

            # 最小组合数算法
            from myTurn import myTurn

            # 当轮到你随便出牌时优先出顺子
            reserved_straight = []
            # if self.state._curAction == None:
            #     best_action = myTurn(self.state._handCards, self.state._actionList)
            #     for action in best_action:
            #         if action[0] == 'Straight':
            #             reserved_straight.append(action)
            
                # for i,a in enumerate(self.action):
                #     for action in best_action:
                #         if a[0] == 'Straight':
                #             if a == action:
                #                 print(a)
                #                 return i

                # for i,a in enumerate(self.action):                
                #     for action in best_action:
                #         if a[0]=='Single':
                        
                #             if a == action:
                               
                #                 return i
                                

            if self.state._greaterAction == [None, None, None] or self.state._curAction == None:
                reserved_straight = []
                if self.state._curAction == None:
                    print('reserve card:',reserve_card)
                    print(self.state._handCards)
                    best_action = myTurn(self.state._handCards, self.state._actionList)
                    for action in best_action:
                        if action[0] == 'Straight':
                            reserved_straight.append(action)
                '''
                如果有两张大王,走单张
                '''
                
                if 'HR' in self.state._handCards:
                    
                    if countCard("R")+countCard("B") >= 1:
                        # self.state._BR = True
                        # for i,a in enumerate(self.action):    
                        #     for single in reserved_single and not partBomb(i):
                        #         if a == single:
                        #             return i
                  
                        single_card =  findSingle()
                        if single_card != 0:
                            for i,action in enumerate(self.action):
                                if action[0]=='Single' and action[1]==single_card:
                                    
                                    return i
                
                '''
                顺子
                如果有四张单牌，可以拆炸打
                如果有三张单牌，非常合适，可以在不拆炸的情况下出
                '''
                for i,a in enumerate(self.action):
                    for action in reserved_straight:
                        if a[0] == 'Straight':
                            if a == action:
                                return i
                for i,a in enumerate(self.action):
                    # 如果顺子中至少有4张单牌且不拆炸
                    if a[0]=="Straight":
                        count_flag = 0
                        for j in a[2]:
                            if countCard(j[-1])==1:
                                count_flag += 1
                        if count_flag>= 5:
                            choose = i
                            return choose

                        if count_flag>= 4 and not partBomb(i):
                            choose = i
                            return choose
                for i,a in enumerate(self.action):
                    # 如果顺子中至少有3张单牌且不拆炸，能接顺子
                    if a[0]=="Straight":
                        count_flag = 0
                        for j in a[2]:
                            if countCard(j[-1])==1:
                                count_flag += 1
                        if count_flag>= 4:
                            choose = i
                            return choose

                        if count_flag>= 3 and not partBomb(i):
                            choose = i
                            return choose


                '''  
                对子
                如果有大对子，优先出小对子
                '''
                # curRank = self.state._curRank
                # for i,action in enumerate(self.action):
                #     if action[0]=="Pair":
                #         temp = i

                #     if action[0]=="Pair" and action[1]==curRank:
                #         if temp != i:
                #             return temp

                '''
                三连对
                '''
                for i,action in enumerate(self.action):
                    if 'ThreePair' in action and countCard(action[1])==2 and countCard(action[2][2][-1]) == 2 and countCard(action[2][-1][-1])==2:
                        return i
                    # if 'ThreePair' in action and countCard(action[1])==3 and countCard(action[2][2][-1]) == 2 and countCard(action[2][-1][-1])==2 and not partBomb(i):
                    #     return i
                    # if 'ThreePair' in action and countCard(action[1])==2 and countCard(action[2][2][-1]) == 3 and countCard(action[2][-1][-1])==2 and not partBomb(i):
                    #     return i
                    # if 'ThreePair' in action and countCard(action[1])==2 and countCard(action[2][2][-1]) == 2 and countCard(action[2][-1][-1])==3 and not partBomb(i):
                    #     return i
                '''
                钢板
                '''
                for i,action in enumerate(self.action):
                    if 'TwoTrips' in action and countCard(action[1]) == 3 and countCard(action[2][-1][-1]) == 3:
                        return i
                '''
                三带二
                '''
                for i,action in enumerate(self.action):
                    if 'ThreeWithTwo' in action and countCard(action[1])==3 and countCard(action[2][-1][-1])==2:
                      
                            # if action[2][-1][-1] != self.state._curRank and action[2][-1][-1] != 'A' and action[2][-1][-1] != 'B' and action[2][-1][-1] != 'R':
                        return i
                
                '''
                三张
                '''
                for i,action in enumerate(self.action):
                    if 'Trips' in action:
                        if partBomb(i) == False and findHeart(i) == False:
                            return i               
                '''
                对子
                '''
                for i,action in enumerate(self.action):
                    if 'Pair' in action and countCard(action[1])==2:
                        if partBomb(i) == False and findHeart(i) == False:
                            return i                

                '''
                单张
                '''
                for i, action in enumerate(self.action):
                    if 'Single' in action:
                        if partBomb(i) == False:
                            return i


                
                
            '''
            接牌时
            '''
            choose = 1
            # 单张
            # 如果只能出单张，优先出只有单张的单牌或者大小王或者级牌
            # onlySingle = False
            # for i in range(1, len(self.action)):
            #     if not self.action[i][0]=="Single":
            #         onlySingle = True
            # if onlySingle:
            #     for i,a in enumerate(self.action):
            #         if countCard(a[1]) == 1 or a[1] == "B" or a[1] == "R":
            #             return i 

            # 如果上家出的是单张，那么优先出只有一张的单张或者大小王
            if self.state._greaterAction[0] == "Single" and not(self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2):
                for i,a in enumerate(self.action):
                    if countCard(a[1]) == 1 and a[0]!="StraightFlush" :
                        return i 

                    if a[1] == "B" or a[1] == "R":
                        return i
                    if a[1] == self.state._curRank:
                        return i

            # 对子
            # 如果上家是对子，那么不拆红桃配
            if self.state._greaterAction[0] == "Pair" and not(self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2):
                for i,a in enumerate(self.action):
                    if countCard(a[1]) == 2:
                        choose = i
                    

            # 三张
            if self.state._greaterAction[0] == "Trips" and not(self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2):
                for i,a in enumerate(self.action):
                    if countCard(a[1]) == 3:
                        return i
                    if findHeart(i):
                        if choose < self.act_range:
                            choose += 1
                        else:
                            choose = 0

            # 顺子
            # 如果上家的牌出的是顺子，则三种选择：不出、接、炸
            if self.state._greaterAction[0] == 'Straight'and not(self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2):
                act = False
                for straight in reserved_straight:
                    for i,a in enumerate(self.action):
                        if a == straight:
                            act = True
                            return i
           
                change = False 
                for i,a in enumerate(self.action):
                    # 如果顺子中至少有2张单牌且不拆炸，能接顺子
                    if a[0]=="Straight":
                        count_flag = 0
                        for j in a[2]:
                            if countCard(j[-1])==1:
                                count_flag += 1
                        if count_flag>= 4:
                            choose = i
                            
                            change = True
                            
                            return choose

                        if count_flag>= 3 and not partBomb(i):
                            choose = i
                            change = True
                            break
                if change == False:       
                    for i,a in enumerate(self.action):
                        # 如果顺子中至少有2张单牌且不拆炸，能接顺子
                        if a[0]=="Straight":
                            count_flag = 0
                            for j in a[2]:
                                if countCard(j[-1])==1:
                                    count_flag += 1
                            if count_flag>= 3:
                                choose = i
                                
                                change = True
                                break
                                return choose

                            if count_flag>= 2 and not partBomb(i):
                                choose = i
                                change = True
                                break
                
                # 如果不能满足上述条件，则选择pass
                if change == False:
                    for i,a in enumerate(self.action):
                        choose = 0
                  
            # 三带二
            # 如果上家出的三带二，优先选择带的对子只有两张
            if self.state._greaterAction[0] == 'ThreeWithTwo'and not(self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2):
                flag = True
                for i,a in enumerate(self.action):
                    if a[0] == "ThreeWithTwo":
                        if countCard(a[1]) == 3 and countCard(a[2][-1][-1]) == 2 and not partBomb(i):
                            flag = False
                            choose = i
                            break
                # if flag == True:
                #     for i,a in enumerate(self.action):
                #         if a[0] == "ThreeWithTwo":
                #             if countCard(a[1]) == 2 and countCard(a[2][-1][-1]) == 2 and not partBomb(i):
                #                 flag = False
                #                 choose = i
                #                 break

                if flag == True:
                    choose = bomb()
                    
                

            # 钢板
            # 如果遇到钢板，优先选择恰好的钢板
            if self.state._greaterAction[0] == 'TwoTrips'and not(self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2):
                flag = True
                for i,a in enumerate(self.action):
                    if countCard(a[1]) >= 2 and countCard(a[2][-1][-1]) >= 2 and not partBomb(i):
                        choose = i
                        flag = False
                        break
                if flag == True:
                    choose = bomb()


            # 三连对
            # 如果遇到三连对，优先选择只有完整的三个对子
            if self.state._greaterAction[0] == 'ThreePair'and not(self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2):
                flag = True
                for i,a in enumerate(self.action):
                    if countCard(a[1]) <= 3 and countCard(a[2][2][-1]) <= 2 and countCard(a[2][-1][-1])<=2 and not partBomb(i):
                        choose = i
                        flag = False
                        break
                    # if countCard(a[1]) == 3 and countCard(a[2][2][-1]) == 2 and countCard(a[2][-1][-1])==2 and not partBomb(i):
                    #     choose = i
                    #     flag = False
                    #     break
                    # if countCard(a[1]) == 2 and countCard(a[2][2][-1]) == 3 and countCard(a[2][-1][-1])==2 and not partBomb(i):
                    #     choose = i
                    #     flag = False
                    #     break
                    # if countCard(a[1]) == 2 and countCard(a[2][2][-1]) == 2 and countCard(a[2][-1][-1])==3 and not partBomb(i):
                    #     choose = i
                    #     flag = False
                    #     break

                if flag == True:
                    choose = bomb()

            # 如果出的三张或者对子中有逢人配，错
            # if self.action[choose][0] == "Trips" or self.action[choose][0] == "Pair":
            #     for i in range(len(self.action[choose][2])):
            #         if self.action[choose][2][i] == 'H' + self.state._curRank:
            #             print("choose:",self.action[choose])
            #             if choose < self.act_range:
            #                 choose += 1
                        
            
            '''
            结尾过滤掉错误的出牌
            '''
            
            # 不拆炸
            if self.action[choose][0] != 'Bomb':
                while(partBomb(choose)):
                    if choose < self.act_range:
                        choose += 1
                    else:
                        return 0

            # 当最大动作来自队友的炸弹时，选择PASS
            if (self.state._greaterAction[0] == 'Bomb' or self.state._greaterAction[0] =='StraightFlush') and (self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2):
                return 0
            # 当最大动作来自队友，不接
            if self.state._greaterPos - self.state._myPos == 2 or self.state._greaterPos - self.state._myPos == -2:
                return 0

     

          
            '''
            如果选择了炸弹，例如五个炸弹，但是只用了四张牌
            所以要确保所有牌一起炸
            
            '''

            
            while(not allBomb(choose)):
                choose += 1



            if self.action[choose][0] == "Bomb":
                cards_number = countCard(self.action[choose][1])
                bomb_number  = len(self.action[choose][2])
                if cards_number > bomb_number:
                    print("ERROR!!-炸弹丢单张了")
                    print(self.action[choose])
                    print(self.state._handCards)

                
                # 如果上家或者下家的牌小于20张，炸！
                last = (self.state._myPos + 4 - 1)%4
                next_ = (self.state._myPos + 1)%4
                if msg["publicInfo"][last]["rest"]<=14 or msg["publicInfo"][next_]["rest"]<=14:
               
                    pass
                else:
                    choose = 0

            # 如果最后的手牌只剩炸弹
            if countCard(self.state._handCards[0][-1]) == len(self.state._handCards) and len(self.state._handCards)>=4:
                choose = bomb()

            # 如果出的是同花顺，那么不出
            # if self.action[choose][0] == "StraightFlush":
            #     choose = 0

            return choose

        return 0
