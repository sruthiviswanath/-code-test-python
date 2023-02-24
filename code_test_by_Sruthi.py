import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


df = pd.read_csv("event_data.csv")
state_name = []
for index, row in df.iterrows():
    print(index)
    point = row['geo'].split('(')[1].split(')')[0]  
    lon, lat = point.split()  
    #print(lon)
    #print(lat)
    url = f"https://us-state-api.herokuapp.com/?lat={lat}&lon={lon}"
    response = requests.get(url)
    json_response = response.json()
    print(json_response)
    if(json_response['state'] != None):
        
        state_name.append(json_response['state']['name'])
            
                
df['state_name'] = pd.DataFrame(state_name)
print(df)


#  visualisation showing the distribution of events across states
num_events = df['state_name'].value_counts().sort_index()
print(num_events )
fig, ax = plt.subplots(figsize=(10,8))
ax.bar(num_events.index, num_events.values)
ax.set_xlabel('State')
ax.set_ylabel('Event count')
ax.set_title('Distribution of events across states')
plt.xticks(rotation=90)
plt.show()

# visualisation showing the sum value of events across states
value = df.groupby('state_name')['eventValue'].sum()
print(value)
fig, ax = plt.subplots(figsize=(10,8))
ax.bar(value.index, value.values)
ax.set_xlabel('State')
ax.set_ylabel('Sum value of events')
ax.set_title('Sum value of events across states')
plt.xticks(rotation=90)
plt.show()

# Identify and visualise temporal trends of the event data
df['created'] = pd.to_datetime(df['created'])
print(df['created'])
df.set_index('created', inplace=True)
daily_event = df['eventValue'].resample('D').sum().fillna(0)
print(daily_event)
daily_event_weekly = daily_event.rolling(window=7).mean()
print(daily_event_weekly)
fig, ax = plt.subplots(figsize=(10,8))
ax.plot(daily_event.index, daily_event.values, label='Daily Event Values')
ax.plot(daily_event_weekly.index, daily_event_weekly.values, label='weekly Moving Average')
ax.set_xlabel('Date')
ax.set_ylabel('Event Value')
ax.set_title('Temporal Trends of the Event Data')
plt.legend()
plt.show()
