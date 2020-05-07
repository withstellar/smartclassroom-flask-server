## smartclassroom-flask-server Windows本地部署
---
注意事项：需安装mysql，所使用的Python版本为2.7

### 安装virtualenv

Windows cmd
```
pip install virtualenv	#安装虚拟环境
cd + current folder		#在当前文件夹中操作
virtualenv venv			#创建虚拟环境 虚拟环境可随意取名不一定要是venv
venv\Scripts\activate	#激活虚拟环境
```

### 在虚拟环境中安装依赖

```
pip install -r requirements.txt
```
### 特殊依赖安装(MySQL-python)

MySQL-python有可能不能在Windows下直接使用pip安装(若可以直接安装，执行pip install MySQL-python即可)，可直接下载驱动安装
[驱动下载地址](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python)
根据操作系统位数选择相应驱动，64位是第二个MySQL_python-1.2.5-cp27-none-win_amd64.whl
下载完之后在命令行中cd到.whl文件即驱动文件所在文件夹，执行以下命令

```
pip install MySQL_python-1.2.5-cp27-none-win_amd64.whl
```
### 创建数据库

进入MySQL Command 首先要输入你设置的密码
```mysql
create database [数据库名字] charset utf8;	#创建数据库
```
### 初始化数据库(所有操作在虚拟环境中进行，要先激活虚拟环境)

在config.py中将数据库名改为设置的名字 如：DATABASE = 'facedata'(facedata即为上一步设置的数据库名字)
检查config.py中的密码配置，确保与自己设置的相同，默认MySQL端口为3306
```python
python manage.py initserver		#根据.xlsx表格数据初始化数据库
```
### 运行服务(先激活虚拟环境)

```python
python app.py  	#运行flask服务，默认在http://127.0.0.1:5000/上开启
```

## smartclassroom-flask-server 服务器部署
---
服务器操作系统： CentOS 7.6 64位

参考文章

> https://juejin.im/post/5a5a7fce6fb9a01caa207d1d

### 特殊依赖安装(MySQL-python)

```
yum install mysql-devel python-devel	#先开发用到的库以及包含文件
yum install gcc							#可选，服务器要安装gcc进行编译
pip install MySQL-python				#安装MySQL-python驱动
```
### MySQL数据库密码安全性设置

MySQL数据库可能因为安全原因拒绝修改默认密码
```mysql
set global validate_password_policy=0;	#修改密码安全性为LOW或者使用更复杂的密码
```
## smartclassroom-flask-server api 使用
---
### 学生登录

请求方式：POST
本地测试请求URL：http://127.0.0.1:5000/api/login
服务器请求URL： http://139.224.232.165/api/login
请求数据格式：json

```json
{
	"stu_id": 2018302110001,	//学号
    "password": "********"		//登录密码
}
```
返回数据格式: json
1.正常返回
```json
{
	"code": 20000,
    "stu_id": 2018302110001,
    "name": "王乐容",			//学生姓名
    "department": "计算机学院"  //学生院系				
}
```
2.异常返回
```json
{
	"code": 40001,
	"text": "学号或密码错误"
}
```
或
```json
{
	"code": 40002,
	"text": "数据格式错误"
}
```
### 获取学生所选课程

请求方式：GET
本地测试请求URL：http://127.0.0.1:5000/api/getcourse
服务器请求URL：http://139.224.232.165/api/getcourse
参数：学号stu_id，如http://139.224.232.165/api/getcourse?stu_id=2018302110001
返回数据格式：json
code状态码，20000代表正常，40001代表无法查询到相关学生信息，40002代表请求数据格式错误，下同
1.正常返回:
```json
{
    "code": 20000,
    "courses":
    [
        {
            "course_id": 1,				//课程id
            "name": "软件工程概论",		//课程名
            "begin_time": "08:00:00",	//课程开始上课时间
            "end_time": "09:35:00"		//课程结束上课时间
        },
        {
            "course_id": 2,
            "name": "软件需求建模",
            "begin_time": "09:50:00",
            "end_time": "11:25:00"
        }
    ]
}
```
2.异常返回
```json
{
	"code": 40001,
	"text": "未查询到相关学生信息"
}
```
或
```json
{
	"code": 40002,
	"text": "数据格式错误"
}
```
### 获取学生所选课程考勤状态

请求方式：GET
本地测试请求URL：http://127.0.0.1:5000/api/getstate
服务器请求URL：http://139.224.232.165/api/getstate
参数：学号stu_id，如http://139.224.232.165/api/getstate?stu_id=2018302110001
返回数据格式：json
code状态码，20000代表正常，40001代表无法查询到相关学生信息，40002代表请求数据格式错误，下同
1.正常返回:
考勤状态state-0：考勤失败 state-1：考勤成功 state-2：上课中 state-3：未到考勤时间

```json
{
    "code": 20000,
    "states":
    [
        {
            "course_id": 1,				//课程id
            "state": 1					//考勤状态state
        },
        {
            "course_id": 2,
            "state": 1
        },
        {
            "course_id": 3,
            "state": 3
        }
    ]
}
```
2.异常返回
```json
{
	"code": 40001,
	"text": "未查询到相关学生信息"
}
```
或
```json
{
	"code": 40002,
	"text": "数据格式错误"
}
```
### 设置学生考勤状态

请求方式：POST
本地测试请求URL：http://127.0.0.1:5000/api/setstate
服务器请求URL： http://139.224.232.165/api/setstate
请求数据格式：json

```json
{
	"stu_id": 2018302110001,
    "begin_time":			//人脸在画面中出现的时间，考勤时长计算开始时刻
    {
        "hour": 10,			//该时刻的时分秒
        "minute": 9,
        "second": 25
    },
    "duration": 60			//人脸在画面中持续出现的时长（秒），每隔60秒刷新一次，最大不超过60
}
```
返回数据格式: json
1.正常返回
```json
{
	"code": 20000				
}
```
2.异常返回
```json
{
	"code": 40001,
	"text": "未查询到相关学生信息"
}
```
或
```json
{
	"code": 40002,
	"text": "数据格式错误"
}
```
## 使用curl模拟GET和POST请求进行测试
---
注意事项：单引号在Linux和Windows的含义不同，curl调用格式也略有差异，Windows下双引号內部使用双引号需要转义，下面将会分别标出Linux和Windows使用的命令

1.GET请求

使用curl发送GET请求的格式为: curl protocol://address:port/url?args
```
curl http://127.0.0.1:5000/api/getcourse?stu_id=2018302110001		#Linux和Windows均可
curl 'http://127.0.0.1:5000/api/getcourse?stu_id=2018302110001'		#Linux下
curl "http://127.0.0.1:5000/api/getcourse?stu_id=2018302110001"		#Linux和Windows均可
```
2.POST请求

Linux:
```
curl -H "Content-Type: application/json" -X POST -d '{"stu_id": 2018302110001, "password": "********"}' http://127.0.0.1:5000/api/login
```
Linux和Windows:
```
curl -H "Content-Type: application/json" -X POST -d "{\"stu_id\": 2018302110001, \"password\": \"********\"}" http://127.0.0.1:5000/api/login
```

Windows可在控制面板->启用或关闭Windows功能中开启`适用于Linux的Windows子系统`功能，在软件商店中下载Ubuntu启用后在命令行使用bash命令