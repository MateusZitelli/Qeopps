import socket, subprocess, re
from threading import *

# Example: 0.18user 0.00system 0:00.18elapsed 99%CPU (0avgtext+0avgdata 3312maxresident)
time_profiler_pattern = r"(.*)user (.*)system (.*)elapsed (.*)%CPU"

class Server( Thread ):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.running = True
        self.process()

    def bindcsock(self):
        self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.csock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.csock.bind(('0.0.0.0', 9091))
        self.csock.listen(10)
        print '[Server] Listening on port 9091'

    def acceptcsock(self):
        self.cconn, self.caddr = self.csock.accept()
        print '[Server] Got connection from', self.caddr
        while 1:
            data = self.cconn.recv(1024)
            if not data:
                break
            if data[0:5] == "BENCH":
                data = data.split("\0")
                self.cfilename = data[1]
                self.compiler = data[2]
                self.flags = data[3]
                self.binaryname = self.cfilename[:-2] + ".serverSide.bin"
                print '[Server] Getting ready to receive "%s"' % self.cfilename
                self.transfer(data[4])
                break
            elif data[0:4] == "EXIT":
                self.running = False
                print '[Server] Received EXIT signal'
                break

    def transfer(self, startBytes):
        print '[Server] Starting file transfer for "%s"' % self.cfilename
        f = open(self.cfilename,"wb")
        f.write(startBytes)
        while 1:
            data = self.cconn.recv(4096)
            if not data: break
            f.write(data)
        f.close()
        self.change_binary_permission()
        print '[Server] Got "%s"' % self.cfilename
        print '[Server] Closing file transfer for "%s"' % self.cfilename

    def compile(self):
        print "[Server] Compiling %s" % self.cfilename
        command_string = self.compiler + " " + self.flags + " " +\
        self.cfilename + " -g -o" + self.binaryname
        print "[Server] Compilation command \"%s\"" % command_string
        proc = subprocess.Popen(command_string , shell=True,\
        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        self.compile_error = False
        for line in proc.stderr:
            self.compile_error = True
            print("stderr: " + line.rstrip())
        for line in proc.stdout:
            print("stdout: " + line.rstrip())

    def close(self):
        self.cconn.close()
        self.csock.close()

    def send_benchmark(self, value):
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect((self.caddr[0], 9092))
        cs.send(value)
        cs.close()

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

    def get_gprof_profile(self):
        proc = subprocess.Popen("gprof -b " + self.binaryname, \
            shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        gprof_output = ";".join([",".join([j.replace("\n", "")\
            for j in i.split(" ") if j != ""]) for i in proc.stdout][5:])
        for line in proc.stdout:
            print line
        for line in proc.stderr:
            print("Gprof stderr: " + line.rstrip())
        print "gprof -b " + self.binaryname
        return gprof_output

    def get_time_profile(self):
        proc = subprocess.Popen("(time %s)" % (self.binaryname), \
            shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        for line in proc.stderr:
            match = re.match(time_profiler_pattern, line)
            if match:
                break

        # Return sys time
        return match.group(1)


    def benchmark(self):
        self.run_binary()
        self.send_benchmark(self.get_time_profile())

    def clean(self):
        subprocess.call("rm -rf gmon.out %s %s" %(self.binaryname,\
            self.cfilename), shell=True)

    def process(self):
        while self.running:
            self.bindcsock()
            self.acceptcsock()
            if self.running:
                self.compile()
                self.benchmark()
                #self.clean()
            self.close()

#------------------------------------------------------------------------
if __name__ == "__main__":
    s = Server()
    s.start()
