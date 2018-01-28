import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df=pd.read_csv('/Users/CoraJune/Google Drive/Pozyx/Data/lab_applications/lab_redos/atwood_machine/alpha_ema_testing/alpha0.9/atwood_0.9_4diff.csv', delimiter=',', usecols=['Time', '0x6103 Range'])

df.columns = ['Time', 'Range']

x = df['Time']
y = df['Range']

n = 25  #small n = less smoothed

fwd = pd.Series.ewm(df,span=n, adjust=True).mean()
bwd = pd.Series.ewm(df[::-1],span=n, adjust=True).mean()
filtered = np.stack(( fwd, bwd[::-1] ))
filtered = np.mean(filtered, axis=0)
plt.subplot(2,1,1)
plt.title('smoothed and raw data')
plt.plot(x,y, color = 'orange')
plt.plot(x,filtered, color='green')
plt.plot(x,fwd, color='red')
plt.plot(x[::-1],bwd, color='blue')
plt.xlabel('time')
plt.ylabel('distance')
plt.tight_layout()

df['Velocity'] = ((df['Range'] - df['Range'].shift(1)) / (df['Time'] - df['Time'].shift(1)))

y2 = df['Velocity']

m = 15
fwd2 = pd.Series.ewm(df.Velocity,span=m, adjust=True).mean()
bwd2 = pd.Series.ewm(df.Velocity[::-1],span=m, adjust=True).mean()
filtered2 = np.stack(( fwd2, bwd2[::-1] ))
filtered2 = np.mean(filtered2, axis=0)
plt.subplot(2,1,2)
plt.title('velocity smoothed and raw data')
plt.plot(x,y2, color = 'orange')
plt.plot(x,filtered2, color='green')
plt.plot(x,fwd2, color='red')
plt.plot(x[::-1],bwd2, color='blue')
plt.xlabel('time')
plt.ylabel('velocity')
plt.tight_layout()

#smoothed_velocity = ((df.filtered - df.filtered.shift(1)) /  df['Time'] - df['Time'].shift(1))

#print(smoothed_velocity)
#plt.subplot (2,2,3)
#plt.title ('smoothed velocity')
#plt.plot (smoothed_velocity, color = 'orange')

plt.tight_layout()
plt.show()

