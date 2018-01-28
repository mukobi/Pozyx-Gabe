import pandas as pd
import matplotlib.pyplot as plt

#df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/Motor_Turntable/rps_motor_turntable_1.txt', delimiter=' ',  usecols=['Time','RPS','Rotations'])

df=pd.read_csv('/Users/CoraJune/Desktop/HomeData/no_anchors_still/testing_anchors_still_4.csv', delimiter=' ', usecols=[2, 13, 14, 15], names=['Time','xpos','ypos','zpos'])

df1=pd.read_csv('/Users/CoraJune/Desktop/HomeData/no_anchors_still/testing_anchors_still_6.csv', delimiter=' ', usecols=[2, 13, 14, 15], names=['Time1','xpos1','ypos1','zpos1'])


#df1=pd.read_csv('/Users/CoraJune/Desktop/HomeData/no_anchors_perp/4_anchors_60s_32.csv', delimiter=' ',  usecols=[2, 13, 14, 15], names=['Time1','xpos1','ypos1','zpos1'])

#df2=pd.read_csv('/Users/CoraJune/Desktop/HomeData/no_anchors_perp/4_anchors_60s_33.csv', delimiter=' ',  usecols=[2, 13, 14, 15], names=['Time2','xpos2','ypos2','zpos2'])

#df3=pd.read_csv('/Users/CoraJune/Desktop/HomeData/no_anchors_perp/6_anchors_60s_perp_21.csv', delimiter=' ',  usecols=[2, 13, 14, 15], names=['Time3','xpos3','ypos3','zpos3'])

#df4=pd.read_csv('/Users/CoraJune/Desktop/HomeData/no_anchors_perp/6_anchors_60s_perp_22.csv', delimiter=' ',  usecols=[2, 13, 14, 15], names=['Time4','xpos4','ypos4','zpos4'])

#df5=pd.read_csv('/Users/CoraJune/Desktop/HomeData/no_anchors_perp/6_anchors_60s_perp_23.csv', delimiter=' ',  usecols=[2, 13, 14, 15], names=['Time5','xpos5','ypos5','zpos5'])

print('STD GRAPH 1')
print(df.std())
print(' ')
print('STD GRAPH 2')
print(df1.std())
print(' ')
#print('STD GRAPH 3')
#print(df1.std())
#print(' ')
#print('STD GRAPH 4')
#print(df4.std())
#print(' ')
#print('STD GRAPH 5')
#print(df2.std())
#print(' ')
#print('STD GRAPH 6')
#print(df5.std())


plt.figure(figsize=(12,7))

x=df['Time']
y1=df['xpos']
y2=df['ypos']
y3=df['zpos']
x1=df1['Time1']
y4=df1['xpos1']
y5=df1['ypos1']
y6=df1['zpos1']
plt.subplot(3,2,1)
plt.tick_params(labelsize=6)
plt.plot(x,y1)
plt.xlabel('Time', fontsize=9)
plt.ylabel('xpos', fontsize=9)
plt.title('xpos 4 anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

plt.subplot(3,2,3)
plt.tick_params(labelsize=6)
plt.plot(x,y2)
plt.xlabel('Time', fontsize=9)
plt.ylabel('ypos', fontsize=9)
plt.title('ypos 4 anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

plt.subplot(3,2,5)
plt.tick_params(labelsize=6)
plt.plot(x,y3)
plt.xlabel('Time', fontsize=9)
plt.ylabel('zpos', fontsize=9)
plt.title('zpos 4 anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

plt.subplot(3,2,2)
plt.tick_params(labelsize=6)
plt.plot(x1,y4)
plt.xlabel('Time', fontsize=9)
plt.ylabel('xpos', fontsize=9)
plt.title('xpos 6 anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

plt.subplot(3,2,4)
plt.tick_params(labelsize=6)
plt.plot(x1,y5)
plt.xlabel('Time', fontsize=9)
plt.ylabel('ypos', fontsize=9)
plt.title('y pos 6 anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

plt.subplot(3,2,6)
plt.tick_params(labelsize=6)
plt.plot(x1,y6)
plt.xlabel('Time', fontsize=9)
plt.ylabel('zpos', fontsize=9)
plt.title('zpos 6 anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

plt.show()
'''
#x1=df1['Time1']
#y4=df1['xpos1']
#y5=df1['ypos1']
#y6=df1['zpos1']
#plt.subplot(3,2,3)
#plt.tick_params(labelsize=6)
#plt.plot(x1,y4)
#plt.plot(x1,y5)
plt.plot(x1,y6)
plt.xlabel('Time', fontsize=9)
plt.ylabel('Position', fontsize=9)
plt.title('4 Anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

x2=df2['Time2']
y7=df2['xpos2']
y8=df2['ypos2']
y9=df2['zpos2']
plt.subplot(3,2,5)
plt.tick_params(labelsize=6)
plt.plot(x2,y7)
plt.plot(x2,y8)
plt.plot(x2,y9)
plt.xlabel('time', fontsize=9)
plt.ylabel('position', fontsize=9)
plt.title('4 Anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

x3=df3['Time3']
y10=df3['xpos3']
y11=df3['ypos3']
y12=df3['zpos3']
plt.subplot(3,2,2)
plt.tick_params(labelsize=6)
plt.plot(x3,y10)
plt.plot(x3,y11)
plt.plot(x3,y12)
plt.xlabel('time', fontsize=9)
plt.ylabel('position', fontsize=9)
plt.title('6 Anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

x4=df4['Time4']
y13=df4['xpos4']
y14=df4['ypos4']
y15=df4['zpos4']
plt.subplot(3,2,4)
plt.tick_params(labelsize=6)
plt.plot(x4,y13)
plt.plot(x4,y14)
plt.plot(x4,y15)
plt.xlabel('time', fontsize=9)
plt.ylabel('position', fontsize=9)
plt.title('6 Anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

x5=df5['Time5']
y16=df5['xpos5']
y17=df5['ypos5']
y18=df5['zpos5']
plt.subplot(3,2,6)
plt.tick_params(labelsize=6)
plt.plot(x5,y16)
plt.plot(x5,y17)
plt.plot(x5,y18)
plt.xlabel('time', fontsize=9)
plt.ylabel('position', fontsize=9)
plt.title('6 Anchors', fontsize=10, weight='bold')
plt.legend( loc=2, prop={'size': 4})
plt.tight_layout()

plt.show()


'''
