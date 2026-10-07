# 添加笔记

在 `content/notes/<slug>/index.md` 创建 Markdown，学习文章放入 `content/learn/<slug>/index.md`。

```yaml
---
title: 我的学习记录
description: 一句话简介
date: 2026-10-07
lang: zh
type: note
category: knowledge
tags: [Buck]
status: draft
---
```

`category` 可为 `knowledge` 或 `engineering`。完成检查后改为 `status: published`。学习文章使用 `type: learn`，可用 `topic` 关联学习地图。

图片放入文章自身的 `assets/`，使用相对 Markdown 链接。支持 LaTeX 数学、代码高亮、表格、引用和标题目录。

也可导入自己的 Markdown 副本：

```sh
npm run import -- --note ./input/note.md --assets ./input/images --slug my-note
```

原文件不会改动，已有文章不会覆盖。重新构建后检查页面和图片。
