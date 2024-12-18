import serial

class WeightScale:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            print(f"Connected to Weight Scale on {self.port}")
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port}: {e}")
            exit(1)

    def read_weight(self):
        """Read weight from the scale, remove 'K+' and convert to kilograms."""
        try:
            if self.serial_connection.in_waiting >= 0:
                weight_str = self.serial_connection.readline().decode('utf-8').strip()
                if weight_str.startswith('K+'):
                    # Remove the 'K+' prefix and convert the weight to kilograms
                    weight_str = weight_str[2:]  # Remove 'K+'
                try:
                    weight_kg = float(weight_str)  # Convert the string to float
                     # Format the weight to 3 decimal places
                    # weight_kg = round(weight_kg, 3)
                    return weight_kg
                except ValueError:
                    print("Error: Weight reading is not a valid number.")
                    return None
            else:
                return None
        except serial.SerialException as e:
            print(f"Error reading from Weight Scale: {e}")
            return None

    def close(self):
        if self.serial_connection:
            self.serial_connection.close()
