Overview:

This project focuses on digitizing and visualizing ECG (Electrocardiogram) signals, providing a user-friendly interface to monitor heart activity in real-time. The system processes analog ECG signals, applies digital filters to remove noise and unwanted components, and displays the cleaned signal on a GUI (Graphical User Interface). Wireless communication is implemented to transmit the processed data to a cloud platform, Adafruit IO, for remote access and storage.

Key Features:

- Signal Filtering: Digital filters remove noise and ensure the ECG signal is clean and ready for visualization.
- GUI Interaction: An intuitive interface allows users to interact with the system, visualize ECG signals, and monitor heart activity in real-time.
- Wireless Communication: The processed ECG data is transmitted from the Python program to Adafruit IO, enabling cloud-based storage and visualization.
- ESP32 Integration: The ESP32 microcontroller handles analog-to-digital conversion by sampling the ECG signal and sending it to the Python code for further processing.

Analog Context:

The analog ECG signal is captured through a Front-End Analog circuit and digitized using the ESP32 microcontroller. The digitized data is then sent to the Python application, where it is processed, visualized, and transmitted to Adafruit IO for remote access.

Technology Stack:

- Programming Language: C++, Python
- Microcontroller: ESP32 for ECG signal digitization
- Cloud Platform: Adafruit IO for wireless communication and data storage
- Libraries/Tools:
    - NumPy, SciPy (sps), Pandas, Matplotlib, Matplotlib Animation, Tkinter, matplotlib.backends.backend_tkagg, Serial (PySerial), serial.tools.list_ports, Adafruit_IO, Threading, Time.
    - Costume Libraries (Project-Specific): ECG_Functions, EMS_FiltrosDigitais, Interface.

Usage Instructions:

1. Connect the ESP32 to the Front-End analog circuit to receiver and sample the data.
2. Run the Python software to receive, filter, and visualize the ECG data on the GUI.
3. Configure the Adafruit IO account and credentials in the Python script to enable wireless communication.
4. Access the ECG data remotely via the Adafruit IO dashboard.

Example Screenshot of the GUI (using a sinusoide):

![Picture 1](https://github.com/user-attachments/assets/211ca06e-112f-4557-b8c0-d4c9c0977b61)

