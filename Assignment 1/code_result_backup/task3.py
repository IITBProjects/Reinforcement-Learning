"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the AlgorithmManyArms class. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)
"""

import numpy as np

# START EDITING HERE
# You can use this space to define any helper functions that you need
# END EDITING HERE

class AlgorithmManyArms:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        # Horizon is same as number of arms
        self.explore=1
        self.preference=np.random.permutation(self.num_arms)
        self.currind=0
        self.num=0
        self.suceess=np.zeros(num_arms)
        self.failure=np.zeros(num_arms)
        self.exploitind=0
        self.const=0.021
        self.pulled=0
        self.values=np.zeros(num_arms)
        
    def give_pull(self):
        # START EDITING HERE
        if self.explore==1:
            self.currind+=1
            self.num+=1
            self.pulled=self.currind-1
            return self.preference[self.currind-1]
        else:
            self.pulled=self.exploitind
            self.num+=1
            return self.preference[self.exploitind]
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if reward ==1:
            self.suceess[self.pulled]+=1
        else:
            self.failure[self.pulled]+=1
        self.values[self.pulled]=self.suceess[self.pulled]/(self.failure[self.pulled]+self.suceess[self.pulled])
        val_ind=np.argmax(self.values)
        val=self.values[val_ind]
        frac=(self.num_arms-self.num)/self.num_arms
        if (1-val)*(0.75*frac+0.2*frac*frac+0.05*frac*frac)<self.const:
            self.explore=0
            self.exploitind=val_ind
        else:
            self.explore=1
        # END EDITING HERE
