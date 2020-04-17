#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob


# ### 1. We need to identify a way to consistently extract features for different cities stored in multiple files.
# Here, I create a list of files with fog data and extract city file names because fog data files are stored as "CityName19xx-xxxxFogData.txt". Inorder to get the city name I extract city name by considering all the string till it encounters first 1

# In[2]:


fogDataFiles = glob.glob("data/*2016_FogData.txt")
cityNames = []
for fileName in fogDataFiles:
    cityNames.append(fileName[5:fileName.find('1')])
del fogDataFiles


# ### 2. I can create a fileList for different cities <font color = 'red'> and naively removing files with "xxPercentagexx" in the  list </font>

# In[3]:


dataL = {}
for city in cityNames :
    fileList = glob.glob(str('data/*'+ city + '*'))
    fileList = [x[5:] for x in fileList if ("Percent" not in x)]
    print([city,len(fileList)])
#     print(fileList)
    dataT = {}
    for fileName in fileList : 
        indexNum = 6
        
        if(not fileName.startswith(city)):
            varName = fileName[:fileName.find('_')]
        
        else :
            varName = fileName[::-1][4:fileName[::-1].find('_')][::-1]
            
            if ('Fog' in varName) :
                indexNum = 0
                if('Mean' in varName):
                    varName = fileName[::-1][4:fileName[::-1].find('6')][::-1]
                    continue # Skipping for time being
#         print(varName)
        
        dataT[varName] = pd.read_csv('data/' + fileName, index_col=indexNum)  
    
    dataL[city] = pd.concat(dataT, axis = 1)

dataF = pd.concat(dataL, axis = 0)
del dataT, dataL, city, fileList, fileName, varName


# In[4]:


dataF


# In[5]:


dataF.columns.get_level_values(1).unique()

