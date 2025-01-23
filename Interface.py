#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 21:53:44 2022

@author: carolinaazevedo
"""
##############################################################################
#                   Biblio Import
##############################################################################
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from tkinter import *
from tkinter import messagebox
import serial.tools.list_ports
import pandas as pd
import threading

#Online Plot on AdaFruit.IO
from Adafruit_IO import MQTTClient, RequestError, Client, Feed

import ECG_Functions as funcECG
import EMS_FiltrosDigitais as filt

##############################################################################
#              Variables used for control
##############################################################################
cond = False       #variable used to control the real plot cycle
cond2 = False       #variable used to control the online plot cycle
i=0
counter = 0

########################################################
########################################################
#IT NEEDS TO BE CHANGED INTO YOUR OWN DATA!!!!!!!!!

#Adafruit IO key.
ADAFRUIT_IO_KEY = YOUR_KEY

#Adafruit IO username.
ADAFRUIT_IO_USERNAME = YOUR_NAME

########################################################
########################################################


####################################################
####################################################
# Class Root_ECG() - Root of the GUI interface
####################################################
####################################################
class RootGUI_ECG():
    def __init__(self):
        self.root = Tk()
        self.root.title("ECG Data Signal")
        self.root.geometry("1500x800")
        self.root.config(bg="#D3D3D3")
        
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        
    def close_window(self):
        print("Closing the window and exit")
        self.root.destroy()
        try:
            self.ser.close()
        except:
            pass
####################################################
####################################################
# Class ComGUI() - implements all buttons and their 
#                  respectives functions 
####################################################
####################################################        
class ComGUI():
    def __init__(self, root):
        '''
        Initialize the connexion GUI and initialize the main widgets
        '''
        self.root = root
        
        #self.frame1 = LabelFrame(root, text="Com Manager", padx=5, pady=5, bg="white")
        #self.label_COM = Label(self.frame1, text = "Port: /dev/cu.usbserial-0001", padx = 5, pady = 5, bg = "white")
        #self.label_Baud = Label(self.frame1, text = "Baud Rate: 115200", padx = 1, pady = 5, bg = "white")
        
        self.frame = LabelFrame(root, text="Com Manager",
                                padx=20, pady=20, bg="white", bd = 7)
        self.label_com = Label(
            self.frame, text="Available Port(s): ", bg="white", width=15, height = 3, anchor="w")
        self.label_bd = Label(
            self.frame, text="Baude Rate: ", bg="white", width=15, anchor="w")
        
        # Setup the Drop option menu
        self.baudOptionMenu()
        self.ComOptionMenu()
        
        # Add the control buttons for refreshing the COMs & Connect
        self.btn_refresh = Button(self.frame, text="Refresh",
                                  width=10,  command=self.com_refresh)
        self.btn_connect = Button(self.frame, text="Connect",
                                  width=10, state="disabled",  command=self.serial_connect)

        self.btn_saveData = Button(root, text="Save Data", font=('calibri', 16), width=10, state='active', command=self.readData_to_file) 
        self.file_name1 = Text(root, height=2, width=20)
        
        self.show_data = Button(root, text="Show Data", font=('calibri', 16), width=10, state='active', command=self.show_data)
        self.file_name2 = Text(root, height=2, width=20)
        
        self.btn_clear = Button(root, text= "Erase Graph", font=('calibri', 16), width=10, state='active', command=self.clear_plot)
        
        self.btn_start = Button(root, text="Start Reading", font=('calibri', 16), width=10, state='disabled', command=self.start_stream)
        self.btn_stop = Button(root, text="Stop Reading", font=('calibri', 16), width=10, state='disabled', command=self.stop_stream)
        
        self.btn_startOnline = Button(root, text="Start Online Plot", font=('calibri', 16), width=10, state='disabled', command=self.start_online_plot)
        self.btn_stopOnline = Button(root, text= "Stop Online Plot",  font=('calibri', 16), width=10, state='disabled', command=self.stop_online_plot)
        
        #self.label_heartBeat = Label(root, text = "-", padx = 5, pady = 5, bg = "white")
        
        # self.fig=Figure();
        # self.ax= self.fig.add_subplot(111)
        
        # self.ax.set_title('ECG')
        # self.ax.set_xlabel('')
        # self.ax.set_ylabel('Voltage')
        # self.ax.set_xlim(0, 250)
        # self.ax.set_ylim(-3,3)
        # self.lines = self.ax.plot([],[])[0]
        
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

        self.cond = False
        self.signal = np.array([])
        self.data = []

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 5

        # Put on the grid all the elements
        self.publish()
        
    def publish(self):
        
        self.frame.grid(row=0, column=0, rowspan=3, columnspan=3, padx=5, pady=5)
        self.label_com.grid(column=1, row=2)
        self.label_bd.grid(column=1, row=3)

        self.drop_baud.grid(column=2, row=3, padx=self.padx, pady=self.pady)
        self.drop_com.grid(column=2, row=2, padx=self.padx)

        self.btn_refresh.grid(column=3, row=2, padx=self.padx, pady=self.pady)
        self.btn_connect.grid(column=3, row=3, padx=self.padx, pady=self.pady)
        
        self.btn_saveData.grid(column = 5, row = 0, padx=self.padx, pady=self.pady)
        self.file_name1.grid(column = 6, row=0, padx=self.padx, pady=self.pady)
        
        self.show_data.grid(column = 5, row = 1, padx=self.padx, pady=self.pady)
        self.file_name2.grid(column = 6, row=1, padx=self.padx, pady=self.pady)
        
        self.btn_clear.grid(column = 4, row = 2, padx=self.padx, pady=self.pady)
        
        self.btn_start.grid(column = 4, row = 0, padx=self.padx, pady=self.pady)
        self.btn_stop.grid(column = 4, row = 1, padx=self.padx, pady=self.pady)
        
        self.btn_startOnline.grid(column = 7, row= 0, padx=self.padx, pady=self.pady)
        self.btn_stopOnline.grid(column = 7, row= 1, padx=self.padx, pady=self.pady)
        
        # self.canvas.get_tk_widget().grid(column = 0, row = 3, padx=5, pady=self.pady)
        # self.canvas.draw()       

        # self.frame2.grid(row=0, column=6)

        # self.label_heartBeat.grid(row = 0, column = 0)
    

    def getCOMList(self):
        '''
        Method that get the lost of available coms in the system
        '''
        ports = serial.tools.list_ports.comports()
        self.com_list = [com[0] for com in ports]
        self.com_list.insert(0, "-")
        
        return self.com_list
    
    def ComOptionMenu(self):
        '''
         Method to Get the available COMs connected to the PC
         and list them into the drop menu
        '''
        # Generate the list of available coms

        self.getCOMList()

        self.clicked_com = StringVar()
        self.clicked_com.set(self.com_list[0])
        self.drop_com = OptionMenu(
            self.frame, self.clicked_com, *self.com_list, command=self.connect_ctrl)

        self.drop_com.config(width=15)

    def baudOptionMenu(self):
        '''
         Method to list all the baud rates in a drop menu
        '''
        self.clicked_bd = StringVar()
        bds = ["-",
               "300",
               "600",
               "1200",
               "2400",
               "4800",
               "9600",
               "14400",
               "19200",
               "28800",
               "38400",
               "56000",
               "57600",
               "115200",
               "128000",
               "256000"]
        self.clicked_bd .set(bds[0])
        self.drop_baud = OptionMenu(
            self.frame, self.clicked_bd, *bds, command=self.connect_ctrl)
        self.drop_baud.config(width=15)

    def connect_ctrl(self, widget):
        '''
        Mehtod to keep the connect button disabled if all the
        conditions are not cleared
        '''
        print("Connect ctrl")
        # Checking the logic consistency to keep the connection btn
        if (self.clicked_bd.get() == "-") or (self.clicked_com.get() == "-"):
            self.btn_connect["state"] = "disabled"
        else:
            self.btn_connect["state"] = "active"

    def com_refresh(self):
        '''
        Method to refresh the COM and Baud Rate selected
        '''
        
        #
        print("Refresh")
        # Get the Widget destroyed
        self.drop_com.destroy()

        # Refresh the list of available Coms
        self.ComOptionMenu()

        # Publish the this new droplet
        self.drop_com.grid(column=2, row=2, padx=self.padx)

        # Just in case to secure the connect logic
        logic = []
        self.connect_ctrl(logic)
    
    def serial_connect(self):
        '''
        Method that Updates the GUI during connect / disconnect status
        Manage serials and data flows during connect / disconnect status
        '''
        if self.btn_connect["text"] in "Connect":
            # Start the serial communication
            try:
                self.ser.is_open
            except:
                PORT = self.clicked_com.get()
                BAUD = self.clicked_bd.get()
                self.ser = serial.Serial()
                self.ser.baudrate = BAUD
                self.ser.port = PORT
                self.ser.timeout = 0.1
    
            try:
                if self.ser.is_open:
                    print("Already Open")
                    self.ser.status = True
                else:
                    PORT = self.clicked_com.get()
                    BAUD = self.clicked_bd.get()
                    self.ser = serial.Serial()
                    self.ser.baudrate = BAUD
                    self.ser.port = PORT
                    self.ser.timeout = 0.01
                    self.ser.open()
                    self.ser.status = True
            except:
                self.ser.status = False

            # If connection established move on
            if self.ser.status:
                # Update the COM manager
                self.btn_connect["text"] = "Disconnect"
                self.btn_refresh["state"] = "disable"
                self.drop_baud["state"] = "disable"
                self.drop_com["state"] = "disable"
                InfoMsg = f"Successful UART connection using {self.clicked_com.get()}"
                messagebox.showinfo("showinfo", InfoMsg)
                
                self.btn_start['state'] = 'active' 
                self.btn_startOnline['state'] = 'active'

            else:
                ErrorMsg = f"Failure to estabish UART connection using {self.clicked_com.get()} "
                messagebox.showerror("showerror", ErrorMsg)
        else:

            # Closing the Serial COM
            # Close the serial communication
            #self.SerialClose(self)
            if(self.btn_stop["state"] == 'active'):
                self.stop_stream()
            
            if(self.btn_stopOnline["state"] == 'active'):
                self.stop_online_plot()
            

            InfoMsg = f"UART connection using {self.clicked_com.get()} is now closed"
            messagebox.showwarning("showinfo", InfoMsg)
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_baud["state"] = "active"
            self.drop_com["state"] = "active"
            self.btn_start['state'] = 'disabled'
            self.btn_stop['state'] = 'disabled'  
            self.btn_startOnline['state'] = 'disabled'  
            self.btn_stopOnline['state'] = 'disabled'  
            
    def clear_plot(self):
        '''
        Method to clear up the plot axes X & Y
        '''

        self.lines.set_xdata(np.array([]))
        self.lines.set_ydata(np.array([]))
        self.canvas.draw() 
        
        #self.ax.cla()

    
    def filter_data(self, data):
        '''
        Method to filter up the data array with digital filters:
            1. Notch Filter
            2. High Pass Filter
            3. Low Pass Filter

        Parameters
        ----------
        data : array that contains all data to be filter.

        Returns
        -------
        signal_filtered3 : array that contains the filtered data.

        '''
        
        signal_filtered1 = filt.low_passFilter_func(data)

        # plt.subplot(5,1,2)
        # #Serial Plotter
        # plt.plot(signal_filtered1)
        # plt.xlabel('Time (seconds)')
        # plt.ylabel('Voltage')
        # plt.title('Filtro Passa Baixo (100Hz)')
        # #plt.show()

        signal_filtered2 = filt.high_passFilter_func(signal_filtered1)

        # plt.subplot(5,1,3)
        # #Serial Plotter
        # plt.plot(signal_filtered2)
        # plt.xlabel('Time (seconds)')
        # plt.ylabel('Voltage')
        # plt.title('Filtro Passa Alto (0.05Hz)')
        # #plt.show()

        signal_filtered3 = filt.notchFilter_func(signal_filtered2)

        # plt.subplot(5,1,5)
        # #Serial Plotter
        # plt.plot(signal_filtered3)
        # plt.xlabel('Time (seconds)')
        # plt.ylabel('Voltage')
        # plt.title('Filtro Notch')
        # plt.show()
        
        return signal_filtered3 
    
    def readData_to_file(self):
        '''
        Method to read data from serial communications
        and save it on a file

        '''
        
        signal = []
        
        file_name = self.file_name1.get("1.0", "end-1c")
        file = str.format(file_name)
        
        # for i in range(500):
        #     print("Não vai ler os primeiros 50 valores para assegurar que esta a ler valores válidos")

        
        print("Ciclo de leitura vai começar")
        
        #for i in range(10000):
        for i in range(1000):
            
            try:
                b = self.ser.readline().decode() # read a byte string  && #decode byte string into Unicode 
                
                string = b.rstrip() # remove \n and \r
                flt = float(string) # convert string to float
                signal.append(flt)  # add to the end of data list

            except:
                print("falhou")
                pass
        
        print("End of the reading cicle")
        
        #show the data - Serial Monitor
            
        # #Serial Plotter
        # plt.plot(signal)
        # plt.xlabel('Time (seconds)')
        # plt.ylabel('Voltage')
        # plt.title('Voltage vs. Time')
        # plt.show()
        
        np.savetxt(file, signal)


    def readData_from_file(self):
        '''
        Method to read data from a given file and save it on a array

        Returns
        -------
        ecg_singal - array that contains all the information read from the file.

        '''
        
        file_name = self.file_name2.get("1.0", "end-1c")
        file = str.format(file_name)
        
        column_names = [
            'ecg']

        #ecg_signal = pd.read_csv('ecg_data1.csv', names=column_names)
        ecg_signal = pd.read_csv(file, names=column_names)
        
        return ecg_signal.ecg
        
    def show_data(self):
        '''
        Method to plot the content returned by the function 
        readData_from_file, filter the data and calculate the heart beat
        '''
        
        ecg_signal = self.readData_from_file()
        
        plt.subplot(5, 1, 1)
        plt.plot(ecg_signal, '-g')
        plt.xlabel('Amplitude')
        plt.grid()
        plt.title("ECG SIGNAL")

        filtered_signal = self.filter_data(ecg_signal)
        
        # figure = plt.figure(figsize = (8,4), dpi=100)
        # figure.add_subplot(111).plot(filtered_signal[0:1000])
        # chart = FigureCanvasTkAgg(figure, self.root)
        # chart.get_tk_widget().grid(column = 5, row = 5, padx=20, pady=5)
        
        # plt.title("ECG Signal")
        # plt.xlabel("Time [ms]")
        # plt.ylabel("Voltage [V]")
        # plt.tight_layout()
        # plt.grid()

        
        self.fig=Figure(figsize = (8,4), dpi=100);
        self.ax= self.fig.add_subplot(111)
        
        self.ax.set_title('ECG')
        self.ax.set_xlabel('')
        self.ax.set_ylabel('Voltage')
        self.ax.set_xlim(0,1000)
        self.ax.set_ylim(-0.5,0.5)
        self.lines = self.ax.plot([],[])[0]
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(column = 0, row = 4, padx=self.padx, pady=self.pady)
        
        self.lines.set_xdata(np.arange(0,len(filtered_signal[0:1000])))
        self.lines.set_ydata(filtered_signal[0:1000])
    
        self.canvas.draw()
        
        ECG_Functions(self.root).heart_Beat(filtered_signal)
        
        
    def plot_data(self):
        '''
        Method to plot data in real time
        '''
        
        #global cond, data, a, i
        global cond, a
        
        print("PLOT DATA FUNCTION ")
        
        if (cond == True):
            
            print("TRUE")
            
            try:
                a = self.ser.readline().decode()
                a = a.rstrip() # remove \n and \r
                a = float(a) # convert string to float
                self.data.append(a)
                print(a)
            except:
                pass

            self.data = self.data[-500:]
            self.lines.set_xdata(np.arange(0,len(self.data)))
            self.lines.set_ydata(self.data)
        
            self.canvas.draw()
        
        #guardamos o ID para quando quisermos parar esta funcao
        self.cycleID = self.root.after(1,self.plot_data)


    def start_stream(self):
        '''
        Method related to the button self.btn_start. 
        Start the functions plot_data

        Returns
        -------
        None.

        '''
        
        global cond
            
        self.btn_start['state'] = 'disabled'
        self.btn_stop['state'] = 'active'
        
        InfoMsg = f"Ready to receive data"
        messagebox.showwarning("showinfo", InfoMsg)

        #funcoes do ECG
        
        #self.cond = True
        cond = True
        self.btn_stop["state"] = "active"
        
        self.fig=Figure(figsize = (8,4), dpi=100);
        self.ax= self.fig.add_subplot(111)
        
        self.ax.set_title('ECG')
        self.ax.set_xlabel('')
        self.ax.set_ylabel('Voltage')
        self.ax.set_xlim(0,500)
        self.ax.set_ylim(-4,4)
        self.lines = self.ax.plot([],[])[0]
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(column = 0, row = 4, padx=self.padx, pady=self.pady)
        self.canvas.draw() 
        
        self.plot_data()
        
        print("Start Stream")
        
            
    def stop_stream(self):
        '''
        Method related to the Button self.btn_stop
        It stops the function plot_data
        '''
        
        global cond
            
        self.root.after_cancel(self.cycleID)
        #self.cond = False 
        cond = False

        self.btn_start["state"] = "active"

        print("Stream Stopped")
        
    def online_plot(self):
        '''
        Method to plot real time data on internet
        '''
        
        global cond2, counter
        
        print("Online Plot")
            
        if (cond2 == True):
            
            try:
                b = self.ser.readline().decode()
                print(b)
                
                try:
                    b = float(b)
                    print(b)
                    
                    try:
                        self.aio.send_data(self.test.key, b)
                        #aio.send_data(test.key, ecg_signal.ecg[counter])
                    except:
                        print("FALHOU3")
                        pass
                except:
                    print("FALHOU2")
                    pass
            except:
                print("FALHOU1")
                pass
            
        time.sleep(2)    
        
        self.cycleID2 = self.root.after(1, self.online_plot)
        
        
    def start_online_plot(self):
        '''
        Method realted to the Button self.btn_startOnline
        It starts the function online_plot

        '''
        
        global cond2
        
        print("Start Online Plot")
        
        self.aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
        print(self.aio)
        
        # column_names = [
        #     'ecg']

        # ecg_signal = pd.read_csv('ecg_data1.csv', names=column_names)

        # ecg_signal.ecg = filt.low_passFilter_func(ecg_signal.ecg)
        
        try:
            self.test = self.aio.feeds("ems")
        except RequestError: #Doesn't exist, create a new feed:
            # self.test_feed = Feed(name="ems")
            # self.test_feed = self.aio.create_feed(self.test_feed)
            self.test = Feed(name="ems")
            self.test = self.aio.create_feed(self.test)
            
        cond2 = True
        
        self.btn_startOnline['state'] = 'disabled'
        self.btn_stopOnline['state'] = 'active'
        
        self.online_plot()
        
    
    def stop_online_plot(self):
        '''
        Method related to the Button self.btn_stop_online
        And it's used to stop the online plot
        '''
        
        global cond2
        
        print("Stop Online Plot")

        cond2 = False   
        
        self.btn_startOnline['state'] = 'active'
        self.btn_stopOnline['state'] = 'disabled'
        
        self.root.after_cancel(self.cycleID2)

####################################################
####################################################
# Class ECG_Functions - it implements all functions
#                imported from the file ECG_Functions
####################################################
####################################################
class ECG_Functions():
    def __init__(self, root):
        
        self.root = root

        self.frame2 = LabelFrame(root, text = "Heart Beat: ", padx=5, pady=5, bg="white", bd=5)
        self.label_heartBeat = Label(self.frame2, text = " - ", bg = "white", width= 5, height = 1, anchor='c')
        
        # Optional Graphic parameters
        self.padx = 5
        self.pady = 5

        # Put on the grid all the elements
        self.publish()
        
    def publish(self):

        self.frame2.grid(column=0, row=10, rowspan=1, columnspan=1, padx=5, pady=5)

        self.label_heartBeat.grid(column = 0,row = 0)
            
            
    def heart_Beat(self, ecg_signal):
        '''
        Method to calculate the heart beat of ECG Signal

        Parameters
        ----------
        ecg_signal : array that contains all the data collected from the ECG Signal

        Returns
        -------
        None.

        '''
        
        frequency = 250
        #frequency = 1000

        #numpy.arange - Return evenly spaced values within a given interval
        # calculating time data with ecg size along with frequency
        time_data1 = np.arange(ecg_signal.size) 
        time_data = time_data1 / frequency

        #calculates from the ECG data the derivative and then it looks for the peaks in the derivative
        d_ecg, peaks_d_ecg = funcECG.decg_peaks(ecg_signal, time_data)
        #it uses the threshold - the last two values need to be between 0 and 1 - alterar para ver as diferencças nos picos filtrados e nao filtrados
        Rwave_peaks_d_ecg = funcECG.d_ecg_peaks(d_ecg, peaks_d_ecg, time_data, 0.7, 0.5)
        # #gives the real time of each peak of the ECG. With this time we can calculate the heart rate
        exercise_Rwave_t = funcECG.Rwave_peaks(ecg_signal, d_ecg, Rwave_peaks_d_ecg, time_data)

        # ####################
        # #   Heart Rate     #
        # ####################
        print("Heart Rate Calcule")
        RR_interval = np.diff(exercise_Rwave_t)

        #converts Hz to bpm
        heart_rate = (1/RR_interval)*60


        media_heartBeat = np.mean(heart_rate)
        print("Heart Rate: ", media_heartBeat)
        
        media_heartBeat = round(media_heartBeat, 2) 
        
        self.label_heartBeat.config(text = media_heartBeat)

if __name__ == "__main__":
   RootGUI_ECG()
   ComGUI()
   ECG_Functions()

