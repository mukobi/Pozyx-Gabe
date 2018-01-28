import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#df=pd.read_csv('/Users/CoraJune/Google Drive/Pozyx/Data/lab_applications/lab_redos/atwood_machine/alpha_ema_testing/alpha0.5/atwood_0.5_27diff.csv', delimiter=',', usecols=['Time', '0x6103 Range'])

df=pd.read_csv('/Users/CoraJune/Google Drive/Pozyx/Data/3D_Data/Overlook_Park/overlook_park_elmer_1.csv', delimiter=',', usecols=['Time', 'Position-X'])


df.columns = ['Time', 'Range']

x = df['Time']
y = df['Range']


#df2=pd.read_csv('/Users/CoraJune/Google Drive/Pozyx/Data/3D_Data/Overlook_Park/overlook_park_elmer_1.csv', delimiter=',', usecols=['Time', 'Position-X'])

#df2.columns = ['Time2', 'Range2']

#x2 = df2['Time2']
#y2 = df2['Range2']

fwd = pd.Series.ewm(df,span=5, adjust=True).mean()
bwd = pd.Series.ewm(df[::-1],span=5, adjust=True).mean()
filtered = np.stack(( fwd, bwd[::-1] ))
filtered = np.mean(filtered, axis=0)
#plt.subplot(2,1,1)
plt.title('smoothed and raw data')
plt.plot(y, color = 'orange')
plt.plot(filtered, color='green')
plt.plot(fwd, color='red')
plt.plot(bwd, color='blue')

#plt.subplot(2,1,2)
#fwd2 = pd.Series.ewm(df2,span=5, adjust=True).mean()
#bwd2 = pd.Series.ewm(df2[::-1],span=5, adjust=True).mean()
#filtered2 = np.stack((fwd2, bwd2[::-1] ))
#filtered2 = np.mean(filtered2, axis=0)

#plt.title('smoothed and raw data')
#plt.plot(x2,y2, color = 'orange')
#plt.plot(x2,filtered2[:,1], color='green')

#z = np.polyfit(x2, filtered2[:,1], 2)
#p = np.poly1d(z)
#plt.plot(x2,p(x2),"--", color='k')

#equation = "y = %.6f x^2 + %.6f x + %.6f"%(z[0],z[1],z[2])

#plt.figtext(.202,.2, equation,  style='italic', size=8)

plt.xlabel('time')
plt.ylabel('distance')
plt.tight_layout()

plt.show()
