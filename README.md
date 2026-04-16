# 微信公众号订阅和文章管理技能 (WeChat Article Skill)

> 管理微信公众号订阅，获取文章列表和详情

## 功能列表

| 功能 | 说明 | 脚本 |
|------|------|------|
| **订阅公众号** | 添加关注的公众号 | `add_mp.py` |
| **获取已订阅公众号** | 查看已关注的公众号列表 | `list_mps.py` |
| **删除订阅** | 取消关注公众号 | `delete_mp.py` |
| **获取文章列表** | 获取特定日期的文章 | `get_articles.py` |
| **获取文章详情** | 获取单篇文章的详细内容 | `get_article_details.py` |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件：

```
ACCESS_KEY=your_access_key
SECRET_KEY=your_secret_key
BASE_URL=https://api.example.com
```

### 3. 使用命令

```bash
# 订阅公众号
python add_mp.py "虎嗅 APP"

# 获取已订阅公众号列表
python list_mps.py

# 删除订阅
python delete_mp.py "虎嗅 APP"

# 获取当天文章
python get_articles.py

# 获取指定日期文章
python get_articles.py --date 2026-04-16

# 获取文章详情
python get_article_details.py <article_id>
```

## 项目结构

```
.trae/skills/wechat-article-skill/
├── SKILL.md                  # 技能定义文件
├── main.py                   # 主入口（可选）
├── scripts/
│   ├── add_mp.py             # 订阅公众号
│   ├── list_mps.py           # 获取已订阅公众号
│   ├── delete_mp.py          # 删除订阅公众号
│   ├── get_articles.py       # 获取文章列表
│   └── get_article_details.py # 获取文章详情
├── requirements.txt          # Python 依赖
└── README.md                 # 使用文档
```

## API 说明

### 1. 订阅公众号 (`add_mp.py`)

**调用方式：**
```python
add_mp(mp_name: str) -> str
```

**逻辑：**
1. 调用 `search_mp.py` 搜索同名公众号
2. 提取 `mp_id`、`mp_cover`、`avatar`、`mp_intro`
3. 调用 `POST /api/v1/wx/mps` 创建订阅

### 2. 获取已订阅公众号 (`list_mps.py`)

**调用方式：**
```python
list_mps(kw: str = "", limit: int = 10, offset: int = 0) -> dict
```

**参数：**
- `kw`: 搜索关键字，默认为空（获取全部）
- `limit`: 返回结果的最大数量 (1-100)
- `offset`: 偏移量

**API:** `GET /api/v1/wx/mps`

### 3. 删除订阅公众号 (`delete_mp.py`)

**调用方式：**
```python
delete_mp(mp_name: str) -> str
```

**逻辑：**
1. 调用 `list_mps.py` 从已订阅列表中查找
2. 提取 `mp_id`
3. 调用 `DELETE /api/v1/wx/mps/{mp_id}` 删除

### 4. 获取文章列表 (`get_articles.py`)

**调用方式：**
```python
get_articles(target_date: str = None, mp_id: str = None) -> list
```

**参数：**
- `target_date`: 目标日期，格式 YYYY-MM-DD，默认为当天
- `mp_id`: 公众号 ID，可选

**特性：**
- 自动分页（每页 20 条）
- 按 `publish_time` 筛选日期（北京时间 UTC+8）
- 终止条件：当某一页没有匹配日期的文章时停止

**返回字段：**
- `id`: 文章 ID
- `created_at`: 创建时间
- `description`: 摘要
- `title`: 标题
- `mp_name`: 公众号名称
- `publish_time`: 发布时间（Unix 时间戳）

### 5. 获取文章详情 (`get_article_details.py`)

**调用方式：**
```python
get_article_details(article_id: str) -> dict
```

**注意：** 必须先调用 `get_articles.py` 获取文章列表，拿到 `article_id` 后才能获取详情。

**API:** `GET /api/v1/wx/articles/{article_id}`

## 典型工作流

```
1. 订阅公众号
   → add_mp("虎嗅 APP")

2. 查看已订阅列表
   → list_mps()

3. 获取某天的文章
   → get_articles(target_date="2026-04-16")
   → 返回文章列表，包含 article_id

4. 获取文章详情
   → get_article_details(article_id)
```

## 环境变量

| 变量名 | 说明 |
|--------|------|
| `ACCESS_KEY` | API 访问密钥 |
| `SECRET_KEY` | API 访问密钥 |
| `BASE_URL` | API 基础 URL |

## 注意事项

1. **环境配置**: 确保 `.env` 文件配置正确
2. **日期格式**: 使用 `YYYY-MM-DD` 格式
3. **时区处理**: `publish_time` 使用北京时间 (UTC+8)
4. **编码**: 所有文件使用 UTF-8 编码
