/**
 * LifeHub 纯前端版本 - 本地数据库层
 * 用 localStorage 替代 SQLite + Django ORM
 */

const DB = {
  prefix: 'lifehub_',
  
  _key(user, table) {
    return this.prefix + (user || 'guest') + '_' + table;
  },
  
  get(table, user) {
    const key = this._key(user, table);
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : [];
  },
  
  set(table, data, user) {
    const key = this._key(user, table);
    localStorage.setItem(key, JSON.stringify(data));
  },
  
  add(table, item, user) {
    const data = this.get(table, user);
    item.id = item.id || Date.now() + Math.random().toString(36).substr(2, 9);
    item.created_at = item.created_at || new Date().toISOString();
    item.updated_at = new Date().toISOString();
    data.push(item);
    this.set(table, data, user);
    return item;
  },
  
  update(table, id, updates, user) {
    const data = this.get(table, user);
    const idx = data.findIndex(x => x.id == id);
    if (idx >= 0) {
      data[idx] = { ...data[idx], ...updates, updated_at: new Date().toISOString() };
      this.set(table, data, user);
      return data[idx];
    }
    return null;
  },
  
  del(table, id, user) {
    const data = this.get(table, user);
    const filtered = data.filter(x => x.id != id);
    this.set(table, filtered, user);
    return filtered.length < data.length;
  },
  
  getOne(table, id, user) {
    const data = this.get(table, user);
    return data.find(x => x.id == id) || null;
  },
  
  query(table, filterFn, user) {
    const data = this.get(table, user);
    return filterFn ? data.filter(filterFn) : data;
  },
  
  clearAll(user) {
    const keys = Object.keys(localStorage);
    const prefix = this._key(user, '');
    keys.forEach(k => {
      if (k.startsWith(prefix)) localStorage.removeItem(k);
    });
  },
  
  export(user) {
    const keys = Object.keys(localStorage);
    const prefix = this._key(user, '');
    const data = {};
    keys.forEach(k => {
      if (k.startsWith(prefix)) {
        const table = k.replace(prefix, '');
        data[table] = JSON.parse(localStorage.getItem(k));
      }
    });
    return data;
  },
  
  import(data, user) {
    Object.keys(data).forEach(table => {
      this.set(table, data[table], user);
    });
  },
  
  size() {
    let total = 0;
    for (let key in localStorage) {
      if (key.startsWith(this.prefix)) {
        total += localStorage[key].length * 2;
      }
    }
    return (total / 1024 / 1024).toFixed(2) + ' MB';
  }
};

// 用户认证（纯本地，无后端）
const Auth = {
  currentUser: null,
  
  hashPassword(password) {
    // 简单哈希 - 生产环境应使用 bcrypt
    let hash = 0;
    for (let i = 0; i < password.length; i++) {
      const char = password.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return 'local_' + Math.abs(hash).toString(16);
  },
  
  register(username, password) {
    const users = DB.get('users', 'system');
    if (users.find(u => u.username === username)) {
      throw new Error('用户名已存在');
    }
    const user = {
      id: 'user_' + Date.now(),
      username,
      password_hash: this.hashPassword(password),
      created_at: new Date().toISOString()
    };
    users.push(user);
    DB.set('users', users, 'system');
    return user;
  },
  
  login(username, password) {
    const users = DB.get('users', 'system');
    const user = users.find(u => u.username === username);
    if (!user || user.password_hash !== this.hashPassword(password)) {
      throw new Error('用户名或密码错误');
    }
    this.currentUser = user;
    localStorage.setItem('lifehub_current_user', JSON.stringify(user));
    return user;
  },
  
  logout() {
    this.currentUser = null;
    localStorage.removeItem('lifehub_current_user');
  },
  
  check() {
    const saved = localStorage.getItem('lifehub_current_user');
    if (saved) {
      this.currentUser = JSON.parse(saved);
      return true;
    }
    return false;
  },
  
  getUser() {
    return this.currentUser || (this.check() ? this.currentUser : null);
  },
  
  getUsername() {
    const u = this.getUser();
    return u ? u.username : 'guest';
  }
};

// 业务 API（替代 Django REST API）
const API = {
  user() { return Auth.getUsername(); },
  
  // 账户
  profile() {
    const users = DB.get('users', 'system');
    const user = users.find(u => u.username === this.user());
    return user || {};
  },
  
  updateProfile(data) {
    const users = DB.get('users', 'system');
    const idx = users.findIndex(u => u.username === this.user());
    if (idx >= 0) {
      users[idx] = { ...users[idx], ...data, updated_at: new Date().toISOString() };
      DB.set('users', users, 'system');
    }
    return users[idx];
  },
  
  // 仪表盘统计
  dashboard() {
    const user = this.user();
    const clothes = DB.get('clothes', user);
    const outfits = DB.get('outfit_logs', user);
    const meals = DB.get('meal_logs', user);
    const recipes = DB.get('recipes', user);
    const expenses = DB.get('expenses', user);
    const tasks = DB.get('tasks', user);
    const inventory = DB.get('inventory', user);
    const trips = DB.get('trips', user);
    const commute = DB.get('commute_logs', user);
    const shopping = DB.get('shopping_items', user);
    
    const today = new Date().toISOString().split('T')[0];
    const month = today.substring(0, 7);
    
    return {
      wardrobe: {
        total_clothes: clothes.length,
        today_outfit_logged: outfits.some(o => o.date === today),
        total_outfits: outfits.length
      },
      food: {
        today_meals: meals.filter(m => m.date === today).length,
        recipe_count: recipes.length,
        pending_shopping: shopping.filter(s => !s.is_purchased).length
      },
      home: {
        month_expense: expenses.filter(e => e.date && e.date.startsWith(month)).reduce((s, e) => s + (parseFloat(e.amount) || 0), 0),
        pending_tasks: tasks.filter(t => !t.is_done).length,
        overdue_tasks: tasks.filter(t => !t.is_done && t.next_due_date && t.next_due_date < today).length,
        low_stock_items: inventory.filter(i => parseFloat(i.quantity) <= parseFloat(i.min_quantity || 0)).length
      },
      travel: {
        upcoming_trips: trips.filter(t => t.status === 'planned' || t.status === 'ongoing'),
        commute_this_week: commute.filter(c => {
          const d = new Date(c.date);
          const now = new Date();
          const diff = (now - d) / (1000 * 60 * 60 * 24);
          return diff >= 0 && diff <= 7;
        }).length
      }
    };
  },
  
  // 衣橱
  clothes: {
    list: (q) => DB.get('clothes', API.user()),
    get: (id) => DB.getOne('clothes', id, API.user()),
    create: (d) => DB.add('clothes', d, API.user()),
    update: (id, d) => DB.update('clothes', id, d, API.user()),
    del: (id) => DB.del('clothes', id, API.user())
  },
  
  outfits: {
    list: (q) => DB.get('outfit_logs', API.user()),
    get: (id) => DB.getOne('outfit_logs', id, API.user()),
    create: (d) => DB.add('outfit_logs', d, API.user()),
    update: (id, d) => DB.update('outfit_logs', id, d, API.user()),
    del: (id) => DB.del('outfit_logs', id, API.user())
  },
  
  suggestOutfit(temp, occ) {
    const user = API.user();
    const clothes = DB.get('clothes', user);
    const today = new Date().toISOString().split('T')[0];
    const todayLog = DB.query('outfit_logs', o => o.date === today, user)[0];
    
    if (todayLog) return { outfit: todayLog, message: '今日已有穿搭记录' };
    
    // 简单推荐逻辑
    const top = clothes.find(c => c.category === 'top') || clothes[0];
    const bottom = clothes.find(c => c.category === 'bottom') || clothes[1];
    const shoes = clothes.find(c => c.category === 'shoes') || clothes[2];
    
    return {
      suggestion: {
        clothes: [top, bottom, shoes].filter(Boolean),
        weather: temp ? temp + 'C' : '未知',
        occasion: occ || '日常',
        reason: '基于你的衣橱推荐'
      }
    };
  },
  
  // 饮食
  recipes: {
    list: (q) => DB.get('recipes', API.user()),
    get: (id) => DB.getOne('recipes', id, API.user()),
    create: (d) => DB.add('recipes', d, API.user()),
    update: (id, d) => DB.update('recipes', id, d, API.user()),
    del: (id) => DB.del('recipes', id, API.user())
  },
  
  meals: {
    list: (q) => DB.get('meal_logs', API.user()),
    get: (id) => DB.getOne('meal_logs', id, API.user()),
    create: (d) => DB.add('meal_logs', d, API.user()),
    update: (id, d) => DB.update('meal_logs', id, d, API.user()),
    del: (id) => DB.del('meal_logs', id, API.user())
  },
  
  shopping: {
    list: (q) => DB.get('shopping_items', API.user()),
    get: (id) => DB.getOne('shopping_items', id, API.user()),
    create: (d) => DB.add('shopping_items', d, API.user()),
    update: (id, d) => DB.update('shopping_items', id, d, API.user()),
    del: (id) => DB.del('shopping_items', id, API.user())
  },
  
  suggestRecipe() {
    const user = API.user();
    const recipes = DB.get('recipes', user);
    if (!recipes.length) return { suggestion: null, message: '暂无菜谱，请先添加' };
    const idx = Math.floor(Math.random() * recipes.length);
    return { suggestion: recipes[idx] };
  },
  
  // 家居
  expenses: {
    list: (q) => DB.get('expenses', API.user()),
    get: (id) => DB.getOne('expenses', id, API.user()),
    create: (d) => DB.add('expenses', d, API.user()),
    update: (id, d) => DB.update('expenses', id, d, API.user()),
    del: (id) => DB.del('expenses', id, API.user()),
    summary: (q) => {
      const expenses = DB.get('expenses', API.user());
      const month = (q || '').replace('?month=', '') || new Date().toISOString().substring(0, 7);
      const monthExpenses = expenses.filter(e => e.date && e.date.startsWith(month));
      const total = monthExpenses.reduce((s, e) => s + (parseFloat(e.amount) || 0), 0);
      const categories = {};
      monthExpenses.forEach(e => {
        categories[e.category] = (categories[e.category] || 0) + (parseFloat(e.amount) || 0);
      });
      return { total, count: monthExpenses.length, categories };
    }
  },
  
  tasks: {
    list: (q) => DB.get('tasks', API.user()),
    get: (id) => DB.getOne('tasks', id, API.user()),
    create: (d) => DB.add('tasks', d, API.user()),
    update: (id, d) => DB.update('tasks', id, d, API.user()),
    del: (id) => DB.del('tasks', id, API.user())
  },
  
  inventory: {
    list: (q) => DB.get('inventory', API.user()),
    get: (id) => DB.getOne('inventory', id, API.user()),
    create: (d) => DB.add('inventory', d, API.user()),
    update: (id, d) => DB.update('inventory', id, d, API.user()),
    del: (id) => DB.del('inventory', id, API.user())
  },
  
  // 出行
  trips: {
    list: (q) => DB.get('trips', API.user()),
    get: (id) => DB.getOne('trips', id, API.user()),
    create: (d) => DB.add('trips', d, API.user()),
    update: (id, d) => DB.update('trips', id, d, API.user()),
    del: (id) => DB.del('trips', id, API.user())
  },
  
  events: {
    list: (tripId) => DB.query('trip_events', e => e.trip_id == tripId, API.user()),
    create: (tripId, d) => DB.add('trip_events', { ...d, trip_id: tripId }, API.user()),
    update: (tripId, id, d) => DB.update('trip_events', id, d, API.user()),
    del: (tripId, id) => DB.del('trip_events', id, API.user())
  },
  
  packing: {
    list: (tripId) => DB.query('packing_items', p => p.trip_id == tripId, API.user()),
    create: (tripId, d) => DB.add('packing_items', { ...d, trip_id: tripId }, API.user()),
    update: (tripId, id, d) => DB.update('packing_items', id, d, API.user()),
    del: (tripId, id) => DB.del('packing_items', id, API.user())
  },
  
  commute: {
    list: (q) => DB.get('commute_logs', API.user()),
    get: (id) => DB.getOne('commute_logs', id, API.user()),
    create: (d) => DB.add('commute_logs', d, API.user()),
    update: (id, d) => DB.update('commute_logs', id, d, API.user()),
    del: (id) => DB.del('commute_logs', id, API.user()),
    summary: () => {
      const logs = DB.get('commute_logs', API.user());
      const totalDuration = logs.reduce((s, l) => s + (parseInt(l.duration_minutes) || 0), 0);
      return { count: logs.length, total_duration: totalDuration };
    }
  }
};
