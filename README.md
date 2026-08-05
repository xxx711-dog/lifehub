# LifeHub - 个人生活工作台

> 一站式管理你的衣食住行，让生活更有条理。

## 项目简介

LifeHub 是一个个人生活工作台应用，将日常生活的四个维度——**衣、食、住、行**——整合在统一平台上，提供数据管理和智能辅助决策。

## 功能模块

### 衣 - 衣橱管理
- 衣物管理：按类别（上装/下装/外套/鞋类/配饰）、季节、颜色、品牌分类管理
- 穿搭日记：记录每日穿搭、场合、天气、心情
- 智能推荐：根据温度和场合推荐搭配组合

### 食 - 饮食管理
- 菜谱库：分类、菜系、难度、烹饪时间、预算、食材步骤
- 每日餐食记录：早中晚餐 + 加餐，记录热量和花费
- 购物清单：管理购物项，支持已购标记和价格追踪
- 智能推荐：根据饮食偏好和过敏食材推荐菜谱

### 住 - 家居生活
- 记账：日常开销分类记录，月度消费统计与分类图表
- 家务待办：周期性家务提醒（每天/每周/每月），到期提醒
- 家居库存：消耗品管理，低库存预警，过期提醒

### 行 - 出行管理
- 行程规划：旅行/出差计划，含时间线事件和打包清单
- 通勤记录：每日出行方式、时间、花费追踪
- 通勤统计：周/月通勤数据汇总

### Dashboard 仪表盘
- 四模块数据聚合概览
- 今日穿搭、今日餐食、本月支出、即将出行一目了然

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 6.0 + Django REST Framework 3.17 |
| 认证 | JWT (SimpleJWT) |
| 数据库 | SQLite |
| 前端 | 原生 HTML/CSS/JS 单页应用 |
| 样式 | 响应式设计，移动端友好 |

## 快速开始

### 1. 安装依赖

```bash
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```

### 2. 数据库迁移

```bash
python manage.py migrate
```

### 3. 填充示例数据

```bash
python manage.py seed_data
```

这会创建演示用户和四个模块的完整示例数据。

### 4. 启动服务器

```bash
python manage.py runserver
```

### 5. 访问应用

- 工作台首页: http://127.0.0.1:8000/
- 管理后台: http://127.0.0.1:8000/admin/
- API 根目录: http://127.0.0.1:8000/api/

### 演示账号

| 用户名 | 密码 |
|--------|------|
| demo | demo123456 |

## API 接口

### 认证
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register/ | 注册 |
| POST | /api/auth/login/ | 登录 |
| POST | /api/auth/refresh/ | 刷新 Token |
| GET/PUT | /api/profile/ | 用户档案 |
| GET | /api/dashboard/ | 仪表盘聚合 |

### 衣
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | /api/wardrobe/clothes/ | 衣物列表/创建 |
| GET/PUT/DELETE | /api/wardrobe/clothes/:id/ | 衣物详情 |
| GET/POST | /api/wardrobe/outfits/ | 穿搭日记 |
| GET | /api/wardrobe/suggest/ | 穿搭推荐 |

### 食
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | /api/food/recipes/ | 菜谱列表/创建 |
| GET/POST | /api/food/meals/ | 餐食记录 |
| GET/POST | /api/food/shopping/ | 购物清单 |
| GET | /api/food/suggest/ | 菜谱推荐 |

### 住
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | /api/home/expenses/ | 记账 |
| GET | /api/home/expenses/summary/ | 消费统计 |
| GET/POST | /api/home/tasks/ | 家务待办 |
| GET/POST | /api/home/inventory/ | 库存管理 |

### 行
| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | /api/travel/trips/ | 行程 |
| GET/POST | /api/travel/trips/:id/events/ | 行程事件 |
| GET/POST | /api/travel/trips/:id/packing/ | 打包清单 |
| GET/POST | /api/travel/commute/ | 通勤记录 |
| GET | /api/travel/commute/summary/ | 通勤统计 |

## 项目结构

```
lifehub/
|-- lifehub/           # Django 项目配置
|   |-- settings.py    # 配置文件
|   |-- urls.py        # URL 路由
|-- accounts/          # 用户认证 + 仪表盘
|   |-- models.py      # UserProfile
|   |-- views.py       # 注册/档案/Dashboard
|   |-- management/
|       |-- commands/
|           |-- seed_data.py  # 种子数据
|-- wardrobe/          # 衣 - 衣橱管理
|-- food/              # 食 - 饮食管理
|-- home/              # 住 - 家居生活
|-- travel/            # 行 - 出行管理
|-- frontend/          # 前端单页应用
|   |-- index.html
|-- manage.py
|-- db.sqlite3
|-- README.md
```
