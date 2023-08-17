import argparse

if __name__ == "__main__":       
    parser = argparse.ArgumentParser()
    parser.add_argument("--value-policy",required=True,type=str,help="Path to value-policy file", default="/")
    parser.add_argument("--states",required=True,type=str,help="Path to state file", default="/")
   
    args = parser.parse_args()
    statefile_path=args.states
    valuepolicyfile_path=args.value_policy
    optimal_action={}
    optimal_value={}
    f = open(valuepolicyfile_path, "r")
    counter=0
    for x in f:
        parts=x.split()
        if len(parts)!=2:
            break
        optimal_value[counter]=float(parts[0])
        optimal_action[counter]=int(parts[1])
        counter+=1
    f.close()
   
    #maps string states to 0 to S-1
    state_mapper={}
    #maps  0 to S-1 to string states
    state_mapper_rev={}
    counter=0
    f = open(statefile_path, "r")
    l=[]
    for x in f:
        parts=x.split()
        if(len(parts[0])!=4):
            break
        s1=parts[0]+"A"
        l.append(parts[0])
        state_mapper[s1]=counter
        state_mapper_rev[counter]=s1
        counter+=1
    f.close()
    for x in l:
        s1=x+"B"
        state_mapper[s1]=counter
        state_mapper_rev[counter]=s1
        counter+=1
    state_mapper["WON"]=counter
    state_mapper_rev[counter]="WON"
    counter+=1
    state_mapper["LOST"]=counter
    state_mapper_rev[counter]="LOST"

    action_mapper={0:0,1:1,2:2,4:3,6:4,8:5}
    
    action_mapper_rev={0:0,1:1,2:2,3:4,4:6,5:8}
   
    for x in l:
        st=state_mapper[x+"A"]
        valu=optimal_value[st]
        act=optimal_action[st]
        act_vir=action_mapper_rev[act]
        if act_vir==8:
            act_vir=0
        if valu==0:
            act_vir=0
        print(x,act_vir,valu)

           
                
        

    
            