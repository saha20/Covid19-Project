import json
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import re
import requests 
import numpy as np

class countryWise:
    def getIndiaData(self):
        worlddf = pd.read_csv("owid-covid-data.csv")
        indiadata = worlddf[worlddf.location == "India"]
        uselessattributesinIndia = ["iso_code","location","total_cases_per_million", "new_cases_per_million", 
        "total_deaths_per_million", "new_deaths_per_million", "new_tests", "total_tests_per_thousand", 
        "new_tests_per_thousand", "tests_units"]
        indiadata.drop(uselessattributesinIndia,axis=1,inplace=True)
        indiadata.replace(r'^\s+$', np.nan, regex=True)
        columnnames = indiadata.columns
        for col in columnnames:
            indiadata[col].fillna("0",inplace=True)
        return indiadata
    def getUSdata(self):
        worlddf = pd.read_csv("owid-covid-data.csv")
        USdata = worlddf[worlddf.location == "United States"]
        uselessattributesinUS = ["iso_code","location","total_cases_per_million", "new_cases_per_million", 
        "total_deaths_per_million", "new_deaths_per_million", "new_tests", "total_tests_per_thousand", 
        "new_tests_per_thousand", "tests_units"]
        USdata.drop(uselessattributesinUS,axis=1,inplace=True)
        USdata.replace(r'^\s+$', np.nan, regex=True)
        columnnames = USdata.columns
        for col in columnnames:
            USdata[col].fillna("0",inplace=True)
        return USdata

# obj = countryWise()
# print(obj.getUSdata())
# print(obj.getIndiaData())


class beds:
    def readData(self):
        mainlist = list()
        fileo = open("beds.json")
        data = json.load(fileo)
        fileo.close()
        all_states = data["data"]["regional"]
        for i in range(0,len(all_states)):
            state = data["data"]["regional"][i]["state"]
            ruralHospitals = data["data"]["regional"][i]["ruralHospitals"]
            ruralBeds = data["data"]["regional"][i]["ruralBeds"]
            urbanHospitals = data["data"]["regional"][i]["urbanHospitals"]
            urbanBeds = data["data"]["regional"][i]["urbanBeds"]
            totalHospitals = data["data"]["regional"][i]["totalHospitals"]
            totalBeds = data["data"]["regional"][i]["totalBeds"]
            temp = list()
            temp.append(state)
            temp.append(ruralHospitals)
            temp.append(ruralBeds)
            temp.append(urbanHospitals)
            temp.append(urbanBeds)
            temp.append(totalHospitals)
            temp.append(totalBeds)
            mainlist.append(temp)
        keylist = ["state","ruralHospitals","ruralBeds","urbanHospitals","urbanBeds","totalHospitals","totalBeds"]
        df = pd.DataFrame(mainlist,columns = keylist)
        df.replace(r'^\s+$', np.nan, regex=True)
        columnnames = df.columns
        for col in columnnames:
            df[col].fillna("0",inplace=True)
        return df

# temp = beds()
# print(temp.readData())

class medicalColleges:
    def readData(self):
        mainlist = list()
        fileo = open("medical-colleges.json")
        data = json.load(fileo)
        fileo.close()
        all_states = data["data"]["medicalColleges"]
        for i in range(0,len(all_states)):
            state = data["data"]["medicalColleges"][i]["state"]
            name = data["data"]["medicalColleges"][i]["name"]
            city = data["data"]["medicalColleges"][i]["city"]
            ownership = data["data"]["medicalColleges"][i]["ownership"]
            admissionCapacity = data["data"]["medicalColleges"][i]["admissionCapacity"]
            hospitalBeds = data["data"]["medicalColleges"][i]["hospitalBeds"]
            temp = list()
            temp.append(state)
            temp.append(name)
            temp.append(city)
            temp.append(ownership)
            temp.append(admissionCapacity)
            temp.append(hospitalBeds)
            mainlist.append(temp)
        keylist = ["state","name","city","ownership","admissionCapacity","hospitalBeds"]
        df = pd.DataFrame(mainlist,columns = keylist)
        df.replace(r'^\s+$', np.nan, regex=True)
        columnnames = df.columns
        for col in columnnames:
            df[col].fillna("0",inplace=True)
        statelist = list(df['state'].unique())
        tempdict = dict()
        for i in range(0,len(statelist)):
            tempdict[statelist[i]] = 0
        for ind in df.index:
            state = df['state'][ind]
            hospitalBeds = int(df['hospitalBeds'][ind])
            tempdict[state] = tempdict[state]+hospitalBeds
        mainlist = []
        for i in tempdict.keys():
            state = i
            medbeds = tempdict[i]
            tlist = list()
            tlist.append(state)
            tlist.append(medbeds)
            mainlist.append(tlist)
        keys = ["state","medicalCollegeBeds"]
        df = pd.DataFrame(mainlist,columns = keys)
        df.replace(r'^\s+$', np.nan, regex=True)
        columnnames = df.columns
        for col in columnnames:
            df[col].fillna("0",inplace=True)
        return df
        
# temp = medicalColleges()
# print(temp.readData())

class mohfw:
    def readData(self):
        mainlist = list()
        fileo = open("covid19/data/mohfw.json")
        data = json.load(fileo)
        fileo.close()
        statedf = pd.read_csv("states.csv")
        states = dict()
        for ind in statedf.index:
            abbr = statedf['A'][ind]
            stat = statedf['B'][ind]
            states[abbr] = stat
        for i in range(0,data["total_rows"]):
            temp = data["rows"][i]["id"].split("T")
            date = temp[0]
            state = data["rows"][i]["value"]["state"]
            state = states[state]
            cured = data["rows"][i]["value"]["cured"]
            death = data["rows"][i]["value"]["death"]
            confirmed = data["rows"][i]["value"]["confirmed"]
            temp = list()
            temp.append(date)
            temp.append(state)
            temp.append(cured)
            temp.append(death)
            temp.append(confirmed)
            mainlist.append(temp)
        keylist = ["date","state","cured","death","confirmed"]
        df = pd.DataFrame(mainlist,columns = keylist)
        df.replace(r'^\s+$', np.nan, regex=True)
        columnnames = df.columns
        for col in columnnames:
            df[col].fillna("0",inplace=True)
        maindict = {}
        statelist = list(df['state'].unique())
        statetoindex = {}
        index = 0
        for i in statelist:
            statetoindex[i] = index
            index = index + 1
        layer3list = list()
        for i in range(0,index):
            templist = list()
            layer3list.append(templist)
        for ind in df.index:
            date = df['date'][ind]
            state = df['state'][ind]
            cured = df['cured'][ind]
            death = df['death'][ind]
            confirmed = df['confirmed'][ind]
            layer1list = list()
            layer1list.append(date)
            layer1list.append(state)
            layer1list.append(cured)
            layer1list.append(death)
            layer1list.append(confirmed)
            stateindex = statetoindex[state]
            layer3list[stateindex].append(layer1list)
        for i in statetoindex.keys():
            statename = i
            index = statetoindex[statename]
            keylist = ["date","state","cured","death","confirmed"]
            df = pd.DataFrame(layer3list[index],columns = keylist)
            maindict[statename] = df
            df.drop_duplicates(subset ="date", 
                     keep = "first", inplace = True)
        return maindict

# temp = mohfw()
# #Note that this returns a dictionary
# statedict = temp.readData()
# print(statedict["Maharashtra"])

class swineflu:
    def readData(self):
        df = pd.read_csv("h1n1.csv",encoding = "ISO-8859-1")
        df['Country'] = df['Country'].apply(lambda x: ''.join([i if ord(i) in range(65,91) or ord(i) in range(97,123) else "" for i in x]))
        for ind in df.index:
            date = df['Update Time'][ind]
            date = date.split(" ")[0]
            temp = date.split("/")
            mm = temp[0]
            dd = temp[1]
            yy = temp[2]
            date = yy + "-" + mm + "-" + dd
            df.at[ind,'Update Time'] = date
        df.replace(r'^\s+$', np.nan, regex=True)
        columnnames = df.columns
        for col in columnnames:
            df[col].fillna("0",inplace=True)
        return df

# temp = swineflu()
# print(temp.readData())

class rawjson:
    def readData(self):
        hugedataset = open("raw_data.json")
        dataset = json.load(hugedataset)
        hugedataset.close()
        keylist = list(dataset["raw_data"][0].keys())
        listoflist = []
        for i in range(len(dataset["raw_data"])):
            templist = list()
            for j in keylist:
                templist.append(dataset["raw_data"][i][j])
            listoflist.append(templist)
        df = pd.DataFrame(listoflist,columns = keylist)
        total = len(dataset["raw_data"])
        usefulattributes = []
        for i in range(len(keylist)):
            temp = (len(df[df[keylist[i]] == ''])*100)/total
            if temp<30:
                usefulattributes.append(keylist[i])
        uselessattributes = []
        for i in keylist:
            if i not in usefulattributes:
                uselessattributes.append(i)
        uselessattributes.append("notes")
        usefulattributes.remove("notes")
        df.drop(uselessattributes,axis=1,inplace=True)
        removelist = []
        for ind in df.index:
            if df['detecteddistrict'][ind]=='' or df['detectedstate'][ind]=='':
                removelist.append(ind)
        df.drop(df.index[removelist],inplace=True)
        print(len(df))
        df.replace(r'^\s+$', np.nan, regex=True)
        columnnames = df.columns
        for col in columnnames:
            df[col].fillna("0",inplace=True)
        return df

# temp = rawjson()
# print(temp.readData())

class timeseries:
    def readData(self,countryname):
        hugedataset = open("timeseries.json")
        dataset = json.load(hugedataset)
        hugedataset.close()
        mainlist = list()
        data = dataset[countryname]
        for i in range(0,len(data)):
            date = data[i]['date']
            confirmed = data[i]['confirmed']
            deaths = data[i]['deaths']
            recovered = data[i]['recovered']
            templist = list()
            templist.append(date)
            templist.append(confirmed)
            templist.append(deaths)
            templist.append(recovered)
            mainlist.append(templist)
        keys = ["date","confirmed","deaths","recovered"]
        df = pd.DataFrame(mainlist,columns = keys)
        df.replace(r'^\s+$', np.nan, regex=True)
        columnnames = df.columns
        for col in columnnames:
            df[col].fillna("0",inplace=True)
        return df
            
# temp = timeseries()
# print(temp.readData("India"))