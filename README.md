# 时分渺OvO 博客系统

Flask + Vue3 + MySQL 5.7 个人博客，暗色科技感 + 日间蓝白双主题。

## 功能特性

### 前台
- 首页：大 banner + 粒子动效背景 + 文章卡片网格
- 文章详情：Markdown 渲染 + 代码高亮 + 目录导航
- 时间轴：按年份展示文章发布记录
- 关于页：个人信息展示（昵称/简介/头像/统计）
- 导航栏：搜索 + 分类筛选 + 日夜间主题切换
- 博客运行时长实时倒计时

### 后台
- JWT 登录认证（单用户）
- 文章管理：Vditor Markdown 编辑器，草稿/发布状态，封面上传
- 分类 & 标签管理
- 账号设置：修改用户名/密码，编辑关于页内容（昵称/简介/头像）
- 若依风格布局：顶部 header + 可折叠左侧菜单

### 技术栈
- 后端：Flask + SQLAlchemy + PyJWT + PyMySQL + Flask-CORS
- 前端：Vue3 + Vite + Vditor + Pinia + Vue Router + Axios + Marked + Highlight.js
- 数据库：MySQL 5.7（远程）
- 部署：Docker Compose + Nginx

---

## 快速开始

### 1. 配置数据库

编辑 `backend/.env`：

```env
DB_HOST=********
DB_PORT=********
DB_USER=********
DB_PASSWORD=********
DB_NAME=blog

JWT_SECRET_KEY=your-random-secret-key-here  # ⚠️ 必须改成随机字符串
BLOG_START_DATE=2026-04-24                  # 博客运行时间起算日期

ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-password         # ⚠️ 必须改成强密码
```

**重要：**
- `JWT_SECRET_KEY` 用随机字符串（至少32位）
- `ADMIN_PASSWORD` 改成强密码
- `BLOG_START_DATE` 改成你想统计的起始日期

### 2. 创建数据库

在 MySQL 服务器上执行：

```sql
CREATE DATABASE blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 本地开发

**后端：**

```bash
cd backend
pip install -r requirements.txt
python run.py
```

后端运行在 http://localhost:5001

**前端：**

```bash
cd frontend
npm install
npm run dev
```

前端运行在 http://localhost:8001

首次启动会自动创建数据库表和管理员账号。

### 4. 生产部署（Docker）

在 `blog/` 目录下：

```bash
docker-compose up -d --build
```

访问：
- 前台：http://服务器IP
- 后台：http://服务器IP/admin/login

---

## 配置说明

### 必须修改的配置

**`backend/.env`** — 唯一需要手动配置的文件

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `DB_HOST` | 数据库IP | `********` |
| `DB_PORT` | 数据库端口 | `********` |
| `DB_USER` | 数据库用户名 | `********` |
| `DB_PASSWORD` | 数据库密码 | `your-password` |
| `DB_NAME` | 数据库名 | `blog` |
| `JWT_SECRET_KEY` | JWT 密钥（⚠️ 必改） | 随机字符串 |
| `BLOG_START_DATE` | 运行时长起算日期 | `2026-04-24` |
| `ADMIN_USERNAME` | 管理员用户名 | `admin` |
| `ADMIN_PASSWORD` | 管理员密码（⚠️ 必改） | 强密码 |

### 可选配置

**`docker-compose.yml`** — 生产环境端口映射

```yaml
frontend:
  ports: ["8001:8001"]      # 前台对外端口
backend:
  ports: ["5001:5001"]  # 后端端口（内部用）
```

**`frontend/vite.config.js`** — 仅本地开发

```js
server: {
  port: 8001,           // 前端开发端口
  proxy: {
    '/api': 'http://localhost:5001',  // 后端代理
  }
}
```

---

## 目录结构

```
blog/
├── backend/              # Flask 后端
│   ├── app/
│   │   ├── models/       # 数据模型（User/Article/Category/Tag/Profile）
│   │   ├── routes/       # API 路由
│   │   └── utils/        # JWT 工具
│   ├── .env              # 环境变量（⚠️ 不提交到 Git）
│   ├── config.py         # 配置加载
│   ├── run.py            # 启动入口
│   ├── requirements.txt  # Python 依赖
│   └── Dockerfile
├── frontend/             # Vue3 前端
│   ├── src/
│   │   ├── views/        # 页面组件（前台 + 后台）
│   │   ├── components/   # 公共组件
│   │   ├── layouts/      # 布局组件
│   │   ├── stores/       # Pinia 状态（auth/theme）
│   │   ├── router/       # 路由配置
│   │   └── api/          # Axios 封装
│   ├── nginx.conf        # Nginx 配置
│   ├── vite.config.js    # Vite 配置
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml    # Docker 编排
├── .gitignore
└── README.md
```

---

## 使用说明

### 后台管理

访问 `http://localhost:8001/admin/login`（本地）或 `http://服务器IP/admin/login`（生产）

默认账号：`admin` / `admin123`（⚠️ 首次登录后立即修改）

**功能：**
- 文章管理：新建/编辑/删除文章，Markdown 编辑器，草稿/发布状态
- 分类管理：添加/删除分类
- 标签管理：添加/删除标签
- 账号设置：
  - 修改用户名/密码
  - 编辑关于页内容（昵称/简介/头像上传）

### 前台功能

- 首页：文章列表，支持搜索和分类筛选
- 文章详情：Markdown 渲染，代码高亮，目录导航
- 时间轴：按年份倒序展示文章发布记录
- 关于页：展示个人信息和博客统计
- 主题切换：右上角 ◑/◐ 按钮切换日夜间模式

---

## 常用命令

### Docker 部署

```bash
# 启动服务
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 查看运行状态
docker-compose ps
```

### 本地开发

```bash
# 后端
cd backend
python run.py

# 前端
cd frontend
npm run dev

# 前端构建
npm run build
```

---

## 注意事项

1. **安全：**
   - `.env` 文件包含敏感信息，不要提交到 Git
   - 生产环境务必修改 `JWT_SECRET_KEY` 和 `ADMIN_PASSWORD`
   - 建议配置 HTTPS（Nginx + Let's Encrypt）

2. **数据库：**
   - 确保 MySQL 5.7 已安装并运行
   - 数据库字符集必须是 `utf8mb4`
   - 首次启动会自动创建表和管理员账号

3. **文件上传：**
   - 上传的图片保存在 `uploads/` 目录
   - Docker 部署时已挂载为 volume，数据持久化
   - 支持格式：PNG / JPG / JPEG / GIF / WebP / SVG

4. **主题：**
   - 默认夜间模式（暗色科技风）
   - 日间模式为蓝白色调
   - 主题选择保存在浏览器 localStorage

---

## 技术细节

- **JWT 认证：** 使用 PyJWT 自封装，token 有效期 24 小时
- **Markdown 渲染：** 前台用 marked + highlight.js，后台编辑器用 Vditor
- **粒子动效：** Canvas 绘制，根据主题动态调整颜色
- **响应式：** 移动端适配，断点 320px+
- **SEO：** 前端 history 模式，Nginx 配置 try_files

---

## License

MIT
