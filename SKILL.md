---
name: wechat-article-skill
description: 微信公众号订阅和文章管理技能
version: 1.0.0
commands:
  - /wechat_subscribe <公众号名称> - 订阅公众号
  - /wechat_list_subs [关键词] - 获取已订阅公众号列表
  - /wechat_unsubscribe <公众号名称> - 删除订阅
  - /wechat_articles [日期 YYYY-MM-DD] - 获取文章列表
  - /wechat_article_detail <文章 ID> - 获取文章详情

metadata:
  clawdbot:
    emoji: 📰
    requires:
      bins: [python]
      env: [ACCESS_KEY, SECRET_KEY, BASE_URL]
    install:
      - id: python-reqs
        kind: pip
        requirements: [requests, python-dotenv]
        label: 安装 Python 依赖
---

# 微信公众号订阅和文章管理技能

管理微信公众号订阅，获取文章列表和详情。

## 使用方法

### 订阅公众号

```bash
/wechat_subscribe 虎嗅 APP
```

### 获取已订阅列表

```bash
/wechat_list_subs
/wechat_list_subs 虎嗅
```

### 删除订阅

```bash
/wechat_unsubscribe 虎嗅 APP
```

### 获取文章列表

```bash
/wechat_articles
/wechat_articles 2026-04-16
```

### 获取文章详情

```bash
/wechat_article_detail <文章 ID>
```

## 环境变量

| 变量 | 说明 |
|------|------|
| ACCESS_KEY | API 访问密钥 |
| SECRET_KEY | API 访问密钥 |
| BASE_URL | API 基础 URL |
