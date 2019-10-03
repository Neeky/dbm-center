## dbm-center
   **dbm-center 是整个 dbm 的核心，dba 、dev 向 dbm-cneter 提任务，dbm-agent 收到任务后会去执行任务，在任务完成后通知 dbm-center 任务完成(或失败)。**

   ---

## 启动dbm-center
   **1、** dbm-center 是一个由 django 开发的网站，生产环境上我们推荐使用 uwsgi + nginx 的组合来启动 web 服务

   **2、** 开发环境可以直接这样启动
   ```bash
   # 进入到 dbm-center 的项目目录
   cd dbm-center

   # 表定义
   python3 manage.py makemigrations hosts
   Migrations for 'hosts':
     apps/hosts/migrations/0001_initial.py
       - Create model HostModel
       - Create model NetIOCounterModel
       - Create model NetInterfaceModel
       - Create model MemoryDistriModel
       - Create model DiskUsageModel
       - Create model DiskIOCounterModel
       - Create model CpuTimesModel
       - Create model CpuFrequencyModel
    
   # 把表的定义应用到数据库(建库、建表)
   python3 manage.py migrate
   Operations to perform:
     Apply all migrations: admin, auth, contenttypes, hosts, sessions
   Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     Applying admin.0001_initial... OK
     Applying admin.0002_logentry_remove_auto_add... OK
     Applying admin.0003_logentry_add_action_flag_choices... OK
     Applying contenttypes.0002_remove_content_type_name... OK
     Applying auth.0002_alter_permission_name_max_length... OK
     Applying auth.0003_alter_user_email_max_length... OK
     Applying auth.0004_alter_user_username_opts... OK
     Applying auth.0005_alter_user_last_login_null... OK
     Applying auth.0006_require_contenttypes_0002... OK
     Applying auth.0007_alter_validators_add_error_messages... OK
     Applying auth.0008_alter_user_username_max_length... OK
     Applying auth.0009_alter_user_last_name_max_length... OK
     Applying auth.0010_alter_group_name_max_length... OK
     Applying auth.0011_update_proxy_permissions... OK
     Applying hosts.0001_initial... OK
     Applying sessions.0001_initial... OK
   
   # 启动 dbm-center 服务
   python3 manage.py runserver 172.16.192.1:8080

   Performing system checks...
   
   System check identified no issues (0 silenced).
   October 03, 2019 - 21:03:41
   Django version 2.2.6, using settings 'dbmc.settings'
   Starting development server at http://172.16.192.1:8080/
   Quit the server with CONTROL-C.
   ```
   ---

   **启动失败的常见问题**

   **1、** 没有配置好 django 环境

   **2、** 没有配置好 dbm-center 用到的后端 mysql 服务，默认情况下 dbm-center 使用如下方式连接它用的 MySQL 服务器 
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'dbm',
           'HOST': '127.0.0.1',
           'PORT': 3306,
           'USER': 'dbmuser',
           'PASSWORD': 'Dirac' # 他给出的狄拉克方程可以描述费米子的物理行为，解释了粒子的自旋，并且首先预测了反粒子的存在
       }
   }
   ```
   ---


  
