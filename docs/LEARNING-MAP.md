# 修改学习地图

主配置文件：`content/site.json`

首页的地图卡片和学习页的分组共用 `learning` 数组，按数组顺序显示，目前依次为

1. 功率及电路基础
2. 同步 DC-DC Buck
3. 多相 DC-DC Buck
4. AI × EDA

这里表达学习结构，个人主要研究方向另在 About 中说明为大电流 DC-DC Buck  
PMIC 是包含 Buck 等电路的较大领域，不再作为地图中与 Buck 并列的第一站

## 修改名称、顺序或描述

一个分组结构如下，示例只展示一组，不要覆盖整个 `site.json`

```json
{
  "category": "buck",
  "code": "BUCK",
  "glyph": "B",
  "eyebrow": "SYNCHRONOUS BUCK",
  "title": {"zh": "同步 DC-DC Buck", "en": "Synchronous DC-DC Buck"},
  "description": {
    "zh": "学习同步 Buck 的工作方式、控制、环路与轻载运行",
    "en": "Learning synchronous Buck operation, control, loop behavior and light-load modes"
  },
  "topics": ["Synchronous DC-DC Buck", "PWM", "COT"]
}
```

- 修改 `title.zh`、`title.en` 更新分组名称
- 修改 `description` 更新卡片和分组简介
- 调整整个对象在 `learning` 数组中的位置，改变显示顺序
- 在 `topics` 中增加、删除或移动主题
- `category` 是链接锚点，必须唯一，使用小写字母和连字符，已有值尽量保留
- `code`、`glyph`、`eyebrow` 是卡片上的短标识，不是文章内容

保持合法 JSON，字符串使用双引号，不加注释，不在最后一项后面添加逗号  
新增英文主题需要中文显示名时，在 `src/i18n/index.mjs` 的 `topicZh` 中补充映射；直接使用中文主题也能显示

## 给主题添加真实文章

新建 `content/learn/<slug>/index.md`，例如

```markdown
---
title: 我的 COT 学习记录
description: 根据自己的实际学习填写简介
lang: zh
type: learn
topic: COT
status: draft
---

## 正文

在这里写学习笔记
```

`topic` 必须与地图中某一项完全一致  
完成后把 `status` 改为 `published`，该主题会出现文章链接和“已发布”标记；未发布的主题保持“计划”  
每个主题目前连接一篇主文章，更多相关内容可在主文章中添加标准 Markdown 链接

预览和发布见[通用步骤](README.md#通用步骤)
