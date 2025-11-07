import numpy as np
import polars as pl
import networkx as nx
import matplotlib.pyplot as plt

#read in sample sheet
ss = pl.read_csv('Final_Project/Ovary/sample_sheet.tsv', separator = '\t')

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
raw_dict = pl.read_excel('Final_Project/Ovary/dictionary_ids.xlsx', read_options = {"header_row": 1})
print(raw_dict.head())

#create dictionary from dataframe
dict_ids = {}
for i in range(raw_dict.height):
    dict_ids[raw_dict["TCGA id"][i]] = raw_dict["Model id"][i]

#print(dict_ids)

#Create list of graphs (Tissue specific)
list_graphs = []
for i in range (ss.height):
    filepath = (f"Final_Project/Ovary/Metabolites-based/Metabolites-based_tissue/meanSum_{ss["Sample.ID"][i]}.graphml")
    print(filepath)
    list_graphs.append(nx.read_graphml(filepath))
    print(len(list_graphs))
print(len(list_graphs))

#create list of graphs (PGDSMM)
#list_graphs = []
#for i in range (raw_dict.height):
    #filepath = (f"BIOL4559hw/Final_Project/Ovary/Metabolites-based/Metabolites-based_PDGSMMs/meanSum_{raw_dict["Model id"][i]}.graphml")
    #print(filepath)
    #list_graphs.append(nx.read_graphml(filepath))
    #print(len(list_graphs))
#print(len(list_graphs))

plt.figure()
nx.draw(list_graphs[1], node_color='blue', edge_color = 'black', node_size = 10)
plt.show()