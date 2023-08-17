# import argparse
# import numpy as np
# def tostring(run_final):
#     if(run_final<=9):
#         s="0"+str(run_final)
#     else:
#         s=str(run_final)
#     return s

# if __name__ == "__main__":       
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--states",required=True,type=str,help="Path to state file", default="/")
#     parser.add_argument("--parameters",required=True,type=str,help="Path to player A parameter file", default="hpi")
#     parser.add_argument("--q",required=False,type=str,help="Parameter for player B", default="0.5")
#     args = parser.parse_args()
#     statefile_path=args.states
#     parameterfile_path=args.parameters
#     q=float(args.q)
    
#     f = open(parameterfile_path, "r")
#     #viable actions for A
#     actions=np.array([0,1,2,4,6])
#     #possible outcomes for actions of A
#     outcomes=np.array([-1,0,1,2,3,4,6])
#     #maps "virtualactionoutcome" to probability for A
#     dict_A={}
#     #maps "virtualactionoutcome" to probability for B
#     dict_B={
#         "8-1":q,"80":(1-q)/2,"81":(1-q)/2,
#     }
#     counter=0
#     for x in f:
#         if counter==0:
#             counter+=1
#             continue
#         parts=x.split()
#         act=parts[0]
#         for i in range(len(parts)-1):
#             outc=str(outcomes[i])
#             dict_A[act+outc]=float(parts[i+1])
#     f.close()
    
#     #maps string states to 0 to S-1
#     state_mapper={}
    
#     #maps  0 to S-1 to string states
#     state_mapper_rev={}
#     counter=0
#     f = open(statefile_path, "r")
#     l=[]
#     for x in f:
#         parts=x.split()
#         if(len(parts[0])!=4):
#             break
#         s1=parts[0]+"A"
#         l.append(parts[0])
#         state_mapper[s1]=counter
#         state_mapper_rev[counter]=s1
#         counter+=1
#     f.close()
#     for x in l:
#         s1=x+"B"
#         state_mapper[s1]=counter
#         state_mapper_rev[counter]=s1
#         counter+=1
#     state_mapper["WON"]=counter
#     state_mapper_rev[counter]="WON"
#     counter+=1
#     state_mapper["LOST"]=counter
#     state_mapper_rev[counter]="LOST"
    
#     #maps virtual actions to 0 to A-1
#     action_mapper={0:0,1:1,2:2,4:3,6:4,8:5}
#     #maps 0 to A-1 to virtual actions
#     action_mapper_rev={0:0,1:1,2:1,3:4,4:6,5:8}
    
#     numStates=len(state_mapper)
#     numActions=len(action_mapper)
#     T=np.zeros((numStates,numActions,numStates))
#     R=np.zeros((numStates,numActions,numStates))
#     print("numStates",numStates)
#     print("numActions",numActions)
#     print("end",counter-1,counter)
    
#     print(dict_A)
#     print(dict_B)
#     for i in range(numStates-2):
#         s1=i
#         s1_string=state_mapper_rev[s1]
#         balls_left=int(s1_string[0:2])
#         runs_left=int(s1_string[2:4])
#         if balls_left==1:
#             if(s1_string[4]=='A'):
                
#             elif(s1_string[4]=='B'):
                
#         else:
#             if(s1_string[4]=='A'):
#                 for key in dict_A:
#                     action_vir=int(key[0])
#                     a=action_mapper(action_vir)
#                     if(key[1]=="-"):
#                         if(dict_A[key]>0):
#                             print("transition",s1,a,state_mapper["LOST"],0.,dict_A[key])
#                     else:
#                         run=int(key[1])
#                         if(run%2==0):
#                             if(balls_left%6==0):
#                                 next="B"
#                             else:
#                                 next="A"
#                         else:
#                             if(balls_left%6==0):
#                                 next="A"
#                             else:
#                                 next="B"
#                         run_final=runs_left-run
#                         if(run_final>0):
#                             rf=tostring(run_final)
#                             bf=tostring(balls_left-1)
#                             if(dict_A[key]>0):
#                                 print("transition",s1,a,state_mapper[bf+rf+next],0.,dict_A[key])    
#                         else:
#                             if(dict_A[key]>0):
#                                 print("transition",s1,a,state_mapper["WON"],1.,dict_A[key])
                    
#             elif(s1_string[4]=='B'):
#                 for key in dict_B:
#                     action_vir=int(key[0])
#                     a=action_mapper(action_vir)
#                     if(key[1]=="-"):
#                         if(dict_B[key]>0):
#                             print("transition",s1,a,state_mapper["LOST"],0.,dict_B[key])
#                     else:
#                         run=int(key[1])
#                         if(run%2==0):
#                             if(balls_left%6==0):
#                                 next="A"
#                             else:
#                                 next="B"
#                         else:
#                             if(balls_left%6==0):
#                                 next="B"
#                             else:
#                                 next="A"
#                         run_final=runs_left-run
#                         if(run_final>0):
#                             rf=tostring(run_final)
#                             bf=tostring(balls_left-1)
#                             if(dict_B[key]>0):
#                                 print("transition",s1,a,state_mapper[bf+rf+next],0.,dict_B[key])    
#                         else:
#                             if(dict_B[key]>0):
#                                 print("transition",s1,a,state_mapper["WON"],1.,dict_B[key])
                    
            
        
        
        
#     print("mdptype episodic")
#     print("discount 1")
        

    
            