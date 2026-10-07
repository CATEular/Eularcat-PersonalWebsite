# Eularcat Personal Website

Eularcat 的双语个人技术网站，以 Markdown 保存学习笔记和论文阅读记录，包含学习地图、工具项目与 AI × IC 内容。主要研究方向是大电流 DC-DC Buck。

## 本地运行

需要 Node.js 22 或更新版本。

```sh
npm ci
npm test
npm run build
npm run check
npm run dev
```

打开 http://127.0.0.1:4321/zh/ 或 /en/。修改内容后重新构建并刷新页面。

## 项目结构

- `content/`：Markdown 内容、论文元数据、图片和站点配置
- `src/`：页面组件、中英文文案、样式与 Markdown 渲染
- `public/`：网站图片、图标和浏览器脚本
- `scripts/`：构建、预览、内容导入、下载包生成和检查
- `skills/analog-ic-notes/`：网站公开提供的论文笔记工具、模板和说明
- `docs/`：内容维护和部署说明

## 添加或修改项目

项目链接在 `content/site.json`，项目页面在 `src/components/pages.mjs`，中英文文案在 `src/i18n/index.mjs`，路由在 `scripts/build.mjs`。

## 内容维护

详见 [维护总览](docs/README.md)。只有 `status: published` 的笔记进入网页、搜索和 RSS；源码仓库内的内容应当适合公开访问。技术笔记保留原始语言，不自动翻译。

`content/notes/rendering-test/index.md` 是明确标注的排版测试，验证公式、代码、图片和表格。

## 部署

构建产物位于 `dist/`，可部署到支持静态网站的平台。通过环境变量 `SITE_ORIGIN` 设置正式站点地址，详见 [部署说明](docs/DEPLOYMENT.md)。网站使用根路径路由，未知页面应返回 `404.html`。
