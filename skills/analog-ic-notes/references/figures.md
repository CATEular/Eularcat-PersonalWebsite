# 论文配图

先查看 PDF 页面，再选择图像区域或矢量裁剪，不能根据图片平均亮度判断照片需要反色

`scripts/extract_figures.py` 按页面渲染结果提取嵌入图片的区域，因此保留 PDF 中的透明合成、遮罩、极性和颜色

```sh
python scripts/extract_figures.py paper.pdf --config config.local.json --paper-id paper-slug
```

矢量电路图、拼合图或缺少图注时，手动选取 PDF 页上的矩形范围

```sh
python scripts/extract_figures.py paper.pdf --config config.local.json --paper-id paper-slug --page 3 --crop 40 80 560 390
```

页码从 1 开始，坐标以 PDF 点为单位，原点在左上角，裁剪范围为 `x0 y0 x1 y1`

图片输出到配置中 `images/paper-slug/`，已有同名文件不会覆盖，更新时使用另一个目录或先明确处理旧文件

这不是自动图号识别器，导出后核对原图号、页码、是否重复，以及标注与图注完整性，再按语义命名与嵌入

保持原始纵横比，技术图不进行风格化、重绘或强制反相，芯片显微照片保留原始颜色，白底来自页面渲染而非篡改内容
