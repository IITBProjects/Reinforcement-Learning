import subprocess, random, os
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
random.seed(0)

parser.add_argument("--parameters",type=str)
parser.add_argument("--analysis",type=int)
args = parser.parse_args()

if(args.analysis == 1):
    balls = 15
    runs = 30
    Q = np.linspace(0, 1, num=25)
    optimal_winnings = []
    random_winnings = []

    for q in Q:
        cmd_states = "python", "cricket_states.py", "--balls", str(balls), "--runs", str(runs)
        cricket_states = subprocess.check_output(cmd_states, universal_newlines=True)
        with open("states", "w") as file_states:
            file_states.write(cricket_states)
        with open("random", "w") as random_policy:
            for i in range(2*balls*runs+2):
                random_policy.write(str(random.randint(0,4))+'\n')

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
    plt.xlabel("B's Strength")
    plt.ylabel("Probability")
    plt.title("Varying strength")
    plt.legend()
    plt.savefig("graph_strength")
    os.remove('mdp')
    os.remove('random')
    os.remove('states')
elif(args.analysis == 2):
    balls = 10
    q = 0.25
    Runs = list(range(1, 21)[::-1])
    optimal_winnings = []
    random_winnings = []

    for runs in Runs:
        cmd_states = "python", "cricket_states.py", "--balls", str(balls), "--runs", str(runs)
        cricket_states = subprocess.check_output(cmd_states, universal_newlines=True)
        with open("states", "w") as file_states:
            file_states.write(cricket_states)
        with open("random", "w") as random_policy:
            for i in range(2*balls*runs+2):
                random_policy.write(str(random.randint(0,4))+'\n')

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

    plt.plot(Runs, optimal_winnings, label='Optimal')
    plt.plot(Runs, random_winnings, label='Random')
    plt.xlabel("Runs needed")
    plt.ylabel("Probability")
    plt.title("Varying runs")
    plt.legend()
    plt.savefig("graph_runs")
    os.remove('mdp')
    os.remove('random')
    os.remove('states')
elif(args.analysis == 3):
    runs = 10
    q = 0.25
    Balls = list(range(1, 16)[::-1])
    optimal_winnings = []
    random_winnings = []

    for balls in Balls:
        cmd_states = "python", "cricket_states.py", "--balls", str(balls), "--runs", str(runs)
        cricket_states = subprocess.check_output(cmd_states, universal_newlines=True)
        with open("states", "w") as file_states:
            file_states.write(cricket_states)
        with open("random", "w") as random_policy:
            for i in range(2*balls*runs+2):
                random_policy.write(str(random.randint(0,4))+'\n')

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

    plt.plot(Balls, optimal_winnings, label='Optimal')
    plt.plot(Balls, random_winnings, label='Random')
    plt.xlabel("Balls left")
    plt.ylabel("Probability")
    plt.title("Varying balls")
    plt.legend()
    plt.savefig("graph_balls")
    os.remove('mdp')
    os.remove('random')
    os.remove('states')
else:
    pass