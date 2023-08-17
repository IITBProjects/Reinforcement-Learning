import subprocess, random, os
import numpy as np
import matplotlib.pyplot as plt
import argparse

def tostring(value):
    value=int(value)
    if(value<=9):
        s="0"+str(value)
    else:
        s=str(value)
    return s

parser = argparse.ArgumentParser()
random.seed(0)
parser.add_argument("--policyfile",required=False,type=str,help="Path to policy file", default="data/cricket/rand_pol.txt")
parser.add_argument("--parameters",type=str)
parser.add_argument("--analysis",type=int)
args = parser.parse_args()
policyfile_path=args.policyfile


action_mapper={0:0,1:1,2:2,4:3,6:4,8:5}
#maps string states to 0 to S-1
state_mapper={}
#maps  0 to S-1 to string states
state_mapper_rev={}
counter=0
f = open(policyfile_path, "r")
l=[]
l2=[]
for x in f:
    parts=x.split()
    if len(parts[0])!=4:
        break
    s1=parts[0]+"A"
    l.append(parts[0])
    l2.append(action_mapper[int(parts[1])])
    state_mapper[s1]=counter
    state_mapper_rev[counter]=s1
    counter+=1
f.close()
for x in l:
    s1=x+"B"
    l2.append(action_mapper[8])
    state_mapper[s1]=counter
    state_mapper_rev[counter]=s1
    counter+=1
state_mapper["WON"]=counter
state_mapper_rev[counter]="WON"
counter+=1
l2.append(action_mapper[8])
state_mapper["LOST"]=counter
state_mapper_rev[counter]="LOST"
l2.append(action_mapper[8])




balls = 15
runs = 30

with open("random", "w") as random_policy:
    for i in range(2*balls*runs+2):
        random_policy.write(str(i)+' '+str(l2[i])+'\n')
        
with open("states", "w") as file_states:
    for x in l:
        file_states.write(x+'\n')
                
                
                
                
if(args.analysis == 1):
    balls = 15
    runs = 30
    Q = np.linspace(0, 1, num=25)
    optimal_winnings = []
    random_winnings = []

    for q in Q:
        
        cmd_encode = "python", "encoder.py", "--states", "states", "--parameters", args.parameters, "--q", str(q)
        mdp_encode = subprocess.check_output(cmd_encode, universal_newlines=True)
        with open("mdp", "w") as file_mdp:
            file_mdp.write(mdp_encode)

        cmd_optimal = "python", "planner.py", "--mdp", "mdp"
        value_optimal = subprocess.check_output(cmd_optimal, universal_newlines=True)
        optimal_winnings.append(float(value_optimal.split()[0]))
        
        cmd_random = "python", "planner.py", "--mdp", "mdp", "--policy", "random"
        value_random = subprocess.check_output(cmd_random, universal_newlines=True)
        random_winnings.append(float(value_random.split()[0]))

    plt.plot(Q, optimal_winnings[::-1], label='Optimal')
    plt.plot(Q, random_winnings[::-1], label='Random')
    plt.xlabel("B's Strength(1-q)" ,fontweight="bold")
    plt.ylabel("Probability" ,fontweight="bold")
    plt.title("Balls=15 Runs=30" , size=22,fontweight="bold")
    plt.legend()
    plt.savefig("graph_strength")
    os.remove('mdp')
    os.remove('random')
    os.remove('states')
elif(args.analysis == 2):
    balls = 10
    q = 0.25
    Runs = list(range(1, 21)[::-1])
    cmd_encode = "python", "encoder.py", "--states", "states", "--parameters", args.parameters, "--q", str(q)
    mdp_encode = subprocess.check_output(cmd_encode, universal_newlines=True)
    with open("mdp", "w") as file_mdp:
        file_mdp.write(mdp_encode)

    cmd_optimal = "python", "planner.py", "--mdp", "mdp"
    value_optimal = subprocess.check_output(cmd_optimal, universal_newlines=True).split()
    
    cmd_random = "python", "planner.py", "--mdp", "mdp", "--policy", "random"
    value_random = subprocess.check_output(cmd_random, universal_newlines=True).split()
    
    i=0
    optimal_dict={}
    for x in value_optimal:
        if i%2==0:
            optimal_dict[i/2]=float(x)
        i+=1
    
    i=0
    random_dict={}
    for x in value_random:
        if i%2==0:
            random_dict[i/2]=float(x)
        i+=1
    optimal_winnings = []
    random_winnings = []
    for runs in Runs:
        stri=tostring(balls)+tostring(runs)+'A'
        optimal_winnings.append(optimal_dict[state_mapper[stri]])
        random_winnings.append(random_dict[state_mapper[stri]])

    plt.plot(Runs, optimal_winnings, label='Optimal')
    plt.plot(Runs, random_winnings, label='Random')
    plt.xlabel("Runs needed" ,fontweight="bold")
    plt.ylabel("Probability" ,fontweight="bold")
    plt.title("Balls=10 q=0.25" , size=22,fontweight="bold")
    plt.legend()
    plt.savefig("graph_balls")
    os.remove('mdp')
    os.remove('random')
    os.remove('states')
    
elif(args.analysis == 3):
    runs = 10
    q = 0.25
    Balls = list(range(1, 16)[::-1])
    cmd_encode = "python", "encoder.py", "--states", "states", "--parameters", args.parameters, "--q", str(q)
    mdp_encode = subprocess.check_output(cmd_encode, universal_newlines=True)
    with open("mdp", "w") as file_mdp:
        file_mdp.write(mdp_encode)

    cmd_optimal = "python", "planner.py", "--mdp", "mdp"
    value_optimal = subprocess.check_output(cmd_optimal, universal_newlines=True).split()
    
    cmd_random = "python", "planner.py", "--mdp", "mdp", "--policy", "random"
    value_random = subprocess.check_output(cmd_random, universal_newlines=True).split()
    
    
    i=0
    optimal_dict={}
    for x in value_optimal:
        if i%2==0:
            optimal_dict[i/2]=float(x)
        i+=1
    
    i=0
    vf=[]
    random_dict={}
    for x in value_random:
        if i%2==0:
            random_dict[i/2]=float(x)
            vf.append(float(x))
        i+=1
    optimal_winnings = []
    random_winnings = []
    i=0
    with open("mdec", "w") as file2_mdp:
        for t in vf:
            file2_mdp.write(str(t)+' '+str(l2[i])+'\n')
            i+=1

    for balls in Balls:
        stri=tostring(balls)+tostring(runs)+'A'
        optimal_winnings.append(optimal_dict[state_mapper[stri]])
        random_winnings.append(random_dict[state_mapper[stri]])

    plt.plot(Balls, optimal_winnings, label='Optimal')
    plt.plot(Balls, random_winnings, label='Random')
    plt.xlabel("Balls left" ,fontweight="bold")
    plt.ylabel("Probability" ,fontweight="bold")
    plt.title("Runs=10 q=0.25" , size=22,fontweight="bold")
    plt.legend()
    plt.savefig("graph_runs")
    os.remove('mdp')
    os.remove('random')
    os.remove('states')
    
else:
    pass