---
title: Analog IC Notes
description: 从论文到自己的模拟 IC 笔记
---

## 能做什么

整理论文信息、系统架构、关键电路、实测指标与引用，保留配图和 LaTeX 公式，输出 Markdown / Obsidian 笔记

由 DC-DC Buck Reader 扩展而来，保留 Buck 的精读模板，也适用于其他模拟与混合信号 IC 论文

## 开始使用

下载并解压技能包，将 `analog-ic-notes` 文件夹放入自己使用的工具支持的技能目录

在新对话中调用 `$analog-ic-notes`，提供论文或 PDF，并说明笔记语言与输出目录

> 使用 Analog IC Notes 阅读这篇论文，整理电路分析、测试指标与配图，保留引用，输出中文 Markdown 笔记

## 配置自己的目录

复制 `config.example.json` 为本地的 `config.local.json`，按自己的目录修改

```json
{
  "paths": {
    "papers": "./papers",
    "notes": "./notes",
    "images": "./notes/assets"
  },
  "language": "zh"
}
```

相对路径以配置文件所在目录为基准，也可以填写自己的绝对路径，个人配置单独保存，分享时不打包

配图辅助脚本需要 Python，安装依赖后可运行

```sh
python -m pip install -r requirements.txt
python scripts/paths.py --config config.local.json
python scripts/extract_figures.py paper.pdf --config config.local.json --paper-id my-paper
```

## 保留证据，也保留疑问

来源不足时标注缺失，区分论文实测、仿真和自己的推导，跨论文比较先核对测试条件

技能不会直接执行电路仿真或替你验证设计，生成的笔记仍需要对照原论文检查

## 包内内容

- 模拟 IC 通用论文模板与 Buck 精读模板
- 可独立配置的输入、笔记和图片目录
- 论文图片区域提取与矢量图裁剪辅助脚本
- 指标、引用与配图的检查说明
