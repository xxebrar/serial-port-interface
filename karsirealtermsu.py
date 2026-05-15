import tkinter as tk
from tkinter import ttk, scrolledtext
import serial
import serial.tools.list_ports

class SerialApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Serial Port Interface")

        self.serial_conn = None

        self.port_var = tk.StringVar()
        self.baud_var = tk.StringVar(value="9600")
        self.parity_var = tk.StringVar(value="None")
        self.data_bits_var = tk.StringVar(value="8")
        self.stop_bits_var = tk.StringVar(value="1")

        self.create_widgets()
        self.update_ports()

    def create_widgets(self):

        port_label = ttk.Label(self, text="Port:")
        port_label.grid(column=0, row=0, padx=5, pady=5)
        self.port_combo = ttk.Combobox(self, textvariable=self.port_var)
        self.port_combo.grid(column=1, row=0, padx=5, pady=5)


        baud_label = ttk.Label(self, text="Baud Rate:")
        baud_label.grid(column=0, row=1, padx=5, pady=5)
        self.baud_combo = ttk.Combobox(self, textvariable=self.baud_var, values=["9600", "19200", "38400", "57600", "115200"])
        self.baud_combo.grid(column=1, row=1, padx=5, pady=5)


        parity_label = ttk.Label(self, text="Parity:")
        parity_label.grid(column=0, row=2, padx=5, pady=5)
        self.parity_combo = ttk.Combobox(self, textvariable=self.parity_var, values=["None", "Odd", "Even", "Mark", "Space"])
        self.parity_combo.grid(column=1, row=2, padx=5, pady=5)


        data_bits_label = ttk.Label(self, text="Data Bits:")
        data_bits_label.grid(column=0, row=3, padx=5, pady=5)
        self.data_bits_combo = ttk.Combobox(self, textvariable=self.data_bits_var, values=["5", "6", "7", "8"])
        self.data_bits_combo.grid(column=1, row=3, padx=5, pady=5)


        stop_bits_label = ttk.Label(self, text="Stop Bits:")
        stop_bits_label.grid(column=0, row=4, padx=5, pady=5)
        self.stop_bits_combo = ttk.Combobox(self, textvariable=self.stop_bits_var, values=["1", "1.5", "2"])
        self.stop_bits_combo.grid(column=1, row=4, padx=5, pady=5)


        connect_button = ttk.Button(self, text="Connect", command=self.connect_serial)
        connect_button.grid(column=0, row=5, columnspan=2, pady=10)


        self.status_label = ttk.Label(self, text="Status: Not Connected")
        self.status_label.grid(column=0, row=6, columnspan=2, pady=5)

        # Received data display
        receive_label = ttk.Label(self, text="Received Data:")
        receive_label.grid(column=0, row=7, padx=5, pady=5)
        self.receive_text = scrolledtext.ScrolledText(self, width=40, height=10, state='disabled')
        self.receive_text.grid(column=0, row=8, columnspan=2, padx=5, pady=5)

        # Send data entry
        send_label = ttk.Label(self, text="Send Data:")
        send_label.grid(column=0, row=9, padx=5, pady=5)
        self.send_entry = ttk.Entry(self, width=30)
        self.send_entry.grid(column=0, row=10, padx=5, pady=5)
        send_button = ttk.Button(self, text="Send", command=self.send_data)
        send_button.grid(column=1, row=10, padx=5, pady=5)

    def update_ports(self):
        ports = serial.tools.list_ports.comports()
        self.port_combo['values'] = [port.device for port in ports]

    def connect_serial(self):
        try:
            self.serial_conn = serial.Serial(
                port=self.port_var.get(),
                baudrate=int(self.baud_var.get()),
                parity=self.parity_var.get()[0],
                stopbits=int(self.stop_bits_var.get()),
                bytesize=int(self.data_bits_var.get())
            )
            self.status_label.config(text=f"Status: Connected to {self.port_var.get()}")
            self.after(100, self.read_serial)
        except Exception as e:
            self.status_label.config(text=f"Status: Connection Failed ({e})")

    def read_serial(self):
        if self.serial_conn and self.serial_conn.in_waiting:
            data = self.serial_conn.read(self.serial_conn.in_waiting).decode('utf-8')
            self.receive_text.configure(state='normal')
            self.receive_text.insert(tk.END, data)
            self.receive_text.configure(state='disabled')
        self.after(100, self.read_serial)

    def send_data(self):
        if self.serial_conn and self.serial_conn.is_open:
            data = self.send_entry.get()
            self.serial_conn.write(data.encode('utf-8'))
            self.send_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = SerialApp()
    app.mainloop()
