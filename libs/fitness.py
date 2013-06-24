# USAGE: python Fitness.py

import sys, socket, subprocess, time

CPORT = 9091
MPORT = 9090
RPORT = 9092

class Fitness:
    def __init__(self, cfile, compiler="", flags="", host="0.0.0.0"):
        self.cfile = cfile
        self.cfileServerSide = cfile[:-2] + ".ss.c"
        self.compiler = compiler
        self.flags = flags
        self.host = host

    def send_instructions(self):
        print "[Client] Sending \"file receive\" task to Server"
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect((self.host, CPORT))
        cs.send("BENCH;%s;%s;%s" % (self.cfileServerSide,self.compiler,\
            self.flags))
        cs.close()

    def send_cfile(self):
        print "[Client] Sending binary"
        self.send_instructions()
        time.sleep(0.01)
        ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ms.connect((self.host, MPORT))
        f = open(self.cfile, "rb")
        data = f.read()
        f.close()
        ms.send(data)
        ms.close()

    def benchmark_parser(self):
        results = []
        self.benchs = self.bench_data.split(";")
        for i, j in enumerate(self.benchs[::1]):
            infos = j.split(",")
            print infos
            try:
                results.append([infos[3], float(infos[0]), float(infos[1]), float(infos[2])])
            except:
                pass
        return results

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
        return self.benchmark_parser()

    def shutdown_server(self):
        print "[Client] Shutting Down server"
        time.sleep(1)
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect((self.host, CPORT))
        cs.send("EXIT")
        cs.close()

    def benchmark(self):
        self.send_cfile()
        return self.receive_benchmark()

if __name__ == '__main__':
    f = Fitness("./teste.c", "gcc", "-pthread -pg -fgnu-tm")
    print f.benchmark()
    f.shutdown_server()
