from threading import Thread
import os
import time
import socket
import sys

SERVER_IP="127.0.0.1"
SERVER_PORT = 10000

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
sock.bind((SERVER_IP, SERVER_PORT))

# Listen for incoming connections
sock.listen(5)

SOURCE = "./img/"
NAMAFILE = ["burger.png","brush.png","phone.png","twitter.png"]
FOLDER = "./server/"

def getRequest():
  while True:
    print "Menunggu request..."
    c, addr = sock.accept()
    data = c.recv(16)
    data_to_string = str(data)
    if(data_to_string[:3] == "REQ"):
      thread = Thread(target = setImage,args = (addr))
      thread.start()
    elif (data_to_string[:3] == "UPD"):
      thread = Thread(target = terima, args = (addr))
      thread.start()

def setImage(ip , port):
  addr = (ip,port)
  for x in NAMAFILE:
    time.sleep(5)
    kirim(x,addr)
  sock.sendto("CLOSE".ljust(1024),addr)

def kirim(imgname,addr):
  nama=os.path.join(SOURCE, imgname)
  fp = open(nama,'rb')
  paket = fp.read()
  terkirim = 0
  fp.close()
  sock.sendto(("START "+imgname).ljust(1024),addr)
  panjangpkt = len(paket)
  iterasi = (panjangpkt/1024)
  for i in range(iterasi+1):
    data=[]
    if (i+1)*1024 > panjangpkt:
      data = paket[i*1024:panjangpkt]
      terkirim = terkirim+len(data)
      data.ljust(1024)
    else:
      data = paket[i*1024:(i+1)*1024]
      terkirim = terkirim+len(data)
    sock.sendto(data,addr)
    print "Mengirim "+str(terkirim)+" dari "+str(panjangpkt)+" ke "+str(addr[0])+":"+str(addr[1])
  sock.sendto(("SELESAI MENGIRIM "+ imgname).ljust(1024),addr)
  getRequest()

def terima():
    print "Receiving..."
    while True:
      data,addr=sock.recvfrom(1024)
      if data[:5] == "START":
        namafile=data[6:].replace(" ","")
        nama=os.path.join(FOLDER,namafile)
        fp=open(nama,'wb+')
        ditulis=0
        print "Menerima "+namafile
      elif data[:3]=="END":
        print namafile+" berhasil diterima"
        fp.close()
      elif data[:5]=="CLOSE":
        print "Memutus koneksi..."
        break
      else:
        fp.write(data)
        ditulis=ditulis+len(data)
        print "Menerima "+str(ditulis)+" bytes"
    print "Done Receiving"

    sock.send('Thank you for connecting')
    sock.close()
    getRequest()

if __name__ == '__main__':
    getRequest()