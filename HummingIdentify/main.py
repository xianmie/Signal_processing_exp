import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import librosa.util

fs = 2000
n_fft = 2048

f = fs*np.array(range(int(1+n_fft/2)))/(n_fft/2)

path =r"C:\Users\young\Music\Hum.wav"
data = librosa.load(path,sr=fs)
length = len(data[0])
spec = np.array(librosa.stft(data[0], n_fft=2048, hop_length=160, win_length=1024, window='hann'))
speca=np.abs(spec)


#y, sr = librosa.load(path, sr=fs, duration=None)
# cent = librosa.feature.spectral_centroid(y=y, sr=sr)
# chroma = librosa.stft(y)
# speca = abs(chroma)

m=speca.shape[1]
n=speca.shape[0]
speca1=np.zeros((n,m))
speca2=np.empty(m)
for j in range (m):#列
    for i in range (n):
        if(speca[i,j]>=8):
            speca1[i,j]=speca[i,j]
            speca2[j]=(i/n)*fs
            break
for j in range (m):
    if ((speca2[j] <=201) ):
        speca2[j] = 1
    if ((speca2[j] > 201)& (speca2[j] < 216)):
        speca2[j] = 2
    if ((speca2[j] >= 216) & (speca2[j] < 226)):
        speca2[j] = 3
    if ((speca2[j] >= 226) & (speca2[j] < 240)):
        speca2[j] = 4
    if((speca2[j]>=240)&(speca2[j]<252)):
        speca2[j]=5
    if((speca2[j]>=252)&(speca2[j]<270)):
        speca2[j]=6
    if((speca2[j]>=270)&(speca2[j]<283)):
        speca2[j]=7
    if((speca2[j]>=283)&(speca2[j]<300)):
        speca2[j]=8
    if((speca2[j]>=300)&(speca2[j]<320)):
        speca2[j]=9
    if((speca2[j]>=320)&(speca2[j]<339)):
        speca2[j]=10
    if((speca2[j]>=339)&(speca2[j]<359)):
        speca2[j]=11
    if((speca2[j]>=359)&(speca2[j]<381)):
        speca2[j]=12
    if((speca2[j]>=381)&(speca2[j]<403)):
        speca2[j]=13
    if((speca2[j]>=403)&(speca2[j]<427)):
        speca2[j]=14
    if((speca2[j]>=427)&(speca2[j]<453)):
        speca2[j]=15
    if((speca2[j]>=453)&(speca2[j]<480)):
        speca2[j]=16
    if((speca2[j]>=480)):
        speca2[j]=17




plt.subplots_adjust(wspace=1, hspace=0.2)
plt.subplot(312)
plt.pcolormesh(np.array(range(int(length/160+1)))/fs, f, speca)
#librosa.display.specshow(speca, sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()

plt.subplot(311)
librosa.display.waveplot(data[0], sr=fs)
plt.xlabel('second')
plt.ylabel('amplitude')

# plt.subplot(413)
# plt.subplots_adjust(wspace=1, hspace=0.2)
# plt.pcolormesh(np.array(range(int(length/160+1)))/fs, f, speca1)

plt.subplot(313)
plt.grid(linewidth=0.5)
plt.yticks(range(1, 18),["3G","3G#","4A","4bB","4B","4C","4C#","4D","4bE","4E","4F","4F#","4G","4G#","5A","bB","5B"])
plt.scatter(range(len(speca2)),speca2, marker="s", s=1, color="red")
plt.show()

