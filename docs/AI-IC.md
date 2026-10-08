# AI × IC 与公开下载

## Virtuoso 多轮对话工作流

第五个首页模块的工作流入口指向 `/zh/ai-ic/virtuoso-workflow/`，英文页面对应 `/en/`。`content/workflows/virtuoso/` 保存八轮示范对话，以及双语总览和 OSC／RC／MOS 案例。真实测量与后续用法示例分别标注。

五个产品技能位于 `skills/virtuoso-workflow/`，GitHub 中的 README 包含可交给 Agent 的安装指令。`scripts/package-virtuoso.mjs` 按 `export-manifest.json` 导出完整套件；默认不包含个人配置和开发预设。五个技能目录必须同级，保留相对引用。

`public/downloads/virtuoso-workflow.zip` 是供 GitHub 下载的已检查产品包；构建另生成 `dist/downloads/virtuoso-workflow.zip`。更改产品文件后，用新构建包更新前者；测试会核对两者的可复现字节。网站主要下载入口指向 GitHub 源码及 ZIP 页面。

真实截图位于 `public/assets/virtuoso/`，发布前检查标题栏、项目／PDK 标识和图片元数据。MOS 案例仅有连通性及 CDF 读回，不能称为完整性能仿真。OSC 本例仅验证 TT 原理图，版图与物理签核未执行。

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
