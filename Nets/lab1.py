import networkx as nx
import matplotlib.pyplot as plt

with open('M_out.txt') as out:
    M_out = [list(map(int, row.split())) for row in out.readlines()]

with open('M_in.txt') as m_in:
    M_in = [list(map(int, row.split())) for row in m_in.readlines()]
    
with open('V_positions.txt') as vpos:
    positions = [[int(x) for x in row.split()] for row in vpos][0]
    

def transition_availability(pos, trans_num):
    for i in range (len(pos)):
        if M_in[trans_num][i] > pos[i]:
            return(False)
    return(True)

def transitions_list(pos):
    trans_list = []
    for i in range (len(M_in)):
        if transition_availability(pos, i):
            trans_list.append(i)
    return(trans_list)

def get_new_positions(pos, trans_num):
    new_pos = pos.copy()
    for i in range (len(new_pos)):
        new_pos[i] =  new_pos[i] - M_in[trans_num][i] + M_out[trans_num][i]
    return new_pos


graph = nx.DiGraph()

processed_situations = [] 
future_positions = []
future_positions.append(positions)
current_positions = []

while len(future_positions) > 0: 
    flag = True 
    current_positions = future_positions[0].copy()
    
    while (flag) and (current_positions not in processed_situations):
        processed_situations.append(current_positions)
        trans_list = transitions_list(current_positions)
        
        if len(trans_list) >= 1: 
            for i in range (1, len(trans_list)):
                trans_num = trans_list[i]
                new_pos = get_new_positions(current_positions, trans_num)
                future_positions.append(new_pos)
                graph.add_edge(' '.join(map(str, current_positions)), ' '.join(map(str,new_pos)), weight = trans_num + 1)
                
            trans_num = trans_list[0]
            new_pos = get_new_positions(current_positions, trans_num)
            graph.add_edge(' '.join(map(str, current_positions)), ' '.join(map(str,new_pos)), weight = trans_num + 1)
            current_positions = new_pos.copy()
        else:
            flag = False
        
        if (sum(current_positions) > 15):
            break
        
    future_positions.pop(0)
    
if current_positions not in processed_situations:
    processed_situations.append(current_positions)
    
pos = nx.spring_layout(graph, k=10.)
labels = nx.get_edge_attributes(graph,'weight')
for key in labels.keys():
    labels[key] = 'T' + str(labels[key])
    
print(labels)

plt.figure(1,figsize=(14,14)) 
nx.draw_networkx_edge_labels(graph,pos, edge_labels=labels, alpha = 1, font_size=15)
nx.draw(graph, pos, node_size=8000, with_labels=True, arrows = True, arrowsize = 20, font_size=15)