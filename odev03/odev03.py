import numpy as np
import matplotlib.pyplot as plt

f = open("./data/lab8_0.30-2.22-1.52.mbd","r")
lines = f.readlines()

sensor_transmitter = {}

for line in lines:
    line_array = line.strip().split(",")
    dataObject = {"timestamp":float(line_array[0]),"sensor": line_array[1],"transmitter":line_array[2],"rssi":int(line_array[3])}
    dict_key = dataObject["sensor"] +"_"+dataObject["transmitter"]

    try:
        sensor_transmitter[dict_key]["data"].append(dataObject)
    except:
        sensor_transmitter[dict_key] ={"data": [dataObject],"maxRssi":-101,"minRssi":2}
    
    if dataObject["rssi"] >= sensor_transmitter[dict_key]["maxRssi"] :
        sensor_transmitter[dict_key]["maxRssi"] = dataObject["rssi"]
        
    if dataObject["rssi"] <= sensor_transmitter[dict_key]["minRssi"]:
        sensor_transmitter[dict_key]["minRssi"] = dataObject["rssi"]


for key in sensor_transmitter.keys():
    histogram_dict = {}
    range = np.arange(sensor_transmitter[key]["minRssi"],sensor_transmitter[key]["maxRssi"]+1)
    
    for value in range:
        histogram_dict[value] = 0;
    for sensorObject in sensor_transmitter[key]["data"]:
        histogram_dict[sensorObject["rssi"]] += 1
    sensor_transmitter[key]["rssi_histogram"] = histogram_dict

fig,subPlotArray =  plt.subplots(2,4)
xIndex = 0
yIndex = 0
for key in sensor_transmitter.keys():
        subPlotArray[xIndex][yIndex].set_title(key,fontsize=9)
        subPlotArray[xIndex][yIndex].bar(sensor_transmitter[key]["rssi_histogram"].keys(),sensor_transmitter[key]["rssi_histogram"].values(),width=0.7)
        yIndex += 1
        if yIndex == 4:
            yIndex = 0
            xIndex = 1
fig.suptitle("Rssi Histograms", fontsize=14)
plt.show()

w = 100
for key in sensor_transmitter.keys():
    analysis_window = []
    sensor_transmitter[key]["frequency_array"] = []
    for data in sensor_transmitter[key]["data"]:
        if len(analysis_window) < w:
            analysis_window.append(data["timestamp"])
        else:
            analysis_window.pop(0)
            analysis_window.append(data["timestamp"])
        
        if len(analysis_window) == w:
            frequency = w/(analysis_window[-1] - analysis_window[0])
            sensor_transmitter[key]["frequency_array"].append(frequency)
    

fig,subPlotArray =  plt.subplots(2,4)
xIndex = 0
yIndex = 0
for key in sensor_transmitter.keys():
        subPlotArray[xIndex][yIndex].set_title(key,fontsize=9)
        subPlotArray[xIndex][yIndex].plot(sensor_transmitter[key]["frequency_array"])
        yIndex += 1
        if yIndex == 4:
            yIndex = 0
            xIndex = 1
fig.suptitle("Anlik frekans degisimi", fontsize=14)
plt.show()
    
for key in sensor_transmitter.keys():
    histogram_dict = {}
    range = np.arange(1.5,2.55,0.05)
    for value in range:
        histogram_dict[value] = 0;
    for frequency in sensor_transmitter[key]["frequency_array"]:
        for value in range:
            if frequency >= value and frequency < value+0.05:
                histogram_dict[value] += 1
                break
        
    sensor_transmitter[key]["frequency_histogram"] = histogram_dict

fig,subPlotArray =  plt.subplots(2,4)
xIndex = 0
yIndex = 0
for key in sensor_transmitter.keys():
        subPlotArray[xIndex][yIndex].set_title(key,fontsize=9)
        subPlotArray[xIndex][yIndex].bar(sensor_transmitter[key]["frequency_histogram"].keys(),sensor_transmitter[key]["frequency_histogram"].values(),width=0.3)
        yIndex += 1
        if yIndex == 4:
            yIndex = 0
            xIndex = 1
fig.suptitle("anlik frekans Histogrami", fontsize=14)
plt.show()
