# 时分渺OvO 博客系统

Flask + Vue3 + MySQL 5.7 个人博客，暗色科技感 + 日间蓝白双主题。

## 功能特性

### 前台
- 首页：大 banner + 粒子动效 + 文章卡片网格，支持搜索和分类筛选
- 文章详情：Markdown 渲染 + 代码高亮 + 目录导航，支持图片/视频嵌入
- 时间轴：按年份展示文章发布记录
- 关于页：个人信息（昵称/简介/头像）+ 统计 + AI 近况分析展示
- 导航栏：搜索框 + 分类下拉 + 日夜间主题切换 + 后台入口
- 博客运行时长实时倒计时（北京时间）
- 自动根据北京时间切换日夜间主题（8:00-20:00 日间，其余夜间）
- 全站响应式，支持手机端

### 后台（/admin）
- JWT 登录认证（单用户），密码显示/隐藏
- 文章管理：Vditor Markdown 编辑器，草稿/发布，封面拖拽上传，图片/视频插入
- 分类 & 标签管理
- 媒体库：图片/视频上传管理，视频自动截取封面帧，支持批量上传
- AI 助手（需配置 API Key）：
  - 近况分析：读取最近文章，AI 生成近况总结，可编辑后保存到关于页
  - 灵感一现：输入描述自动生成文章，支持指定分类/标签/封面，不存在自动创建
- 账号设置：修改用户名/密码，编辑关于页内容（昵称/简介/头像）
- 若依风格布局：顶部 header + 可折叠左侧菜单，手机端汉堡菜单

### 技术栈
- 后端：Flask + SQLAlchemy + PyJWT + PyMySQL + Flask-CORS + requests
- 前端：Vue3 + Vite + Vditor + Pinia + Vue Router + Axios + Marked + Highlight.js
- 数据库：MySQL 5.7
- 部署：Docker Compose + Nginx

---

## 快速开始

### 1. 配置环境变量

编辑 `backend/.env`：

```env
# 数据库（当前使用外部远程 MySQL）
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=blog

# ⚠️ 上线前必须改成随机字符串（至少32位）
JWT_SECRET_KEY=your-random-secret-key

# 博客运行时长起算日期
BLOG_START_DATE=2026-04-24

# 首次启动自动创建管理员账号（⚠️ 上线前修改密码）
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-strong-password
```

### 2. 创建数据库

```sql
CREATE DATABASE blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 本地开发

**后端：**
```bash
cd backend
pip install -r requirements.txt
python run.py
# 运行在 http://localhost:5001
```

**前端：**
```bash
cd frontend
npm install
npm run dev
# 运行在 http://localhost:8001
```

首次启动自动建表并创建管理员账号。

### 4. 生产部署（Docker）

```bash
cd blog
docker-compose up -d --build
```

访问：
- 前台：`http://服务器IP`
- 后台：`http://服务器IP/admin/login`

---

## 数据库切换

### 当前：外部远程 MySQL
`backend/.env` 中配置远程数据库地址即可，`docker-compose.yml` 中 db service 已注释。

### 切换为本地 Docker MySQL
1. 取消 `docker-compose.yml` 中 `db` service、`backend.depends_on`、`db_data` volume 的注释
2. 修改 `backend/.env`：
   ```env
   DB_HOST=db
   DB_PORT=3306
   ```

---

## 配置说明

### `backend/.env`（唯一需要手动配置的文件）

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `DB_HOST` | 数据库地址 | - |
| `DB_PORT` | 数据库端口 | `3306` |
| `DB_USER` | 数据库用户名 | `root` |
| `DB_PASSWORD` | 数据库密码 | - |
| `DB_NAME` | 数据库名 | `blog` |
| `JWT_SECRET_KEY` | JWT 密钥 ⚠️ 必改 | - |
| `BLOG_START_DATE` | 运行时长起算日期 | `2026-04-24` |
| `ADMIN_USERNAME` | 管理员用户名 | `admin` |
| `ADMIN_PASSWORD` | 管理员密码 ⚠️ 必改 | `admin123` |

### `docker-compose.yml`（生产端口映射）

```yaml
frontend: "8001:8001"     # 前台对外端口
backend: "5001:5001"  # 后端（内部用）
```

### `frontend/vite.config.js`（仅本地开发）

```js
port: 8001            # 前端开发端口
proxy: 5001           # 代理到后端
```

---

## 目录结构

```
blog/
├── backend/
│   ├── app/
│   │   ├── models/       # User / Article / Category / Tag / Profile / Media / AiConfig
│   │   ├── routes/       # auth / articles / categories / tags / upload / media / account / ai / site
│   │   └── utils/        # JWT 工具
│   ├── .env              # ⚠️ 环境变量，不提交 Git
│   ├── config.py
│   ├── run.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── front/    # Home / Article / Timeline / About
│   │   │   └── admin/    # Login / Articles / ArticleEdit / Categories / Tags / Media / AiAnalysis / Account
│   │   ├── components/   # NavBar / FooterBar / RunningTime / ArticleCard / ComboBox / GlobalToast
│   │   ├── layouts/      # FrontLayout / AdminLayout
│   │   ├── stores/       # auth / theme / toast
│   │   ├── router/
│   │   └── api/
│   ├── nginx.conf
│   ├── vite.config.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## AI 助手使用

后台 → 🤖 AI 助手，需先配置 API。

### 支持的服务商（OpenAI 兼容格式）

| 服务商 | API Base URL | 推荐模型 |
|--------|-------------|---------|
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-turbo` |
| Kimi | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` |
| OpenAI | `https://api.openai.com/v1` | `gpt-3.5-turbo` |
| 智谱 GLM | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-flash` |

### 近况分析
读取最近 20 篇已发布文章，AI 生成近况总结，可编辑后保存到关于页展示。

### 灵感一现（AI 写文章）
输入文章描述，AI 自动生成完整 Markdown 文章，支持：
- 指定分类（不存在自动创建）
- 指定标签（逗号分隔，不存在自动创建）
- 从媒体库选择封面图
- 选择草稿或直接发布

---

## 常用命令

```bash
# 启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 重启
docker-compose restart

# 停止
docker-compose down

# 本地后端
cd backend && python run.py

# 本地前端
cd frontend && npm run dev
```

---

## 注意事项

1. `.env` 包含敏感信息，已加入 `.gitignore`，不会提交到 Git
2. 生产环境务必修改 `JWT_SECRET_KEY` 和 `ADMIN_PASSWORD`
3. 上传文件保存在 `uploads/` 目录，Docker 部署时挂载为 volume 持久化
4. 支持上传格式：图片（PNG/JPG/GIF/WebP/SVG）、视频（MP4/WebM/MOV/OGG）
5. 单文件上传限制 200MB
6. AI 功能需要服务器能访问对应 API 地址（注意网络策略）

---

## License

MIT
