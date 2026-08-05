# LifeHub 线上部署指南

> 推荐使用 **Render**（免费套餐，支持 HTTPS，无需信用卡）

## 快速部署（5 分钟）

### 方案 A：Render 自动部署（推荐）

1. **Fork 或下载项目**
   - 将 `lifehub.zip` 解压到本地文件夹
   - 将代码推送到 GitHub/GitLab 仓库

2. **注册 Render**
   - 访问 https://render.com 用 GitHub 账号登录

3. **创建 Web Service**
   - 点击 **New > Web Service**
   - 选择你的 GitHub 仓库
   - 配置如下：
     - **Name**: `lifehub`
     - **Runtime**: `Python 3`
     - **Build Command**: `bash build.sh`
     - **Start Command**: `gunicorn lifehub.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 60`
     - **Plan**: `Free`（免费）

4. **添加环境变量**
   - 在 Environment 标签页添加：
     - `DJANGO_SECRET_KEY` → 点击 Generate 自动生成
     - `DJANGO_DEBUG` → `False`
     - `DJANGO_ALLOWED_HOSTS` → `你的域名.onrender.com`（例如 `lifehub-xxx.onrender.com`）
     - `RENDER` → `true`

5. **添加磁盘（存储上传的图片）**
   - 在 Disks 标签页点击 **Add Disk**
   - **Name**: `media-storage`
   - **Mount Path**: `/opt/render/project/src/media`
   - **Size**: `1 GB`（免费额度）

6. **部署完成**
   - 点击 Deploy，等待 2-3 分钟
   - 访问分配的 URL（如 `https://lifehub-xxx.onrender.com`）
   - 使用 demo 账号登录：`demo` / `demo123456`

---

### 方案 B：本地 zip 上传部署

如果你不想用 GitHub，可以直接上传 zip：

1. 在 Render 创建 Web Service 时选择 **Upload** 而非 GitHub
2. 上传 `lifehub.zip` 文件
3. 按照方案 A 的第 3-6 步配置

---

## 方案 C：其他平台

### PythonAnywhere（免费，长期在线）

1. 注册 https://www.pythonanywhere.com（免费版永久在线）
2. 上传 zip 文件并解压到 `~/lifehub/`
3. 创建 virtualenv 并安装依赖：`pip install -r requirements.txt`
4. 在 Web 标签页：
   - 配置 WSGI 文件指向 `/home/你的用户名/lifehub/lifehub/wsgi.py`
   - 设置 static files：`/static/` → `/home/你的用户名/lifehub/staticfiles/`
   - 设置 media files：`/media/` → `/home/你的用户名/lifehub/media/`
5. 在 Bash console 中执行：
   ```bash
   cd ~/lifehub
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py seed_data
   ```
6. Reload 网站即可访问

### Railway（免费额度 $5/月）

1. 访问 https://railway.app 用 GitHub 登录
2. New Project > Deploy from GitHub repo
3. 选择仓库，Railway 自动检测 Python 并部署
4. 添加环境变量（同 Render）
5. 自动生成 HTTPS 域名

---

## 重要配置说明

### 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `DJANGO_SECRET_KEY` | Django 密钥（必须保密） | 自动生成的长字符串 |
| `DJANGO_DEBUG` | 调试模式 | `False`（生产环境） |
| `DJANGO_ALLOWED_HOSTS` | 允许的域名 | `lifehub-xxx.onrender.com` |
| `RENDER` | Render 平台标识 | `true` |

### 免费套餐限制

| 平台 | 休眠 | 带宽 | 磁盘 |
|------|------|------|------|
| Render | 15 分钟无访问休眠 | 100GB/月 | 1GB |
| PythonAnywhere | 无休眠 | 低（个人项目够用） | 512MB |
| Railway | 无休眠 | 按需计费 | 按需 |

**注意**：Render 免费版在 15 分钟无访问后会休眠，首次访问需等待 30-60 秒唤醒。如果希望 7×24 在线，可以考虑 PythonAnywhere 免费版或 Railway 付费版。

---

## 部署后验证

访问部署的 URL 后，按顺序验证：

1. **登录页显示正常**：多巴胺风格、登录表单可交互
2. **登录成功**：`demo` / `demo123456`
3. **仪表盘数据加载**：显示衣物、菜谱、记账、行程统计
4. **四模块功能**：衣/食/住/行各模块能正常打开
5. **添加数据**：在任一模块创建新记录，确认能保存

---

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 页面空白 | WhiteNoise 静态文件未收集 | 在 Render Dashboard 点击 Manual Deploy > Deploy Latest Commit |
| 500 错误 | 数据库未迁移 | 在 Render Shell 执行 `python manage.py migrate` |
| 图片上传失败 | media 目录不存在 | 确认 Disk 已挂载到 `/opt/render/project/src/media` |
| 登录 403 | ALLOWED_HOSTS 不匹配 | 更新环境变量为实际域名 |

---

## 技术栈

- **后端**: Django 6.0 + DRF + SimpleJWT + SQLite
- **前端**: 原生 HTML/CSS/JS SPA（多巴胺风格）
- **静态文件**: WhiteNoise
- **WSGI**: Gunicorn
- **部署平台**: Render（推荐）/ PythonAnywhere / Railway

---

## 联系方式

部署遇到问题？检查 Render 的 **Logs** 标签页查看详细错误信息。
