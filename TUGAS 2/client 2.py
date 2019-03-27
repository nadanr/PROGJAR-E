import socket
import time
import os

SERVER_IP="127.0.0.1"
SERVER_PORT= 10000

sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

ditulis=0
folder="./client2/"
sock.sendto("REQ",(SERVER_IP,SERVER_PORT))
print "Mengirim request..."
while True:
  data,addr=sock.recvfrom(1024)
  if data[:5] == "START":
    namafile=data[6:].replace(" ","")
    nama=os.path.join(folder,namafile)
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
print "Request selesai."