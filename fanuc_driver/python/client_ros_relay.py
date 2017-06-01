# May 30, 2017
# Masahiro Furukawa
#
# ref:
# http://qiita.com/nadechin/items/28fc8970d93dbf16e81b 
# http://inaz2.hatenablog.com/entry/2013/12/05/234357

# ref:                                                                          
# http://inaz2.hatenablog.com/entry/2013/12/05/234357                           
# https://docs.python.jp/3/library/struct.html                                  


# -*- coding:utf-8 -*-
import socket 
import array
import struct
import numpy
import math


#
# test codes 
#
# string -> float
xs =b'\x28\xa5\x8a\x3d'
print ":".join("{:02x}".format(ord(c)) for c in xs)

# float -> string
f = numpy.fromstring(xs, dtype=numpy.float32, count=1)[0]
print f

# string -> float
s = numpy.array([f], dtype=numpy.float32)[0].tostring()
print ":".join("{:02x}".format(ord(c)) for c in s)


#
# cliate socket
#
host = "192.168.1.54"
port= 11000 # ros_relay
#port= 11002 # ros_state

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

#READ fd(this.length_)
length_ = b'\x38\x00\x00\x00'
#READ fd(this.msg_type_)
msg_type_ = b'\x0a\x00\x00\x00'
#READ fd(this.comm_type_)
comm_type_ = b'\x01\x00\x00\x00'
#READ fd(this.reply_type_)
reply_type_ = b'\x00\x00\x00\x00'
#READ fd(this.seq_nr_)
seq_nr_ = b'\x00\x00\x00\x00'
#READ fd(this.joint_data_[i__])
data_0= b'\x28\xa5\x8a\x3d'
data_1= b'\xb0\x5f\x09\xbd'
data_2= b'\xbe\x68\xf7\xbd'
data_3= b'\xe9\xf1\x82\x3f'
data_4= b'\x2f\x1b\xf6\xbe'
data_5= b'\x4a\x35\xad\x3f'
data_6= b'\x00\x00\x00\x00'
data_7= b'\x00\x00\x00\x00'
data_8= b'\x00\x00\x00\x00'
data_9= b'\x00\x00\x00\x00'

#
# prepare header byte list
#
head = length_ + msg_type_ + comm_type_ + reply_type_ + seq_nr_
    

print numpy.fromstring(data_0, dtype=numpy.float32, count=1)[0]
print numpy.fromstring(data_1, dtype=numpy.float32, count=1)[0]
print numpy.fromstring(data_2, dtype=numpy.float32, count=1)[0]
print numpy.fromstring(data_3, dtype=numpy.float32, count=1)[0]
print numpy.fromstring(data_4, dtype=numpy.float32, count=1)[0]
print numpy.fromstring(data_5, dtype=numpy.float32, count=1)[0]


#
# test trajectories
#
# origin position (x, y, z, w, p, r)
pos = [ 0.0, 0.0, -500.0 ] # [mm]
wpr = [ 0.0, 0.0, 0.0 ]    # [deg]
omg = [ 5.1, 8.2, 10.3 ]    # [deg/cycle time]

vel = [0.0, 0.0, 0.0]      # [deg/cycle time]
r   = [20.0, 20.0, 10.0]
ofs = [0.0, 0.0, -500]

while True:

    pos[0] = r[0] * math.sin(vel[0] / 180.0 * math.pi) + ofs[0]
    pos[1] = r[1] * math.sin(vel[1] / 180.0 * math.pi) + ofs[1]
    pos[2] = r[2] * math.sin(vel[2] / 180.0 * math.pi) + ofs[2]

    vel[0] = vel[0] + omg[0]
    vel[1] = vel[1] + omg[1]
    vel[2] = vel[2] + omg[2]
    wpr = wpr + omg
                                                     
    # check overflow
    if (wpr[0] > 180): 
        wpr[0] = wpr[0] - 180.0
    if (wpr[1] > 180): 
        wpr[1] = wpr[1] - 180.0
    if (wpr[2] > 180): 
        wpr[2] = wpr[2] - 180.0


    print pos
        
    data_0 = numpy.array(pos, dtype=numpy.float32)[0].tostring()
    data_1 = numpy.array(pos, dtype=numpy.float32)[1].tostring()
    data_2 = numpy.array(pos, dtype=numpy.float32)[2].tostring()

    data_3 = numpy.array(wpr, dtype=numpy.float32)[0].tostring()
    data_4 = numpy.array(wpr, dtype=numpy.float32)[1].tostring()
    data_5 = numpy.array(wpr, dtype=numpy.float32)[2].tostring()

    # print ":".join("{:02x}".format(ord(c)) for c in data_0)


    #
    # join command byte list
    #
    data = data_0 + data_1 + data_2 + data_3 + data_4 + data_5 + data_6 + data_7 + data_8 + data_9
    cmd = head + data
    print ":".join("{:02x}".format(ord(c)) for c in cmd)
                                                                               

    #
    # send packet and receive responce
    #
    client.send(cmd)
    s = client.recv(4096)       
    print ":".join("{:02x}".format(ord(c)) for c in s)
