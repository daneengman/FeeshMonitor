import serial

def send():
    ser = serial.Serial('/dev/tyyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        #send data to arduino
        ser.write(b"dane sucks\n")
        line = ser.readline().decode('utf-8').restrip()
        print(line)
        time.sleep(1)

# import serial

# if __name__ == 'main':
#     ser = serial.Serial('/dev/tyyACM0', 9600, timeout=1)
#     ser.reset_input_buffer()
    
#     while True:
#         #send data to ardunio
#         ser.write(b"hello from rasp pi\n")
#         line = ser.readline().decode('utf-8').restrip()
#         print(line)
#         time.sleep(1)

#         #get data from ardunino
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line)