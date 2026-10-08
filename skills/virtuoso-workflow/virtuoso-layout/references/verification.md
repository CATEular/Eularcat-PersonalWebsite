# DRC / LVS / PEX 与 GDS

- DRC 检查工艺几何规则；LVS 检查布局提取连接与参考原理图；PEX 生成寄生模型用于后仿真。三者是独立证据。
- 从 PDK/project 获取实际 rule deck、layer map、model sections、允许网格及工具版本。历史验证工艺的宽度/间距/guard-ring 数字不作为其他工艺默认值。
- GDS 导出优先已核验的 `client.layout.export_gds`；不支持时用当前安装工具的官方 batch 接口。传入当前 stream map，区分本机文件与远端文件。见 [layout-python-api.md](layout-python-api.md)。
- 每轮 GDS/DRC/LVS/PEX 使用独立目录；只认可本轮日志与新生成 artifact。不能以已有 GDS 非空推出这次导出成功。
- DRC 输出区分真实违规、排除项和规则/工具设置错误；修复后重跑对应检查。LVS 失败先排查 pins/labels、供电、器件模型、实例参数、层映射和 view 选择。
- PEX 导出后记录其对应布局版本、寄生角点和模型；通过测试平台进行 pre/post-layout 对比。没有实际仿真时不宣称性能保持。
- 不自动修改 rule deck 放宽要求。环境不完整时报告缺项，保留日志和可交付文件。
