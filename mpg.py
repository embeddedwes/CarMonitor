import serial
stream = serial.Serial("COM9")

buffer = bytearray(4)


def process(command):
        buffer = bytearray()

        while 1:
                buffer += stream.read()
                if buffer.endswith(b">"):
                        break;
                
        #print(buffer.decode())

        index = buffer.find(command.encode())
        #print (index)
        
        if index > 0 :
                sub = buffer[index + 6:index + 6 + 2]
                #print(sub.decode())
                return int(sub.decode(), 16)
        else:
                return 0;

def process2(command):
        buffer = bytearray()

        while 1:
                buffer += stream.read()
                if buffer.endswith(b">"):
                        break;
                
        #print(buffer.decode())

        index = buffer.find(command.encode())
        #print(index)

        
        if index > 0 :
                sub = buffer[index + 6:index + 6 + 5]
                #print(sub.decode())
                #print(sub[0:2].decode())
                #print(sub[3:5].decode())
                a = int(sub[0:2].decode(), 16)
                b = int(sub[3:5].decode(), 16)
                #print(a)
                #print(b)
                return ((a*256)+b)
        else:
                return 0;

def process4(command):
        return 0;

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
        rpm = process2("41 0C") / 4
        stream.write("0104\r".encode())
        load = process("41 04") * 100 / 255
        stream.write("010d\r".encode())
        speed = process("41 0D")
        stream.write("0110\r".encode())
        maf = process2("41 10")
        mpg = 710.7 * speed / maf
        print("RPM %f Load %f Speed %f, MAF %f, MPG: %f" % (rpm, load, speed, maf, mpg))
        file = open ("data.txt" , "a")
        file.write("RPM %f Load %f Speed %f, MAF %f, MPG: %f\r\n" % (rpm, load, speed, maf, mpg))
        file.close()
