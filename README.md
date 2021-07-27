## 安乐窝自动化测试系统

### 说明

基于 django rest framework + HttpRunner 开发

python 3.6 以上。 使用 ldap 认证

### 官方教程

- django:   <https://docs.djangoproject.com/zh-hans/3.2/>
- django drf :  <https://www.django-rest-framework.org/>
- drf中文文档： <https://www.w3cschool.cn/lxraw/lxraw-pdz435oa.html>  


### 目录结构说明

~~~shell
.
├── config.py       # 配置文件
├── hrunmanage
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py        # 基础配置
│   └── wsgi.py
├── manage.py
├── manager
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations          # 数据迁移文件
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   ├── models              # 数据模型
│   │   ├── base.py
│   │   ├── project.py
│   ├── serializers         # 序列化
│   │   ├── project.py
│   │   └── users.py
│   ├── tests.py            # 单元测试
│   └── views               # 视图
│       ├── project.py
│       └── users.py
├── README.md
├── requirements.txt
├── urls            # 路由
│   └── base.py
└── utils           # 公共类
    └── common.py
~~~

### 部署

- 安装依赖

  ~~~shell
  pip install -r requirements.txt
  ~~~
  
- 修改数据库配置（mysql5.7 以上版本）

  ~~~python
  # config.py
  class Config:
      # base
      DEBUG = True    # docker 下运行需要设置为 False
      LEVEL = 'INFO'   # log level
      CACHE = False    # Django 缓存
      ALLOWED_HOSTS = ['*']
  
      # 数据库配置
      DATABASE = {
          'engine': 'mysql',
          'host': '192.168.8.130',
          'port': '3306',
          'user': 'root',
          'password': '123456',
          'dbname': 'hrunmanage'
      }
  ~~~

- 运行

  ~~~shell
  python manage.py runserver 0.0.0.0:8000
  ~~~
