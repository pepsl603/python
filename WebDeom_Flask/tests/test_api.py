import unittest
from app import create_app, db
from base64 import b64encode
from app.models import User, Role, Post, Comment
from flask import url_for
import re
import json


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization':
                'Basic ' + b64encode(
                    (username + ':' + password).encode('utf-8')
                ).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        response = self.client.get(url_for('api.get_posts'), content_type='application/json')
        self.assertTrue(response.status_code == 401)

    def test_posts(self):
        # 添加一个用户
        r = Role.query.filter_by(name='普通用户').first()
        self.assertIsNotNone(r)
        u = User(mail='john@example', password='cat', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        response = self.client.post(
            url_for('api.new_post'),
            headers=self.get_api_headers('john@example', 'cat'),
            data=json.dumps({'body': 'I have a *new* idea.'})
        )
        # print(response.headers)
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # 获取刚刚发表的文章
        response = self.client.get(url,
                                   headers=self.get_api_headers('john@example', 'cat'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response['body'] == 'I have a *new* idea.')
        # print(json_response['body_html'])
        self.assertTrue(json_response['body_html'] == '<p>I have a <em>new</em> idea.</p>')


