# USAGE: python Fitness.py

import sys, socket, subprocess, time, re

CPORT = 9091
RPORT = 9092

class Fitness:
    def __init__(self, cfile, compiler="gcc", flags="", host="0.0.0.0"):
        self.cfile = cfile
        self.cfileServerSide = cfile[:-2] + ".ss.c"
        self.compiler = compiler
        self.flags = flags
        self.host = host

    def send_cfile(self):
        print "[Client] Sending \"file receive\" task to Server"
        f = open(self.cfile, 'rb')
        filedata = f.read()
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect((self.host, CPORT))
        cs.send("BENCH\0%s\0%s\0%s\0%s" % (self.cfileServerSide,self.compiler,\
            self.flags,filedata))
        cs.close()

    def benchmark_gprof_parser(self):
        results = []
        self.benchs = self.bench_data.split(";")
        for i, j in enumerate(self.benchs[::1]):
            match = re.match(r'\[1\],100\.0,([0-9\.]*),.*', j)
            if match:
              return match.group(1)

    def benchmark_time_parser(self):
        return float(self.bench_data)

    def bindbsock(self):
        self.bsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bsock.bind(('', RPORT))
        self.bsock.listen(1)

    def receive_benchmark(self):
        self.bindbsock()
        self.bconn, self.maddr = self.bsock.accept()
        print "[Client] Receiving benchmark"
        self.bench_data = self.bconn.recv(1024)
        self.bsock.close()
        return self.benchmark_time_parser()

    def shutdown_server(self):
        print "[Client] Shutting Down server"
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect((self.host, CPORT))
        cs.send("EXIT")
        cs.close()

    def benchmark(self):
        self.send_cfile()
        return self.receive_benchmark()

if __name__ == '__main__':
    f = Fitness("./../Programs/nbody.c", "gcc", "-pthread -pg -fgnu-tm")
    print f.benchmark()
    f.shutdown_server()
