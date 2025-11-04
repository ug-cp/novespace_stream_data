# SPDX-FileCopyrightText: 2025 Daniel Maier, Daniel Mohr, Thomas Villatte
#
# SPDX-License-Identifier: GPL-3.0-or-later
# rev 2025-02

"""
This program emulates the UDP broadcast of the Data-unit,
sending data from a csv file (row by row) to a UDP port on a
specific IP address, every 0.1s
"""

import csv
import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variable to control the stop flag
stop_flag = False  # pylint: disable = C0103
entry_file = None  # pylint: disable = C0103
entry_ip = None  # pylint: disable = C0103
entry_port = None  # pylint: disable = C0103
text_output = None  # pylint: disable = C0103
DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = "3131"


# Function to browse and select a CSV file
def browse_file():  # pylint: disable = C0116
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry_file.delete(0, tk.END)  # Clear previous file path
        entry_file.insert(0, file_path)  # Insert the selected file path


# Function to start the UDP data transmission
def start_sending():  # pylint: disable = C0116
    global stop_flag  # pylint: disable = C0103, W0603
    file_path = entry_file.get()  # Get the file path from the entry widget
    ip_address = entry_ip.get()  # Get the IP address from the entry widget
    port = int(entry_port.get())  # Get the port number from the entry widget

    if not file_path or not ip_address or not port:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    stop_flag = False  # Reset stop flag when starting new transmission

    # Start the UDP transmission in a separate thread to avoid blocking the GUI
    thread = threading.Thread(target=send_udp_data,
                              args=(file_path, ip_address, port))
    # Daemonize the thread to automatically close on program exit:
    thread.daemon = True
    thread.start()


# Function to send data line by line from CSV over UDP
def send_udp_data(file_path, ip_address, port):  # pylint: disable = C0116
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Open the CSV file
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)

            # Read each line and send it over UDP
            for row in csvreader:
                if stop_flag:  # Check if we need to stop sending
                    print("Transmission stopped")
                    break

                # Join the columns into a single string
                message = ",".join(row)
                sock.sendto(message.encode(), (ip_address, port))  # Send data

                # Display the sent message in the Text widget
                text_output.insert(tk.END, f"Sent: {message}\n")
                text_output.yview(tk.END)  # Auto-scroll to the latest entry

                # Wait for a short time before sending the next line
                # Adjust this to control the rate of data transmission
                time.sleep(0.1)

        # Close the socket after sending all data
        sock.close()

        if not stop_flag:  # Check if the transmission wasn't stopped manually
            messagebox.showinfo("Success", "Data sent successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to stop the data transmission
def stop_sending():  # pylint: disable = C0116
    global stop_flag  # pylint: disable = C0103, W0603
    stop_flag = True  # Set the stop flag to True to stop the transmission


# Main function to set up the GUI
def main():  # pylint: disable = C0116
    # Create the main window
    root = tk.Tk()
    root.title("UDP CSV Data Sender")

    # Make the window resizable
    root.resizable(True, True)  # Allow resizing in both directions

    # Configure the layout
    tk.Label(
        root,
        text="This program emulates the UDP broadcast of the Data-unit, "
        "sending data from a csv file (row by row) to a UDP port on a "
        "specific IP address, every 0.1s").grid(
            row=0, column=1, padx=10, pady=10)
    tk.Label(root, text="CSV File:").grid(
        row=1, column=0, padx=10, pady=10, sticky="e")
    tk.Label(root, text="IP Address:").grid(
        row=2, column=0, padx=10, pady=10, sticky="e")
    tk.Label(root, text="Port:").grid(
        row=3, column=0, padx=10, pady=10, sticky="e")

    # Entry widgets with default values for IP Address and Port
    global entry_file, entry_ip, entry_port  # pylint: disable = C0103, W0603
    entry_file = tk.Entry(root, width=40)
    entry_file.grid(row=1, column=1, padx=10, pady=10,
                    sticky="ew")  # Stretch horizontally

    # Set default IP Address to '127.0.0.1'
    entry_ip = tk.Entry(root, width=40)
    entry_ip.insert(0, DEFAULT_IP)  # Set default IP
    entry_ip.grid(row=2, column=1, padx=10, pady=10,
                  sticky="ew")  # Stretch horizontally

    # Set default Port to '3131'
    entry_port = tk.Entry(root, width=40)
    entry_port.insert(0, DEFAULT_PORT)  # Set default Port
    entry_port.grid(row=3, column=1, padx=10, pady=10,
                    sticky="ew")  # Stretch horizontally

    # Browse button to select a CSV file
    browse_button = tk.Button(root, text="Browse", command=browse_file)
    browse_button.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    # Start button to begin sending data
    start_button = tk.Button(root, text="Start Sending", command=start_sending)
    start_button.grid(row=4, column=0, padx=10, pady=20, sticky="e")

    # Stop button to stop sending data
    stop_button = tk.Button(root, text="Stop Sending", command=stop_sending)
    stop_button.grid(row=4, column=1, padx=10, pady=20, sticky="w")

    # Create a Text widget for showing the sent messages
    global text_output  # pylint: disable = C0103, W0603
    text_output = tk.Text(root, height=10, wrap=tk.WORD)
    text_output.grid(row=5, column=0, columnspan=3, padx=10,
                     pady=10, sticky="nsew")  # Stretch in all directions

    # Make the grid rows/columns expand with window resizing
    root.grid_rowconfigure(5, weight=1)  # Make row 4 (Text widget) expand
    # Make column 0 (Text widget) expand
    root.grid_columnconfigure(0, weight=1)
    # Make column 1 expand (entry widgets and buttons)
    root.grid_columnconfigure(1, weight=1)

    # Run the GUI
    root.mainloop()


# Run the main function if the script is executed
if __name__ == "__main__":
    main()
