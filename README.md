# Flask Web 团队项目 - 新手友好指南

欢迎来到我们的第一个小组作业！这是一个基于Flask框架的Web应用项目，专门为### 📄 **`app.py` - 应用启动文件**
**这个文件的角色**：像总经理一样，只负责统筹协调，不干具体活

**应该放什么内容**：
- 创建Flask应用的代码
- 加载配置文件的命令
- 连接数据库的初始化
- 注册路由的代码
- 启动应用的命令

**绝对不要放什么**：
- 具体的网页处理逻辑（比如登录验证、数据查询）
- 数据库的增删改查操作
- 表单验证
- 邮件发送等功能性代码

**简单理解**：app.py就像公司的总经理，只管"让各部门开始工作"，不管具体业务细节。开发经验的同学**设计。别担心，我们会从零开始，一步步带你了解Web开发的世界！

## 🤔 什么是Flask？为什么选择它？

### Flask简单来说就是...
想象一下，你要开一家餐厅：
- **Flask就像是厨房** - 它提供了做菜（开发网站）所需的基本工具
- **Python代码就像是菜谱** - 告诉厨房怎么做菜
- **网页就像是端给客人的菜** - 最终用户看到的成果

### 为什么Flask适合新手？
1. **简单易学** - 几行代码就能创建一个网站
2. **功能强大** - 虽然简单，但能做出复杂的网站
3. **社区活跃** - 遇到问题容易找到解决方案
4. **逐步扩展** - 可以从简单开始，慢慢添加功能

## 🌐 Web开发基础知识（5分钟快速了解）

### 网站是怎么工作的？
```
你在浏览器输入网址 → 浏览器发送请求 → 服务器处理请求 → 服务器返回网页 → 你看到网页
```

### 我们的项目中有什么？
- **前端**：用户看到的界面（HTML + CSS + JavaScript）
- **后端**：处理逻辑的程序（Python + Flask）
- **路由**：决定不同网址显示什么内容

## 📁 项目结构详解（每个文件都有什么用？）

```
开放数据/
├── app.py                 # 🏠 Flask应用启动文件
├── requirements.txt       # 📦 需要安装的工具清单
├── .gitignore            # 🚫 告诉Git哪些文件不要管
├── README.md             # 📖 你现在看的说明书
├── config.py             # ⚙️ 配置文件（数据库、密钥等）
├── .github/              # ⚙️ GitHub相关设置
│   └── copilot-instructions.md # 🤖 AI助手的使用说明
├── backend/              # 🔧 后端代码文件夹
│   ├── __init__.py      # 📄 Python包标识文件
│   ├── models.py        # 🗃️ 数据库模型（表结构定义）
│   ├── routes.py        # 🛣️ 路由处理（URL对应的函数）
│   ├── database.py      # 💾 数据库操作函数
│   └── utils.py         # 🔧 工具函数（通用功能）
├── templates/            # 🎨 网页模板文件夹
│   ├── base.html        # 📄 所有页面的基础模板
│   ├── index.html       # 🏠 首页
│   ├── about.html       # ℹ️ 关于我们页面
│   ├── login.html       # 🔐 登录页面
│   ├── register.html    # 📝 注册页面
│   ├── 404.html         # ❌ 页面找不到时显示
│   └── 500.html         # 💥 服务器出错时显示
├── static/              # 🎯 静态文件（不会改变的文件）
│   ├── css/
│   │   └── style.css    # 🎨 网页样式文件
│   ├── js/
│   │   └── main.js      # ⚡ JavaScript功能文件
│   └── images/          # 🖼️ 图片存放处
└── database/            # 💾 数据库文件夹
    └── app.db           # 🗄️ SQLite数据库文件（运行后自动生成）
```

## 🔍 详细的文件内容分工指南

### � **`app.py` - 应用启动文件**
**作用**：只负责启动应用，像总指挥一样协调各个部分
**内容**：应用初始化、配置加载、启动命令
**❌ 不要放**：具体的业务逻辑、数据库操作、页面处理

```python
# ✅ app.py 应该包含的内容
from flask import Flask
from config import Config
from backend.models import db
from backend.routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # 加载配置
    db.init_app(app)               # 初始化数据库
    init_routes(app)               # 加载路由
    return app

# ❌ 不要在 app.py 中写这些
@app.route('/login')  # 路由应该在 routes.py
def login():
    pass

def create_user():    # 数据库操作应该在 database.py
    pass
```

### ⚙️ **`config.py` - 配置文件**
**作用**：存放所有的配置信息，像设置面板一样
**内容**：数据库连接、密钥、上传限制、邮件设置等
**❌ 不要放**：业务逻辑、数据库操作

```python
# ✅ config.py 应该包含的内容
class Config:
    # 安全配置
    SECRET_KEY = 'your-secret-key-here'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'static/uploads'
    
    # 邮件配置
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    
    # 分页配置
    POSTS_PER_PAGE = 10

# ❌ 不要在 config.py 中写这些
def send_email():     # 功能函数应该在 utils.py
    pass

class User:           # 数据模型应该在 models.py
    pass
```

### 🗃️ **`backend/models.py` - 数据库模型**
**作用**：定义数据库表结构，像建筑图纸一样
**内容**：表定义、字段类型、关系定义、数据验证
**❌ 不要放**：数据查询、业务逻辑、页面处理

```python
# ✅ models.py 应该包含的内容
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """用户表 - 存储用户基本信息"""
    __tablename__ = 'users'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系定义
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # 数据转换方法
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }

class Post(db.Model):
    """文章表 - 存储文章内容"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ❌ 不要在 models.py 中写这些
def get_all_users():  # 查询函数应该在 database.py
    pass

@app.route('/users')  # 路由应该在 routes.py
def users():
    pass
```

### 🛣️ **`backend/routes.py` - 路由处理**
**作用**：处理用户请求，像接待员一样
**内容**：URL路由、请求处理、页面跳转、API接口
**❌ 不要放**：数据库操作细节、复杂计算、工具函数

```python
# ✅ routes.py 应该包含的内容
from flask import render_template, request, jsonify, redirect, url_for
from backend.database import *  # 导入数据库操作函数

def init_routes(app):
    
    @app.route('/')
    def index():
        """首页 - 显示最新文章"""
        recent_posts = get_recent_posts(limit=5)  # 调用database.py的函数
        return render_template('index.html', posts=recent_posts)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """登录页面"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # 验证用户（调用database.py的函数）
            user = get_user_by_username(username)
            if user and verify_password(user, password):
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='用户名或密码错误')
        
        return render_template('login.html')
    
    @app.route('/api/users')
    def api_users():
        """API - 获取用户列表"""
        users = get_all_users()  # 调用database.py的函数
        return jsonify({
            'status': 'success',
            'users': [user.to_dict() for user in users]  # 调用models.py的方法
        })

# ❌ 不要在 routes.py 中写这些
def create_user(username, email, password):  # 数据库操作应该在 database.py
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()

def validate_email(email):  # 工具函数应该在 utils.py
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)
```

### 💾 **`backend/database.py` - 数据库操作**
**作用**：专门处理数据的增删改查，像仓库管理员一样
**内容**：查询函数、创建函数、更新函数、删除函数
**❌ 不要放**：页面路由、HTML模板、前端逻辑

```python
# ✅ database.py 应该包含的内容
from backend.models import db, User, Post
from werkzeug.security import generate_password_hash, check_password_hash

# 用户相关操作
def create_user(username, email, password):
    """创建新用户"""
    try:
        # 检查用户是否已存在
        if get_user_by_username(username):
            return {'success': False, 'message': '用户名已存在'}
        
        # 创建用户
        password_hash = generate_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        db.session.add(user)
        db.session.commit()
        return {'success': True, 'user_id': user.id}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}

def get_user_by_username(username):
    """根据用户名查找用户"""
    return User.query.filter_by(username=username).first()

def get_all_users():
    """获取所有用户"""
    return User.query.all()

def verify_password(user, password):
    """验证密码"""
    return check_password_hash(user.password_hash, password)

# 文章相关操作
def create_post(title, content, author_id):
    """创建新文章"""
    try:
        post = Post(title=title, content=content, author_id=author_id)
        db.session.add(post)
        db.session.commit()
        return {'success': True, 'post_id': post.id}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': str(e)}

def get_recent_posts(limit=10):
    """获取最新文章"""
    return Post.query.order_by(Post.created_at.desc()).limit(limit).all()

def get_posts_by_author(author_id):
    """获取指定作者的文章"""
    return Post.query.filter_by(author_id=author_id).all()

# ❌ 不要在 database.py 中写这些
@app.route('/create_user')  # 路由应该在 routes.py
def create_user_page():
    pass

def format_datetime(dt):  # 工具函数应该在 utils.py
    pass
```

### 🔧 **`backend/utils.py` - 工具函数**
**作用**：提供通用的辅助功能，像工具箱一样
**内容**：验证函数、格式化函数、计算函数、辅助类
**❌ 不要放**：数据库操作、路由处理、数据模型

```python
# ✅ utils.py 应该包含的内容
import re
from datetime import datetime

# 验证函数
def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """验证用户名格式"""
    if len(username) < 3 or len(username) > 20:
        return False, "用户名长度应为3-20个字符"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "用户名只能包含字母、数字和下划线"
    return True, "格式正确"

def validate_password(password):
    """验证密码强度"""
    if len(password) < 6:
        return False, "密码至少需要6个字符"
    if not re.search(r'[a-zA-Z]', password):
        return False, "密码需要包含字母"
    if not re.search(r'\d', password):
        return False, "密码需要包含数字"
    return True, "密码强度合格"

# 格式化函数
def format_datetime(dt, format_type='default'):
    """格式化日期时间"""
    formats = {
        'default': '%Y-%m-%d %H:%M:%S',
        'date': '%Y-%m-%d',
        'chinese': '%Y年%m月%d日 %H:%M'
    }
    return dt.strftime(formats.get(format_type, formats['default']))

def truncate_text(text, max_length=100):
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'

def format_file_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

# 辅助类
class ResponseHelper:
    """API响应辅助类"""
    @staticmethod
    def success(data=None, message="操作成功"):
        response = {'status': 'success', 'message': message}
        if data:
            response['data'] = data
        return response
    
    @staticmethod
    def error(message="操作失败"):
        return {'status': 'error', 'message': message}

# ❌ 不要在 utils.py 中写这些
class User(db.Model):  # 数据模型应该在 models.py
    pass

def get_all_users():  # 数据库查询应该在 database.py
    pass

@app.route('/utils')  # 路由应该在 routes.py
def utils_page():
    pass
```

## 🎯 实际开发场景示例

### 场景1：添加用户注册功能

**❓ 需求**：用户可以在网站注册账号

**👥 团队分工**：
1. **数据库同学**：在 `models.py` 中确认User表结构，在 `database.py` 中写 `create_user()` 函数
2. **后端同学**：在 `routes.py` 中写 `/register` 路由
3. **前端同学**：在 `templates/register.html` 中设计注册页面
4. **工具同学**：在 `utils.py` 中写邮箱和密码验证函数

```python
# 数据库同学在 database.py 中写：
def create_user(username, email, password):
    # 创建用户的逻辑

# 后端同学在 routes.py 中写：
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 调用工具函数验证
        # 调用数据库函数创建用户

# 工具同学在 utils.py 中写：
def validate_email(email):
    # 验证邮箱格式

# 前端同学在 templates/register.html 中写：
<form method="POST">
    <!-- 注册表单 -->
</form>
```

### 场景2：显示文章列表

**❓ 需求**：在首页显示最新的文章列表

**👥 团队分工**：
1. **数据库同学**：在 `database.py` 中写 `get_recent_posts()` 函数
2. **后端同学**：在 `routes.py` 中修改首页路由，传递文章数据
3. **前端同学**：在 `templates/index.html` 中显示文章列表
4. **工具同学**：在 `utils.py` 中写时间格式化函数

```python
# 数据库同学在 database.py 中写：
def get_recent_posts(limit=10):
    return Post.query.order_by(Post.created_at.desc()).limit(limit).all()

# 后端同学在 routes.py 中写：
@app.route('/')
def index():
    posts = get_recent_posts(5)  # 获取最新5篇文章
    return render_template('index.html', posts=posts)

# 工具同学在 utils.py 中写：
def format_datetime(dt):
    return dt.strftime('%Y年%m月%d日')

# 前端同学在 templates/index.html 中写：
{% for post in posts %}
    <div class="post">
        <h3>{{ post.title }}</h3>
        <p>{{ post.content[:100] }}...</p>
        <small>{{ post.created_at|format_datetime }}</small>
    </div>
{% endfor %}
```

## 📋 文件内容检查清单

### ✅ 检查你的代码放对地方了吗？

#### 如果你写的是数据库相关：
- [ ] 表结构定义 → `models.py`
- [ ] 数据查询函数 → `database.py`
- [ ] 数据验证 → `utils.py`

#### 如果你写的是页面相关：
- [ ] URL路由 → `routes.py`
- [ ] HTML模板 → `templates/`
- [ ] CSS样式 → `static/css/`
- [ ] JavaScript → `static/js/`

#### 如果你写的是配置相关：
- [ ] 数据库连接 → `config.py`
- [ ] 密钥设置 → `config.py`
- [ ] 上传限制 → `config.py`

#### 如果你写的是通用功能：
- [ ] 验证函数 → `utils.py`
- [ ] 格式化函数 → `utils.py`
- [ ] 辅助类 → `utils.py`

这样分工的好处是：**每个人专注自己的领域，减少代码冲突，提高开发效率！**

## � Flask核心概念（通俗解释）

### 1. 什么是路由（Route）？
路由就像是**网站的目录**：
```python
@app.route('/')          # 访问 localhost:8080/ 时
def index():             # 执行这个函数
    return "欢迎来到首页!" # 显示这些内容
```

### 2. 什么是模板（Template）？
模板就像是**网页的模具**：
- 写一次基础结构（base.html）
- 其他页面继承这个结构
- 只需要填入不同的内容

### 3. 什么是静态文件？
静态文件就是**不会变的资源**：
- CSS文件：控制网页样式（颜色、字体、布局）
- JavaScript文件：添加交互功能（按钮点击、动画）
- 图片文件：网页上的图片

### 4. 什么是数据库？
数据库就像是**网站的记忆**：
- **存储信息**：用户信息、文章内容、评论等
- **快速查找**：可以快速找到需要的数据
- **持久保存**：关闭网站后数据不会丢失
- **SQL语言**：和数据库"对话"的专用语言

#### 为什么需要数据库？
想象一个没有数据库的网站：
- 用户注册后，关闭网站就忘记了用户信息
- 发布的内容无法保存
- 无法记录用户的操作历史

#### SQL是什么？
SQL (Structured Query Language) 就是**和数据库交流的语言**：
```sql
-- 创建用户表
CREATE TABLE users (
    id INTEGER PRIMARY KEY,     -- 用户ID（主键）
    username TEXT NOT NULL,     -- 用户名
    email TEXT NOT NULL,        -- 邮箱
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- 创建时间
);

-- 插入新用户
INSERT INTO users (username, email) VALUES ('张三', 'zhangsan@example.com');

-- 查询所有用户
SELECT * FROM users;

-- 根据用户名查找
SELECT * FROM users WHERE username = '张三';
```

## �🛠️ 安装和运行（跟着做就行！）

### 第一次使用？跟着这些步骤：

#### 步骤1：准备工作
```bash
# 1. 确保你有Python（通常Mac都有）
python3 --version

# 2. 进入项目文件夹
cd 开放数据
```

#### 步骤2：创建虚拟环境（为什么需要？）
虚拟环境就像是**给项目准备一个独立的工作空间**，避免和其他项目冲突。

```bash
# 创建虚拟环境
python3 -m venv .venv

# 激活虚拟环境（每次开发前都要做）
source .venv/bin/activate

# 看到命令行前面有 (.venv) 就说明成功了！
```

#### 步骤3：安装依赖
```bash
# 安装项目需要的工具包
pip install -r requirements.txt
```

#### 步骤4：启动网站
```bash
# 运行Flask应用
python app.py
```

#### 步骤5：访问网站
在浏览器打开：`http://127.0.0.1:8080`

### 看到什么说明成功了？
终端会显示：
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:8080
```

## � 我们的网站有什么功能？

### 页面介绍
- **首页** (`/`) - 项目介绍，有个测试API的按钮
- **关于我们** (`/about`) - 团队信息展示
- **API接口** (`/api/hello`) - 返回JSON数据的接口

### 技术特性
- **响应式设计** - 手机电脑都能正常显示
- **错误处理** - 访问不存在的页面会有友好提示
- **API接口** - 可以为其他程序提供数据

## 👥 团队协作指南（新手版）

### Git是什么？为什么要用它？
Git就像是**代码的时光机器**：
- 记录每次修改的历史
- 多人同时开发不会冲突
- 出错了可以回到之前的版本

### 基本工作流程（按顺序做）：

#### 第一次下载项目：
```bash
# 1. 复制项目到本地
git clone <项目地址>
cd 开放数据

# 2. 查看项目状态
git status
```

#### 日常开发流程：
```bash
# 1. 开始工作前，获取最新代码
git pull

# 2. 创建自己的分支（用你的名字）
git checkout -b 张三-添加登录功能

# 3. 进行开发...
# 修改代码，测试功能

# 4. 保存修改
git add .
git commit -m "添加了用户登录功能"

# 5. 上传到GitHub
git push origin 张三-添加登录功能

# 6. 在GitHub上创建Pull Request请求合并
```

### 团队分工建议：

#### 🎨 前端同学负责：
- 修改HTML模板（templates文件夹）
- 调整CSS样式（static/css/style.css）
- 添加JavaScript交互（static/js/main.js）
- **学习重点**：HTML、CSS、Bootstrap

#### ⚙️ 后端同学负责：
- 编写Python逻辑（app.py）
- 设计API接口
- 处理数据和业务逻辑
- **学习重点**：Python、Flask、数据处理

#### 📊 数据同学负责：
- **设计数据库表结构**
- **编写SQL查询语句**
- **数据的存储和查询逻辑**
- 数据可视化和图表
- 数据分析和统计
- **学习重点**：SQL语法、数据库设计、Flask-SQLAlchemy

#### 🔧 后端数据库同学负责：
- **在Flask中集成数据库**
- **编写数据模型（Model）**
- **实现数据的增删改查API**
- 数据验证和处理
- **学习重点**：Python、Flask、SQLAlchemy、数据库操作

#### 📋 项目管理同学负责：
- 协调开发进度
- 代码审查
- 文档维护
- 测试和bug修复

## 🔧 技术栈详解（都是什么？）

### 后端技术：
- **Python 3.9+** - 编程语言（像说话一样和电脑交流）
- **Flask 3.0** - Web框架（建网站的工具箱）
- **SQLite** - 轻量级数据库（适合学习和小项目）
- **SQL** - 数据库查询语言（和数据库对话的语言）

### 数据库技术：
- **SQLite** - 文件型数据库，无需安装服务器
- **Flask-SQLAlchemy** - Python操作数据库的工具
- **SQL语法** - 增删改查数据的标准语言

### 前端技术：
- **HTML** - 网页结构（像房子的框架）
- **CSS** - 网页样式（像房子的装修）
- **JavaScript** - 网页交互（让网页"活"起来）
- **Bootstrap 5** - UI框架（预制的漂亮组件）

### 开发工具：
- **VS Code** - 代码编辑器（写代码的地方）
- **Git** - 版本控制（代码的时光机器）
- **GitHub** - 代码托管（代码的云端仓库）

## � 学习资源推荐

### Flask学习：
- [Flask官方教程](https://flask.palletsprojects.com/) - 官方文档
- [Flask入门教程](https://tutorial.helloflask.com/) - 中文教程
- YouTube搜索"Flask教程"

### 前端学习：
- [MDN Web文档](https://developer.mozilla.org/) - 权威的Web技术文档
- [Bootstrap官网](https://getbootstrap.com/) - UI框架文档

### Git学习：
- [Git简明指南](https://rogerdudler.github.io/git-guide/index.zh.html)
- [GitHub使用教程](https://guides.github.com/)

### SQL和数据库学习：
- [SQL教程 - 菜鸟教程](https://www.runoob.com/sql/sql-tutorial.html) - 中文SQL基础教程
- [SQLite官方文档](https://www.sqlite.org/) - SQLite数据库官方文档
- [Flask-SQLAlchemy文档](https://flask-sqlalchemy.palletsprojects.com/) - Flask数据库操作
- [DB Browser for SQLite](https://sqlitebrowser.org/) - SQLite可视化工具

## 🐛 常见问题解决

### 问题1：运行时出现"端口被占用"
**解决**：改用其他端口，我们已经设置为8080端口

### 问题2：pip install失败
**解决**：
```bash
# 升级pip
pip install --upgrade pip
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 问题3：页面显示不正常
**解决**：
1. 检查Flask是否正常运行
2. 清除浏览器缓存
3. 检查终端是否有错误信息

### 问题4：Git操作失败
**解决**：
```bash
# 查看Git状态
git status
# 如果有冲突，寻求帮助或重新克隆项目
```

### 问题5：数据库相关错误
**解决**：
```bash
# 检查SQLite是否安装
sqlite3 --version

# 如果Flask-SQLAlchemy报错，重新安装
pip install flask-sqlalchemy

# 数据库文件权限问题
chmod 664 database.db
```

### 问题6：SQL语法错误
**解决**：
1. 检查SQL语句的拼写和语法
2. 确认表名和字段名是否正确
3. 使用DB Browser等工具可视化查看数据库
4. 参考SQL教程确认语法

## 📝 下一步开发计划

我们可以逐步添加这些功能：

### 🥇 初级功能（新手友好）：
- [ ] 添加更多页面
- [ ] 美化界面样式
- [ ] 添加图片和内容
- [ ] **配置SQLite数据库**
- [ ] **创建基础数据表**
- [ ] 简单的表单处理

### 🥈 中级功能（有一定基础后）：
- [ ] **用户注册登录系统**
- [ ] **数据的增删改查操作**
- [ ] 文件上传功能
- [ ] 搜索功能
- [ ] **数据展示和列表页面**

### 🥉 高级功能（熟练后挑战）：
- [ ] **复杂的数据库关系设计**
- [ ] 数据可视化
- [ ] API文档
- [ ] 单元测试
- [ ] 部署到云服务器
- [ ] **数据库性能优化**

## � 给新手的建议

1. **不要害怕出错** - 程序员每天都在调试bug
2. **多问问题** - 团队合作就是要互相帮助
3. **小步快跑** - 每次只改一点点，测试成功再继续
4. **多看文档** - 官方文档是最好的老师
5. **保持耐心** - 编程需要时间，慢慢来

## 📞 需要帮助？

### 团队内部：
- 随时在群里提问
- 可以视频通话一起调试
- 互相review代码

### 外部资源：
- [Stack Overflow](https://stackoverflow.com/) - 程序员的问答社区
- Google搜索错误信息
- Flask官方文档

### 联系信息：
- 项目负责人：35618164
- 邮箱：2300016605@stu.pku.edu.cn

## 📅 开发日志

### 2025年8月6日
- ✅ 项目环境搭建完成
- ✅ Flask应用成功启动
- ✅ 数据库自动创建并初始化
- ✅ 开发环境配置完毕，准备团队协作

---

**记住：每个大神都是从新手开始的！加油！🚀**

*"The best way to learn is by doing!" - 最好的学习方法就是动手实践！*
