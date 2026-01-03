import serial
import time

#SERIAL_PORT = 'COM5'
PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# virtual WSL environment
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    print(f"{PORT} connected successfully!")
except Exception as e:
    print(f"Fehler: {e}")


def capture_one_photo(ser, index):
    # reset Puffer, delete old Boot-Messages
    ser.reset_input_buffer()
    
    print(f"Send the capture command for the photo: {index}")
    # Send 'C' followed by a line break
    ser.write(b'C\n') 
    ser.flush()

    start_time = time.time()
    while True:
        # Check timeout (if ESP32 does not respond)
        if time.time() - start_time > 10:
            print("Timeout: ESP32 is not responding")
            return False

        line = ser.readline().decode('ascii', errors='ignore').strip()
        
        if line == "START_IMAGE":
            # read size
            size_line = ser.readline().decode('ascii', errors='ignore').strip()
            if not size_line.isdigit():
                continue
                
            img_size = int(size_line)
            print(f"Receiving {img_size} Bytes...")

            # read the data exactly
            img_data = b""
            while len(img_data) < img_size:
                chunk = ser.read(img_size - len(img_data))
                if not chunk: break
                img_data += chunk
            
            with open(f"data/camera_esp32/foto_{index}.jpg", "wb") as f:
                f.write(img_data)
            
            print(f"Photo {index} saved!")
            return True

def main():
    try:
        ser = serial.Serial()
        ser.port = PORT
        ser.baudrate = BAUD_RATE
        ser.timeout = 2
        ser.dtr = False # prevents permantent reset
        ser.rts = False # prevents permantent reset
        ser.open()

        print("Initializing connection")
        time.sleep(3)
        
        while True:
            cmd = input("Press 'Enter' for a photo or 'q' to exit: ")
            if cmd.lower() == 'q':
                break
            capture_one_photo(ser, int(time.time()))
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    main()