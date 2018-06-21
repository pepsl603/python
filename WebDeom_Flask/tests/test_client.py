import unittest
from app import create_app, db
from app.models import User, Role
from flask import url_for
import re


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('请点击右上角登录' in response.get_data(as_text=True))

    def test_register_and_login(self):
        # data的字段内容要对上表单上的字段
        response = self.client.post(url_for('auth.register'), data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat',
            'phonenumber': '18685718318'
        })
        self.assertEqual(response.status_code, 302)

        # 用新注册的账号登录测试
        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password': 'cat'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        # print(data)
        self.assertTrue(re.search('你好,\s*john', data))
        self.assertTrue('你还没有验证你的账号' in data)

        user = User.query.filter_by(mail='john@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        # print(data)
        self.assertTrue('你已经成功验证了账号，可正常使用' in data)

        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('你退出了登录' in data)