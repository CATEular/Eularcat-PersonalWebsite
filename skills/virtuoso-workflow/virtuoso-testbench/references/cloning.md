# 测试平台与依赖电路复制

来源为旧 `virtuoso-librarian` 的 TB clone 实践。本套件保留其核心 mechanics，增加目标库/路径/冲突检查、唯一临时文件和显式执行模式。源设计保持只读。

## 使用

```text
python scripts/tb_clone/clone_tb_full.py SRC_LIB SRC_CELL DST_LIB
python scripts/tb_clone/clone_tb_full.py SRC_LIB SRC_CELL DST_LIB --execute
```

第一条只读取层级并报告计划。第二条要求目标库已注册且为空（无 cell 目录）、目标不是 PDK/外部库、实际路径与源库互不包含、库和 cell 名符合工具支持的字符集。名称/路径超出字符集时使用经核验的替代流程，不能删减名字来绕过检查。

## 复制前必须检查

- 外部库默认分类来自模式规则，可按项目核实；只读计划输出全部外部引用。
- 工具扫描 schematic declared `instHeaders`。config-only binding、view switch、Verilog-A include、模型/刺激文件和测量脚本可能引入额外依赖；计划不代表已完整覆盖它们。先补齐这些依赖，复杂 config 不直接执行这个有限范围工具。
- 同名 cell 来自不同源库时一律拒绝，不凭名字判断相同。先显式重命名或分别复制。
- 不删源/目标锁。目标有锁时停止，确认归属后按 Cadence 正常会话流程处理。
- PEX 派生视图和 TB results 默认不打包；这适用于原理图级克隆，不是完整 tapeout/PEX 归档。若 config 用被排除的视图，先改用完整包流程。

## 数据不变量

1. 在 rsync 源头排除 `.cdslck*` 和 SOS markers，避免锁缓存污染。
2. 只处理本次新目标库内的 symlinks，将 SOS cache 文件复制为真实文件；不修改源缓存。缺失 symlink 目标导致复制失败，不能忽略。
3. config 与 Maestro 库引用按字段/绑定范围替换，不全局替换路径文本。缺失文件条件跳过。
4. IC618 的旧工作流使用 delete+recreate 重绑定实例。保留 name、位置、方向、有效 master view；property 从稳定源 view 读取并按 name/type/value 恢复，不经字符串损失类型。
5. 保存前对修改的 schematic 执行 `schCheck`。子 cell 无 schematic 与真实连通性错误分开判断。
6. 结构检查只有在每个要求的 view 都成功打开、每次调用没有 bridge/SKILL 错误且无 stale refs 时才成立。不能把空结果自动解释为“已干净”。

工具遇到失败保留目标和日志，不自动回滚删除。重试选新目标库或明确检查部分复制数据，不用覆盖模式掩盖失败。脚本完成只证明限定范围的克隆检查通过；交付独立复现还需比较网表、实例关键参数、config/ADE 绑定和指定仿真结果。
