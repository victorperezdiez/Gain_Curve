#!/usr/bin/env python

def filter(data):
   f = open(data, "r")
   lines = f.readlines()
   my_dict = {"Channel":[],"Elevation":[],"Tsys":[],"SEFD":[],"Gain":[]};
   

   print("Reading data \n")

   for x in lines:
      if (x.split(' ')[0][-3:] == 'VAL'):
         try:
            my_dict["Gain"].append(float(x.split()[9])/float(x.split()[10]))
         except ValueError:
            #gain.append($$$$$$)
            continue				#Delete files with non-numeric values

         my_dict["Channel"].append(str(x.split()[4]))
         my_dict["Elevation"].append(float(x.split()[3]))
         my_dict["Tsys"].append(float(x.split()[9]))
         my_dict["SEFD"].append(float(x.split()[10]))
   f.close()

   #Writing files
   chan = set(my_dict['Channel'])
   print ("Writting files for: \n")    
   temp = 0   
   for i in chan:
      temp = temp + 1
      print("     Channel " + str(i) + ": " + str(temp) + "/" + str(len(chan)))
      with open('Data/data_' + i + ".dat", 'w') as f:
         f.write(str("Channel Elevation Tsys SEFD Gain") + '\n')
         for j in range(len(my_dict["Channel"])):
            if (my_dict['Channel'][j] == i and 0 < my_dict['Gain'][j] < 0.15):
               f.write(i + ' ' + str(my_dict['Elevation'][j]) + ' ' + str(my_dict['Tsys'][j]) + ' ' + str(my_dict['SEFD'][j]) + ' ' + str(my_dict['Gain'][j]) + ' ' + '\n')
   f.close()    

   return chan


def clean(channels, outlierConstant):
   #Removing outliers
   print ("Removing outliers for: \n")
   import numpy as np

   h = 0

   for i in channels:
      f = open("Data/data_" + i + ".dat", 'r')
      next(f)
      lines=f.readlines()

      SEFD_clean=[]  
      ele_clean=[]
      gain_clean=[]
      tsys_clean=[]

      for j in range(1, 17): 
         tsys=[]
         SEFD=[]   
         ele=[]
         gain=[]   
      
         for x in lines:
            if (10+(j-1)*5 <= float(x.split(' ')[1]) <= 10+j*5):          #Splitting in 5º portions, we eliminate values far from mean
               ele.append(float(x.split(' ')[1]))
               gain.append(float(x.split(' ')[4]))
               tsys.append(float(x.split(' ')[2])) 
               SEFD.append(float(x.split(' ')[3]))  
         f.close()

         a = np.array(gain)
         upper_quartile = np.percentile(a, 75)
         lower_quartile = np.percentile(a, 25)
         IQR = (upper_quartile - lower_quartile) * outlierConstant
         quartileSet = (lower_quartile - IQR, upper_quartile + IQR)
         k = 0
         for y in a.tolist():
            if (y >= quartileSet[0] and y <= quartileSet[1] and 0.005 < y < 1):
               ele_clean.append(ele[k])
               gain_clean.append(gain[k])
               tsys_clean.append(tsys[k])
               SEFD_clean.append(SEFD[k])

            k = k + 1

      #Writing files
      with open('Clean_Data/data_' + i + ".dat", 'w') as f:
         f.write(str("Channel Elevation Tsys SEFD Gain") + '\n')
         for j in range(len(gain_clean)):
            f.write(i + ' ' + str(ele_clean[j]) + ' ' + str(tsys_clean[j]) + ' ' + str(SEFD_clean[j]) + ' ' + str(gain_clean[j]) + ' ' + '\n')
      f.close()  
      print("     Channel " + str(i) + ": " + str(h) + "/" + str(len(channels)))
      h = h + 1


def graph(data, cle, outlierConstant):
   import matplotlib.pyplot as plt
   import os
   if not os.path.exists('Plots'):
    os.makedirs('Plots')
   if not os.path.exists('Data'):
    os.makedirs('Data')
   if not os.path.exists('Clean_Data'):
    os.makedirs('Clean_Data')

   chan = filter(data)
   clean(chan, outlierConstant)
   
   
   print("\nPlotting graph for: \n")
   temp = 0

   for i in chan:
      temp = temp + 1
      print("     Channel " + str(i) + ": " + str(temp) + "/" + str (len(chan)) )	
      f = open(str(cle) + "Data/data_" + i + ".dat", 'r')
      next(f)
      lines=f.readlines()
      

      ele=[]
      gain=[]

      for x in lines:
         ele.append(float(x.split(' ')[1]))
         gain.append(float(x.split(' ')[4])) 

      f.close()

      fig1, ax1 = plt.subplots(1, 1, figsize=(12, 7), facecolor='w', edgecolor='k')
      ax1.scatter(ele, gain, marker='o', s=1, label='SBD')
      ax1.set_title("Channel " + i)
      ax1.set_xlabel('Elevation (º)')
      ax1.set_ylabel('Gain (K/Jy)')
      ax1.set_xlim(0, 90)
      ax1.set_ylim(0, 0.15)
      fig1.savefig("Plots/chan_" + i + "_clean" + str(outlierConstant) + ".png")
      plt.close(fig1)


print("\n GAIN CURVES \n")
data =  "tsys32vo_353.log"             # Filename
cle = "Clean_"                         # "Clean_" for cleaning, "" for no cleaning
outlierConstant = 1.1                    # The smaller, the more clean         
graph(data, cle, outlierConstant)
