## dbm-center
   **dbm-center 是整个 dbm 的核心，dba 、dev 向 dbm-cneter 提任务，dbm-agent 收到任务后会去执行任务，在任务完成后通知 dbm-center 任务完成(或失败)。**

   ---

## 后台数据库的配置
   **dbm-center 会把用到的信息保存到后台的 mysql 数据库中，后台数据库相关的配置保存在 dbmc/settings.py 文件中**
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
   连接到后台数据库执行如下语句完成用户授权
   ```sql
   create database dbm;

   create user dbmuser@'127.0.0.1' identified by 'Dirac';

   grant all on dbm.* to dbmuser@'127.0.0.1';
   ```
   在数据库中创建对应的表
   ```bash
   python3 manage.py makemigrations
   No changes detected

   python3 manage.py migrate
   Operations to perform:
     Apply all migrations: admin, auth, contenttypes, sessions
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
     Applying sessions.0001_initial... OK
   ```

   ---
  
