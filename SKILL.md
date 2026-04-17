---
name: wechat-article-skill
description: 微信公众号订阅和文章管理技能。支持订阅公众号、获取已订阅列表、删除订阅、获取文章列表和文章详情。
version: 1.0.0
commands:
  - /wechat_subscribe - 订阅公众号 (e.g., /wechat_subscribe 虎嗅 APP)
  - /wechat_list_subs - 获取已订阅公众号列表 (e.g., /wechat_list_subs)
  - /wechat_unsubscribe - 删除订阅公众号 (e.g., /wechat_unsubscribe 虎嗅 APP)
  - /wechat_articles - 获取特定日期的文章 (e.g., /wechat_articles 2026-04-16)
  - /wechat_article_detail - 获取文章详情 (e.g., /wechat_article_detail article_id_123)

使用方式：
    python main.py subscribe <公众号名称>
    python main.py list_subs [关键词]
    python main.py unsubscribe <公众号名称>
    python main.py articles [日期 YYYY-MM-DD]
    python main.py article_detail <文章 ID>
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["python"],"env":["ACCESS_KEY","SECRET_KEY","BASE_URL"]},"install":[{"id":"python-reqs","kind":"pip","requirements":["requests"],"label":"安装 Python 依赖"}]}}
---

# 微信公众号订阅和文章管理技能

管理微信公众号订阅，获取文章列表和详情。

## 功能列表

1. **订阅公众号** - 添加关注的公众号
2. **获取已订阅公众号** - 查看已关注的公众号列表
3. **删除订阅** - 取消关注公众号
4. **获取文章列表** - 获取特定日期的文章
5. **获取文章详情** - 获取单篇文章的详细内容

## 使用方法

所有命令都通过 `main.py` 统一调用：

### 1. 订阅公众号

```bash
# 只传公众号名称，自动搜索获取信息
python main.py subscribe "虎嗅 APP"
```

**逻辑：**
- 先搜索同名公众号获取 `mp_id`、`mp_cover`、`avatar`、`mp_intro`
- 然后调用 API 创建订阅

### 2. 获取已订阅公众号

```bash
# 获取全部已订阅公众号
python main.py list_subs

# 搜索关键字过滤
python main.py list_subs 虎嗅
```

### 3. 删除订阅公众号

```bash
# 传入公众号名称
python main.py unsubscribe "虎嗅 APP"
```

**逻辑：**
- 先从已订阅列表中查找该公众号
- 提取 `mp_id`
- 调用 API 删除

### 4. 获取特定日期的文章

```bash
# 获取当天文章
python main.py articles

# 获取指定日期文章
python main.py articles 2026-04-16

# 获取指定公众号的文章（需要配合 --mp_id 参数）
python main.py articles 2026-04-16 --mp_id MP_WXS_xxxxxx
```

**特性：**
- 自动分页（每页 20 条）
- 按 `publish_time` 筛选：
  - 不传日期或传当天日期：获取最近 24 小时的文章
  - 传历史日期：获取该日期 00:00:00 到 23:59:59 的文章
- 返回字段：`id`、`created_at`、`description`、`title`、`mp_name`、`publish_time`（已格式化为 YYYY-MM-DD HH:MM:SS）

### 5. 获取文章详情

```bash
# 需要先获取文章列表得到 article_id
python main.py article_detail <article_id>
```

**注意：** 必须先调用 `articles` 命令获取文章列表，拿到 `article_id` 后才能获取详情。

## 项目结构

```
.trae/skills/wechat-article-skill/
├── SKILL.md                  # 技能定义文件
├── scripts/
│   ├── add_mp.py             # 订阅公众号
│   ├── list_mps.py           # 获取已订阅公众号
│   ├── delete_mp.py          # 删除订阅公众号
│   ├── get_articles.py       # 获取文章列表
│   └── get_article_details.py # 获取文章详情
└── README.md                 # 使用文档
```

## 环境变量

| 变量 | 说明 |
|------|------|
| ACCESS_KEY | API 访问密钥 |
| SECRET_KEY | API 访问密钥 |
| BASE_URL | API 基础 URL |

## 典型工作流

```
1. 订阅公众号
   → python main.py subscribe "虎嗅 APP"

2. 查看已订阅列表
   → python main.py list_subs

3. 获取某天的文章
   → python main.py articles 2026-04-16
   → 返回文章列表，包含 article_id

4. 获取当天的文章
   → python main.py articles
   → 返回文章列表，包含 article_id

5. 获取文章详情
   → python main.py article_detail <article_id>
```
