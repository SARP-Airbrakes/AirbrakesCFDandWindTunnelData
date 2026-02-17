
multigraphs =''         #To print multiple graphs on the same graph input a string either 'q','length','dimple_cone','fins'
length = 4             #4/5.5
desired_q = 40           #40,45,50
dimple_cone = False      #True/False
fins = False              #True/False
flap_angle = 5         #0-45 per 5  -1 ifexit you want a graph of all angles


import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

CD = 0

#file Path of all the data folder
path = 'C:/Users/lucar/OneDrive/Desktop/College/Wind_Tunnel_Data/Look_Up/*.csv' 
# Get a list of all CSV files in the directory
# The glob.glob() function finds all path names matching the specified pattern
all_files = glob.glob(path)

# Create a list of DataFrames by reading each CSV file
# The (pd.read_csv(f) for f in all_files) is a generator expression
dfs = (pd.read_csv(f) for f in all_files)
# Concatenate all DataFrames in the list into a single DataFrame
# ignore_index=True resets the index of the combined DataFrame
combined_df = pd.concat(dfs, ignore_index=True)
# Remove Wind off Zero
combined_df = combined_df[combined_df['CODE'] != 1]
# radius of Rocket in ft
r = 1.616/2/12 
#Refrence Area in ft^2
A = np.pi*r**2
#CD EQ
CDEQ = lambda drag,q: drag/(A*q)
#creates an array with all angles
angles = np.linspace(0,45,10)
#for plotting
fig, QPlotsplt = plt.subplots()
def plotting(data):
    if(fins==True):
        fins_label = 'With Fins'
    else:
        fins_label = 'With Fins'
    if(dimple_cone==True):
        cone_label = 'Dimpled Cone'
    else:
        cone_label = 'Smooth Cone'

    plot_label = f"L={length}, Q={desired_q}, {fins_label}, {cone_label}"
    QPlotsplt.plot(angles,data,label=plot_label)
    QPlotsplt.set_xlabel('Angle of Flaps')
    QPlotsplt.set_ylabel('CD')
    QPlotsplt.set_title('CD Graph')
    QPlotsplt.legend(title="Configuration Specs", loc="best")

#Returns CD for a set angle
def findCD(angle):
    local_df = combined_df
    #remove alt flaps length
    local_df = local_df[local_df['Length'] == length]
    #remove alt Angle
    local_df = local_df[local_df['Flap Angle'] == angle]
    #remove Dimple Cone
    if(dimple_cone == True):
        local_df = local_df[local_df['DC/SC'] == 'DC']
    else:
        local_df = local_df[local_df['DC/SC'] != 'DC']
    #remove Fins
    if(fins == True):
        local_df = local_df[local_df['FCY/N'] == 'Y']
    else:
        local_df = local_df[local_df['DC/SC'] != 'Y']
    #Desired Q value
    if(desired_q == 40):
        local_df = local_df[local_df['TP'] == 2.0]
    elif(desired_q == 45):
        local_df = local_df[local_df['TP'] == 3.0]
    elif(desired_q == 50):
        local_df = local_df[local_df['TP'] == 4.0]
    return CDEQ(local_df['Drag (lbf)'].iloc[0],local_df['DYNAMIC PRESSURE'].iloc[0])

#prints a graph of all angles
def graphflapangles():
    if(flap_angle<0):
        graphCD = np.zeros(10)
        i = 0
        for x in angles:
            graphCD[i] = findCD(x)
            i=i+1
        plotting(graphCD)
#just returns CD PT
    else: 
        CD = findCD(flap_angle)
        print(CD)

#prints multiple graphs
if(multigraphs=='length'):
    length=4
    graphflapangles()
    length=5.5
    graphflapangles()
elif(multigraphs=='q'):
    desired_q = 40
    graphflapangles()
    desired_q = 45
    graphflapangles()
    desired_q = 50
    graphflapangles()
elif(multigraphs=='dimple_cone'):
    dimple_cone = True
    graphflapangles()
    dimple_cone = False
    graphflapangles()
elif(multigraphs=='fins'):
    fins = False
    graphflapangles()
    fins = True
    graphflapangles()
else:
    graphflapangles()
if(flap_angle<0):
    plt.show()









