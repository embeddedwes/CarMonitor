import serial
stream = serial.Serial("COM3")

data = bytearray(100)

def process(command, count):
        buffer = bytearray()

        while 1:
                buffer += stream.read()
                if buffer.endswith(b">"):
                        break;
                
        #print(buffer.decode())

        index = buffer.find(command.encode())
        #print (index)
        
        if index > 0:
                index += 6
                portion = buffer[index:index + 2 + (count * 3)]
                
                #print(sub.decode())

                for i in range(count):
                        data[i] = int(portion[(i * 3):(i * 3) + 2].decode(), 16)
                
                return;
        else:
                return;

def wait():
        buffer = bytearray()

        while 1:
                buffer += stream.read()
                if buffer.endswith(b">"):
                        break;
                
        print(buffer.decode())
        return;

stream.write("atz\r".encode())
wait()

stream.write("atrv\r".encode())
wait()

stream.write("atsp0\r".encode())
wait()

while 1:
        stream.write("010c\r".encode())
        process("41 0C", 2)
        rpm = ((data[0] * 256) + data[1]) / 4
        
        stream.write("0104\r".encode())
        process("41 04", 1)
        load = data[0] * (100.0 / 255)
        
        stream.write("010d\r".encode())
        process("41 0D", 1)
        speed = data[0]

        stream.write("0105\r".encode())
        process("41 05", 1)
        coolant_temp = data[0] - 40
        
        stream.write("0110\r".encode())
        process("41 10", 2)
        maf = ((data[0] * 256) + data[1])
        
        mpg = 710.7 * speed / maf
        print("RPM %f Load %f Speed %f, MAF %f, MPG: %f, Cool Temp: %f" % (rpm, load, speed, maf, mpg, coolant_temp))
        #file = open ("data.txt" , "a")
        #file.write("RPM %f Load %f Speed %f, MAF %f, MPG: %f\r\n" % (rpm, load, speed, maf, mpg))
        #file.close()
