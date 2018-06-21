from selenium import webdriver
import unittest
from app import create_app, db
from app.models import Role, User, Post
import threading
import time
import re


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        print('setUpClass.....')
        try:
            cls.client = webdriver.Firefox()
            print(cls.client)
        except Exception as ex:
            print(ex)
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # try:
        #     cls.client = webdriver.Chrome(chrome_options=options)
        # except Exception as ex:
        #     print(ex)

        if cls.client:
            print('app init')
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            admin_role = Role.query.filter_by(name='系统管理员').first()
            admin = User(mail='john@example.com', username='john', password='cat',
                         role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # 在一个线程中启动Flask服务器
            cls.server_thread = threading.Thread(target=cls.app.run, kwargs={'debug': False})
            cls.server_thread.start()

            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass......')
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            db.session.remove()
            db.drop_all()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('请点击右上角登录', self.client.page_source))

        self.client.find_element_by_link_text('请登录').click()
        self.assertTrue('<h1>登录</h1>' in self.client.page_source)

        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue('欢迎登录H2D官方网站' in self.client.page_source)

        time.sleep(2)

        self.client.find_element_by_link_text('首页').click()
        self.assertTrue('<h1>你好 john</h1>' in self.client.page_source)
        time.sleep(1)

        # 发帖
        self.client.find_element_by_name('body').send_keys('演员，火速来请我吃虾子！！！<br>陈二，速度来！！！')
        time.sleep(1)
        self.client.find_element_by_name('submit').click()
        time.sleep(1.5)

        self.client.find_element_by_link_text('测试').click()
        self.assertTrue('<h1>Hello,test from base</h1>' in self.client.page_source)
        time.sleep(1.5)

        self.client.find_element_by_link_text('用户').click()
        self.assertTrue('<h1>john</h1>' in self.client.page_source)
        time.sleep(2)
