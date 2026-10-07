---
title: Markdown 渲染测试：公式、代码与技术图
description: 一篇明确标注的测试笔记，用来检查正文、公式、代码、表格、图片和目录的显示。
date: 2026-10-07
updated: 2026-10-07
lang: zh
type: note
category: engineering
tags: [渲染测试, Markdown]
status: published
test: true
---

> **渲染测试**
>
> 这篇笔记仅用于检查网站排版。下面的公式、变量和数据都是显示示例，不代表我的实际设计、仿真或测量结果。

## 正文与层级

技术笔记需要在手机和电脑上都保持可读。这里测试**粗体强调**、*斜体*、`行内代码`，以及中文与 English 混排。

我希望正文有足够的呼吸空间，但不要为追求留白而打断阅读。长段落、图注和参考链接都应该有清晰的层级。

### 一个小问题

如果一段内容还没有想清楚，可以先把问题留在笔记里。它不必看起来已经完整。

## LaTeX 公式

行内公式的排版示例：$x(t)=A\sin(2\pi f t)$。

独立公式示例：

$$
H(s)=\frac{1}{1+s\tau}
$$

较长的公式用于检查手机上的横向滚动：

$$
\mathcal{L}\{a\,x(t)+b\,y(t)\}=a\,X(s)+b\,Y(s),\qquad \int_0^\infty e^{-st}\sin(\omega t)\,dt=\frac{\omega}{s^2+\omega^2}
$$

## 代码块

下面是用于检查 Python 高亮的简单示例：

```python
from pathlib import Path

def list_notes(folder: Path) -> list[Path]:
    """Return Markdown files for a rendering example."""
    return sorted(folder.glob("**/*.md"))

for note in list_notes(Path("content")):
    print(note.name)
```

## 技术表格

这里的表格只检查显示效果，没有电路性能数据。

| 排版对象 | 测试内容 | 期望表现 |
| --- | --- | --- |
| 公式 | 行内与独立 LaTeX | 基线自然，长公式可以滚动 |
| 代码 | Python | 高亮清晰，暗色主题可读 |
| 图片 | 概念插画 | 自适应宽度，保留原始颜色 |
| 链接 | 内部和外部页面 | 可识别，可用键盘访问 |

## 图片与图注

![用于检查图片渲染的芯片概念插画](/assets/knowledge-cover.webp "图 1 · AI 生成的概念插画，仅用于排版测试，并非真实芯片或版图。")

## 引用与链接

> 好的笔记可以保留疑问、失败和尚未完成的理解。这里测试引用块的留白与对比度。

- 内部链接：[IC Schematics Studio 项目介绍](/zh/projects/ic-schematics-studio/)。
- 真实工具：[打开原理图编辑器](https://ic-schematic-studio.pages.dev/#editor)。
- 关于页：[关于 Eularcat](/zh/about/)。

## 阅读后再检查

1. 切换明暗主题，检查代码和公式。
2. 缩窄页面，检查表格与长公式。
3. 点击目录，检查标题定位。
4. 确认图片与图注始终一起显示。

这篇测试笔记之后可以直接删除，或换成自己的真实记录。


## 联系方式

[GitHub](https://github.com/CATEular)
