# 本工程使用方法
* win10等x86_64或x86 cpu系统（包括x86的linux）  
首先设置pip源，这里未采用pipy源，太慢了，在文件工程目录下使用cmd或者linux shell，使用阿里源
> ```
> pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
> ```
然后直接安装requirements.txt中的相关wheel。
> ```
> pip install -r requirements.txt
> ```
* arm的cpu系统（这里只给基于debain的树莓派系统）
> ```
> sudo apt-get install python3-pyqt5
> sudo apt-get install at-spi2-core
> sudo apt-get install python3-opencv
> ```
注意如果提示pyserial找不到则直接安装requirements.txt中的pyserial
> ```
> pip install  pyserial==3.4
> ```
