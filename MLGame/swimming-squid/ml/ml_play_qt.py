import random
from ml.Environment import Environment as env
from ml.QT import QLearningTable
import pandas as pd
import os

class MLPlay:
    def __init__(self,*args, **kwargs):
        self.env = env()        
        self.action = self.env.action
        self.state = [self.env.observation]    
        self.state_ = [self.env.observation]   
        self.status = "GAME_ALIVE"         
        
        self.QT = QLearningTable(actions=list(range(self.env.n_actions)))        
        folder_path = './save'
        os.makedirs(folder_path, exist_ok=True)


        self.QT.q_table =pd.read_pickle('.\\ml\\save\\qtable.pickle')                        
        print("Initial ml script")

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        self.env.set_scene_info(scene_info)        
        observation, reward, done, info = self.env.step(self.action)


        self.state_ = [observation]
        
        action = self.QT.choose_action(str(self.state))                

        self.state = self.state_
        self.action = action        
        
        action_space = [["UP"], ["DOWN"], ["LEFT"], ["RIGHT"],["NONE"]]
        
        return action_space[action]
        
    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")        
        self.env.reset()
        pass