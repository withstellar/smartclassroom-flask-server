# encoding: utf-8
# _*_ coding: utf-8 _*_
# author: wong
# date: 2019-08-16

from datetime import time
from flask_script import Manager
from app import app, Teacher, Course, Student, Student_Course, db
import xlrd

manager = Manager(app)

# 将表格中的学生信息加载到数据库中
@manager.command
def initserver():
    teacherData = xlrd.open_workbook('teacherList.xlsx')
    table = teacherData.sheets()[0]
    teacherName = table.col_values(0)

    for i in range(1, table.nrows):
        teacher = Teacher(name = teacherName[i])
        db.session.add(teacher)

    courseData = xlrd.open_workbook('courseList.xlsx')
    table = courseData.sheets()[0]
    courseName = table.col_values(0)
    beginTime = table.col_values(1)
    duration = table.col_values(2)
    tchId = table.col_values(3)

    for i in range(1, table.nrows):
        timeRes = beginTime[i].split(',')
        course = Course(name=courseName[i], begin_time=time(hour=int(timeRes[0]), minute=int(timeRes[1]), second=int(timeRes[2])), duration=int(duration[i]), tch_id=tchId[i])
        db.session.add(course)

    studentData = xlrd.open_workbook('studentList.xlsx')
    table = studentData.sheets()[0]
    stuId = table.col_values(0)
    studentName = table.col_values(1)
    studentDepartment = table.col_values(2)

    for i in range(1, table.nrows):
        student = Student(stu_id=stuId[i], name=studentName[i], department=studentDepartment[i], password='smartclassroom')
        db.session.add(student)

    scData = xlrd.open_workbook('student_courseList.xlsx')
    table = scData.sheets()[0]
    stuId = table.col_values(0)
    courseId = table.col_values(1)

    for i in range(1, table.nrows):
        sc = Student_Course(stu_id=stuId[i], course_id=courseId[i], attendance_time=0, attendance_state=False)
        db.session.add(sc)

    db.session.commit()

    print("init successfully")

# 将选课表中所有选课记录的考勤时间和状态置为0
@manager.command
def resetdata():
    scs = Student_Course.query.filter(Student_Course.attendance_time != 0)
    for sc in scs:
        sc.attendance_time = 0
        sc.attendance_state = False
    db.session.commit()

    print("reset successfully")


if __name__ == '__main__':
    manager.run()