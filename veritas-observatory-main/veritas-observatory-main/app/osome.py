import requests
import webbrowser
import re
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, output_file, show

def osome(query, startdate, enddate):

    url = "https://osome-public.p.rapidapi.com/time-series"
    
    querystring = {"start": startdate,"q":query,"end":enddate}
    
    headers = {
        'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        'x-rapidapi-host': "osome-public.p.rapidapi.com"
        }
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    
    print(response.text)
    
    file=open("osomeresults.txt", "w")
    file.write(str(response.text))
    file.close()
    text = str(response.text)
    match = re.search("result_url\": \"(.+?)\"" ,text, flags=re.IGNORECASE)
    
    try:
        result = match.group(1)
    except:
        result = "no match found"
        
    
    url2 = result
    response2 = requests.request("GET", url2)
    
    
    file = open("osomequery", "w")
    file.write(str(response2.text))
    file.close()
    a_file = open("osomequery")
    
    listatwdate = []
    listatwvol= []
    for line in a_file:
        key, value = line.split()
        listatwdate.append(key)
        listatwvol.append(value)
    
    dataframetw = pd.DataFrame({'dates': listatwdate, 'num': listatwvol})
    
    dataframetw['dates'] = pd.to_datetime(dataframetw['dates'], format='%Y-%m-%d')
    
    sourcetw = ColumnDataSource(dataframetw)
    return sourcetw
    #plot = figure(title='Sentiment analysis over time', x_axis_type="datetime", plot_width=600, plot_height=350, x_axis_label='date', y_axis_label='sentiment analysis')
    #line1=plot.line('dates', 'num', source=sourcetw)
    #line2=plot.line('dates2', 'se2', source=source2, color="red", legend_label=htq2)
    #show(plot)

