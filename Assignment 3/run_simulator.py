from importlib.resources import path

from regex import P
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """
        self.epsilon=0.01
        self.alpha=0.01
        self.gamma=1
        # self.features=["speed","angle","target","topwall","bottomwall","rightwall","leftwall"]
        self.features=["angle"]
        self.steeractions=[-3,0,3]
        self.accelerationactions=[-5,-3.95,0,3.95,5]
        self.dict={
            
            # 'speed_tilewidth':1,
            # 'speed_tilings':10,
            # 'speed_min':0,
            # 'speed_max':10,
            
            'angle_tilewidth':10,
            'angle_tilings':10,
            'angle_min':-180,
            'angle_max':180,
            
            # 'target_tilewidth':100,
            # 'target_tilings':10,
            # 'target_min':0,
            # 'target_max':1000,
            
            # 'topwall_tilewidth':10,
            # 'topwall_tilings':10,
            # 'topwall_max':200,
            # 'topwall_min':0,
            
            # 'bottomwall_tilewidth':10,
            # 'bottomwall_tilings':10,
            # 'bottomwall_max':200,
            # 'bottomwall_min':0,
            
            # 'rightwall_tilewidth':10,
            # 'rightwall_tilings':10,
            # 'rightwall_max':200,
            # 'rightwall_min':0,
            
            # 'leftwall_tilewidth':10,
            # 'leftwall_tilings':10,
            # 'leftwall_max':200,
            # 'leftwall_min':0,

        }
        self.state=np.zeros(len(self.dict)//4).astype(np.int64)
        self.steerparameters={}
        self.accelerationparameters={}
        self.steeractiontaken=0
        self.accelerationactiontaken=0
        self.greedysteer=0
        self.greedyacc=0
        self.targetdistance=0
        self.leftwalltime=0
        self.topwalltime=0
        self.bottomwalltime=0
        self.anglediff=0
        self.newepisode=1
        for i in range(len(self.steeractions)):
            parameters={}
            for feature in self.features:
                n_tilings=self.dict[feature+"_tilings"]
                maxx=self.dict[feature+"_max"]
                minn=self.dict[feature+"_min"]
                tw=self.dict[feature+"_tilewidth"]
                assert (n_tilings*(maxx-minn+tw))%tw==0
                parameters[feature]=np.random.rand((n_tilings*(maxx-minn+tw))//tw-1)
            self.steerparameters[i]=parameters.copy()
        for i in range(len(self.accelerationactions)):
            parameters={}
            for feature in self.features:
                n_tilings=self.dict[feature+"_tilings"]
                maxx=self.dict[feature+"_max"]
                minn=self.dict[feature+"_min"]
                tw=self.dict[feature+"_tilewidth"]
                assert (n_tilings*(maxx-minn+tw))%tw==0
                parameters[feature]=np.random.rand((n_tilings*(maxx-minn+tw))//tw-1)
            self.accelerationparameters[i]=parameters.copy()
        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """
        

        # Replace with your implementation to determine actions to be taken
        eps=np.random.uniform(0,1)
        if self.newepisode or eps<self.epsilon:
            action_steer=np.random.randint(0,len(self.steeractions))
            action_acc=np.random.randint(0,len(self.accelerationactions))
            self.steeractiontaken=action_steer
            self.accelerationactiontaken=action_acc

        else:
            action_steer=self.greedysteer
            action_acc=self.greedyacc
            self.steeractiontaken=action_steer
            self.accelerationactiontaken=action_acc

        action = np.array([action_steer, action_acc])  

        return action

    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        def obtain_features(x_pos,y_pos,speed,angle):
            values={}
            values["speed"]=speed
            if angle>180:
                angle=angle-360
            values["angle"]=180*(np.arctan2(0-y_pos,350-x_pos)/np.pi)-angle
            values["target"]=np.linalg.norm(np.array([0-y_pos,350-x_pos]))
            self.targetdistance=np.linalg.norm(np.array([0-y_pos,350-x_pos]))
            self.anglediff=np.abs(values["angle"])
            v_vert=speed*np.sin(angle/np.pi)
            v_hor=speed*np.cos(angle/np.pi)
            values["topwall"]=10000
            values["bottomwall"]=10000
            values["rightwall"]=10000
            values["leftwall"]=10000
            if v_vert>0:
                values["topwall"]=np.linalg.norm(np.array([350-y_pos,0]))/(v_vert+1e-8)
            if v_vert<0:  
                values["bottomwall"]=np.linalg.norm(np.array([-350-y_pos,0]))/(-v_vert+1e-8)
            if v_hor>0:
                values["rightwall"]=np.linalg.norm(np.array([0,350-x_pos]))/(v_hor+1e-8)
            if v_hor<0:  
                values["leftwall"]=np.linalg.norm(np.array([0,-350-x_pos]))/(-v_hor+1e-8)
            self.leftwalltime=np.linalg.norm(np.array([0,-350-x_pos]))
            self.topwalltime=np.linalg.norm(np.array([350-y_pos,0]))
            self.bottomwalltime=np.linalg.norm(np.array([-350-y_pos,0]))
            i=0
            for feature in self.features:
                n_tilings=self.dict[feature+"_tilings"]
                maxx=self.dict[feature+"_max"]
                minn=self.dict[feature+"_min"]
                tw=self.dict[feature+"_tilewidth"]
                if values[feature]<minn:
                    values[feature]=minn
                if values[feature]>maxx:
                     values[feature]=maxx-0.00005
                right_index=(n_tilings*(values[feature]-minn+tw))//tw-1
                assert(right_index>=n_tilings-1)
                if  right_index<n_tilings-1:
                    right_index=n_tilings-1
                assert(right_index<=(n_tilings*(maxx-minn+tw))//tw-2)
                if  right_index>(n_tilings*(maxx-minn+tw))//tw-2:
                    right_index=(n_tilings*(maxx-minn+tw))//tw-2
                self.state[i]=right_index-n_tilings+1
                i+=1
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator
            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                
                x_pos,y_pos,speed,angle=state
                old_statefeatures=self.state
                old_anglediff=self.anglediff
                old_distance=self.targetdistance
                old_leftwalltime=self.leftwalltime
                old_topwalltime=self.topwalltime
                old_bottomwalltime=self.bottomwalltime
                obtain_features(x_pos,y_pos,speed,angle)
                new_distance=self.targetdistance
                new_anglediff=self.anglediff
                new_leftwalltime=self.leftwalltime
                new_topwalltime=self.topwalltime
                new_bottomwalltime=self.bottomwalltime
                #found out the value function at s'
                action_steer=0
                valuefunc_steer=0
                for i in range(len(self.steeractions)):
                    parameter=self.steerparameters[i]
                    j=0
                    val=0
                    for feature in self.features:
                        val+=np.sum(parameter[feature][self.state[j]:self.dict[feature+"_tilings"]+self.state[j]])
                        j+=1
                    if i==0:
                        valuefunc_steer=val
                    else:
                        if val>valuefunc_steer:
                            action_steer=i
                            valuefunc_steer=val
                
                action_acc=0
                valuefunc_acc=0
                for i in range(len(self.accelerationactions)):
                    parameter=self.accelerationparameters[i]
                    j=0
                    val=0
                    for feature in self.features:
                        val+=np.sum(parameter[feature][self.state[j]:self.dict[feature+"_tilings"]+self.state[j]])
                        j+=1
                    if i==0:
                        valuefunc_acc=val
                    else:
                        if val>valuefunc_acc:
                            action_acc=i
                            valuefunc_acc=val
                #store the greedy actions to be taken at s'            
                self.greedysteer=action_steer
                self.greedyacc=action_acc
                
                #calcuate Q(s,a)
                curr_value_steer=0
                parameter=self.steerparameters[self.steeractiontaken]
                j=0
                val=0
                for feature in self.features:
                    curr_value_steer+=np.sum(parameter[feature][old_statefeatures[j]:self.dict[feature+"_tilings"]+old_statefeatures[j]])
                    j+=1
                
                parameter=self.accelerationparameters[self.accelerationactiontaken]
                j=0
                curr_value_acc=0
                for feature in self.features:
                    curr_value_acc+=np.sum(parameter[feature][old_statefeatures[j]:self.dict[feature+"_tilings"]+old_statefeatures[j]])
                    j+=1
                
                #calculate delta
                delta_steer=0
                delta_acc=0
                if terminate:
                    if reached_road:
                        delta_steer+=100000
                        delta_acc+=100000
                    if not reached_road:
                        delta_steer+=-100000
                        delta_acc+=-100000
                # if new_bottomwalltime<10 and new_bottomwalltime-old_bottomwalltime<0:
                #     delta+=-1000
                # if new_leftwalltime<10 and new_leftwalltime-old_leftwalltime<0:
                #     delta+=-1000
                # if new_topwalltime<10 and new_topwalltime-old_topwalltime<0:
                #     delta+=-1000
                 
                # if new_anglediff>50 and new_anglediff-old_anglediff>=0:
                #     delta_steer+=-60
                # if new_anglediff>50 and new_anglediff-old_anglediff<0:
                #     delta_steer+=60
                    
                # if new_anglediff<=50 and new_anglediff>=10 and new_anglediff-old_anglediff>=0:
                #     delta_steer+=-40
                # if new_anglediff<=50 and new_anglediff>=10 and new_anglediff-old_anglediff<0:
                #     delta_steer+=40
                    
                # if new_anglediff<10 and new_anglediff-old_anglediff>0:
                #     delta_steer+=-20
                # if new_anglediff<10 and new_anglediff-old_anglediff<=0:
                #     delta_steer+=20
                delta_steer+=-new_anglediff*(new_anglediff-old_anglediff)

                if new_anglediff<10 and speed>0.25:
                    delta_acc+=50
                if new_anglediff<10 and speed<0.25:
                    delta_acc-=50
                if new_anglediff>10 and speed>0.25 and new_distance>250:
                    delta_acc-=50
                delta_steer+=reward+self.gamma*valuefunc_steer-curr_value_steer
                delta_acc+=reward+self.gamma*valuefunc_acc-curr_value_acc
        
                #modify weights
                if not self.newepisode:
                    parameter=self.steerparameters[self.steeractiontaken]
                    j=0
                    for feature in self.features:
                        parameter[feature][old_statefeatures[j]:self.dict[feature+"_tilings"]+old_statefeatures[j]]+=self.alpha*delta_steer
                        j+=1
                    
                    parameter=self.accelerationparameters[self.accelerationactiontaken]
                    j=0
                    for feature in self.features:
                        parameter[feature][old_statefeatures[j]:self.dict[feature+"_tilings"]+old_statefeatures[j]]+=self.alpha*delta_acc
                        j+=1
                self.newepisode=0
                
                
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    self.newepisode=1
                    break

            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """

        # Replace with your implementation to determine actions to be taken
        action_steer = None
        action_acc = None

        action = np.array([action_steer, action_acc])  

        return action

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False

            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
