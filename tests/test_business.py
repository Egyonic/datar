import unittest
import logging
from app import create_app, db
from app.models import User, Group, Task, Record

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelTestCase(unittest.TestCase):
    # def setUp(self):
    #     self.app = create_app('testing')
    #     self.app_context = self.app.app_context()
    #     self.app_context.push()
    #     db.create_all()

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.app_context.pop()

    def test_0_init(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_1_add_users(self):
        print('------ add users ----------')
        names = ['bob', 'mike', 'tom']
        users = []
        for name in names:
            u = User(name=name, email=f'{name}@exp.com')
            users.append(u)
            db.session.add(u)
        db.session.commit()
        print(User.query.all())
        # logger.info(User.query.all())


    def test_2_add_groups(self):
        print('\n------ add groups ----------')
        names = ['math', 'english', 'history']
        groups = []
        for name in names:
            group = Group(name=name)
            groups.append(group)
            db.session.add(group)
        db.session.commit()
        print(Group.query.all())

    def test_3_add_tasks(self):
        print('\n------ add task ----------')
        names = ['homework1', 'experiment1', 'experiment2']
        names2 = ['homework2', 'exp3']
        tasks = []
        groups = Group.query.all()
        for name in names:
            task = Task(name=name, group_id=groups[0].id)
            tasks.append(task)
            db.session.add(task)
        for name in names2:
            task = Task(name=name, group_id=groups[1].id)
            tasks.append(task)
            db.session.add(task)
        db.session.commit()
        Task.query.all()
        print(Task.query.all())

    # 测试给用户添加从属的组，用户与组的多对多关系
    def test_4_add_group_for_user(self):
        print('\n------ add group for user --------')
        users = User.query.all()
        groups = Group.query.all()

        users[0].groups += groups
        users[1].groups += groups[0:2]
        users[2].groups.append(groups[0])
        print('user {} is in groups:'.format(users[0].name))
        print(users[0].groups)
        print('user {} is in groups:'.format(users[1].name))
        print(users[1].groups)
        print('user {} is in groups:'.format(users[1].name))
        print(users[2].groups)
        print('------')
        print(f'{groups[0].name} has members:')
        print(groups[0].members)
        print(f'{groups[1].name} has members:')
        print(groups[1].members)


    def test_5_add_record_for_user(self):
        print('\n------ add record for user --------')
        users = User.query.all()
        tasks = Task.query.all()
        u1 = users[0]
        for task in tasks:
            record = Record(uid=u1.id, tid=task.id, done=True)
            db.session.add(record)
        db.session.commit()
        print(f'user {u1.name} has records:')
        print(u1.records)

