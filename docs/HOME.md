# 更新首页章节

首页中文入口为 `/zh/`，英文入口为 `/en/`  
内容自动从 Markdown 和 JSON 配置读取，章节结构在 `src/components/home.mjs`

## 当前结构

| 编号 | 章节 | 内容与更新入口 |
| --- | --- | --- |
| 01 | 精选项目 | IC Schematics Studio，链接在 `content/site.json`，说明见 [项目维护](../README.md#添加或修改项目) |
| 02 | 学习地图 | `content/site.json` 中的 `learning`，操作见 [学习地图](LEARNING-MAP.md) |
| 03 | 最近笔记 | `content/notes/` 中已发布的笔记，手记式面板，操作见 [添加笔记](NOTES.md) |
| 04 | 最近阅读 | `content/reading/` 中已发布的论文记录，带年份的论文卡片，操作见 [添加论文](PAPERS.md) |
| 05 | AI × IC | 工作流记录与技能库两个入口，操作见 [AI × IC](AI-IC.md) |

03 与 04 各显示最多四篇，按记录的 `date` 从新到旧排序  
论文卡片显示的年份来自论文元数据 `year`，不等同于笔记日期  
修改 `updated` 会更新文章信息，但不会改变首页排序

新增或隐藏文章只需维护原 Markdown 的 `status`，首页、资料页、搜索和 RSS 会随重新构建更新，不需要手工再加一张卡片

## 修改文案或样式

| 想改什么 | 对应文件 |
| --- | --- |
| 章节标题、简介、按钮等中英文文案 | `src/i18n/index.mjs` |
| 首页章节顺序、数量和排版结构 | `src/components/home.mjs` |
| AI 入口卡片、阅读区技能跳转 | `src/components/ai.mjs` |
| 圆角、间距、颜色、响应式与动效 | `src/styles/site.css` |

03、04、05 保持独立章节，标题与编号放在卡片外，和 02 对齐  
03 侧重自己的推导和工程手记，04 侧重论文来源，两者保留不同的视觉排版  
阅读区的简短技能入口同时出现在首页 04 和阅读资料页，由 `readingSkillLink()` 统一生成

当前技能入口为 `/zh/ai-ic/analog-ic-notes/`，英文界面使用对应 `/en/` 路径

## 检查更新

运行 `npm run build` 后启动 `npm run dev`，检查电脑和手机宽度下的标题、卡片、长论文标题、明暗主题与技能跳转  
涉及结构或逻辑变更时还需执行 `npm test` 与 `npm run check`

线上更新重新构建并部署，不直接编辑生成目录 `dist/`
