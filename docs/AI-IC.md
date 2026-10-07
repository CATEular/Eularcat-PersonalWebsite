# AI × IC 与公开下载

工作流分类和技能卡片配置在 `content/ai-ic.json`。分类只展示已存在且已发布的笔记，空分类保持待补充。首页笔记、阅读与 AI × IC 保持独立章节。

## Analog IC Notes

网站公开提供的论文笔记工具位于 `skills/analog-ic-notes/`，包括 `SKILL.md`、`resources/` 模板、`references/` 参考说明、`scripts/` 图片与路径辅助程序、通用配置示例和依赖清单。

中文和英文介绍分别在 `content/skills/analog-ic-notes/zh.md` 和 `en.md`。

`npm run build` 按 `scripts/package-skill.mjs` 的明确文件清单生成 ZIP 与可浏览文件，输出到 `dist/downloads/`。个人配置、工具界面预设、本地 PDF 均不在公开下载包中。

复制 `config.example.json` 为自己的 `config.local.json`，填写个人目录。相对路径以配置文件目录为基准。

```sh
python -m pip install -r requirements.txt
python scripts/paths.py --config config.local.json
python scripts/extract_figures.py paper.pdf --config config.local.json --paper-id my-paper
```

添加其他工具时需要同时补齐实际说明页、路由、下载源文件与打包逻辑。更新后检查详情页、ZIP 和所有本地链接。
