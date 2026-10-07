---
document_id: JSSC2004_Lee_Mok_CurrentSensing
title: >-
  A Monolithic Current-Mode CMOS DC–DC Converter With On-Chip Current-Sensing
  Technique
authors:
  - Cheung Fai Lee
  - Philip K. T. Mok
doi: 10.1109/JSSC.2003.820870
process_node: Standard 0.6 µm CMOS (AMS)
vin_range: 3.0V ~ 5.2V (锂离子电池 3.6V 标称)
vout_range: 1.0V ~ 3.3V (< Vin - 0.2V)
iout_max: 500 mA (连续承载 50mA ~ 450mA)
fsw: 300 kHz ~ 1 MHz (实验设定 500 kHz)
topology: Monolithic Synchronous Step-Down Buck Converter
control_mode: Peak Current-Mode PWM Control + Active Slope Compensation
peak_efficiency: '89.5% (@ Vin=3.6V, Vo=2.0V, Io=300mA)'
fom_transient: Sensing Absolute Error < 4% (全片内集成无损采样，无额外引脚与阻抗功耗)
tags:
  - 论文笔记
  - PMIC
  - DCDC_Buck
  - 模拟IC
  - 峰值电流模控制
  - 片上电流采样
  - 虚短电压镜像
  - 斜坡补偿
  - 浮动Class-AB
  - 工艺容差对消
  - 防直通死区控制
status: published
updated: '2026-09-11'
lang: zh
venue: IEEE Journal of Solid-State Circuits (JSSC)
year: 2004
date: '2026-09-11'
description: 片上电流采样与单片电流模 Buck 的论文阅读记录
url: 'https://doi.org/10.1109/JSSC.2003.820870'
type: reading
---


> **论文核心亮点与芯片定位**
> - **行业学术地位**：本文是香港科技大学（HKUST）模拟与电源集成电路名家**莫国泰（Philip K. T. Mok）教授团队**与**李祥辉（Cheung Fai Lee）博士**于 2004 年在顶级期刊 *IEEE Journal of Solid-State Circuits (JSSC)* 上发表的奠基之作。该工作在国际上首次在标准数字 CMOS 工艺下实现了**全片上高精度无损电流采样与片上斜坡叠加技术的全集成单片同步整流 Buck 变换器**，彻底摆脱了传统电流模开关电源对高功耗外置采样电阻（Sense Resistor）、高成本 BiCMOS 工艺或强温漂依赖的功率管导通电阻（$R_{DS(on)}$）采样的束缚。
> - **四大核心技术突破**：
>   1. **基于运算放大器虚短的高精度电流镜像采样结构（Matched Current-Sensing Scheme）**：采用微型检测 PMOS 管（$M_2$）按 $1:1000$ 比例与主功率 PMOS 管（$M_1$）并联，通过片上集成的高增益轨到轨运放构建负反馈电压镜像环路，强制采样管与功率管的漏极节点电压完全钳位一致（$V_A = V_B$），消除了沟道长度调制效应带来的失配。实测在 $300\,\text{mA}$ 负载下**绝对采样误差 $< 4\%$（电流误差 $< 10\,\text{mA}$）**，相比传统方案降低功耗数十毫瓦，且免去了专用的外部引脚。
>   2. **带浮动 Class-AB 输出级的宽摆幅两级折叠共源共栅运放（Two-Stage Op-Amp with Floating Class-AB Stage）**：为满足在宽输入电压（$3.0\,\text{V} \sim 5.2\,\text{V}$）及功率管极小导通压降（仅数十毫伏）条件下的超高采样精度，设计了专门的低压差高增益运算放大器，采用 Monticelli 浮动 Class-AB 输出级，确保反馈环路在纳米级响应速度下稳定维持虚短，并防止节点漂移进入非饱和区。
>   3. **全差分双通道非理想抵消型电压-电流（V-to-I）线性求和网络**：针对电流模 PWM 控制中片上斜坡信号与电感采样信号必须线性相加且不受工艺离散影响的难题，首创由两组完全对称的源极跟随电平移位与源极退化共源放大级组成的差分抵消电路，**不仅消除了源极跟随器阈值电压 $V_{SG}$ 与温度漂移的影响，更使最终合成电流仅取决于片上多晶硅电阻的几何比值（$\frac{R_{sense}}{R_s}$）**，实现了完全免疫绝对电阻工艺角偏差（Process-Independent）的高精度信号叠加。
>   4. **无直通短路功耗的交叉耦合死区控制驱动器与无死锁启动逻辑**：针对单片集成功率管易产生的直通漏电（Shoot-Through Current），采用带反向节点状态交叉反馈的缓冲链，彻底杜绝了高边 PMOS 与低边 NMOS 同时导通造成的瞬态击穿尖峰；同时在脉宽发生器中引入防死锁门控组合逻辑，解决了上电启动初期比较器异常电平导致的 SR 锁存器态混乱。
> - **芯片实测指标速记**：
>   - **工艺制程**：标准 AMS $0.6\,\mu\text{m}$ CMOS 工艺；
>   - **电气规格**：供电输入 $V_{IN} = 3.0\,\text{V} \sim 5.2\,\text{V}$（锂电池 $3.6\,\text{V}$ 标称）；输出电压支持连续动态调节 $V_{OUT} = 1.0\,\text{V} \sim 3.3\,\text{V}$；额定承载负载电流高达 $500\,\text{mA}$；
>   - **效率表现**：在 $50\,\text{mA} \sim 450\,\text{mA}$ 宽负载区间内效率均保持在 $80\%$ 以上，在 $V_{IN} = 3.6\,\text{V}, V_{OUT} = 2.0\,\text{V}, I_{LOAD} = 300\,\text{mA}$ 条件下录得**最高转换效率 $89.5\%$**；
>   - **纹波与面积**：在 $L=4.7\,\mu\text{H}, C_{OUT}=10\,\mu\text{F}$ 滤波条件下输出纹波仅约 $20\,\text{mV}$；控制器核心面积仅为 $0.2575\,\text{mm}^2$（含功率管与全部测试焊盘总面积为 $2.87\,\text{mm}^2$）。

---

## 1. 芯片电气性能与设计指标 (Specs Table)

| 参数类别 | 参数项 (Parameter) | 论文数值 / 实测表现 | 测试条件与备注说明 (Conditions & Notes) |
| :--- | :--- | :--- | :--- |
| **工艺制程** | Process Technology | **AMS 0.6 µm CMOS** | 双层多晶硅、双层金属（2P2M）标准互补工艺 |
| **输入电压** | Input Voltage Range ($V_{IN}$) | **3.0 V ~ 5.2 V** (标称值 3.6 V) | 完美覆盖单节锂离子电池（2.7V~4.2V）及USB供电范围 |
| **输出电压** | Output Voltage Range ($V_{OUT}$) | **1.0 V ~ 3.3 V** ($< V_{IN} - 0.2\,\text{V}$) | 实验分别验证了 $V_{OUT}=1.4\,\text{V}$ ($D<0.5$) 与 $2.1\,\text{V}$ ($D>0.5$) |
| **最大负载电流** | Maximum Load Current ($I_{OUT}$) | **500 mA** | 连续承载电流范围：50 mA ~ 450 mA |
| **开关频率** | Switching Frequency ($f_{SW}$) | **300 kHz ~ 1.0 MHz** (测试 500 kHz) | 通过外部定时电阻 $R_t$ 与电容 $C_t$ 精确设定 |
| **功率电感** | Filter Inductor ($L$) | **4.7 µH** | 外挂微型功率贴片电感 |
| **输出滤波电容** | Output Capacitor ($C_{OUT}$) | **10 µF** | 外挂低 ESR 陶瓷贴片电容 |
| **振荡定时元件** | Timing Resistor / Capacitor | $R_t < 100\,\text{k}\Omega,\, C_t = 22\,\text{pF}$ | 设定充放电电流源与时钟振荡周期 |
| **片上补偿网络** | Compensator Resistor / Capacitor | $R_z < 100\,\text{k}\Omega,\, C_c = 1.0\,\text{nF}$ | 跨导 OTA 单零点-单极点极零对消网络 |
| **电流采样比例** | Current Sensing Ratio ($K_{sense}$) | **1 : 1000** | 功率管 $M_1$（500 fingers）与感知管 $M_2$ 尺寸比 |
| **片上采样电阻** | On-Chip Sensing Resistor ($R_{sense}$)| **400 Ω** | 片内高阻多晶硅（High-Resistive Poly）精密匹配电阻 |
| **电流转电压增益** | Current-to-Voltage Ratio ($k$) | **2.5 A/V** ($0.4\,\text{V/A}$) | $k = 1000 / 400 = 2.5\,\text{A/V}$，定义斜坡叠加换算基准 |
| **采样绝对误差** | Sensing Absolute Error | **< 4%** (实测电流偏差 $<10\,\text{mA}$) | 评估于 $I_L = 300\,\text{mA}$ 标称负载工作点 |
| **峰值转换效率** | Peak Power Efficiency ($\eta_{max}$) | **89.5%** | 测试点：$V_{IN} = 3.6\,\text{V},\, V_{OUT} = 2.0\,\text{V},\, I_{OUT} = 300\,\text{mA}$ |
| **宽载效率保持** | Efficiency Range | **> 80%** (负载 50 mA ~ 450 mA) | 轻载受开关损耗主导，重载受导通损耗主导 |
| **输出纹波电压** | Output Ripple Voltage ($\Delta V_o$) | **~ 20 mV** | 在 $V_{IN}=3.6\,\text{V},\, V_o=2.1\,\text{V}$ 稳态条件测试 |
| **PWM比较器延时**| Comparator Propagation Delay | **~ 15 ns** | 正反馈自举加速，支持高达 1 MHz 调制需求 |
| **功率管物理尺寸**| Power PMOS / NMOS Sizing | PMOS: $20000\,\mu\text{m}/0.6\,\mu\text{m}$<br>NMOS: $8000\,\mu\text{m}/0.6\,\mu\text{m}$ | PMOS 500 fingers ($W=40\,\mu\text{m}$)，NMOS 200 fingers |
| **芯片总面积** | Total Die Size (with Pads) | **2.87 mm²** | 包含全部测试 Pad、打线保护结构与片上功率开关管 |
| **控制器核心面积**| Buck Controller Active Area | **0.2575 mm²** | 仅含核心模拟信号链、采样电路、振荡器与逻辑模块 |

| 电流模降压转换器完整拓扑系统框图 (Fig. 1) | 0.6 µm 芯片实测显微照片与模块版图划分 (Fig. 12) |
| :---: | :---: |
| ![fig01_current_mode_buck_block_diagram](./assets/fig01_current_mode_buck_block_diagram.png) | ![fig12_die_micrograph](./assets/fig12_die_micrograph.png) |
| **图 1**：单片电流模同步 Buck 变换器完整系统架构（包含集成功率级、OTA 极零对消补偿器、振荡与斜坡发生器、差分 V-to-I 叠加求和网络、正反馈 PWM 比较器及驱动缓冲链） | **图 2**：采用 AMS 0.6 µm CMOS 工艺制作的芯片显微照片（总面积 $2.87\,\text{mm}^2$，控制器核心面积仅 $0.2575\,\text{mm}^2$，功率 PMOS/NMOS 对称分布） |

---

## 2. 研究背景与设计痛点 (Motivation & Bottlenecks)

### 2.1 传统电流采样技术的三大瓶颈

在便携式电池供电设备中，峰值电流模脉宽调制（Peak Current-Mode PWM）相比电压模控制具备诸多内在物理优势：
1. **控制环路降阶**：将电感转化为压控受控电流源，二阶共轭复数极点降阶为由输出电容 $C_{OUT}$ 和负载电阻 $R_L$ 构成的单极点系统，极大地简化了环路补偿；
2. **极速输入电压前馈响应**：输入电压波动会直接在电感电流斜率上体现，瞬时改变占空比，无需等待输出误差电容积分延迟；
3. **内在逐周期过流保护（Cycle-by-Cycle Over-Current Protection）**：直接限制误差放大器输出峰值即可严格钳位电感极限峰值电流。

然而，电流模控制的**命门在于如何精确、低功耗且低成本地获取电感电流信号**。在本文发表之前，工业界与学术界主要采用以下三类方案，但均存在严重的物理短板：

| 现有集成变换器主流电流采样方案特性对比 (Table I) |
| :---: |
| ![tab01_overview_existing_current_sensing](./assets/tab01_overview_existing_current_sensing.png) |
| **图 3**：传统电流采样方案对比（外接电阻法、无感积分器法、MOS管导通阻抗采样法） |

```
[方案 1: 串联外置采样电阻 (External Sensing Resistor)]
Inductor Current I_L ───► [ Rsense (0.1~0.2 Ω) ] ───► Load
痛点: 为克服系统失调，需 ΔV ≥ 100 mV。在 500 mA 下功耗达 50 mW! 
严重拉低整机转换效率 5%~10%，且需要专用芯片引脚与昂贵精密外围贴片电阻。

[方案 2: 状态观测器/无感积分器法 (Sensorless / Integrator Method)]
基于电感端电压积分: i_L(t) = (1/L) ∫ (V_in - V_o) dt
痛点: 积分时间常数 RC 必须与电感感值 L 严格对齐 (RC = L/DCR)。
片外电感与片内 RC 存在高达 ±20%~±30% 的非相关制造容差与温漂，精度极差且拓扑重构繁复。

[方案 3: 功率管导通阻抗采样 (R_DS(on) Sensing)]
利用功率开关管工作在线性区的等效电阻采样: V_sense = I_L * R_DS(on)
痛点: R_DS(on) 具有高达 +5000 ppm/°C 的剧烈正温度系数，且随输入栅压强非线性变化。
深线性区小电阻压降微弱（仅十几毫伏），极易被开关地弹噪声湮灭，精度恶化。
```

### 2.2 本文切入点与核心创新动机

针对上述困境，作者明确提出了在**标准数字 CMOS 工艺**下实现高精度、完全无损且工艺免疫的单片集成解决方案：

> **原文核心动机论述 (Verbatim Quote)**
> *"In order to provide a low-cost low-power and fully integrated CMOS power module for battery-operated applications, a monolithic current-mode DC–DC buck converter with novel on-chip current sensor for feedback control has been fabricated with a standard commercial 0.6-µm CMOS process... All power switches, feedback control circuit, and current-sensing circuit are fabricated on-chip. Only one off-chip inductor and one off-chip capacitor are needed at the power stage, and no off-chip inductor current sensor is needed; thus reducing the number of I/O pins and the number of reactive components needed for the converter... In order to have an accurately sensed current for current-mode PWM converter, a monolithic current-sensing technique, which is not strongly dependent on parameter variations, such as temperature, operating frequency and external components, is mandatory."*
> 
> **【核心要义解读】**：莫国泰教授团队在此确立了本工作的根本立论：在便携式单节锂电池供电（$3.0\,\text{V} \sim 5.2\,\text{V}$）体系中，电源芯片的终极演进方向是**单片高集成度与最低物料清单（BOM）成本**。传统的 BiCMOS 采样技术工艺昂贵，而传统 CMOS 方案要么功耗过大，要么严重受制于温漂与无源元件容差。本文的核心目标正是通过严谨的模拟集成电路拓扑创新，在系统内部构建“虚短电压镜像”与“工艺容差对消网络”，实现精度优于 $4\%$、无额外引脚、无外围器件且无高功耗损耗的完美片上电流感知。

---

## 3. 系统拓扑与电流模控制架构 (Topology & Control Architecture)

### 3.1 峰值电流模工作机理与次谐波振荡抑制

| 次谐波振荡与斜坡补偿扰动抑制波形对比 (Fig. 2) |
| :---: |
| ![fig02_subharmonic_oscillation_and_compensation](./assets/fig02_subharmonic_oscillation_and_compensation.png) |
| **图 4**：(a) 无斜坡补偿时占空比 $D > 0.5$ 导致的电感电流扰动发散；(b) 引入补偿斜坡 $m_c$ 后电感电流扰动的收敛稳定过程 |

在峰值电流模控制的降压变换器中，每个开关周期开始时，时钟信号将 SR 锁存器置位（$S=1$），高边主功率 PMOS 管 $M_1$ 开启，电感电流以斜率 $m_1$ 线性上升：
$$m_1 = \frac{V_{IN} - V_{OUT}}{L} \tag{13}$$

当检测到的电流信号与斜坡信号之和达到误差放大器输出电压 $V_c$ 时，比较器翻转，SR 锁存器复位（$R=1$），$M_1$ 关断，低边同步整流 NMOS 管 $M_3$ 导通，电感电流以斜率 $-m_2$ 线性下降：
$$m_2 = \frac{V_{OUT}}{L} \tag{14}$$

#### 次谐波振荡的数学机理推导
当稳态占空比 $D = \frac{V_{OUT}}{V_{IN}} > 0.5$ 时，若初始电感电流产生微小扰动 $\Delta i_L(0)$，在无外加斜坡补偿的情况下，经过一个周期 $T$ 后，电流扰动的传播规律为：
$$\Delta i_L(T) = -\left(\frac{m_2}{m_1}\right) \Delta i_L(0) = -\left(\frac{D}{1-D}\right) \Delta i_L(0) \tag{15}$$

- 当 $D < 0.5$ 时，$\left|\frac{D}{1-D}\right| < 1$，电流扰动逐周期几何级数衰减收敛；
- 当 $D > 0.5$ 时，$\left|\frac{D}{1-D}\right| > 1$，电流扰动逐周期反相几何级数发散，导致开关脉宽在长脉冲与短脉冲之间交替振荡，系统产生**二分之一开关频率（$f_{SW}/2$）的次谐波自激振荡**。

#### 斜坡补偿的设计准则 (Equations 4 & 5)
为彻底抑制次谐波振荡，必须向电流比较节点叠加一个斜率为 $m_c$ 的人工补偿斜坡（Compensation Ramp）。扰动传递因子修正为：
$$\alpha = -\frac{m_2 - m_c}{m_1 + m_c} \tag{16}$$
为保证系统稳定，必须满足 $|\alpha| < 1$，其边界临界条件为：
$$m_c \ge \frac{1}{2} m_{2,\max} = \frac{1}{2} \cdot \frac{V_{o,\max}}{L} \quad (\text{A/s}) \tag{4}$$

若取 $m_c = m_2$，则扰动传递因子 $\alpha = 0$，系统将在单个开关周期内瞬间消除全部电流扰动，达成**无差拍控制（Deadbeat Control）**。

在电路实现中，由于片上振荡器产生的斜坡为电压信号（摆幅 $V_H - V_L$），其在时间周期 $T$ 内的电压斜率为：
$$\text{slope of compensation ramp} = \frac{V_H - V_L}{T} = \frac{m_c}{k} \quad (\text{V/s}) \tag{5}$$
其中 $k$ 为电流模系统的电流-电压转换比率（$\text{A/V}$）。在本文架构中，电感电流按 $1:1000$ 采样并流经 $R_{sense} = 400\,\Omega$ 电阻，因此系统的电流-电压换算比率为：
$$k = \frac{1000}{R_{sense}} = \frac{1000}{400\,\Omega} = 2.5\,\text{A/V} \quad (0.4\,\text{V/A}) \tag{17}$$
该严谨的比例换算为后续振荡器阈值 $V_H, V_L$ 的取值奠定了坚实的理论基石。

---

### 3.2 误差放大器与零极点对消补偿网络 (Pole-Zero Cancellation Compensator)

| 极零对消误差放大补偿网络原理图 (Fig. 3) |
| :---: |
| ![fig03_pole_zero_cancellation_compensator](./assets/fig03_pole_zero_cancellation_compensator.png) |
| **图 5**：基于跨导放大器（OTA）与串联 $R_z-C_c$ 阻抗网络的单极点-单零点误差放大器 |

电流模功率级的控制-输出传递函数表现为主极点位于由输出滤波电容 $C$ 和负载电阻 $R_L$ 决定的低频处：
$$\omega_{p,load} = \frac{1}{R_L C} \tag{18}$$
当负载电阻增大（轻载）时，该极点向超低频移动。为扩展系统闭环带宽并提升瞬态响应速度，论文摒弃了牺牲带宽的主极点主导补偿，采用**极零对消技术（Pole-Zero Cancellation）**。

图 5 所示补偿器的复频域传递函数由式 (1) 给出：
$$A(s) = \frac{v_a}{b v_o} \approx g_m R_o \frac{1 + s C_c R_z}{1 + s C_c R_o}, \quad \text{for } R_o \gg R_z \tag{1}$$
- **直流增益**：$A_0 = g_m R_o$；
- **主极点位置**：$\omega_{p1} = \frac{1}{R_o C_c}$（由 OTA 超高输出阻抗 $R_o$ 与补偿电容 $C_c$ 决定）；
- **补偿零点位置**：$\omega_{z1} = \frac{1}{R_z C_c}$。

设计中将补偿零点 $\omega_{z1}$ 精确对齐在最大负载电阻 $R_{L,\max}$（最恶劣工况）对应的功率主极点 $\omega_{p,load}$ 处，使得环路增益以标准的 $-20\,\text{dB/dec}$ 单极点斜率平稳穿越，保证闭环单位增益带宽设定在开关频率的 $20\%$ 以下（避免放大开关输出纹波），并获得充足的相位裕度（$\text{PM} > 60^\circ$）。

---

## 4. 晶体管级关键子电路创新 (Transistor-Level Subcircuits)

### 4.1 高精度片上无损电流采样传感器 (On-Chip Current Sensor)

| 提出的单片集成电流采样电路原理图 (Fig. 5) |
| :---: |
| ![fig05_proposed_current_sensing_circuit](./assets/fig05_proposed_current_sensing_circuit.png) |
| **图 6**：基于高增益运放虚短电压镜像的低损耗片上电流检测电路（匹配管 $M_2$、钳位运放、微偏置消除管 $M_{cs1}\sim M_{cs5}$ 及多晶硅采样电阻 $R_{sense}$） |

#### 4.1.1 电路工作机理与虚短电压镜像
图 6 为本文最具里程碑意义的核心创新电路。主功率开关 PMOS $M_1$（尺寸极大，承载安培级瞬态电流）与采样 PMOS $M_2$ 共用源极并连接至供电电源 $V_g$。采样管 $M_2$ 的栅极常接地（在 ON-state 导通），其纵横比与功率管严格成比例：
$$\left(\frac{W}{L}\right)_{M1} : \left(\frac{W}{L}\right)_{M2} = 1000 : 1 \tag{19}$$

若能使 $M_2$ 的漏极节点电压 $V_B$ 与 $M_1$ 的漏极节点电压 $V_A$ 完全相等，则由于两管具有完全一致的 $V_{GS} = -V_g$ 和 $V_{DS}$，两者的漏极电流密度将严格相等，从而实现理想的无损分流：
$$I_s = \frac{I_L}{1000} \tag{20}$$

为此，电路引入了一个高增益运算放大器，将反相输入端接至节点 $A$（通过保护开关 $M_{s1}$），同相输入端接至节点 $B$。运放输出驱动两个共栅 NMOS 管 $M_{cs4}$ 与 $M_{cs5}$，形成深度的负反馈闭环：
- 若 $V_B > V_A$，运放输出升高，增大 $M_{cs5}$ 的栅压，抽取更多电流下拉 $V_B$；
- 闭环高开环增益迫使节点 $A$ 与节点 $B$ 达成高度精确的**虚短（Virtual Short, $V_A = V_B$）**。

> **原文电路原理论述 (Verbatim Quote)**
> *"The current sensor is realized by a matched PMOS transistor $M_2$ with the aspect ratio much smaller than that of the power PMOS transistor $M_1$... In order to achieve an accurate current sensor, an opamp is used to enforce the same voltage at node A and node B... As a result, the drain-to-source voltage $V_{DS}$ of transistors $M_1$ and $M_2$, as well as their drain current density, are almost the same... As the sensed inductor current is scaled down, the power loss in the sensing circuit is significantly reduced to improve the efficiency of the converter. An opamp is used as a voltage mirror such that the sensing current $I_{\text{sense}}$ is matched to the inductor current $I_L$."*
> 
> **【电路精髓深度剖析】**：传统 SenseFET 采样往往因缺乏运放高增益闭环强行钳位，受限于功率开关管工作在线性区时漏极电位的快速跳变，导致检测管进入饱和区而功率管在线性区，产生高达数十百分比的严重电流失配。本文通过专用高带宽折叠运放构建的有源电压镜像（Active Voltage Mirror），在动态开关全周期内严格维持两管等电位，将电流采样精度提升至学术界前所未有的水准。

#### 4.1.2 静态微偏置电流对消与关断相电平保护
为保障运放输入级在电感电流过零甚至轻载时依然能够建立正常的共模直流偏置，电路在节点 $A$ 和节点 $B$ 分别引入微小且完全相等的偏置电流源 $I_1$ 与 $I_2$（由 $M_{cs1}, M_{cs2}, M_{cs3}$ 镜像产生，$I_1 = I_2$）。
此时，流经共栅管 $M_{cs5}$ 的总电流为 $I_s + I_2$。在采样电阻支路中，MOS 管 $M_{rs}$ 构成电流镜，将抽取的 $I_2$ 精确扣除：
$$I_{\text{sense}} = I_s + I_2 - I_2 = I_s = \frac{I_L}{1000} \tag{21}$$
最终，流经片内高阻多晶硅电阻 $R_{\text{sense}} = 400\,\Omega$ 的电流纯净等同于缩放后的电感电流，产生精确的采样电压信号：
$$V_{\text{sense}} = I_{\text{sense}} R_{\text{sense}} = \frac{I_L}{1000} R_{\text{sense}} \tag{2}$$

此外，由于降压变换器仅在导通相（ON-state，即电感电流上升沿）需要峰值电流信号用于 PWM 调制，在关断相（OFF-state，$\bar{Q}=\text{High}$），开关管 $M_{s1}$ 关断，而开关管 $M_{s2}$ 导通将节点 $V_A$ 直接强行拉至电源轨 $V_g$。这不仅彻底阻断了关断相续流时负压对采样运放输入管的倒灌损伤，更将关断期间采样支路的动态功耗彻底冻结。

---

### 4.2 浮动 Class-AB 两级低压差高增益运算放大器 (Floating Class-AB Op-Amp)

| 两级折叠共源共栅 Class-AB 运放原理图 (Fig. 6) |
| :---: |
| ![fig06_two_stage_opamp_class_ab](./assets/fig06_two_stage_opamp_class_ab.png) |
| **图 7**：集成于电流采样环路中的高增益运放（左侧为自偏置 Cascode 偏置核，中间为 PMOS 差分折叠输入级，右侧为 Monticelli 浮动 Class-AB 宽摆幅输出级） |

电流检测环路对内部运放提出了极其严苛的指标要求：
1. **输入共模覆盖高供电轨**：由于采样发生在高端开关管，输入电压接近电源轨 $V_g$（仅相差 $V_{DS} \approx 10\,\text{mV} \sim 100\,\text{mV}$），因此必须采用 **NMOS 差分输入对管（$M_1, M_2$）**；
2. **极高直流增益**：为使 $V_A$ 与 $V_B$ 的静态电位失配 $< 1\,\text{mV}$，运放开环直流增益必须 $> 70\,\text{dB}$；
3. **宽输出动态摆幅**：运放输出端需要驱动 NMOS 镜像管 $M_{cs4}, M_{cs5}$，且必须克服阈值电压降并确保器件始终处于饱和区。

为此，论文采用了经典的 **Monticelli 浮动 Class-AB 两级运算放大器架构**：
- **输入级与折叠 Cascode**：$M_1, M_2$ 接收输入差分信号，电流注入折叠共源共栅负载 $M_5, M_6$ 与 $M_7, M_8$，提供极高的单级开环增益；
- **浮动 Class-AB 控制核**：由晶体管 $M_{o1}, M_{o2}, M_{o3}, M_{o4}$ 构成紧凑的浮动电压源偏置，直接跨接在输出级 PMOS $M_{o9}$ 与 NMOS $M_{o10}$ 的栅极之间；
- **大信号压摆率增强**：Class-AB 输出级使得运放在承受大动态跳变瞬态时，输出推挽电流不受静态尾电流限制，实现极高的压摆率（Slew Rate）与纳秒级快速恢复，避免在开关换向瞬间丢失采样瞬态精度；
- **密勒极点分裂补偿**：由集成片上电容 $C_c$ 与由传输门构成的调零电阻 $M_{nc}, M_{pc}$ 构成高频超前补偿，彻底消除右半平面零点（RHP Zero），确保闭环相位裕度 $> 65^\circ$。

---

### 4.3 正反馈高速 PWM 比较器与标准 Cascode OTA

| 正反馈高速比较器原理图 (Fig. 7) | 标准宽摆幅 Cascode OTA 原理图 (Fig. 4) |
| :---: | :---: |
| ![fig07_comparator_schematic](./assets/fig07_comparator_schematic.png) | ![fig04_cascode_ota_schematic](./assets/fig04_cascode_ota_schematic.png) |
| **图 8**：带交叉耦合正反馈自举负载的高速迟滞比较器（延时仅 15 ns） | **图 9**：用于电压反馈环路误差放大与极零对消补偿的单级全共源共栅 OTA |

#### 4.3.1 高速比较器正反馈自举机理 (Equation 3)
图 8 所示比较器用于 PWM 调制以及振荡器迟滞判决。输入差分对 $M_1, M_2$ 驱动包含正反馈交叉耦合晶体管 $M_5, M_6$ 的有源负载。
该正反馈增益级的开环电压增益由式 (3) 严格定义：
$$A_v = \sqrt{\frac{\mu_p \left(\frac{W}{L}\right)_1}{\mu_n \left(\frac{W}{L}\right)_3}} \frac{1}{1 - \alpha} \tag{3}$$
其中 $\alpha$ 为正反馈自举系数：
$$\alpha = \frac{\left(\frac{W}{L}\right)_5}{\left(\frac{W}{L}\right)_3} \tag{22}$$
- 当设计满足 $\alpha < 1$（且逼近 1）时，分母 $1-\alpha$ 急剧趋近于零，使得比较器在小信号差分输入跨越零点时瞬间激发出超高增益；
- 输出后级串联高速互补倒相链（$M_9 \sim M_{18}$），不仅实现了轨到轨方波陡峭边沿整形，更有效隔离了后端逻辑门大电容对内部高阻节点的反冲影响，使得**整体信号传播延时被严格压缩至 15 ns 左右**，完美支撑 1 MHz 开关调制。

---

### 4.4 振荡器与片上斜坡发生器 (Oscillator & Ramp Generator)

| 振荡器与斜坡发生电路原理图 (Fig. 8) |
| :---: |
| ![fig08_oscillator_and_ramp_generator](./assets/fig08_oscillator_and_ramp_generator.png) |
| **图 10**：时钟与补偿斜坡同步发生器（包含运放基准 V-I 充电级、外接定时电容 $C_t$、高速放电开关 $M_4$ 与双门限迟滞比较器环路） |

图 10 展示了高精度同步振荡器与斜坡生成电路：
1. **基准电荷泵恒流充电**：外部参考电压 $V_{ref}$ 加载至由运放和外部贴片电阻 $R_t$ 构成的压控电流源，生成极其精准且无温漂的恒定充电电流：
   $$I_t = \frac{V_{ref}}{R_t} \tag{23}$$
2. **电流积分上升**：电流 $I_t$ 经由 PMOS 电流镜 $M_1, M_2$ 注入定时电容 $C_t$，产生线性上升的锯齿波斜坡：
   $$\frac{d V_{\text{ramp}}}{dt} = \frac{I_t}{C_t} = \frac{V_{ref}}{R_t C_t} \tag{24}$$
3. **双门限迟滞翻转与瞬态快速放电**：
   - 当斜坡电压爬升至上限阈值 $V_H$（表 II 设定为 $0.9\,\text{V}$）时，上位比较器翻转将 SR 锁存器置位，导通大尺寸下拉 NMOS $M_4$；
   - 电容 $C_t$ 经由 $M_4$ 以极高电流极速放电，斜坡骤跌；
   - 当跌落至下限阈值 $V_L$（表 II 设定为 $0.5\,\text{V}$）时，下位比较器翻转将锁存器复位，关断 $M_4$，重新开始新一轮充电积分；
4. **频率与斜率的一致性同步**：
   $$f_{SW} \approx \frac{I_t}{C_t (V_H - V_L)} = \frac{V_{ref}}{R_t C_t (V_H - V_L)} \tag{25}$$
   通过外挂 $R_t, C_t$，系统不仅能够灵活定制 $300\,\text{kHz} \sim 1\,\text{MHz}$ 的工作频率，而且保证斜坡电压的斜率与开关周期在物理机制上保持天然的刚性同步。

---

### 4.5 工艺容差对消型电压-电流 (V-to-I) 线性转换与叠加求和网络

在电流模控制中，电感采样信号 $V_{\text{sense}}$ 与振荡斜坡信号 $V_{\text{ramp}}$ 均为单端电压信号。若直接采用传统电阻网络相加，会引入严重的无源阻抗衰减、电荷再分配及极大的温漂误差。为此，论文设计了图 11 所示的**差分工艺容差对消型 V-to-I 转换网络**：

| 工艺容差对消型 V-to-I 转换器原理图 (Fig. 9) |
| :---: |
| ![fig09_voltage_to_current_converter](./assets/fig09_voltage_to_current_converter.png) |
| **图 11**：完全消除源极跟随器阈值电压 $V_{SG}$ 且抵消多晶硅电阻工艺偏差的差分抵消式 V-to-I 线性转换器 |

#### 4.5.1 单通道非理想转换特性推导 (Equations 6 ~ 8)
图 11 右侧虚线框内展示了单路非理想 V-I 转换单元，由第一级 PMOS 源极跟随器（$M_1$）与第二级带源极负反馈退化的 NMOS 共源级（$M_2, R_s$）级联而成。
由于输入电压（$300\,\text{mV} \sim 1000\,\text{mV}$）较低，无法直接驱动高阈值的 NMOS，第一级源极跟随器天然承担了**直流电平抬升（DC Level Shifter）**的功能：
$$V_A = V_{\text{in}} + V_{SG1} \tag{6}$$
其中晶体管 $M_1$ 的衬底与其源极直接相连，彻底根除了由于体效应（Body Effect）带来的非线性失真。

第二级 NMOS $M_2$ 串联源极退化电阻 $R_s$。当环路设计满足深度负反馈条件 $g_{m2} R_s \gg 1$ 时，等效跨导为：
$$G_{m2} = \frac{I_1}{V_A} = \frac{g_{m2}}{1 + g_{m2} R_s} \approx \frac{1}{R_s} \tag{7}$$
因此第一支路拉出的总电流 $I_1$ 为：
$$I_1 = \frac{V_A}{R_s} = \frac{V_{\text{in}} + V_{SG1}}{R_s} = \frac{V_{\text{in}}}{R_s} + \frac{V_{SG1}}{R_s} \tag{8}$$
式 (8) 清楚地揭示了一个致命缺陷：输出电流中包含了一个由晶体管制造工艺和温度强相关的寄生非线性偏移项 $\frac{V_{SG1}}{R_s}$！

#### 4.5.2 双差分对称抵消拓扑 (Equations 9 ~ 10)
为了彻底根除这一系统偏差，论文在左侧并联了一个**结构完全相同但输入接地（$V_2 = 0\,\text{V}$）的参考抵消通道**（$M_3, M_4, R_s$）：
左侧第二级电流 $I_2$ 严格等于纯直流电平项：
$$I_2 = \frac{V_{SG3}}{R_s} \tag{9}$$
随后，通过顶部的高精度 PMOS 电流镜（$M_5 \sim M_8$）执行电流镜像与代数相减：
$$I_{\text{out}} = I_1 - I_2 = \left(\frac{V_{\text{in}}}{R_s} + \frac{V_{SG3}}{R_s}\right) - \frac{V_{SG1}}{R_s} \tag{10}$$
由于版图共模匹配使得 $M_1$ 与 $M_3$ 偏置及尺寸完全一致（$V_{SG1} = V_{SG3}$），寄生阈值项被**完全对消剔除**：
$$I_{\text{out}} = \frac{V_{\text{in}}}{R_s} \propto V_{\text{in}} \tag{10'}$$

#### 4.5.3 绝对电阻工艺角（Corner）离散的终极免疫机制 (Equations 11 ~ 12)
采样检测电阻 $R_{\text{sense}}$ 上的电压降由式 (11) 给出：
$$V_{\text{sense}} = I_{\text{sense}} R_{\text{sense}} \tag{11}$$
将该采样电压输入至图 11 所示的差分抵消型 V-I 转换网络，其输出电流为：
$$I_{\text{out}} = \frac{V_{\text{sense}}}{R_s} = I_{\text{sense}} \left(\frac{R_{\text{sense}}}{R_s}\right) \tag{12}$$

> **工艺免疫精髓 (Process-Independent Invariance)**
> **式 (12) 具有极高的模拟电路设计哲学美感**：
> 最终进入求和节点的检测电流不仅与复杂的晶体管阈值参数无关，而且**完全取决于片上两个同材质高阻多晶硅电阻的比值 $\frac{R_{\text{sense}}}{R_s}$**！
> 在半导体制造中，尽管片内多晶硅电阻的绝对阻值在 Slow/Fast 工艺角下可能产生高达 $\pm 20\% \sim \pm 30\%$ 的剧烈离散，但通过标准模拟共质心版图（Common-Centroid Layout）与虚拟保护环，**几何电阻比值的相对匹配精度能够轻松控制在 $0.1\% \sim 0.5\%$ 以内**！这意味着整个电流感知与斜坡求和信号链对半导体制造工艺离散展现出极强的鲁棒性。

两个独立的 V-to-I 模块分别将电感采样信号与振荡斜坡信号转换为对应的电流，最终在同一个无源多晶硅负载电阻 $R_f$ 上汇聚相加，产生用于 PWM 比较的合成控制电压 $V_c$（见图 1），实现了极为优雅的高线性度无损信号叠加。

---

### 4.6 交叉耦合防直通驱动缓冲级与防死锁脉宽发生器

| 防直通短路功耗 CMOS 栅驱动缓冲器 (Fig. 10) | 防死锁门控 SR 脉宽发生器 (Fig. 11) |
| :---: | :---: |
| ![fig10_cmos_buffer_without_shoot_through](./assets/fig10_cmos_buffer_without_shoot_through.png) | ![fig11_pulsewidth_generator_logic](./assets/fig11_pulsewidth_generator_logic.png) |
| **图 12**：带内部节点交叉反馈的自适应防直通驱动器（杜绝功率管交叠导通损耗） | **图 13**：带组合门控屏蔽保护的改进型 SR 锁存器（消除启动锁死态） |

#### 4.6.1 防直通短路驱动机理 (Fig. 10)
单片集成的同步整流 Buck 变换器中，高边 PMOS（$W=20000\,\mu\text{m}$）与低边 NMOS（$W=8000\,\mu\text{m}$）具有极大的栅极寄生电容。若采用常规简单反相器链驱动，在换向瞬间两管会同时处于微导通状态，引发**从输入电源 $V_g$ 直通到地线的毁灭性短路直通电流（Shoot-Through Current）**，不仅产生数十毫瓦的额外无效功耗，还会诱发严重的地弹噪声。

图 12 采用了由 Yoo 提出的自适应交叉反馈驱动器拓扑：
- 高边驱动节点 $N_1$ 的状态直接交叉反馈至低边驱动管 $M_7$ 的栅极；
- 低边驱动节点 $N_2$ 的状态直接交叉反馈至高边驱动管 $M_4$ 的栅极；
- **先断后通逻辑（Break-Before-Make）**：在高边 PMOS 开启之前，驱动器强制等待低边 NMOS 栅压彻底拉低至关断阈值以下；反之亦然。这在没有额外数字死区延时发生器的极简硅片面积下，自适应达成了零直通短路功耗。

#### 4.6.2 启动防死锁门控逻辑 (Fig. 11)
在传统电流模 PWM 变换器启动（Startup）阶段，输出电压尚未建立，$V_o \approx 0$，导致误差放大器输出 $V_c$ 处于低电平，而电感采样与斜坡求和信号可能瞬间高过 $V_c$，导致比较器复位端 $R$ 持续为高。此时若振荡器置位脉冲 $S$ 恰好到来，传统的 NOR 架构 SR 锁存器将面临 $S=1, R=1$ 的非法禁用态，引发输出逻辑不定态或系统锁死。

图 13 在锁存器输入前端嵌入了一组由 AND 和 NAND 构成的门控对消网络：
- 当 $R$ 和 $S$ 同时为高时，NAND 门输出变低，直接截断 AND 门的输出，强制将输入重置为合法的单一置位态；
- 确保系统在全电源电压范围、全负载上电瞬态下输出互补控制信号 $Q$ 与 $\bar{Q}$ 始终具备唯一的确定性，彻底铲除了启动异常死锁隐患。

---

## 5. 芯片实测结果与 SOTA 对比 (Silicon Results & FoM)

### 5.1 实测测试平台配置

| 芯片实验测试系统接线原理图 (Fig. 13) | 外部测试无源元件与基准电压配置 (Table II) |
| :---: | :---: |
| ![fig13_experimental_setup](./assets/fig13_experimental_setup.png) | ![tab02_component_values](./assets/tab02_component_values.png) |
| **图 14**：实验台测试接线拓扑（展示片内模块与片外 $L, C, R_t, C_t, R_z, C_c$ 的精密互连） | **图 15**：实测环境关键元器件取值与基准偏置电位一览表 |

实测平台基于图 14 建立：采用标称锂电池输入 $V_{IN} = 3.6\,\text{V}$，外挂 $L = 4.7\,\mu\text{H}$ 贴片电感与 $C_{OUT} = 10\,\mu\text{F}$ 陶瓷电容。斜坡定时电阻取 $R_t = 12\,\text{k}\Omega$，电容取 $C_t = 22\,\text{pF}$，标定开关频率为 $500\,\text{kHz}$。

---

### 5.2 稳态波形全面解析：宽占空比与次谐波免疫验证

| 大占空比稳态测试波形 ($D > 0.5, V_o = 2.1\,\text{V}$) (Fig. 14) | 小占空比稳态测试波形 ($D < 0.5, V_o = 1.4\,\text{V}$) (Fig. 15) |
| :---: | :---: |
| ![fig14_steady_state_measurements_d_gt_0p5](./assets/fig14_steady_state_measurements_d_gt_0p5.png) | ![fig15_steady_state_measurements_d_lt_0p5](./assets/fig15_steady_state_measurements_d_lt_0p5.png) |
| **图 16**：$V_{OUT} = 2.1\,\text{V}$ ($D \approx 0.58 > 0.5$) 下的实测波形：(a) 电感电流与片上采样电压波形完全重合；(b) 开关节点 $V_x$ 方波；(c) 直流输出电压；(d) 交流输出纹波（仅 20 mV） | **图 17**：$V_{OUT} = 1.4\,\text{V}$ ($D \approx 0.39 < 0.5$) 下的实测波形：开关周期极其稳定，无任何双周期跳变或抖动 |

#### 实验波形核心结论剖析：
1. **采样波形的高度保真度**：
   观察图 16(a) 与图 17(a) 中的曲线 A（片上检测电压 $V_{\text{sense}}$）与曲线 B（通过外部高频电流探头实测的真实电感电流 $I_L$）：
   - 在高边管开通期间，片上感知电压 $V_{\text{sense}}$ 呈现出近乎完美的线性上升三角形波形，其斜率、转折点与外部真实电感电流完全一致；
   - 在关断相，保护开关动作使检测端电压迅速归零，杜绝杂散电荷积累；
   - 经高精度采样数据标定，**片上采样信号与真实电感电流的绝对满量程误差 $< 4\%$（在 $300\,\text{mA}$ 负载下误差幅值 $< 10\,\text{mA}$）**。这雄辩地证实了虚短运放与有源电压镜像的高保真度。
2. **次谐波振荡彻底根除**：
   在图 16 所示的 $V_o = 2.1\,\text{V}$ 工况下，稳态占空比高达 $D = 2.1/3.6 \approx 58.3\% > 50\%$。波形显示开关节点 $V_x$ 的方波脉宽整齐划一，相邻开关周期间没有任何高低交替或周期倍增振荡，证实了式 (4) 设计的补偿斜坡成功抑制了次谐波失稳。
3. **优异的输出纹波抑制**：
   图 16(d) 实测交流输出纹波电压仅为 **$20\,\text{mV}_{p-p}$**，说明电流控制环路具备良好的动态抗扰度与低噪声基底。

---

### 5.3 转换效率与功率损耗分布 (Efficiency & Power Loss)

| 实测功率转换效率随负载电流变化曲线 (Fig. 16) | 芯片整体实测性能规格汇总 (Table III) |
| :---: | :---: |
| ![fig16_efficiency_vs_load](./assets/fig16_efficiency_vs_load.png) | ![tab03_chip_performance](./assets/tab03_chip_performance.png) |
| **图 18**：标称 $V_{IN}=3.6\,\text{V}, V_o=2.0\,\text{V}$ 下的转换效率曲线（峰值达 89.5%） | **图 19**：芯片综合测试指标卡片（覆盖工艺、频段、效率与面积） |

图 18 展示了芯片在标称工作点（$V_{IN}=3.6\,\text{V}, V_{OUT}=2.0\,\text{V}$）下的效率实测曲线：
- **峰值效率**：在额定中载 $I_{LOAD} = 300\,\text{mA}$ 处录得**最高转换效率 $89.5\%$**；
- **重载区损耗分析（$I_L > 300\,\text{mA}$）**：效率曲线呈现平缓下降，主要由功率开关管的导通阻抗损耗 $I_{rms}^2 (R_{on,P} \cdot D + R_{on,N} \cdot (1-D))$ 及电感寄生 DCR 损耗主导；
- **轻载区损耗分析（$I_L < 300\,\text{mA}$）**：由于芯片采用固定频率 PWM 模式（未引入脉冲跨周期跳跃 PFM），功率开关管栅极电荷充放电损耗 $f_{SW} (Q_{g,P} + Q_{g,N}) V_{IN}$ 及控制模拟核心静态电流损耗占比上升，但即使在 $50\,\text{mA}$ 的极轻载下，转换效率依然坚挺在 **$80.4\%$** 以上。

> **原文测试论断 (Verbatim Quote)**
> *"The current-mode DC–DC buck converter has been implemented with a standard 0.6-µm CMOS process... The size of the whole chip is 2.87 mm² and the buck controller is 0.2575 mm²... The results show that the converter regulates properly for different duty ratios without any subharmonic oscillation. The sensing signal shown in Figs. 14 and 15 are matched to the inductor current for current-mode control. In fact, the current-sensing circuit performs accurately and the absolute error between the sensing signal and the scaled inductor current is less than 4%, corresponding to 10 mA with load current of 300 mA. This absolute error is mainly due to the mismatch of transistors in the sensing circuit... The maximum efficiency is 89.5% at loading current 300 mA."*
> 
> **【测试结果评估】**：作者通过详实的实验数据证明：所提出的片上有源电流感知结构在达成 $<4\%$ 工业级采样精度的同时，丝毫没有牺牲整体转换效率；控制器核心仅占用微小的 $0.2575\,\text{mm}^2$ 硅片面积，在经济性、能效与控制稳定性之间达成了极佳的综合平衡。

---

### 5.4 关键学术成果横向对比 (Benchmark Table)

| 对比性能指标 (Metric) | 本文 (Lee & Mok, JSSC 2004) | Smith et al. (TCAS-I 2000) [17] | Givelin et al. (IEE 1995) [21] | Midya et al. (PESC 1997) [16] |
| :--- | :--- | :--- | :--- | :--- |
| **发表来源** | **IEEE JSSC 2004** | IEEE TCAS-I 2000 | IEE Proc. CDS 1995 | IEEE PESC 1997 |
| **制造工艺** | **0.6 µm Standard CMOS** | 1.2 µm CMOS | BiCMOS Process | 离散元器件 / 宏模型 |
| **电流采样机制** | **单片有源虚短 PMOS 比例镜像** | 功率管 $R_{DS(on)}$ 导通压降 | BiCMOS 比例电流镜 | 状态无感无损观测器 |
| **采样精度 / 误差** | **高精度 (< 4% 绝对误差)** | 精度极差 (强温漂与非线性) | 中等 (依赖双极晶体管) | 较差 (强依赖外围 L 容差) |
| **额外引脚与器件** | **完全零额外引脚 / 零外围器件** | 需专用采样运放与引脚 | 需要额外集成管脚 | 需精准匹配积分 RC 网络 |
| **输入电压 ($V_{IN}$)**| **3.0 V ~ 5.2 V** (锂电池) | 4.0 V ~ 6.0 V | 10 V ~ 15 V | 5.0 V |
| **输出电压 ($V_{OUT}$)**| **1.0 V ~ 3.3 V** | 1.5 V ~ 3.3 V | 5.0 V | 3.3 V |
| **最大负载电流** | **500 mA** | 300 mA | 1.0 A | 500 mA |
| **开关频率 ($f_{SW}$)**| **300 kHz ~ 1.0 MHz** | 200 kHz | 100 kHz | 250 kHz |
| **峰值转换效率** | **89.5%** | 82.0% | 85.0% | 84.0% |
| **次谐波抑制** | **片内同步斜坡差分抵消叠加** | 无针对性设计 | 外部注入 | 算法抑制 |
| **控制器核心面积** | **0.2575 mm²** | -- | 较大 (含双极管) | -- |

---

## 6. Cadence Virtuoso 仿真与设计借鉴 (IC Design & Virtuoso Takeaways)

> **课题借鉴与工程落地思考**
> 1. **核心可复用拓扑结构**：
>    - **虚短电流镜像传感器 (Fig. 5)**：极具借鉴价值。在现代深亚微米（如 0.18 µm BCD、65 nm CMOS）工艺中，可完全移植该结构用于高端 PMOS 或低端 NMOS 的逐周期采样与过流保护（OCP）。现代设计可将双极型微偏置电流源升级为温度补偿的绝对温度互补（CTAT/PTAT）偏置，进一步压低轻载采样失配。
>    - **差分工艺容差对消 V-to-I 转换器 (Fig. 9)**：该结构是模拟计算的典范，巧妙利用一对对称的共源级消除直流跟随电平，并依靠电阻几何比值 $\frac{R_{\text{sense}}}{R_s}$ 消除工艺偏差，在需要高线性度片上模拟求和（如斜坡补偿叠加、电容电流重构）场景下可直接复现。
> 2. **Cadence Virtuoso 仿真要点**：
>    - **采样运放稳定性与建立时间验证**：采样运放处于极深的局部负反馈中，其输入端受功率管开关高速跳变驱动。在 ADE 中必须进行 `PSTB`（周期性小信号稳定性仿真）与大信号瞬态建立测试，确保开环增益 $>75\,\text{dB}$，相位裕度 $\text{PM} > 60^\circ$，且在开关导通上升沿（$< 5\,\text{ns}$）内运放输出能迅速建立虚短，避免产生采样毛刺导致比较器早翻转。
>    - **极端工艺角（Corner: TT/SS/FF/SNFP/FNSP）与温度（-40°C ~ 125°C）扫描**：重点监控 V-to-I 转换器的电流镜像平衡度，确保在交叉 Corner（如 SNFP）下两路源极跟随器的 $V_{SG}$ 依然能保持高度一致，抵消误差控制在 $1\%$ 以内。
>    - **次谐波振荡大信号瞬态验证**：在开环瞬态仿真中，设置输入电压为最低（$V_{IN}=3.0\,\text{V}$），输出电压为最高（$V_o=2.5\,\text{V}$），使稳态占空比达到 $D > 0.8$ 的极限恶劣工况，验证斜坡补偿幅值是否充足，电感电流是否呈现完美的单周期纹波。
> 3. **版图与可靠性避坑要点**：
>    - **功率管与感知管的共质心布局（Common-Centroid Matching）**：感知 PMOS $M_2$ 必须放置在功率 PMOS $M_1$（500 fingers）的正中心，周围包裹虚设管（Dummy Devices），并采用完全一致的多晶硅栅取向与金属布线密度，以抵消热梯度（Thermal Gradients）与应力带来的失配。
>    - **Kelvin 独立引线与地弹隔离**：采样运放的输入拾取端（节点 $A$ 和 $B$）必须采用 Kelvin 连接直接打到功率管与感知管的漏极活性区金属根部，严禁与功率大电流走线共用寄生金属走线电阻；控制核心与驱动级必须采用独立的模拟地（AGND）与功率地（PGND），并在芯片焊盘处执行单点星型物理隔离。

---

## 7. 关联文献与学术网络 (Academic References)

- **电流采样理论先驱与对比工作**：
  - Smith2000 T. A. Smith et al., *"Controlling a DC-DC converter by using the power MOSFET as a voltage controlled resistor,"* IEEE TCAS-I, 2000.（提出了 MOSFET 导通电阻采样法，但受制于温漂与低信噪比）
  - Midya1997 P. Midya et al., *"Sensorless current mode control—An observer-based technique for DC-DC converters,"* IEEE PESC, 1997.（无感状态观测器电流采样先驱文献，因参数匹配苛刻难以广泛集成）
  - Givelin1995 P. Givelin et al., *"Application of CMOS current mode approach to on-chip current sensing in smart power circuits,"* IEE Proc. CDS, 1995.（BiCMOS 工艺下的片上采样尝试）
- **模拟电路经典基础模块**：
  - Monticelli1986 D. M. Monticelli, *"A quad CMOS single-supply op amp with rail-to-rail output swing,"* IEEE JSSC, 1986.（两级浮动 Class-AB 宽摆幅运放的奠基论文）
  - Yoo2000 C. Yoo, *"A CMOS buffer without short-circuit power consumption,"* IEEE TCAS-II, 2000.（交叉耦合自适应防直通驱动器拓扑来源）
- **后续学术演进脉络**：
  - JSSC-2014-Cheng Lin Cheng, Wing-Hung Ki et al., *"A 10/30 MHz Fast Reference-Tracking Buck Converter With DDA-Based Type-III Compensator,"* IEEE JSSC, 2014.（同为香港科技大学团队在超高频（30 MHz）下解决电流感知与 Type-III 面积瓶颈的跨时代演进工作）
