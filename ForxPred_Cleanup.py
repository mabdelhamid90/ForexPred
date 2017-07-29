import pandas as pd
import numpy as np

print('loading trading data')
tradeData = pd.read_csv('DAT_MT_EURUSD_M1_201707.csv', header=None)
print('done loading trading data')

# add colummn names
tradeData.columns = ['date', 'time', 'open', 'upperShadow', 'lowerShadow', 'close', 'obsolete']

#########################################################
################    Data Cleanup   ######################
#########################################################

# TODO: remove Fri and Sat automaticaly
# drop the data for 2017.07.02 since it starts @5:00PM (we don't have the whole day data)
tradeData = tradeData[tradeData['date'] != '2017.07.02']
# drop the data for 2017.07.21 since it ends @5:00PM (we don't have the whole day data)
tradeData = tradeData[tradeData['date'] != '2017.07.21']

# for now we only need date, time and close. so remove the rest
tradeData.drop(['open', 'upperShadow', 'lowerShadow', 'obsolete'], axis=1, inplace=True)

# combine the data and time column
temp_dateTime = tradeData['date'] + ' ' + tradeData['time']
tradeData['dateTime'] = pd.to_datetime(temp_dateTime)
tradeData.drop(['date', 'time'], axis=1, inplace=True)
tradeData = tradeData[['dateTime', 'close']]
tradeData.to_csv('close_1.csv', index=False, float_format='%.6f')
print(tradeData.shape)

# fill the gaps in the data
# make dates the index

idx = pd.DatetimeIndex(start=min(tradeData.dateTime), end=max(tradeData.dateTime), freq='min')
tradeData_clean = pd.DataFrame()
tradeData_clean['dateTime'] = idx
tradeData = tradeData.reset_index(drop=True)
tradeData_clean = tradeData_clean.reset_index(drop=True)
tradeData_clean['close'] = 0.000000
for index, row in tradeData.iterrows():
    if index % 100 == 0:
        print(index)    
    temp = tradeData_clean['dateTime'] == row['dateTime']
    temp_index = temp[temp == True].index[0]
    tradeData_clean['close'][temp_index]= row['close']
print(tradeData.shape)

print('writing clean trading data....')
tradeData_clean.to_csv('DAT_MT_EURUSD_M1_201707_clean.csv', index=False, float_format='%.6f')
print('done writing clean trading data')
