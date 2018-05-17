from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


# 让模板文件中也可也访问，不用每个地方都传参数
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


