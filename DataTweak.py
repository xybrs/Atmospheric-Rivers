from matplotlib.colors import same_color
import numpy as np
import pandas
import matplotlib.pyplot as plt
import os
import pandas
from statistics import mean
from functools import reduce

path = "\Datasets"
start_dir = os.getcwd() + path

col_list = ["Date", "SWE"]

snotel_sites = os.listdir(start_dir)
snotel_data = {}            #This is the accumulated swe of snotel sites
snotel_daily_swe = {}       #This is the daily positive swe of snotel sites
snotel_normal_swe = {}      #This is the daily non-extreme positive swe of snotel sites
snotel_ewe_swe = {}         #This is the daily extreme swe of snotel sites


total_swe = [None]* len(snotel_sites)                   #This is the accumulated swe of all of the years combined 
average_annual_swe = [None]* len(snotel_sites)          #This is the average accumulated swe per water year

total_ewe_swe = [None]* len(snotel_sites)               #This is the accumulated extreme weather swe for all the years combined
average_annual_ewe_swe = [None]* len(snotel_sites)      #This is the average accumulated extreme weather swe for a water year

ewe_percentage_contribution = [None]*len(snotel_sites)

#Reading DATA from Snotels
for snotel in snotel_sites:
    file_path = start_dir + "\\" + snotel
    file_dataframe = pandas.read_csv(file_path, parse_dates=["Date"], usecols=["Date", "Snow Water Equivalent (in) Start of Day Values"], index_col=["Date"])
    file_dataframe = file_dataframe['10/1/1989' : '09/30/2020']
    snotel_data[snotel] = file_dataframe #Adding data to coin_datas
    
    #Calculating Daily SWE from ACC SWE
    diff_dataframe = file_dataframe.diff()
    diff_dataframe = diff_dataframe.clip(lower=0.1)

    snotel_daily_swe[snotel] = diff_dataframe

def preprocessing(index):
    global snotel_ewe_swe
    global ewe_percentage_contribution
    global average_annual_ewe_swe
    global total_ewe_swe
    global total_swe


    ########### Getting the snotel_positive values
    sample_snotel = snotel_daily_swe[snotel_sites[index]]
    #sample_snotel.to_csv(snotel_sites[index][:-4] + ' positive SWE.csv')

    ######CALCULATING AND STORING ONLY THE 99th Percentile
    percentile = sample_snotel.quantile(q = .99, axis = 0, numeric_only = True)
    percentile_cutoff = percentile[0]        #This is the value of our interest as all values >= are in the 99th percentile
    sample_snotel_99percentile = sample_snotel[sample_snotel['Snow Water Equivalent (in) Start of Day Values'] >= percentile_cutoff]
    
    snotel_ewe_swe[snotel_sites[index]] = sample_snotel_99percentile

    #sample_snotel_99percentile.to_csv(snotel_sites[index][:-4] + ' 99th percentile.csv')

    ##### Calculating accumulated SWE for all 31 years
    swe_total = sample_snotel.sum()[0]
    total_swe[index] = swe_total

    #######Calculating accumulated SWE for all 31 years contributed by EWE's
    swe_99percentile_total = sample_snotel_99percentile.sum()[0]
    total_ewe_swe[index] = swe_99percentile_total

    ####### Calculating percentage of accumulated SWE contributed by EWE's
    swe_99percentile_contribution_percentage = swe_99percentile_total/swe_total*100
    ewe_percentage_contribution[index] = swe_99percentile_contribution_percentage

    ############AVERAGES OF SWE's of previous step
    ### Calculating average accumulated SWE for a water year
    average_annual_swe[index] =  sample_snotel.sum()[0]/31

    ### Calculating average accumulated SWE contributed by EWE's for a water year
    average_annual_ewe_swe[index] =  sample_snotel_99percentile.sum()[0]/31

### These methods graph the datasets
def graph_raw_data(index):
    sample_snotel = snotel_data[snotel_sites[index]]
    #GRAPHING
    plt.title(snotel_sites[index][:-4])
    plt.xlabel('Date')
    plt.ylabel('Accumulated SWE (inches)')
    plt.plot(sample_snotel,label= snotel_sites[index][:-4])

    plt.legend()
    figure = plt.gcf()
    figure.set_size_inches(19, 10)

    ### IF you want to save the graph uncomment this line
    plt.savefig("Graphs/Raw Datasets/" + snotel_sites[index][:-4] + " Raw Data.png", bbox_inches='tight', dpi=120*2)
    plt.show()

def graph_daily_swe(index):
    sample_snotel = snotel_daily_swe[snotel_sites[index]]
    #GRAPHING
    plt.title(snotel_sites[index][:-4])
    plt.xlabel('Date')
    plt.ylabel('SWE (inches)')
    plt.plot(sample_snotel,label= snotel_sites[index][:-4])

    plt.legend()
    figure = plt.gcf()
    figure.set_size_inches(19, 10)

    plt.savefig("Graphs/Daily SWE/" + snotel_sites[index][:-4] + "SWE .png", bbox_inches='tight',dpi=120*2)
    plt.show()

def graph_daily_ewe_swe(index):
    sample_snotel = snotel_ewe_swe[snotel_sites[index]]
    #GRAPHING
    plt.title(snotel_sites[index][:-4])
    plt.xlabel('Date')
    plt.ylabel('SWE (inches)')
    
    plt.scatter(x=snotel_ewe_swe[snotel_sites[index]].index.values, y = sample_snotel,label= snotel_sites[index][:-4])

    plt.legend()
    figure = plt.gcf()
    figure.set_size_inches(19, 10)
    
    plt.savefig("Graphs/Daily EWE SWE/99 Percentile/" + snotel_sites[index][:-4] + "99 Percentile EWE SWE.png", bbox_inches='tight',dpi=120*2)
    plt.show()

def graph_ewe_percentage_contribution():
    #GRAPHING
    fig = plt.figure(figsize = (10, 5)) 
    # creating the bar plot
    plt.bar([site[:-4] for site in snotel_sites[:10]], ewe_percentage_contribution[:10])
    
    plt.xlabel("Snotel Sites")
    plt.ylabel("Percentage of SWE contributed by EWE")
    plt.show()

def graph_total_swe():
    #GRAPHING
    fig = plt.figure(figsize = (10, 5)) 
    # creating the bar plot
    plt.barh(snotel_sites[:], average_annual_swe[:])

    plt.xlabel("Total SWE")
    plt.ylabel("Snotel Sites")
    plt.show()

def graph_total_ewe():
    #GRAPHING
    fig = plt.figure(figsize = (10, 5)) 
    # creating the bar plot
    plt.barh(snotel_sites[:], average_annual_ewe_swe[:])

    plt.xlabel("Total Extreme Weather SWE")
    plt.ylabel("Snotel Sites")
    plt.show()

def graph_annual_swe():
    #GRAPHING
    fig = plt.figure(figsize = (10, 5)) 
    # creating the bar plot
    plt.barh(snotel_sites[:], average_annual_swe[:])

    plt.xlabel("Average SWE")
    plt.ylabel("Snotel Sites")
    plt.show()

def graph_annual_ewe():
    #GRAPHING
    fig = plt.figure(figsize = (10, 5)) 
    # creating the bar plot
    plt.barh(snotel_sites[:], average_annual_ewe_swe[:])

    plt.xlabel("Average Extreme Weather SWE")
    plt.ylabel("Snotel Sites")
    plt.show()

#### This function graphs the SWE contribution in the Yampa river basin by its constituent normal SWE and extreme weather SWE
def graph_swe_breakdown():

    extremeSWE = [None] * len(snotel_sites)
    normalSWE = [None] * len(snotel_sites)

    basin_normalSWE = None
    basin_extremeSWE = None

    for i in range(len(snotel_sites)):
        extremeSWE[i] = average_annual_swe[i]
        normalSWE[i] = average_annual_swe[i] - average_annual_ewe_swe[i]

    ########This step is for Yampa River Basin
    #Calculating the swe's for the basin
    basin_normalSWE = mean(normalSWE)
    basin_extremeSWE = mean(extremeSWE)
    snotel_sites.append("YAMPA RIVER BASIN.csv")
    extremeSWE.append(basin_extremeSWE)
    normalSWE.append(basin_normalSWE)

    #GRAPHING
    fig, ax = plt.subplots() 
    # creating the bar plot
    ax.barh([site[:-4] for site in snotel_sites], extremeSWE[:], label = "Extreme Weather SWE per Water Year", color = 'C1')
    ax.barh([site[:-4] for site in snotel_sites], normalSWE[:], label = "Non-extreme SWE per Water Year", color = 'C0')
    
    ax.set_xlabel("Total SWE (inches)")
    ax.set_ylabel("Snotel Sites")
    plt.title("SWE Breakdown of Yampa River Basin")
    ax.legend()

    plt.legend(bbox_to_anchor=(1.05, 1))
    figure = plt.gcf()
    figure.set_size_inches(19, 10)

    plt.savefig("Graphs/SWE Breakdown/99 Percentile/" + "99 Percentile SWE Breakdown.png", bbox_inches='tight',dpi=120*2)
    plt.show()
    snotel_sites.remove("YAMPA RIVER BASIN.csv")

#This function graphs all of the days Extreme Weather occured and their corresponding SWE's
def graph_ewe_days():

    #####Finding Yampa River Basin Mean EWE
    yampa_river_basin = reduce(lambda x, y: x.add(y, fill_value=0), [snotel_daily_swe[site] for site in snotel_sites])
    yampa_river_basin = yampa_river_basin/len(snotel_sites)

     ######CALCULATING AND STORING ONLY THE 99th Percentile
    percentile = yampa_river_basin.quantile(q = .99, axis = 0, numeric_only = True)
    percentile_cutoff = percentile[0]        #This is the value of our interest as all values >= are in the 99th percentile
    yampa_river_99percentile = yampa_river_basin[yampa_river_basin['Snow Water Equivalent (in) Start of Day Values'] >= percentile_cutoff]
    
    snotel_ewe_swe["Yampa River Basin.csv"] = yampa_river_99percentile
    snotel_sites.append("Yampa River Basin.csv")

    #GRAPHING
    fig = plt.figure() 
    # creating the bar plot

    #for site in snotel_sites:
    #    df = snotel_ewe_swe[site].astype(str)
    #    df['Snow Water Equivalent (in) Start of Day Values'] = df['Snow Water Equivalent (in) Start of Day Values'].replace([row[0] for _,row in df.iterrows()],site[:-4])
    #    plt.scatter(df.index.values, df["Snow Water Equivalent (in) Start of Day Values"], label= site[:-4], s = 1)


    #for site in snotel_sites:
    #    plt.scatter(snotel_ewe_swe[site].index.values, snotel_ewe_swe[site]["Snow Water Equivalent (in) Start of Day Values"], label= site[:-4])
    
    i=1
    for site in snotel_sites[-9:]:
        plt.subplot(3,3,i)
        plt.scatter(snotel_ewe_swe[site].index.values, snotel_ewe_swe[site]["Snow Water Equivalent (in) Start of Day Values"], label= site[:-4])
        plt.title(site[:-4])
        i+=1

    plt.xlabel("Water Years")
    plt.ylabel("Snotel Sites")
    
    plt.legend(bbox_to_anchor=(1.05, 1))
    figure = plt.gcf()
    figure.set_size_inches(19, 10)

    plt.savefig("Graphs/EWE Days/99 Percentile/" + "99 Percentile EWE Days.png", bbox_inches='tight', dpi=120*2)
    plt.show()

def main():
    for i in range (len(snotel_sites)):
        preprocessing(i)
        #graph_raw_data(i)
        #graph_daily_swe(i)
        #graph_daily_ewe_swe(i)

    #graph_swe_breakdown()
    graph_ewe_days()

if __name__ == "__main__":
    main()