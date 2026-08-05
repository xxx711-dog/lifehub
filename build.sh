#!/usr/bin/env bash
# Render 部署构建脚本

set -o errexit

echo "===== LifeHub 构建开始 ====="

# 1. 安装依赖
pip install -r requirements.txt

# 2. 数据库迁移
echo "--> 执行数据库迁移..."
python manage.py migrate --noinput

# 3. 收集静态文件
echo "--> 收集静态文件..."
python manage.py collectstatic --noinput --clear

# 4. 填充示例数据（仅当 demo 用户不存在时）
echo "--> 检查并填充示例数据..."
python manage.py seed_data

echo "===== 构建完成 ====="
