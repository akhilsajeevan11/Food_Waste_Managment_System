import serial

class ArduinoSerial:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            print(f"Connected to Arduino on {self.port}")
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}")
            exit(1)

    def read_signal(self):
        """Read signal from Arduino."""
        try:
            if self.serial_connection.in_waiting > 0:
                signal = self.serial_connection.readline().decode('utf-8').strip()
                return signal
            else:
                return None
        except serial.SerialException as e:
            print(f"Error reading from Arduino: {e}")
            return None

    def send_signal(self, message):
        """Send signal to Arduino."""
        try:
            if self.serial_connection:
                self.serial_connection.write(message.encode('utf-8'))
        except serial.SerialException as e:
            print(f"Error sending to Arduino: {e}")

    def close(self):
        if self.serial_connection:
            self.serial_connection.close()
