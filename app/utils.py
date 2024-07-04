# app/utils.py
def is_teacher(user):
    return user.is_teacher

def is_student(user):
    return user.is_student

def is_admin(user):
    return user.is_superuser