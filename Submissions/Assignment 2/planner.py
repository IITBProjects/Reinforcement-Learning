from pulp import *
import argparse
import numpy as np

def maxnorm(x):
    return np.max(np.absolute(x))

#Returns the value function for a policy given the transition function,reward function,policy and gamma
def value_for_policy(T,R,policy,gamma):
    numStates,numActions,_=T.shape
    policy=policy.flatten()
    one_hot=np.zeros((numStates,numActions))
    
    #a 2d matrix where for index (S,pi(S)) value is one and rest it is zero
    one_hot[np.arange(numStates),policy]=1
    one_hot=one_hot[:,:,None]
    
    #broaadcasted the above 2d matrix to 3d where for index(S,pi(S),S')  value is one and rest it is zero
    one_hot=np.tile(one_hot,(1,1,numStates))
    
    #obtained the transition matrix for the given policy where for index(S,pi(S),S')  value is T(S,pi(S),S') and rest it is zero
    T_matrix=np.multiply(T,one_hot)
    
    #converted the above matrix to 2d where for index(S,S')  value is T(S,pi(S),S') 
    A_matrix=np.sum(T_matrix,axis=1)
    A_matrix=-gamma*A_matrix
    
    #Used the equation V(s)= summation(   T(s,pi(s),s')(R(s,pi(s),s') + gamma*V(s')   ) and rearranges it to get
    #summation( -T(s,pi(s),s')*gamma*V(s') ) + V(s) = summation(   T(s,pi(s),s')(R(s,pi(s),s') )
    # Each state has a similar equation.There are n linear equations in n variable V(s) and hence the A matrix below is the corresponding coefficient matrix
    A_matrix=np.add(A_matrix,np.identity(numStates))
    
    B_matrix=np.multiply(T_matrix,R)
    B_matrix=np.sum(B_matrix,axis=1)
    B_matrix=np.sum(B_matrix,axis=1)
    
    # B matrix is the corresponding B matrix used in linear equations
    B_matrix=B_matrix[:,None]
    
    #AV=B and thus V=A^(-1)B
    A_inv=np.linalg.inv(A_matrix)
    V=np.matmul(A_inv,B_matrix)
    V=V.squeeze()
    return V

#For a given value function calculates Q(S,a){using V as V^pi} and thus returns optimal action for policy improvement and B(V) for value iteration
def policy_for_value(T,R,V,gamma):
    numStates,numActions,_=T.shape
    V=V.flatten()
    V=V[None,None,:]
    # a 3d matrix where V(s,a,s') is Value function(s')
    V=np.tile(V,(numStates,numActions,1))
    
    # 2d action value function matrix
    Q_pi=np.sum(np.multiply(T,np.add(R,gamma*V)),axis=2)
    policy=np.argmax(Q_pi,axis=1)
    new_value=np.max(Q_pi,axis=1)
    return policy,new_value

def Value_Iteration(T,R,gamma):
    numStates,_,_=T.shape
    V=np.random.rand(numStates)
    policy=np.zeros(numStates)
    diff=5.
    while diff>0.0000000001:
        policy,new_value=policy_for_value(T,R,V,gamma)
        diff=maxnorm(np.subtract(V,new_value))
        V=new_value
    for i in range(numStates):
        print("{:.6f}".format(V[i]),int(policy[i]))

def Howard_policy_Iteration(T,R,gamma):
    numStates,numActions,_=T.shape
    diff=5
    policy=np.random.randint(0,numActions,size=numStates)
    while diff>0:
        V=value_for_policy(T,R,policy,gamma)
        new_policy,new_V=policy_for_value(T,R,V,gamma)
        mask=new_V-V>0.0000000001
        policy[mask]=new_policy[mask]
        diff=np.sum(mask)
    for i in range(numStates):
        print("{:.6f}".format(V[i]),int(policy[i]))
        
def Linear_Programming(T,R,gamma):
    numStates,numActions,_=T.shape
    T_f= -gamma*T
    TR=T*R
    TR_matrix=np.sum(TR,axis=2)
    States=np.arange(numStates)
    prob = LpProblem("LinearProgrammingforValueFunction", LpMinimize)
    value_vars = LpVariable.dicts("x",States,cat='Continuous')
    prob += (
    lpSum([ 1 * value_vars[i] for i in States]),
    "Sum of V(s) for all S",
    )
    for s in range(numStates):
        for a in range(numActions):
            prob += (value_vars[s]+
                lpSum([T_f[s,a,k] * value_vars[k] for k in States]) >= TR_matrix[s,a],
                "s"+str(s)+" a"+str(a),
            )
    # prob.writeLP("model.lp")
    prob.solve(PULP_CBC_CMD(msg=0))
    if LpStatus[prob.status]!="Optimal":
        print("unoptimal")
    else:
        V=np.zeros(numStates)
        for i in range(numStates):
            V[i] = value_vars[i].varValue
        policy,_=policy_for_value(T,R,V,gamma)
        for i in range(numStates):
            print("{:.6f}".format(V[i]),int(policy[i]))
        
        
        
if __name__ == "__main__":       
    parser = argparse.ArgumentParser()
    parser.add_argument("--mdp",required=True,type=str,help="Path to mdp file", default="/")
    parser.add_argument("--algorithm",required=False,type=str,help="Algorithm: one of hpi,vi,lp", default="hpi")
    parser.add_argument("--policy",required=False,type=str,help="Path to policy file", default="None")
    args = parser.parse_args()

    mdp_path=args.mdp
    algorithm=args.algorithm
    policy=args.policy
    numStates=0
    numActions=0
    end_states=[]
    mdptype="episodic"
    gamma=1.0
    policy_action=[]
    f = open(mdp_path, "r")
    for x in f:
        parts=x.split()
        if parts[0]=='transition':
            R[int(parts[1])][int(parts[2])][int(parts[3])]=float(parts[4])
            T[int(parts[1])][int(parts[2])][int(parts[3])]=float(parts[5])
        elif parts[0]=='numStates':
            numStates=int(parts[1])
        elif parts[0]=='numActions':
            numActions=int(parts[1])
            T=np.zeros((numStates,numActions,numStates))
            R=np.zeros((numStates,numActions,numStates))
        elif parts[0]=='end':
            for s in parts[1:]:
                end_states.append(int(s))
        elif parts[0]=='discount':
            gamma=float(parts[1])
            break
        elif parts[0]=='mdptype':
            mdptype=parts[1]
    f.close()

    if policy !="None":
        f = open(policy, "r")
        #for a given mdp and a policy file assuming the actions specified in the policy file and in mdp match 
        #Assuming the policy file will have the actions as=A(S0),A(S1),A(S2),...A(S(n-1) in consequtive lines
        for x in f:
            parts=x.split()
            policy_action.append(int(parts[-1]))
        f.close()
        policy=np.array(policy_action)
        policy=policy.squeeze()
        V=value_for_policy(T,R,policy,gamma)
        for s in range(numStates):
            print("{:.6f}".format(V[s]),int(policy[s]))
    else:
        if algorithm=="vi":
            Value_Iteration(T,R,gamma)
        elif algorithm=="hpi":
            Howard_policy_Iteration(T,R,gamma)
        elif algorithm=="lp":
            Linear_Programming(T,R,gamma)
            