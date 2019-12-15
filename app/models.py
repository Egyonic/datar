from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime, date, time, timedelta

# 用来定义组和用户的多对多映射关系的表
user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('groups.id'))
    )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True,index=True)
    email = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(20))

    # 定义组和用户之间的多对多关系
    groups = db.relationship('Group',
                             secondary=user_group,
                             back_populates='members')
    # 定义用户和记录的1对多关系
    records = db.relationship('Record', backref='user')

    def verify_password(self, password):
        return password == self.password

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.name = self.email

    def __repr__(self):
        return '<User %r>' % self.name


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, index=True)
    detail = db.Column(db.Text, default='')

    # 定义组和用户之间的多对多关系
    members = db.relationship('User',
                              secondary=user_group,
                              back_populates='groups')
    # 定义组合任务的一对多关系
    tasks = db.relationship('Task', backref='group')

    def __init__(self, **kwargs):
        super(Group, self).__init__(**kwargs)

    def __repr__(self):
        return '<Group %r>' % self.name


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    # start = db.Column(db.DateTime, default=datetime.now())
    # end = db.Column(db.DateTime)
    # 定义任务所属的分组
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    # def __init__(self, **kwargs):
    #     super(Task, self).__init__(**kwargs)
    #     if(self.start is None):
    #         self.start = datetime.now()
    #     if(self.end is None):
    #         t = datetime(self.start)
    #         days = timedelta(days=3)
    #         self.end = t + days

    def __repr__(self):
        return '<Task %r>' % self.name


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    # 定义用户和记录的1对多关系
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    tid = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    done = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Record id %d>' % self.id

