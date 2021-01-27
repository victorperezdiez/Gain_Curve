#!/usr/bin/env python

def filter():

   f = open("tsys32vo_353.log", "r")
   lines = f.readlines()
   my_dict = {"Channel":[],"Elevation":[],"Tsys":[],"SEFD":[],"Gain":[]};

   print("Reading data \n")

   for x in lines:
      if (x.split(' ')[0][-3:] == 'VAL'):
         try:
            my_dict["Gain"].append(float(x.split()[9])/float(x.split()[10]))
         except ValueError:
            #gain.append($$$$$$)
            continue				#Algunas filas no tienen algún valor, las eliminamos

         my_dict["Channel"].append(str(x.split()[4]))
         my_dict["Elevation"].append(float(x.split()[3]))
         my_dict["Tsys"].append(float(x.split()[9]))
         my_dict["SEFD"].append(float(x.split()[10]))
   f.close()

   chan = set(my_dict['Channel'])
   print ("Writting files for: \n")    
   temp = 0   
   for i in chan:
      temp = temp + 1
      print("     Channel " + str(i) + ": " + str(temp) + "/" + str(len(chan)))
      with open('data_' + i + ".dat", 'w') as f:
         f.write(str("Channel Elevation Tsys SEFD Gain") + '\n')
         for j in range(len(my_dict["Channel"])):
            if (my_dict['Channel'][j] == i):
               f.write(i + ' ' + str(my_dict['Elevation'][j]) + ' ' + str(my_dict['Tsys'][j]) + ' ' + str(my_dict['SEFD'][j]) + ' ' + str(my_dict['Gain'][j]) + ' ' + '\n')
   f.close()    

   return chan


def graph():
   import matplotlib.pyplot as plt

   chan = filter()  
   
   print("\nPlotting graph for: \n")
   temp = 0

   for i in chan:
      temp = temp + 1
      print("     Channel " + str(i) + ": " + str(temp) + "/" + str (len(chan)) )	
      f = open("data_" + i + ".dat", 'r')
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
      #ax1.set_ylim(0, 0.03)
      ax1.set_xlim(0, 90)
      fig1.savefig("chan_" + i + ".png")
      plt.close(fig1)

print("GAIN CURVES \n")
graph()

	
   














	


