"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
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

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
# You can use this space to define any helper functions that you need
    
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.num=0
        self.count=np.zeros(num_arms)
        self.prob=np.zeros(num_arms)
        self.values=np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if self.num < self.num_arms:
            return self.num
        else:
            return np.argmax(self.values)
        
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if self.num<self.num_arms:
            self.num+=1
            self.count[arm_index]+=1
            self.prob[arm_index]=reward
        else:
            self.num+=1
            self.count[arm_index]+=1
            n=self.count[arm_index]
            val=self.prob[arm_index]
            final_val=((n-1)*val+reward)/n
            self.prob[arm_index]=final_val
            scalar=2*math.log(self.num)
            self.values=np.add(self.prob,np.sqrt(scalar*np.reciprocal(self.count)))  
        # END EDITING HERE

class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.num=0
        self.counts=np.zeros(num_arms)
        self.prob=np.zeros(num_arms)
        self.values=np.zeros(num_arms)
        self.rhs=np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if self.num < self.num_arms:
            return self.num
        else:
            return np.argmax(self.values)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        def find_q(i):
            p_val=self.prob[i]
            time=self.num
            rhs=self.rhs[i]
            if rhs<=0:
                return p_val
            
            high=1
            low=p_val
            mid=(high+low)/2
            while high-low>=0.0001:
                mid=(high+low)/2
                if p_val==1:
                    lhs=math.log(1/mid)
                elif p_val==0:
                    lhs=math.log(1/(1-mid))
                else:
                    lhs=p_val*math.log(p_val/mid)+(1-p_val)*math.log((1-p_val)/(1-mid))
                if(lhs>rhs):
                    high=mid
                else:
                    low=mid
            return (low+high)/2
        
        self.num+=1
        self.counts[arm_index]+=1
        if self.num<self.num_arms:
           self.prob[arm_index]=reward
        else:
            n=self.counts[arm_index]
            val=self.prob[arm_index]
            final_val=((n-1)*val+reward)/n
            self.prob[arm_index]=final_val
            vali=math.log(self.num)+3*math.log(math.log(self.num))
            self.rhs=vali*np.reciprocal(self.counts)
            p=np.vectorize(find_q)
            self.values=p(np.arange(self.num_arms))

        # END EDITING HERE


class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.num=0
        self.suceess=np.zeros(num_arms)
        self.failure=np.zeros(num_arms)
        self.values=np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if self.num < self.num_arms:
            return self.num
        else:
            return np.argmax(self.values)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        def sample(i):
            return np.random.beta(self.suceess[i]+1,self.failure[i]+1)
        if self.num<self.num_arms:
            self.num+=1
            if reward ==1:
                self.suceess[arm_index]+=1
            else:
                self.failure[arm_index]+=1
        else:
            self.num+=1
            if reward ==1:
                self.suceess[arm_index]+=1
            else:
                self.failure[arm_index]+=1
            p=np.vectorize(sample)
            self.values=p(np.arange(self.num_arms))
        # END EDITING HERE
