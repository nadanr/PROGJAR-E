import socket
import sys
import os

SERVER_IP="127.0.0.1"
SERVER_PORT= 10000
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
# print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect((SERVER_IP, SERVER_PORT))

ditulis=0
folder="./client1/"
imgname = ["burger.png","brush.png","phone.png","twitter.png"]

def terima():
    pesan = 'REQ'
    sock.sendall(pesan)
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


def upload():
    pesan = 'UPD'
    sock.sendall(pesan)
    nama = os.path.join(folder, imgname)
    fp = open(nama, 'rb')
    paket = fp.read()
    terkirim = 0
    fp.close()
    sock.sendto(("START " + imgname).ljust(1024), addr)
    panjangpkt = len(paket)
    iterasi = (panjangpkt / 1024)
    for i in range(iterasi + 1):
        data = []
        if (i + 1) * 1024 > panjangpkt:
            data = paket[i * 1024:panjangpkt]
            terkirim = terkirim + len(data)
            data.ljust(1024)
        else:
            data = paket[i * 1024:(i + 1) * 1024]
            terkirim = terkirim + len(data)
        sock.sendto(data, addr)
        print "Mengirim " + str(terkirim) + " dari " + str(panjangpkt) + " ke " + str(addr[0]) + ":" + str(addr[1])
    sock.sendto(("SELESAI MENGIRIM " + imgname).ljust(1024), addr)

if __name__ == '__main__':
    print("1. REQUEST\n2. UPLOAD\n")
    choice = int(input())

    if choice == 1:
        terima()

    elif choice == 2:
        upload()