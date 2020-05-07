# encoding: utf-8
# _*_ coding: utf-8 _*_
# author: wong
# date: 2019-08-16

from datetime import datetime, time, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

# 建立ORM模型

# 如果多对多联系没有额外属性，使用中间表，否则使用关联对象
# s_c = db.Table('s_c',
#                db.Column('stu_id', db.String(100), db.ForeignKey('student.stu_id'), primary_key=True),
#                db.Column('course_id', db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
#                )

class Student_Course(db.Model):
    __tablename__ = 'student_course'
    stu_id = db.Column(db.String(100), db.ForeignKey('student.stu_id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
    attendance_time = db.Column(db.Integer, nullable=False)
    attendance_state = db.Column(db.Boolean, nullable=False)

    student = db.relationship('Student', back_populates='courses')
    course = db.relationship('Course', back_populates='students')

class Teacher(db.Model):
    __tablename__ = 'teacher'
    tch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    begin_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    tch_id = db.Column(db.Integer, db.ForeignKey('teacher.tch_id'))

    teacher = db.relationship('Teacher', backref=db.backref('courses'))
    students = db.relationship('Student_Course', back_populates='course')

class Student(db.Model):
    __tablename__ = 'student'
    stu_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    courses = db.relationship('Student_Course', back_populates='student')

db.create_all()

# 默认的视图函数，只能采用GET请求，若使用POST请求，请详细说明
# code表示状态码，40001, 40002请求出现异常，20000正常

# POST请求登录
@app.route('/api/login',methods=['POST'])
def login():
    try:
        receivedData = request.get_json()
        stu_id = receivedData['stu_id']
        password = receivedData['password']
    except:
        data = {
            'code': 40002,
            'text': '数据格式错误'
        }
        return jsonify(data)
    else:
        student = Student.query.filter(Student.stu_id == stu_id).first()
        if student == None:
            data = {
                'code': 40001,
                'text': '学号或密码错误'
            }
            return jsonify(data)

        if student.password != password:
            data = {
                'code': 40001,
                'text': '学号或密码错误'
            }
            return jsonify(data)

        studentDepartment = student.department
        studentName = student.name
        data = {
            'code': 20000,
            'stu_id': stu_id,
            'name': studentName,
            'department': studentDepartment
        }
        return jsonify(data)

# GET请求获取课程
@app.route('/api/getcourse', methods=['GET'])
def getcourse():
    id = request.args.get('stu_id')

    if id == None:
        data = {
            'code': 40002,
            'text': '数据格式错误'
        }
        return jsonify(data)

    student = Student.query.filter(Student.stu_id == id).first()

    if student == None:
        data = {
            'code': 40001,
            'text': '未查询到相关学生信息'
        }
        return jsonify(data)

    courses = []
    courseList = []
    scs = student.courses
    for sc in scs:
        courses.append(sc.course)

    for course in courses:
        courseDict = {}
        courseDict['course_id'] = course.course_id
        courseDict['name'] = course.name
        courseDict['begin_time'] = str(course.begin_time)
        delta = timedelta(seconds=course.duration)
        courseDict['end_time'] = str(time_plus(course.begin_time, delta))
        courseList.append(courseDict)

    data = {
        'code': 20000,
        'courses': courseList
    }
    return jsonify(data)

# 使用GET请求获取学生的考勤信息
@app.route('/api/getstate',methods=['GET'])
def getstate():
    now = datetime.now().time()
    id = request.args.get('stu_id')

    if id == None:
        data = {
            'code': 40002,
            'text': '数据格式错误'
        }
        return jsonify(data)

    student = Student.query.filter(Student.stu_id == id).first()
    if student == None:
        data={
            'code': 40001,
            'text': '未查询到相关学生信息'
        }
        return jsonify(data)

    # state-0:考勤失败 state-1:考勤成功 state-2:上课中 state-3:未到考勤时间
    stateList = []
    scs = student.courses
    for sc in scs:
        stateDict = {}
        stateDict['course_id'] = sc.course_id
        delta = timedelta(seconds=sc.course.duration)
        course_begin_time = sc.course.begin_time
        course_end_time = time_plus(course_begin_time, delta)
        if now < course_begin_time:
            stateDict['state'] = 3
        elif now > course_end_time:
            stateDict['state'] = int(sc.attendance_state)
        else:
            if sc.attendance_state:
                stateDict['state'] = 1
            else:
                stateDict['state'] = 2
        stateList.append(stateDict)

    data = {
        'code': 20000,
        'states': stateList
    }
    return jsonify(data)

# POST请求设置学生的考勤信息
@app.route('/api/setstate',methods=['POST'])
def setstate():
    try:
        receivedData = request.get_json()
        id = receivedData['stu_id']
        hour = receivedData['begin_time']['hour']
        minute = receivedData['begin_time']['minute']
        second = receivedData['begin_time']['second']
        duration = receivedData['duration']
        begin_time = time(hour=hour, minute=minute, second=second)
    except:
        data = {
            'code': 40002,
            'text': '数据格式错误'
        }
        return jsonify(data)
    else:
        student = Student.query.filter(Student.stu_id == id).first()
        if student == None:
            data = {
                'code': 40001,
                'text': '未查询到相关学生信息'
            }
            return jsonify(data)

        scs = student.courses
        for sc in scs:
            delta = timedelta(seconds=duration)
            end_time = time_plus(begin_time, delta)
            course_begin_time = sc.course.begin_time
            course_delta = timedelta(seconds=sc.course.duration)
            course_end_time = time_plus(course_begin_time, course_delta)

            # if begin_time > course_begin_time and end_time < course_end_time:
            #     new_attendance_time = sc.attendance_time + duration
            #     sc.attendance_time += duration
            #     # 如果已经是签到成功状态，则不用进行计算
            #     if not sc.attendance_state:
            #         res = new_attendance_time / float(sc.course.duration)
            #         if res > 0.9:
            #             sc.attendance_state = True
            # elif begin_time > course_begin_time and begin_time < course_end_time and end_time > course_end_time:
            #     duration = time_minus(course_end_time, begin_time).seconds
            #     new_attendance_time = sc.attendance_time + duration
            #     sc.attendance_time += duration
            #     # 如果已经是签到成功状态，则不用进行计算
            #     if not sc.attendance_state:
            #         res = new_attendance_time / float(sc.course.duration)
            #         if res > 0.9:
            #             sc.attendance_state = True
            # elif begin_time < course_begin_time and end_time > course_begin_time:
            #     duration = time_minus(end_time, course_begin_time).seconds
            #     new_attendance_time = sc.attendance_time + duration
            #     sc.attendance_time += duration
            #     # 如果已经是签到成功状态，则不用进行计算
            #     if not sc.attendance_state:
            #         res = new_attendance_time / float(sc.course.duration)
            #         if res > 0.9:
            #             sc.attendance_state = True

            if begin_time > course_begin_time:
                if end_time < course_end_time:
                    new_attendance_time = sc.attendance_time + duration
                    sc.attendance_time += duration
                    # 如果已经是签到成功状态，则不用进行计算
                    if not sc.attendance_state:
                        res = new_attendance_time/float(sc.course.duration)
                        if res > 0.9:
                            sc.attendance_state = True
                else:
                    if begin_time < course_end_time:
                        duration = time_minus(course_end_time, begin_time).seconds
                        new_attendance_time = sc.attendance_time + duration
                        sc.attendance_time += duration
                        # 如果已经是签到成功状态，则不用进行计算
                        if not sc.attendance_state:
                            res = new_attendance_time / float(sc.course.duration)
                            if res > 0.9:
                                sc.attendance_state = True
            else:
                if end_time > course_begin_time:
                    duration = time_minus(end_time, course_begin_time).seconds
                    new_attendance_time = sc.attendance_time + duration
                    sc.attendance_time += duration
                    # 如果已经是签到成功状态，则不用进行计算
                    if not sc.attendance_state:
                        res = new_attendance_time / float(sc.course.duration)
                        if res > 0.9:
                            sc.attendance_state = True

        db.session.commit()
        data = {
            'code': 20000
        }
        return jsonify(data)

# 返回值为一个新的时间
def time_plus(time, timedelta):
    start = datetime(2000, 1, 1, hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()

# 返回值为一个timedelta
def time_minus(endtime, begintime):
    end = datetime(2000, 1, 1, hour=endtime.hour, minute=endtime.minute, second=endtime.second)
    start = datetime(2000, 1, 1, hour=begintime.hour, minute=begintime.minute, second=begintime.second)
    delta = end - start
    return delta

if __name__ == '__main__':
    app.run()