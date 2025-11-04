# SPDX-FileCopyrightText: 2025 Daniel Maier, Daniel Mohr, Thomas Villatte
#
# SPDX-License-Identifier: GPL-3.0-or-later
# rev 2025-03

import socket
import time
from datetime import datetime
from pathlib import Path
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread, Event

# Global variables
data_receiving_thread = None
label_directory = None
button_browse = None
label_port = None
entry_port = None
text_box = None
button_start = None
button_stop = None
label_instruction = None
DEFAULT_PORT = "3131"
stop_event = Event()  # Event to properly stop data collection
csv_file_path = ""
CSV_FIELDNAMES: str = ['Miliseconds since 00:00:00 (ms)', 'Time', 'Jx (g)', 'Jy (g)', 'Jz (g)', \
                       'Temperature (°C)', 'Humidity (%)','Pressure (mbar)', \
                       'Parabola','Announcement']

# Graphical User Interface
def browse_directory():
    """Opens a dialog box to choose the directory to store the CSV file."""
    global csv_file_path
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        csv_file_path = folder_selected
        label_directory.config(text=f"Selected folder : {csv_file_path}")

def start_receiving():
    """Starts receiving UDP data in a separate thread."""
    global data_receiving_thread, stop_event
    if not csv_file_path:
        messagebox.showerror("Error", "Please select a folder to store the csv file.")
        return
    
    # Get the port from the input field
    try:
        port = int(entry_port.get())  # Get the port number from the entry field
    except ValueError:
        messagebox.showerror("Error", "Invalid port number. Please enter a valid port number.")
        return    

    stop_event.clear()  # Reset the event to allow data collection
    data_receiving_thread = Thread(target=receive_data, args=(port,))  # Pass port to the function
    data_receiving_thread.start()
    
    button_start.config(state=tk.DISABLED)  # Disable the "Start" button
    button_stop.config(state=tk.NORMAL)    # Enable the "Stop" button

def stop_receiving():
    """Stops receiving UDP data."""
    global stop_event
    stop_event.set()  # Signal the thread to stop collecting data
    button_stop.config(state=tk.DISABLED)  # Disable the "Stop" button
    button_start.config(state=tk.NORMAL)   # Enable the "Start" button again

def receive_data(port):
    """Function to receive data and display it in the graphical interface."""
    global udp_socket
    try:
        # Create the UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_address = ('', port)  # Use the user-provided port
        udp_socket.bind(local_address)

        # Create the CSV file
        CSV_file = Path(csv_file_path, f'Flight_data_{datetime.now().strftime("%Y%m%d-%Hh%Mm%Ss")}.csv')
        CSV_file.touch()

        with open(CSV_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES, delimiter=';')
            writer.writeheader()

        while not stop_event.is_set():  # Check if the stop event has been signaled
            data, address = udp_socket.recvfrom(1024)
            data_str = data.decode('utf-8')

            # Save the data into the CSV file
            with open(CSV_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([data_str])

            # Update the interface with the received data
                text_box.insert(tk.END, f"Data received: {data_str}\n")
                text_box.yview(tk.END)  # Scroll vers la fin de la fenêtre

    except Exception as e:
        print(f"Error in receiving data: {e}")

    finally:
        udp_socket.close()

# Main function to set up the GUI
def main():
    global label_directory, button_browse, label_port, entry_port, text_box, button_start, button_stop, label_instruction
    # Graphical Interface Configuration
    root = tk.Tk()
    root.title("UDP Data Receiver")

    # Configuration to allow the window to expand
    root.grid_rowconfigure(0, weight=0)  # Leave the first row for labels
    root.grid_rowconfigure(1, weight=0)  # Leave the second row for buttons
    root.grid_rowconfigure(2, weight=0)  # Leave the second row for buttons
    root.grid_rowconfigure(3, weight=1)  # The third row expands for the Text Box
    root.grid_columnconfigure(0, weight=1)  # The column expands for the Text Box

    # Folder selection
    label_directory = tk.Label(root, text="Folder not selected")
    label_directory.grid(row=2, column=0, pady=10, padx=10, sticky="w")

    button_browse = tk.Button(root, text="Select a folder", command=browse_directory)
    button_browse.grid(row=1, column=0, pady=5, padx=10, sticky="w")

    # Port input
    label_port = tk.Label(root, text="Enter UDP Port:")
    label_port.grid(row=1, column=0, pady=5, padx=10, sticky="e")

    entry_port = tk.Entry(root)
    entry_port.grid(row=1, column=1, pady=5, padx=10, sticky="w")
    entry_port.insert(0, DEFAULT_PORT)  # Default port value

    # Data display area (text area that adapts to window size)
    text_box = tk.Text(root, height=15, width=80)
    text_box.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

    # Start and Stop buttons
    button_start = tk.Button(root, text="Start data collection", command=start_receiving)
    button_start.grid(row=1, column=2, pady=5, padx=50)

    button_stop = tk.Button(root, text="Stop data collection", command=stop_receiving, state=tk.DISABLED)
    button_stop.grid(row=2, column=2, pady=5, padx=50)

    # Instructions
    label_instruction = tk.Label(root, text="This program collects data from UDP port 3131 and stores it in a csv file")
    label_instruction.grid(row=0, column=0, pady=5, padx=10)

    # Start the graphical interface
    root.mainloop()

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
