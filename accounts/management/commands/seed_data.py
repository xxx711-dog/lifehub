"""填充 LifeHub 示例数据

用法: python manage.py seed_data
会创建演示用户 demo / demo123456 并填充四个模块的示例数据
"""

from datetime import date, timedelta
from decimal import Decimal
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from accounts.models import UserProfile
from wardrobe.models import Clothing, OutfitLog
from food.models import Recipe, MealLog, ShoppingItem
from home.models import Expense, HouseTask, HomeInventory
from travel.models import Trip, TripEvent, CommuteLog, PackingItem


class Command(BaseCommand):
    help = "填充 LifeHub 示例数据"

    def handle(self, *args, **options):
        # 创建演示用户
        user, created = User.objects.get_or_create(
            username="demo", defaults={"email": "demo@lifehub.com"}
        )
        if created:
            user.set_password("demo123456")
            user.save()
            self.stdout.write(self.style.SUCCESS("创建演示用户: demo / demo123456"))
        else:
            self.stdout.write(self.style.WARNING("用户 demo 已存在，跳过创建"))

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.nickname = "生活家"
        profile.city = "北京"
        profile.bio = "认真生活的人"
        profile.height = 175
        profile.weight = 68
        profile.diet_preference = "无限制"
        profile.monthly_budget = Decimal("8000")
        profile.commute_mode = "地铁"
        profile.commute_minutes = 40
        profile.save()

        self._seed_wardrobe(user)
        self._seed_food(user)
        self._seed_home(user)
        self._seed_travel(user)

        self.stdout.write(self.style.SUCCESS("=== 示例数据填充完成 ==="))

    def _seed_wardrobe(self, user):
        """衣 - 示例衣物"""
        if Clothing.objects.filter(user=user).exists():
            return

        clothes_data = [
            ("白色T恤", "top", "白色", "优衣库", "summer", 79),
            ("黑色衬衫", "top", "黑色", "ZARA", "all", 199),
            ("灰色卫衣", "top", "灰色", "Nike", "spring", 399),
            ("蓝色牛仔裤", "bottom", "蓝色", "Levis", "all", 499),
            ("黑色休闲裤", "bottom", "黑色", "优衣库", "all", 199),
            ("卡其色工装裤", "bottom", "卡其色", "GU", "autumn", 159),
            ("黑色羽绒服", "outer", "黑色", "波司登", "winter", 899),
            ("牛仔外套", "outer", "蓝色", "ZARA", "spring", 399),
            ("风衣", "outer", "卡其色", "优衣库", "autumn", 599),
            ("白色运动鞋", "shoes", "白色", "Nike", "all", 699),
            ("黑色皮鞋", "shoes", "黑色", "ECCO", "all", 1299),
            ("帆布鞋", "shoes", "白色", "Vans", "summer", 459),
            ("棒球帽", "accessory", "黑色", "New Era", "summer", 199),
            ("皮带", "accessory", "棕色", "金利来", "all", 299),
            ("围巾", "accessory", "灰色", "优衣库", "winter", 149),
        ]

        for name, cat, color, brand, season, price in clothes_data:
            Clothing.objects.create(
                user=user,
                name=name,
                category=cat,
                color=color,
                brand=brand,
                season=season,
                price=Decimal(str(price)),
                wear_count=random.randint(0, 20),
                is_favorite=random.choice([True, False, False]),
            )

        self.stdout.write(f"  衣: 创建 {len(clothes_data)} 件衣物")

    def _seed_food(self, user):
        """食 - 示例菜谱"""
        if Recipe.objects.filter(user=user).exists():
            return

        recipes_data = [
            (
                "番茄炒蛋",
                "家常菜",
                "",
                1,
                15,
                2,
                200,
                Decimal("8"),
                "鸡蛋 3个\n番茄 2个\n葱花 适量\n盐 1勺\n糖 1勺\n食用油 2勺",
                "鸡蛋打散加盐搅匀\n番茄切块\n热油炒蛋盛出\n锅中放番茄炒出汁\n加糖盐调味\n倒回鸡蛋翻炒均匀\n撒葱花出锅",
                "快手,家常,下饭",
            ),
            (
                "红烧肉",
                "家常菜",
                "本帮",
                3,
                60,
                4,
                450,
                Decimal("25"),
                "五花肉 500g\n冰糖 30g\n生抽 2勺\n老抽 1勺\n料酒 2勺\n八角 2个\n桂皮 1小块\n姜片 3片",
                "五花肉切块冷水下锅焯水\n捞出洗净沥干\n锅中放冰糖小火炒糖色\n放入肉块翻炒上色\n加料酒生抽老抽\n加开水没过肉\n放八角桂皮姜片\n大火烧开转小火炖40分钟\n大火收汁即可",
                "硬菜,下饭,待客",
            ),
            (
                "蒜蓉西兰花",
                "家常菜",
                "",
                1,
                10,
                2,
                80,
                Decimal("6"),
                "西兰花 1棵\n大蒜 4瓣\n盐 1勺\n食用油 1勺",
                "西兰花掰小朵洗净\n大蒜切末\n水开焯西兰花1分钟\n热油爆香蒜末\n放入西兰花翻炒\n加盐调味即可",
                "快手,健康,素菜",
            ),
            (
                "葱油拌面",
                "主食",
                "上海",
                1,
                15,
                1,
                350,
                Decimal("5"),
                "面条 200g\n小葱 4根\n生抽 2勺\n老抽 1勺\n白糖 1勺\n食用油 3勺",
                "小葱切段\n锅中多放油小火煎葱至焦黄\n捞出葱段\n油中加生抽老抽白糖煮开\n另起锅煮面\n面熟捞出淋上葱油汁拌匀",
                "快手,主食,一人食",
            ),
            (
                "酸辣土豆丝",
                "家常菜",
                "川菜",
                2,
                20,
                2,
                150,
                Decimal("5"),
                "土豆 2个\n干辣椒 3个\n花椒 10粒\n蒜末 适量\n白醋 1勺\n盐 1勺\n葱花 适量",
                "土豆去皮切细丝\n清水浸泡去淀粉\n沥干水分\n热油爆香干辣椒花椒蒜末\n放入土豆丝大火翻炒\n淋白醋加盐调味\n撒葱花出锅",
                "下饭,快手,素菜",
            ),
            (
                "可乐鸡翅",
                "家常菜",
                "",
                2,
                30,
                3,
                380,
                Decimal("18"),
                "鸡翅中 10个\n可乐 1罐\n生抽 2勺\n老抽 1勺\n姜片 3片\n料酒 1勺",
                "鸡翅两面划口\n冷水下锅加料酒姜片焯水\n捞出洗净\n锅中少油煎鸡翅至两面金黄\n倒入可乐没过鸡翅\n加生抽老抽\n大火烧开转小火炖15分钟\n大火收汁",
                "待客,下饭,甜口",
            ),
            (
                "紫菜蛋花汤",
                "汤品",
                "",
                1,
                10,
                3,
                60,
                Decimal("4"),
                "紫菜 1小把\n鸡蛋 2个\n盐 1勺\n香油 几滴\n葱花 适量",
                "紫菜撕碎\n鸡蛋打散\n水烧开放入紫菜\n淋入蛋液\n加盐调味\n滴香油撒葱花",
                "快手,汤品,素菜",
            ),
            (
                "黄瓜拌木耳",
                "凉菜",
                "",
                1,
                15,
                3,
                50,
                Decimal("5"),
                "黄瓜 1根\n木耳 10朵\n蒜末 适量\n生抽 1勺\n醋 1勺\n辣椒油 1勺\n白糖 半勺\n盐 适量",
                "木耳提前泡发洗净\n水开焯木耳2分钟捞出\n黄瓜拍碎切段\n蒜末生抽醋辣椒油白糖盐调汁\n淋在黄瓜木耳上拌匀",
                "凉菜,快手,素菜",
            ),
            (
                "蛋炒饭",
                "主食",
                "",
                1,
                10,
                1,
                400,
                Decimal("5"),
                "剩米饭 1碗\n鸡蛋 2个\n葱花 适量\n火腿肠 1根\n盐 1勺\n生抽 1勺\n食用油 2勺",
                "鸡蛋打散\n火腿肠切丁\n热油炒蛋盛出\n锅中放油炒火腿\n倒入米饭炒散\n加鸡蛋翻炒\n加盐生抽调味\n撒葱花",
                "快手,主食,一人食",
            ),
            (
                "糖醋排骨",
                "家常菜",
                "江浙",
                3,
                45,
                3,
                420,
                Decimal("30"),
                "排骨 500g\n冰糖 40g\n醋 3勺\n生抽 2勺\n料酒 2勺\n姜片 3片\n白芝麻 适量",
                "排骨冷水下锅焯水洗净\n锅中放冰糖炒糖色\n放入排骨翻炒上色\n加料酒生抽醋\n加开水没过排骨\n大火烧开转小火炖30分钟\n大火收汁撒芝麻",
                "硬菜,待客,下饭",
            ),
        ]

        for data in recipes_data:
            Recipe.objects.create(
                user=user,
                title=data[0],
                category=data[1],
                cuisine=data[2],
                difficulty=data[3],
                cook_time=data[4],
                servings=data[5],
                calories=data[6],
                budget=data[7],
                ingredients=data[8],
                steps=data[9],
                tags=data[10],
                is_public=True,
            )

        # 今日餐食记录
        today = date.today()
        MealLog.objects.create(
            user=user,
            date=today,
            meal_type="breakfast",
            custom_food="豆浆+包子",
            calories=350,
            cost=Decimal("8"),
        )
        MealLog.objects.create(
            user=user,
            date=today,
            meal_type="lunch",
            custom_food="番茄炒蛋+米饭",
            calories=550,
            cost=Decimal("15"),
        )

        # 购物清单
        shopping_data = [
            ("鸡蛋", "30个", "蛋类", Decimal("25"), False),
            ("番茄", "1斤", "蔬菜", Decimal("5"), False),
            ("五花肉", "500g", "肉类", Decimal("25"), True),
            ("牛奶", "2盒", "乳制品", Decimal("15"), False),
            ("大米", "5斤", "主食", Decimal("30"), False),
        ]
        for name, qty, cat, price, done in shopping_data:
            ShoppingItem.objects.create(
                user=user,
                name=name,
                quantity=qty,
                category=cat,
                estimated_price=price,
                is_purchased=done,
                store="盒马鲜生" if not done else "美团买菜",
            )

        self.stdout.write(
            f"  食: 创建 {len(recipes_data)} 道菜谱 + 餐食记录 + 购物清单"
        )

    def _seed_home(self, user):
        """住 - 示例记账 + 家务 + 库存"""
        if Expense.objects.filter(user=user).exists():
            return

        today = date.today()
        expenses_data = [
            (
                today - timedelta(days=0),
                Decimal("32"),
                "food",
                "午餐外卖",
                "美团",
                "微信",
            ),
            (
                today - timedelta(days=0),
                Decimal("15"),
                "transport",
                "地铁通勤",
                "",
                "支付宝",
            ),
            (
                today - timedelta(days=1),
                Decimal("68"),
                "shopping",
                "超市采购",
                "盒马",
                "微信",
            ),
            (
                today - timedelta(days=1),
                Decimal("45"),
                "food",
                "晚餐",
                "楼下餐馆",
                "支付宝",
            ),
            (
                today - timedelta(days=2),
                Decimal("120"),
                "utility",
                "水电费",
                "物业",
                "银行卡",
            ),
            (today - timedelta(days=2), Decimal("25"), "food", "早餐+午餐", "", "微信"),
            (
                today - timedelta(days=3),
                Decimal("199"),
                "entertainment",
                "电影票+爆米花",
                "万达影城",
                "支付宝",
            ),
            (
                today - timedelta(days=3),
                Decimal("35"),
                "transport",
                "打车",
                "滴滴",
                "支付宝",
            ),
            (
                today - timedelta(days=4),
                Decimal("56"),
                "shopping",
                "洗衣液+纸巾",
                "京东",
                "微信",
            ),
            (
                today - timedelta(days=5),
                Decimal("3000"),
                "rent",
                "月租",
                "房东",
                "银行卡",
            ),
            (
                today - timedelta(days=5),
                Decimal("18"),
                "food",
                "早餐",
                "便利店",
                "微信",
            ),
            (
                today - timedelta(days=6),
                Decimal("88"),
                "medical",
                "感冒药",
                "药店",
                "支付宝",
            ),
            (today - timedelta(days=7), Decimal("42"), "food", "午餐+晚餐", "", "微信"),
        ]

        for exp_date, amount, cat, title, store, pay in expenses_data:
            Expense.objects.create(
                user=user,
                date=exp_date,
                amount=amount,
                category=cat,
                title=title,
                store=store,
                payment_method=pay,
            )

        # 家务待办
        tasks_data = [
            ("倒垃圾", True, "每天", 1, today, 1),
            ("拖地", True, "每周", 7, today + timedelta(days=2), 2),
            ("洗床单", True, "每两周", 14, today + timedelta(days=5), 2),
            ("清理冰箱", True, "每月", 30, today + timedelta(days=10), 3),
            ("换牙刷", True, "每三个月", 90, today + timedelta(days=30), 3),
            ("整理衣柜", False, "", None, today, 2),
        ]
        for title, recurring, freq, interval, due, priority in tasks_data:
            HouseTask.objects.create(
                user=user,
                title=title,
                is_recurring=recurring,
                frequency=freq,
                interval_days=interval,
                next_due_date=due,
                priority=priority,
            )

        # 家居库存
        inventory_data = [
            ("抽纸", "日用品", 3, "包", 1, "客厅柜"),
            ("卷纸", "日用品", 6, "卷", 2, "卫生间"),
            ("洗衣液", "清洁", 1, "瓶", 1, "阳台"),
            ("洗洁精", "清洁", 0.5, "瓶", 0.3, "厨房"),
            ("大米", "食品", 5, "kg", 2, "厨房"),
            ("食用油", "食品", 1.5, "L", 0.5, "厨房"),
            ("盐", "调味品", 1, "包", 0.2, "厨房"),
            ("生抽", "调味品", 0.8, "瓶", 0.3, "厨房"),
        ]
        for name, cat, qty, unit, min_qty, loc in inventory_data:
            HomeInventory.objects.create(
                user=user,
                name=name,
                category=cat,
                quantity=Decimal(str(qty)),
                unit=unit,
                min_quantity=Decimal(str(min_qty)),
                location=loc,
            )

        self.stdout.write(
            f"  住: 创建 {len(expenses_data)} 条记账 + {len(tasks_data)} 个家务 + {len(inventory_data)} 个库存"
        )

    def _seed_travel(self, user):
        """行 - 示例行程 + 通勤"""
        if Trip.objects.filter(user=user).exists():
            return

        # 即将到来的旅行
        trip1 = Trip.objects.create(
            user=user,
            title="杭州周末游",
            destination="杭州",
            start_date=date.today() + timedelta(days=14),
            end_date=date.today() + timedelta(days=16),
            trip_type="travel",
            status="planned",
            budget=Decimal("2000"),
            transport="高铁",
            accommodation="西湖附近民宿",
            companions="2人",
        )

        TripEvent.objects.create(
            trip=trip1,
            title="高铁出发",
            date=trip1.start_date,
            start_time="08:00",
            end_time="09:30",
            location="上海虹桥-杭州东",
            category="交通",
            cost=Decimal("146"),
            order=1,
        )
        TripEvent.objects.create(
            trip=trip1,
            title="入住民宿",
            date=trip1.start_date,
            start_time="10:00",
            end_time="11:00",
            location="西湖区",
            category="住宿",
            cost=Decimal("500"),
            order=2,
        )
        TripEvent.objects.create(
            trip=trip1,
            title="游览西湖",
            date=trip1.start_date,
            start_time="14:00",
            end_time="17:00",
            location="西湖景区",
            category="景点",
            order=3,
        )
        TripEvent.objects.create(
            trip=trip1,
            title="晚餐-楼外楼",
            date=trip1.start_date,
            start_time="18:00",
            end_time="20:00",
            location="楼外楼",
            category="餐饮",
            cost=Decimal("300"),
            order=4,
        )
        TripEvent.objects.create(
            trip=trip1,
            title="灵隐寺",
            date=trip1.end_date,
            start_time="09:00",
            end_time="12:00",
            location="灵隐寺",
            category="景点",
            cost=Decimal("75"),
            order=1,
        )

        # 打包清单
        packing_data = [
            ("换洗衣物", "衣物", 2),
            ("洗漱用品", "洗护", 1),
            ("充电器", "电子", 1),
            ("身份证", "证件", 1),
            ("现金", "证件", 1),
            ("雨伞", "日用品", 1),
            ("常用药", "药品", 1),
            ("零食", "食品", 3),
        ]
        for name, cat, qty in packing_data:
            PackingItem.objects.create(
                trip=trip1,
                name=name,
                category=cat,
                quantity=qty,
            )

        # 已完成的旅行
        trip2 = Trip.objects.create(
            user=user,
            title="成都美食之旅",
            destination="成都",
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() - timedelta(days=27),
            trip_type="travel",
            status="completed",
            budget=Decimal("3000"),
            actual_cost=Decimal("2800"),
            transport="飞机",
            accommodation="太古里酒店",
        )

        # 通勤记录
        for i in range(7):
            d = date.today() - timedelta(days=i)
            CommuteLog.objects.create(
                user=user,
                date=d,
                mode="地铁",
                destination="公司",
                duration_minutes=40,
                distance_km=Decimal("15.5"),
                cost=Decimal("6"),
            )

        self.stdout.write(f"  行: 创建 2 个行程 + 5 个事件 + 8 个打包项 + 7 天通勤")
