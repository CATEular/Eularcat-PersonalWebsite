# 添加论文阅读记录

阅读记录保存在 `content/reading/<slug>/`：`note.md` 为正文，`metadata.yaml` 为书目信息，`assets/` 为相关图片。

## 导入

```sh
npm run import:paper -- --note ./input/paper-note.md --assets ./input/images --slug my-paper --description "阅读简介"
npm run import -- --type reading --note ./input/note.md --bibliography ./input/paper.bib --assets ./input/images --slug another-paper
```

支持 BibTeX、RIS 与 CSL JSON，多条记录用 `--key` 指定。导入默认生成草稿，核对标题、作者、年份、DOI、语言与图片后再设为 `published`。可通过 `--help` 查看选项。

Obsidian 图片链接转换为相对 Markdown 链接；缺失图片或同名冲突会报错。不会修改原文库，也不会抓取或分发出版商 PDF。

标签筛选仅来自已发布论文的真实 `tags`。运行 `npm test`、`npm run build` 和 `npm run check` 检查导入结果。
