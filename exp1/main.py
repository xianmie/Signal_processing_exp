import numpy as np
import matplotlib.pyplot as plt

# 产生size点取样的三角波，其周期为1
def triangle_wave(size):
    x = np.arange(0, 0.02, 0.02/ size)
    y = np.where(x < 0.01, 300*x, 0)
    y = np.where(x >= 0.01, 300*(0.02 - x), y)
    return x, y


def square_wave(size):
    x = np.arange(0, 0.02, 0.02/ size)
    y = np.where(x < 0.01, 1.5, -1.5)
    return x, y

fft_size = 256

x, y = triangle_wave(fft_size)
fy = np.fft.fft(y) / fft_size

def fft_combine(freqs, n, loops=1):
  length = len(freqs) * loops
  data = np.zeros(length)
  index = loops * np.arange(0, length, 1.0) / length * (2 * np.pi)
  for k, p in enumerate(freqs[:n]):
    if k != 0: p *= 2 # 除去直流成分之外，其余的系数都*2
    data += np.real(p) * np.cos(k*index) # 余弦成分的系数为实数部
    data -= np.imag(p) * np.sin(k*index) # 正弦成分的系数为负的虚数部
  return index, data

plt.figure()
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data', 0))
plt.plot(x,y, label="original tirangle_wave", linewidth=2)
plt.xlabel('time/(s)')
plt.ylabel('Amplitude/(V)')

for i in [1,3,5,7,9]:
    index, data = fft_combine(fy, 1+i, 1) # 计算两个周期的合成波形
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.plot(x,data, label = "N=%s" %i)
plt.legend()
plt.title("partial Fourier series of triangle wave")
plt.show()

