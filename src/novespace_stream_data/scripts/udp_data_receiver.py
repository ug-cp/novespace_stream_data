# SPDX-FileCopyrightText: 2025 Daniel Maier, Daniel Mohr, Thomas Villatte
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
This program gets the UDP broadcast stream, logs and display it.
"""

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox


from novespace_stream_data.receive import NoSpaStream


class GUINoSpaStream(NoSpaStream):
    """
    This class allows to get the stream from
    Novespace ( https://www.airzerog.com/ ),
    which is provided in scrientific research flights.

    This stream data was first provided during
    45. DLR parabolic flight campaign in October 2025.
    """
    # pylint: disable = R0902

    def __init__(self, csv_path, inputport=3131, printing=False):
        """
        :param csv_path: path to store the data
        :param inputport: port to listen.
        :param printing: If set to True the data is not only logged, but also
                         printed on the console (stdout).
        """
        super().__init__(csv_path, inputport, printing)
        self.display_data_callback = self.display_data
        self.label_directory = None
        self.button_browse = None
        self.label_port = None
        self.entry_port = None
        self.text_box = None
        self.button_start = None
        self.button_stop = None
        self.label_instruction = None
        self.do_exit = False

    def __call__(self):
        """
        Graphical Interface Configuration
        """
        root = tk.Tk()
        root.title("UDP Data Receiver")

        # Configuration to allow the window to expand
        root.grid_rowconfigure(0, weight=0)  # Leave the first row for labels
        root.grid_rowconfigure(1, weight=0)  # Leave the second row for buttons
        root.grid_rowconfigure(2, weight=0)  # Leave the second row for buttons
        # The third row expands for Text Box
        root.grid_rowconfigure(3, weight=1)
        # The column expands for Text Box
        root.grid_columnconfigure(0, weight=1)

        # Folder selection
        self.label_directory = tk.Label(root, text="Folder not selected")
        self.label_directory.grid(
            row=2, column=0, pady=10, padx=10, sticky="w")

        self.button_browse = tk.Button(
            root, text="Select a folder", command=self.browse_directory)
        self.button_browse.grid(row=1, column=0, pady=5, padx=10, sticky="w")

        # Port input
        self.label_port = tk.Label(root, text="Enter UDP Port:")
        self.label_port.grid(row=1, column=0, pady=5, padx=10, sticky="e")

        self.entry_port = tk.Entry(root)
        self.entry_port.grid(row=1, column=1, pady=5, padx=10, sticky="w")
        self.entry_port.insert(0, self.streamport)  # Default port value

        # Data display area (text area that adapts to window size)
        self.text_box = tk.Text(root, height=15, width=80)
        self.text_box.grid(
            row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # Start and Stop buttons
        self.button_start = tk.Button(
            root, text="Start data collection", command=self.start_receiving)
        self.button_start.grid(row=1, column=2, pady=5, padx=50)

        self.button_stop = tk.Button(
            root, text="Stop data collection", command=self.stop_receiving,
            state=tk.DISABLED)
        self.button_stop.grid(row=2, column=2, pady=5, padx=50)

        # Instructions
        self.label_instruction = tk.Label(
            root,
            text="This program collects data from UDP port 3131 and "
            "stores it in a csv file")
        self.label_instruction.grid(row=0, column=0, pady=5, padx=10)

        # Start the graphical interface
        root.mainloop()

    def browse_directory(self):
        """
        Opens a dialog box to choose the directory to store the CSV file.
        """
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.streampath = folder_selected
            self.label_directory.config(
                text=f"Selected folder : {self.streampath}")

    def start_receiving(self):
        """
        Starts receiving UDP data in a separate thread.
        """
        if not self.streampath:
            messagebox.showerror(
                "Error", "Please select a folder to store the csv file.")
            return

        # Get the port from the input field
        try:
            # Get the port number from the entry field
            self.streamport = int(self.entry_port.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Invalid port number. Please enter a valid port number.")
            return

        self.csv_file = Path(
            self.streampath,
            f'Flight_data_{datetime.now().strftime("%Y%m%d-%Hh%Mm%Ss")}.csv')
        self.csv_file.touch()
        self.start_streaming(create_csv_file=False)
        # Disable the "Start" button
        self.button_start.config(state=tk.DISABLED)
        self.button_stop.config(state=tk.NORMAL)    # Enable the "Stop" button

    def stop_receiving(self):
        """
        Stops receiving UDP data.
        """
        self.end_streaming()
        self.button_stop.config(state=tk.DISABLED)  # Disable the "Stop" button
        # Enable the "Start" button again
        self.button_start.config(state=tk.NORMAL)

    def display_data(self, data_str):
        """
        display data in GUI
        """
        # Update the interface with the received data
        self.text_box.insert(tk.END, f"Data received: {data_str}\n")
        self.text_box.yview(tk.END)  # Scroll vers la fin de la fenêtre


def main():
    """
    This function provides a GUI to get the streaming of airplanedata and
    writes them into a csv-file.
    """
    datastreamgui = GUINoSpaStream(None, 3131)
    datastreamgui()


# Run the main function if the script is executed
if __name__ == "__main__":
    main()
