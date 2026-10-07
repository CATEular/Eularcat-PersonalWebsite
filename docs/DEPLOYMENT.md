# 静态网站部署

需要 Node.js 22 或更新版本。

```sh
npm ci
npm test
npm run build
npm run check
```

正式部署时先设置环境变量 `SITE_ORIGIN` 为实际域名，再运行构建。默认地址为本地预览地址。该变量用于 canonical、语言 alternates、Open Graph、sitemap 与 RSS。

上传 `dist/` 内的文件到静态托管平台。网站使用 `/zh/`、`/en/` 和 `/assets/` 等根路径，部署在域名根目录，未知路由返回 `404.html`。GitHub 项目 Pages 的仓库子路径需要额外的路径适配，不能直接按当前根路径配置部署。

构建不依赖平台专用配置、数据库或后台服务。修改内容后重新构建再部署。
