


import json
from ws4py.client.threadedclient import WebSocketClient
from state import State
from min_action import Action
from time import sleep
from sys_change import sys_stdout
 
logger = sys_stdout()
class ExampleClient(WebSocketClient):

    def __init__(self, url):
        super().__init__(url)
        self.state = State()
        self.action = Action()
        # self.beginning = False

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state.parse(message) 
        logger.print_to_file("../logger/logger1.txt", message)
        if "stage" in message:
            if message["stage"]=="episodeOver":
                print("我方等级：{} 对方等级：{} ".format(self.state._selfRank, self.state._oppoRank))
        # 调用状态对象来解析状态
        self.action.state = self.state  
                                    
        # if message["stage"]=="beginning":
        #     self.beginning = True
        # if self.beginning == True and "actionList" in message:
        #     from myTurn import myTurn
        #     reserved_straight = []
        #     reserved_single = []
        #     best_action = myTurn(self.state._handCards, self.state._actionList)
        #     for action in best_action:
        #         if action[0] == 'Straight':
        #             reserved_straight.append(action)
        #         if action[0] == 'Single':
        #             reserved_single.append(action)
        #     self.state.reserved_straight = reserved_straight
            
        #     print("best action",best_action)
        #     self.beginning = False
        
                                                    
        if "actionList" in message:                                           # 需要做出动作选择时调用动作对象进行解析
            act_index = self.action.parse(message)
          
            self.send(json.dumps({"actIndex": act_index}))



if __name__ == '__main__':
    try:
        ws = ExampleClient('ws://127.0.0.1:9618/game/gd/client1')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
