# 本机只读证据

优先使用当前环境可用的 Zotero 连接工具。Zotero 本地 API 可位于 `http://127.0.0.1:23119/api/users/0`；只向 localhost 发读取请求。不要硬编码其他人的插件安装路径。

attachment children 可能漏掉批注；不能仅凭 API 返回空列表就断言没有批注。可使用随附 helper 从只读数据库快照核对全部批注。

```sh
python scripts/read_paper.py --query "文章标题片段" --out evidence.json
python scripts/read_paper.py --item-key <parent-item-key> --data-dir <zotero-data-directory> --out evidence.json
```

命令从 skill 目录运行，或将脚本路径替换为实际位置。`--query` 匹配多篇时只返回候选，不挑一篇；`--item-key` 必须是父文献 key。

helper 可从 Windows 用户目录下的 Zotero profile `prefs.js` 中寻找 `extensions.zotero.dataDir`；未找到、多个目录冲突或其他系统时，使用用户确认的 `--data-dir`，不猜文库。

脚本不写源 SQLite。它复制 sqlite 与 WAL/SHM 到临时目录，校验源文件签名在复制前后未变及快照 `quick_check`，通过后才读取；否则停止，请稍后重试。签名检查比较大小和修改时间，不是对源数据库的完整内容校验。

结果包括文献元数据、附件路径、全部非删除批注、position 中 paths、内容 hash。链接附件的相对路径需提供 `--linked-base`（对应用户的 baseAttachmentPath）或人工核实。helper 面向个人文库；它按 key 查到多篇时返回候选，群组条目须通过支持群组的连接工具核实文库及来源。

原文用输出中的真实 PDF 路径读取；用可用的本地 PDF 工具抽取文字，框选和手绘应渲染对应页查看。JSON 仅作本机证据，不直接当笔记交付，也不上传公开仓库。脚本仅用 Python 标准库。
