# parkingsys停车场系统模拟
基于python vene的停车场系统模拟
## 1. 为模拟程序设置虚拟环境
以下设置过程只需要做一次即可

1.1 先在命令提示符程序中，进入程序所在目录，如`C:\ch2.4\ParkingSys`

1.2 创建虚拟环境：执行`python -m venv venv`

1.3 激活虚拟环境：执行`.\venv\Scripts\activate`，激活刚创建好的虚拟环境

1.4 安装依赖包：执行`pip install -r requirements.txt`; 如果安装速度较慢，可以自行在网上查找镜像网址，并在上述命令后使用`-i 镜像网址`参数来安装。

## 2. 运行模拟程序
2.1 先在命令提示符程序中，进入程序所在目录，如`C:\ch2.4\ParkingSys`

2.2 激活虚拟环境：执行`.\venv\Scripts\activate`

2.3 使用`python run.py`或者直接运行目录下run.bat文件

2.4 打开任一网络浏览器，使用`http://127.0.0.1:5000`来使用模拟程序

## 3. 初始化数据库
清空原数据库，生成日期比较近的20条随机记录

3.1 先在命令提示符程序中，进入程序所在目录，如`C:\ch2.4\ParkingSys`

3.2 激活虚拟环境：执行`.\venv\Scripts\activate`

3.3 设置FLASK APP信息：分别执行下面的命令：
```
set FLASK_APP=run.py
set FLASK_ENV=development
flask init-db
```
当看到“数据库初始化完毕”信息，初始化完成。

或者直接运行目录下的`initdb.bat`文件来初始化数据库。
