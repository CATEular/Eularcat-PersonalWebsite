# 参数修改与读回

首先通过实际安装源码/签名核对 `set_instance_params`。本次本地 bridge 0.7.0 源码显示：

```python
from virtuoso_bridge.virtuoso.schematic.params import set_instance_params

# 先打开并确认目标 schematic；此函数操作当前活动原理图。
applied = set_instance_params(client, "M1", w="2u", l="180n", nf="4", strict=True)
```

- Python 的 `nf=` 是包装层简写，本次源码映射到 PDK CDF 的 `fingers`。不能据此推定所有 PDK 都有同名字段，也不能把“直接写 nf”与“包装层 nf 参数”混为一谈。
- `w` 与 `wf` 的语义由目标 PDK/CDF 决定，不能同时传入并假定回调顺序正确；改变 fingers 后核对总宽、单指宽和网表中的有效倍数。`m` 和 fingers 不等价。实测 nmos2v 同时设置 w=4u/fingers=2 后读回 w=4u、wf=8u，存在派生值不一致风险，因此仅“参数已写入”不能证明有效尺寸正确。尺寸优化前先解决 CDF/网表一致性。
- 使用 PDK 的 CDF callback 更新派生值；只改数据库 property 可能导致显示和净表参数不同。
- 包装层参数过滤可能忽略不在 allowlist 中的字段，使用当前版本支持的严格模式并读回实际应用值。根据目标 master 的 CDF 核对允许参数。
- 修改活动原理图前确认 lib/cell/view，多个窗口下不靠当前窗口猜目标。
- 修改后执行 Check & Save，并从原理图/网表核对数值。标注更新不是电气验证。
- 数值读回按单位归一化比较；实测电阻 `2k` 读回 `2K`、长度 `180n` 读回 `180.0n`，不能用字符串相等判断失败。

参考 [schematic-skill-api.md](../../virtuoso-testbench/references/schematic-skill-api.md) 和 [schematic-python-api.md](../../virtuoso-testbench/references/schematic-python-api.md)。
