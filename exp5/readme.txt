代码主要架构：
1.定义sound_rec进行录音：先定义好通道、采样速率等数据流常数，使用pyaudio库例化一个pyaudio对象，读取数据流中的数据，读取完毕后关闭数据流，
  将读取内容写入录音文件
2.定义wave_read对音频文件进行读取：用wave库的wave.open()打开文件，用wave.open.gernframes()、wave.open.getframerate()、
  wave.open.readframes()读取音频文件的帧数量、帧速率以及每帧的数据等
3.定义time_plt函数绘制音频的时域图：根据wave_read读出的数据进行绘制
4.定义freq_plt绘制音频的频域图：对wave_read读取的数据进行一定采样率的采样，使用numoy.fft.fft()对信号进行fft变换，最后将变换后的数据可视化
5.主函数流程：先调用sound_rec(t)进行录音；用wave_read（’path‘）读取录音文件；使用time_plt绘制时域图；使用freq_plt绘制频域图