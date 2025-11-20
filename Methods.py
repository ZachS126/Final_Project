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
print(len(list_graphs))
print(np.mean(avg_k_in))
print(np.mean(avg_k_out))

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
