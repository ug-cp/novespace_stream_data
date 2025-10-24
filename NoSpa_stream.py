#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 08:47:40 2025

@author: daniel_m
"""

#necessary imports
import socket
from datetime import datetime
from pathlib import Path
import csv
from threading import Thread
import os
import sys

#class definition

class NoSpaStream():
    def __init__(self,csv_path,inputport="3131",printing=False):
        self.streampath=csv_path
        self.streamport=inputport
        self.print_on_console=printing
        self.socket_adress=('', self.streamport)
        self.streaming_status=False
        self.CSV_fieldnames= ['Miliseconds since 00:00:00 (ms)', 'Time', 'Jx (g)', 'Jy (g)', 'Jz (g)', \
                               'Temperature (°C)', 'Humidity (%)','Pressure (mbar)', \
                               'Parabola','Announcement']
        
        if not os.path.isdir(self.streampath):
            print("ERROR! No valid folder for csv-file is given.")
                        
    def connect_socket(self):
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(self.socket_adress)
            print(f"Creation of UDP-socket with port {self.streamport} sucessfull.")
        
            
            
    def get_status(self):
        if self.streaming_status==True:
           print(f"Active datastream from port {self.streamport} to {self.CSV_file}.")
        else:
           print("No active datastream!") 
                
             
    def start_streaming(self):
        if self.streaming_status==True:
            print("The stream is allready active!")
        else: 
           # try:    
            self.connect_socket()
            #except:
             #print("ERROR! Creation of UDP-socket failed. Check the portnumber.")
             #sys.exit()                
            self.CSV_file = Path(self.streampath, f'NoveSpa_planedata_{datetime.now().strftime("%Y%m%d-%Hh%Mm%Ss")}.csv')
            self.CSV_file.touch()
            with open(self.CSV_file, mode='a', newline='', encoding='utf-8') as file:
                self.CSV_writer = csv.DictWriter(file, fieldnames=self.CSV_fieldnames, delimiter=';')
                self.CSV_writer.writeheader() 
            print(f"Starting datastream from port {self.streamport} to file: {self.CSV_file}")
            print ("To end streaming use: CTRL+C\n")    
            self.streaming_status=True
            self.streaming_thread=Thread(target=self.stream_data(),daemon=True)
            self.streaming_thread.start()                
            
                    
    def end_streaming(self):
        if self.streaming_status==False:
            print("No active data-stream to be terminated.")
        else:
           try:
               self.socket.close()
               #self.CSV_file.close
               self.streaming_status=False
               print(f"\nEnd of streaming to {self.CSV_file}")
               print(datetime.now().strftime("Streaming ended on %Y-%m-%d at %H:%M:%S"))
           except:
               print("ERROR! Ending of Datastream was not sucessfull!")                
            
            
    def stream_data(self):       
        print("streaming data\n")
        try:
            while self.streaming_status==True:
                  
                    #Recive and decode datastream
                    self.data, self.address = self.socket.recvfrom(1024)
                    self.data_str = self.data.decode('utf-8')

                    # Save the data into the CSV file
                    with open(self.CSV_file, mode='a', newline='', encoding='utf-8') as file:
                        self.CSV_writer = csv.writer(file)
                        #self.CSV_writer.writerow(['1','2','3','4','5','6','7','8','9','10'])
                        self.CSV_writer.writerow([self.data_str])
                        if self.print_on_console==True:
                            print(self.data_str)
                
        except KeyboardInterrupt:
             #print(f"Error in receiving data: {e}")
             self.end_streaming()

                    
            
        
        