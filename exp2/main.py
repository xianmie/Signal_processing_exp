import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import math
import scipy.integrate as si
import tkinter as tk
import tkinter.font as tkFont
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#采样
def Sample(n):
    t = np.arange(0, 1, 0.001)
    x=np.arange(0, 1, 0.001)
    for index in range(len(t)):
         if(t[index]==0):
             x[index]=1
         else:
             x[index] = t[index]*(1/t[index])
    i=0
    while i < n:
        x[i::n + 1] = 0
        i = i + 1
    return x
#巴特沃斯滤波
def Butterworth(data):
    b, a = signal.butter(8, 0.07, 'lowpass')
    filtedData = signal.filtfilt(b, a, data)
    return filtedData
def triangle_wave():
    x = np.arange(0, 1, 0.001)
    y = np.where(x < 0.5, 4*x, 0)
    y = np.where(x >= 0.5, 4*(1 - x), y)
    return x, y

def square_wave():
    t = np.arange(0, 1, 0.001)
    y = np.where(t < 0.5, 3.0, 0)
    return t, y


def fft_combine(freqs, n, loops=1):
  length = len(freqs) * loops
  data = np.zeros(length)
  index = loops * np.arange(0, length, 1.0) / length * (2 * np.pi)
  for k, p in enumerate(freqs[:n]):
    if k != 0: p *= 2 # 除去直流成分之外，其余的系数都*2
    data += np.real(p) * np.cos(k*index) # 余弦成分的系数为实数部
    data -= np.imag(p) * np.sin(k*index) # 正弦成分的系数为负的虚数部
  return index, data


# 定义Frequece Amplitude函数 Fre_ampl
# 第一个参数为信号时间的list，第二个参数为信号对应时间的幅度的list
# 返回两个参数，第一个参数为frequecy的list(所得频率序列需除以总时长)，第二个参数为amplitude的list
def Fre_ampl(x, y):
    y_f = np.fft.fft(y)
    f = np.arange(len(x))
    abs_y = np.abs(y_f)
    normalization_y = abs_y / (len(x))
    half_x = f[range(int(len(x) / 2))]
    normalization_y = normalization_y[range(int(len(x) / 2))]
    return half_x, normalization_y


# 定义Show sin函数 Show_sin
def Show_sin(N1,N2):
    # 定义信号时间
    t = np.arange(0, 1, 0.001)
    # 定义正弦波
    y_sin = 3 * np.sin(2 * np.pi * t)
    plt.figure(num=1, figsize=(8, 6))
    plt.subplot(4, 2, 1)
    plt.axis([0, 1.05, -3.2, 3.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.plot(t, y_sin, 'b')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    #滤波
    y_sin_butter=Butterworth(y_sin);
    plt.subplot(4,2,2)
    plt.axis([0, 1.05, -3.2, 3.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.plot(t,y_sin_butter)
    # 正常采样
    y_sin1 = y_sin.copy()
    sample=Sample(int(N1))
    plt.subplot(4,2,3)
    plt.plot(t,sample)
    y_sin1=y_sin1*Sample(int(N1))
    plt.subplot(4, 2, 4)
    plt.axis([0, 1.05, -3.2, 3.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.vlines(t, 0, y_sin1, 'r')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 欠采样
    y_sin2 = y_sin.copy()
    sample2=Sample(int(N2))
    plt.subplot(4,2,5)
    plt.plot(t,sample2)
    y_sin2=y_sin2*Sample(int(N2))
    plt.subplot(4, 2, 6)
    plt.axis([0, 1.05, -3.2, 3.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.vlines(t, 0, y_sin2, 'c')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 还原信号
    y_sinh1=Butterworth(y_sin1)
    y_sinh2=Butterworth(y_sin2)
    #b, a = signal.iirdesign(0.08, 0.1, 1, 40)  # 设置低通滤波器
    #y_sinh1 = signal.filtfilt(b, a, y_sin1)
    #y_sinh2 = signal.filtfilt(b, a, y_sin2)
    plt.subplot(4, 2, 7)
    plt.axis([0, 1.05, -0.25, 0.25])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.plot(t, y_sinh1, color='r', label='enough')
    plt.plot(t, y_sinh2, color='c', label='low')
    plt.legend(loc='upper right')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    img.draw()
def Show_squr(N1,N2):
    fft_size = 1000
    t,y = square_wave()
    fy = np.fft.fft(y) / fft_size

    index, y_squr = fft_combine(fy, 20, 1)  # 计算两个周期的合成波形

    plt.figure(num=1, figsize=(8, 6))
    plt.subplot(4, 2, 1)
    plt.axis([0, 1.05, -4.2, 4.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.plot(t, y_squr, 'b')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    #滤波
    y_squr_butter=Butterworth(y_squr);
    plt.subplot(4,2,2)
    plt.axis([0, 1.05, -4.2, 4.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.plot(t,y_squr_butter[0:1000])
    # 正常采样
    y_squr1 = y_squr.copy()
    sample=Sample(int(N1))
    plt.subplot(4,2,3)
    plt.plot(t,sample)
    y_squr1=y_squr1*Sample(int(N1))
    plt.subplot(4, 2, 4)
    plt.axis([0, 1.05, -3.2, 3.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.vlines(t, 0, y_squr1, 'r')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 欠采样
    y_squr2 = y_squr.copy()
    sample2=Sample(int(N2))
    plt.subplot(4,2,5)
    plt.plot(t,sample2)
    y_squr2=y_squr2*Sample(int(N2))
    plt.subplot(4, 2, 6)
    plt.axis([0, 1.05, -3.2, 3.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.vlines(t, 0, y_squr2, 'c')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 还原信号
    y_squrh1=Butterworth(y_squr1)
    y_squrh2=Butterworth(y_squr2)
    #b, a = signal.iirdesign(0.08, 0.1, 1, 40)  # 设置低通滤波器
    #y_sinh1 = signal.filtfilt(b, a, y_sin1)
    #y_sinh2 = signal.filtfilt(b, a, y_sin2)
    plt.subplot(4, 2, 7)
    plt.axis([0, 1.05, -0.25, 0.25])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.plot(t, y_squrh1, color='r', label='enough')
    plt.plot(t, y_squrh2, color='c', label='low')
    plt.legend(loc='upper right')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    img.draw()

def Show_tri(N1,N2):
    fft_size = 1000
    t,y = triangle_wave()
    fy = np.fft.fft(y) / fft_size

    index, y_squr = fft_combine(fy, 20, 1)  # 计算两个周期的合成波形

    plt.figure(num=1, figsize=(8, 6))
    plt.subplot(4, 2, 1)
    plt.axis([0, 1.05, -4.2, 4.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.plot(t, y_squr, 'b')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    #滤波
    y_squr_butter=Butterworth(y_squr);
    plt.subplot(4,2,2)
    plt.axis([0, 1.05, -4.2, 4.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))

    plt.plot(t,y_squr_butter)
    # 正常采样
    y_squr1 = y_squr.copy()
    sample=Sample(int(N1))
    plt.subplot(4,2,3)
    plt.plot(t,sample)
    y_squr1=y_squr1*Sample(int(N1))
    plt.subplot(4, 2, 4)
    plt.axis([0, 1.05, -3.2, 3.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.vlines(t, 0, y_squr1, 'r')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 欠采样
    y_squr2 = y_squr.copy()
    sample2=Sample(int(N2))
    plt.subplot(4,2,5)
    plt.plot(t,sample2)
    y_squr2=y_squr2*Sample(int(N2))
    plt.subplot(4, 2, 6)
    plt.axis([0, 1.05, -3.2, 3.2])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.vlines(t, 0, y_squr2, 'c')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 还原信号
    y_squrh1=Butterworth(y_squr1)
    y_squrh2=Butterworth(y_squr2)
    #b, a = signal.iirdesign(0.08, 0.1, 1, 40)  # 设置低通滤波器
    #y_sinh1 = signal.filtfilt(b, a, y_sin1)
    #y_sinh2 = signal.filtfilt(b, a, y_sin2)
    plt.subplot(4, 2, 7)
    plt.axis([0, 1.05, -0.5, 0.5])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))
    plt.axis([0, 1.05, -0.2, 0.2])
    plt.plot(t, y_squrh1, color='r', label='enough')
    plt.plot(t, y_squrh2, color='c', label='low')
    plt.legend(loc='upper right')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    img.draw()

# 定义函数is_number 判断一个字符串是不是数字。
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# 定义函数callback 显示轨迹按键的界面响应。
def callback():
    plt.clf()
    if is_number(info[0].get()) and is_number(info[1].get()) and is_number(info[2].get()):
        fun_show()
    else:
        tk.messagebox.showerror("错误", "数据不符合要求，请重新输入")

def ui_init():
    ui = tk.Tk()
    ui.resizable(False, False)  # 取小最大化的按键

    ui.title("exp2:信号的抽样和内插")
    ui.geometry("1200x700+0+0")  # 设置界面大小

    ##设置输入界面
    label1 = tk.Label(ui, text='输入要绘制的波形代号（1-sin/2-tri/3-squr）', fg='Purple')
    label1.place(relx=0.12, rely=0.1, width=250, height=30)
    label2 = tk.Label(ui, text='输入抽样间隔1(enough)', fg='Purple')
    label2.place(relx=0.12, rely=0.3, width=150, height=30)
    label3 = tk.Label(ui, text='输入抽样间隔2(low)', fg='Purple')
    label3.place(relx=0.12, rely=0.5, width=150, height=30)

    R1 = tk.StringVar()
    R2 = tk.StringVar()
    R3 = tk.StringVar()

    entry1 = tk.Entry(ui, textvariable=R1)
    entry1.place(relx=0.12, rely=0.1, width=120, y=30)
    entry2 = tk.Entry(ui, textvariable=R2)
    entry2.place(relx=0.12, rely=0.3, width=120, y=30)
    entry3 = tk.Entry(ui, textvariable=R3)
    entry3.place(relx=0.12, rely=0.5, width=120, y=30)
    info = [entry1, entry2, entry3]

    ##设置按键及点击事件
    button1 = tk.Button(ui, text='显示波形', command=callback)
    button1.place(relx=0.12, rely=0.7, width=120, height=70)
    return ui, info


# 定义函数fig_init plot界面初始化，返回视图fig，以及画板img。
def fig_init(ui):
    matplotlib.use('TkAgg')
    fig = plt.figure(num=1)
    img = FigureCanvasTkAgg(fig, master=ui)
    img.draw()
    img.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
    toolbar = NavigationToolbar2Tk(img, ui)
    toolbar.update()
    img._tkcanvas.place(relx=0.4, rely=0.1, width=600, height=600)
    return fig, img
def fun_show():
    type = float(info[0].get())
    sample1 = float(info[1].get())
    sample2 = float(info[2].get())
    if(type==1):
        Show_sin(sample1,sample2)
    if(type==2):
        Show_tri(sample1,sample2)
    if(type==3):
        Show_squr(sample1,sample2)

# 运行界面
ui, info = ui_init()
fig, img = fig_init(ui)
ui.mainloop()


