
import numpy as np
import matplotlib.pyplot as plt
from pozyx_funcs import read_ranging,zero_time,array_stats,array_diff


tFast1,xFast1,p1=read_ranging()
tFast2,xFast2,p2=read_ranging(filename='110fast.txt')
#tFast3,xFast3,p2=read_ranging(filename='FAST3.txt')
#tFast3,xFast3,p2=read_ranging(filename='FASTLONG.txt')#####
#tFast4,xFast4,p2=read_ranging(filename='FASTBALL.txt')#####
tPrecision1,xPrecision1,p2=read_ranging(filename='110precision.txt')
#tPrecision2,xPrecision2,p2=read_ranging(filename='PRECISION2.txt')
#tPrecision2,xPrecision2,p2=read_ranging(filename='PRECISIONLONG.txt')#####
#tPrecision3,xPrecision3,p2=read_ranging(filename='PRECISION3.txt')#####
#tPrecision4,xPrecision4,p2=read_ranging(filename='BALLPRECISION.txt')#####

#import pdb;pdb.set_trace()


tFast1=zero_time(tFast1)
tPrecision1=zero_time(tPrecision1)
tPrecision3=zero_time(tPrecision3)
tPrecision4=zero_time(tPrecision4)
tFast4=zero_time(tFast4)

tFast3=zero_time(tFast3)
tPrecision2=zero_time(tPrecision2)

d1=array_diff(tFast3)
d2=array_diff(tPrecision2)

print('Stats')
print('Fast3')
array_stats(xFast3,start=100)
print('Precision2')
array_stats(xPrecision2)
print('Precision3')
array_stats(xPrecision3)

print('Time Array 0-10')
print('Fast')
print(tFast1[0:10])
print('Precision')
print(tPrecision1[0:10])

print('Average Time Steps')
print('Fast 1')
print(np.mean(d1))
print('Precision')
print(np.mean(d2))

psize=10
fsize=12

fig,ax11 = plt.subplots(figsize=(15,9),nrows=1,ncols=1)

#ax11.plot(tFast1,xFast1,'bo',ms=psize)
#ax11.plot(tPrecision1,xPrecision1,'ro',ms=psize)
#ax11.plot(tFast3,xFast3,'bo',ms=psize,label='Fast')
#ax11.plot(tPrecision2,xPrecision2,'ro',ms=psize,label='Precision')
#ax11.set_xlim([0,500])
ax11.plot(tFast4,xFast4,'bo',ms=psize,label='Fast')
ax11.plot(tPrecision4,xPrecision4,'ro',ms=psize,label='Precision')

#ax11.plot(tPrecision3,xPrecision3,'ro',ms=psize,label='Precision')
plt.legend(numpoints=1,loc='upper left',fontsize=fsize)
plt.show()
