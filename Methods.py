import numpy as np
import polars as pl
import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

'''
#Normal Tissue Network
graph = nx.read_graphml('Ovary.xml')

print(f"Number of nodes: {graph.number_of_nodes()}")

'''


#Cancer Networks

#read in sample sheet
ss = pl.read_csv('More_Github_Bullshit/Ovary/sample_sheet.tsv', separator = '\t')
#print(ss.head())

# Get the list of column names
column_names = ss.columns

# Print each column name
#print("Headers (Column Names):")
#for name in column_names:
    #print(name)

#Example for getting element in the Sample.ID column
#print(ss["Sample.ID"][100])

#read in dictionary
raw_dict = pl.read_excel('More_Github_Bullshit/Ovary/dictionary_ids.xlsx', read_options = {"header_row": 1})
print(raw_dict.head())

#create dictionary from dataframe
dict_ids = {}
for i in range(raw_dict.height):
    dict_ids[raw_dict["TCGA id"][i]] = raw_dict["Model id"][i]

#print(dict_ids)

avg_k_in = []
avg_k_out = []

#Create list of graphs (Tissue specific )
list_graphs = []
for i in range (ss.height):
    filepath = (f"More_Github_Bullshit/Ovary/Metabolites-based/Metabolites-based_tissue/meanSum_{ss['Sample.ID'][i]}.graphml")
    #print(filepath)

    in_deg = []
    out_deg = []

    g = nx.read_graphml(filepath)
    
    for n, d in g.in_degree():
        in_deg.append(d)
    for n, d in g.out_degree():
        out_deg.append(d)
    
    avg_k_in.append(np.mean(in_deg))
    avg_k_out.append(np.mean(out_deg))

    list_graphs.append(g)
    #print(len(list_graphs))

per_node_in = {}
per_node_out = {}
count = 0


#Calculate average in and out degree for every node across all graphs
for g in list_graphs:
    for i, n in enumerate(g.nodes()):
        if n not in per_node_in or n not in per_node_out:
            per_node_in[n] = 0
            per_node_out[n] = 0
        per_node_in[n] += g.in_degree(n)
        per_node_out[n] += g.out_degree(n)
    for n in g.nodes():
        per_node_in[n] /= len(list_graphs)
        per_node_out[n] /= len(list_graphs)

test_in = []
test_out = []

for n, d in enumerate(list_graphs[0].nodes()):
    test_in.append(list_graphs[0].in_degree(d))
    test_out.append(list_graphs[0].out_degree(d))

np.save('test_in.npy', test_in)
np.save('test_out.npy', test_out)

#Save per_node_in and per_node_out in .npy files
np.save('per_node_in1.npy', np.array(list(per_node_in.values())))
np.save('per_node_out1.npy', np.array(list(per_node_out.values())))


print(len(list_graphs))
print(np.mean(avg_k_in))
print(np.mean(avg_k_out))


filepath = (f"More_Github_Bullshit/Ovary/Metabolites-based/Metabolites-based_tissue/meanSum_TCGA-04-1331-01A.graphml")
G = nx.read_graphml(filepath)


pos = nx.forceatlas2_layout(G, max_iter = 100, scaling_ratio = 0.5, gravity = 0.5, dissuade_hubs=True)
#pos = nx.spring_layout(G, k=1000, iterations=50, method = 'energy', gravity = 0.5, scale = 20)

#nx.draw_networkx_nodes(G, pos, node_size=1)


weights_dict = nx.get_edge_attributes(G, 'weight')
edge_weights = [weights_dict[edge] for edge in G.edges()]

scaled_weights = [w * 0.1 for w in edge_weights]

#plt.figure(figsize=(20, 16))
#nx.draw_networkx_edges(G, pos, width=scaled_weights)

degrees = [deg for _, deg in G.in_degree()] # For any graph G

vals, freq = np.unique(degrees, return_counts=True)

plt.scatter(vals, freq, marker="o")
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("In-Degree Distribution (Ovarian Cancer Tissue)")
plt.show()



#create list of graphs (PGDSMM)
#list_graphs = []
#for i in range (raw_dict.height):
    #filepath = (f"BIOL4559hw/Final_Project/Ovary/Metabolites-based/Metabolites-based_PDGSMMs/meanSum_{raw_dict["Model id"][i]}.graphml")
    #print(filepath)
    #list_graphs.append(nx.read_graphml(filepath))
    #print(len(list_graphs))
#print(len(list_graphs))

#plt.figure()
#nx.draw(list_graphs[1], node_color='blue', edge_color = 'black', node_size = 10)
#plt.show()
