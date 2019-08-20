"""
    Created by TinsFox on 2019-08-21.
"""
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.classroom import Room
from app.libs.helper import randomID
__author__ = 'TinsFox'

api = Redprint('room')


@api.route('/room')
def room():
    return "room"


@api.route('/initroom')
def initroom():
    initdata = [
        {"bNum": "A1"}, {"lBum": [1, 2, 3, 4]}, {"rNum": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    ]
    classroomid = randomID()
    for i in initdata:
        print(i)
    print(initdata)
    return Success()


