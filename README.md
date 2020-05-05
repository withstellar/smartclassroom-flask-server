# flask-server Windows本地部署文档

## 需安装mysql

## 所使用的Python版本为2.7

## 解压压缩包

## 安装virtualenv

	Windows cmd
```
	pip install virtualenv	#安装虚拟环境
	cd + 当前项目文件夹地址	#在当前文件夹中操作
	virtualenv venv			#创建虚拟环境 虚拟环境可随意取名不一定要是venv
	venv\Scripts\activate	#激活虚拟环境
```

## 在虚拟环境中安装依赖

```
	pip install -r requirements.txt
```
## 特殊依赖安装(mysql-python)

```
	mysql-python有可能不能在Windows下直接使用pip安装(若可以直接安装，执行pip install mysql-python即可)，可直接下载驱动安装
	[驱动下载地址](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python)
	根据操作系统位数选择相应驱动，64位是第二个MySQL_python-1.2.5-cp27-none-win_amd64.whl
	下载完之后在命令行中cd到.whl文件即驱动文件所在文件夹，执行以下命令
	pip install MySQL_python-1.2.5-cp27-none-win_amd64.whl
```
## 创建数据库

```
	进入MySQL Command 首先要输入你设置的密码
	create database [数据库名字] charset utf8;	#创建数据库
```
## 初始化数据库(所有操作在虚拟环境中进行，要先激活虚拟环境)

```
	在config.py中将数据库名改为设置的名字 如：DATABASE = 'facedata'(facedata即为上一步设置的数据库名字)
	检查config.py中的密码配置，确保与自己设置的相同，默认MySQL端口为3306
	python manage.py initserver		#根据.xlsx表格学生名单初始化数据库
```
## 运行服务(先激活虚拟环境)

```
	python app.py  	#运行flask服务，默认在http://127.0.0.1:5000/上开启
```



# flask-server api 使用文档

## 获取学生考勤状态

```
	请求方式： GET
	请求URL实例: http://127.0.0.1:5000/api/getstate?stu_id=2018302110001		#stu_id为学号参数，根据学号获取学生的考勤信息
	返回数据格式: json
	1.正常返回:
		{
			"attendance": false,		#false代表缺勤，true为已考勤
			"code": 20000,				#code状态码，20000代表正常，40001代表无法查询到相关学生信息，40002代表请求数据格式错误，下同
			"name": "王乐容",
			"stu_id": 2018302110001
		}

	2.异常返回
		{
			"code": 40001,
			"text": "未查询到相关学生信息"
		}或
		{
			"code": 40002,
			"text": "数据格式错误"
		}
```
## 设置学生考勤状态

```
	请求方式: POST
	请求URL: http://127.0.0.1:5000/api/setstate
	请求数据格式: json
		{
			"attendance": true,			#可将考勤状态设置为false或true
			"stu_id": 2018302110001
		}
	返回数据格式: json
	1.正常返回
		{
			"code": 20000
		}

	2.异常返回
		{
			"code": 40001,
			"text": "未查询到相关学生信息"
		}或
		{
			"code": 40002,
			"text": "数据格式错误"
		}
```
## 使用curl模拟GET和POST请求进行测试(可在网上查阅相关教程)

注意事项: 单引号在Linux和Windows的含义不同，curl调用格式也略有差异，Windows下双引号內部使用双引号需要"\"转义，下面将会分别标出Linux和Windows使用的命令

1.GET请求

```
	使用curl发送GET请求的格式为: curl protocol://address:port/url?args
	curl http://127.0.0.1:5000/api/getstate?stu_id=2018302110001		#Linux和Windows均可
	curl 'http://127.0.0.1:5000/api/getstate?stu_id=2018302110001'		#Linux下
	curl "http://127.0.0.1:5000/api/getstate?stu_id=2018302110001"		#Linux和Windows均可
```
2.POST请求

```
	Linux:
	curl -H "Content-Type: application/json" -X POST -d '{"stu_id": 2018302110001, "attendance": true}' http://127.0.0.1:5000/api/setstate

	Windows:
	curl -H "Content-Type: application/json" -X POST -d "{\"stu_id\": 2018302110001, \"attendance\": true}" http://127.0.0.1:5000/api/setstate
```

Windows可在控制面板->启用或关闭Windows功能中开启`适用于Linux的Windows子系统`功能，在软件商店中下载Ubuntu启用后在命令行使用bash命令