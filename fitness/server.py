import socket, subprocess
from threading import *

class Server( Thread ):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.running = True
        self.process()

    def bindmsock(self):
        self.msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.msock.bind(('', 9090))
        self.msock.listen(1)
        print '[Server] Listening on port 9090'

    def acceptmsock(self):
        self.mconn, self.maddr = self.msock.accept()
        print '[Server] Got connection from', self.maddr
    
    def bindcsock(self):
        self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.csock.bind(('', 9091))
        self.csock.listen(1)
        print '[Server] Listening on port 9091'

    def acceptcsock(self):
        self.cconn, self.maddr = self.csock.accept()
        print '[Server] Got connection from', self.maddr
        
        while 1:
            data = self.cconn.recv(1024)
            if not data:
                break
            if data[0:5] == "BENCH":
                data = data.split(";")
                self.cfilename = data[1]
                self.compiler = data[2]
                self.flags = data[3]
                self.binaryname = self.cfilename[:-2] + ".serverSide.bin"
                print '[Server] Getting ready to receive "%s"' % self.cfilename
                break
            elif data[0:4] == "EXIT":
                self.running = False
                print '[Server] Received EXIT signal'
                break

    def transfer(self):
        print '[Server] Starting file transfer for "%s"' % self.cfilename

        f = open(self.cfilename,"wb")
        while 1:
            data = self.mconn.recv(4096)
            if not data: break
            f.write(data)
        f.close()
        self.change_binary_permission()
        print '[Server] Got "%s"' % self.cfilename
        print '[Server] Closing file transfer for "%s"' % self.cfilename   

    def compile(self):
        print "[Server] Compiling %s" % self.cfilename
        command_string = self.compiler + " " + self.flags + " " +\
        self.cfilename + " -o" + self.binaryname
        print "[Server] Compilation command \"%s\"" % command_string
        proc = subprocess.Popen(command_string , shell=True,\
        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        for line in proc.stderr:
            print("stderr: " + line.rstrip())
        for line in proc.stdout:
            print("stdout: " + line.rstrip()) 
    
    def close(self):
        self.cconn.close()
        self.csock.close()
        self.mconn.close()
        self.msock.close()

    def send_benchmark(self, value):
        ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ms.connect(("localhost", 9092))
        ms.send(value)
        ms.close()

    def change_binary_permission(self):
        proc = subprocess.Popen(["chmod +x", self.binaryname], \
            shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    def run_binary(self):
        proc = subprocess.Popen(self.binaryname, \
            shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        #for line in proc.stdout:
        #    print("stdout: " + line.rstrip())
        for line in proc.stderr:
            print("stderr: " + line.rstrip())

    def get_profile(self):
        proc = subprocess.Popen("gprof -b " + self.binaryname, \
            shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        gprof_output = ";".join([",".join([j.replace("\n", "")\
            for j in i.split(" ") if j != ""]) for i in proc.stdout][5:])
        for line in proc.stderr:
            print("Gprof stderr: " + line.rstrip())
        return gprof_output

    def benchmark(self):
        self.run_binary()
        self.send_benchmark(self.get_profile())

    def clean(self):
        subprocess.call("rm -rf gmon.out %s %s" %(self.binaryname,\
            self.cfilename), shell=True)

    def process(self):
        while self.running:
            self.bindcsock()
            self.acceptcsock()
            if self.running:
                self.bindmsock()
                self.acceptmsock()
                self.transfer()
                self.compile()
                self.benchmark()
                self.clean()
            self.close()

#------------------------------------------------------------------------

s = Server()
s.start()
