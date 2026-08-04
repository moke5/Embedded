# WSL 下 drvfs 交叉编译 Make 卡顿优化笔记

## 环境

| 项目     | 值                                               |
| :------- | :----------------------------------------------- |
| 系统     | Windows 11 + WSL2 Ubuntu                         |
| 项目路径 | /mnt/d/YQ/code/4concurrency/lv_pic（drvfs 挂载） |
| 工具链   | arm-linux-gcc 交叉编译                           |
| GUI 框架 | LVGL v8.2.0                                      |

## 问题现象

在 WSL 中对 /mnt/d/ 下的项目执行 make，出现两段明显卡顿：

1. make 启动阶段无任何输出，卡住 5 秒才开始编译
2. 最后 gcc 链接阶段卡住，无输出等待约 30 秒

## 诊断方法

通过 time make 观察 real / user / sys 三项数据：

real 0m36.182s user 0m0.280s sys 0m1.274s

关键判断：real 远大于 user + sys，说明 CPU 几乎没有工作，时间全部消耗在 I/O 等待上。这是 drvfs（WSL 访问 Windows 文件系统的驱动）的固有延迟导致的。

## 根因分析

Makefile 的 include 链中存在大量动态文件扫描：

| 文件                 | 调用方式              | 影响                           |
| :------------------- | :-------------------- | :----------------------------- |
| demos/lv_demos.mk    | $(shell find -L ...)  | 递归遍历 demos/ 目录树         |
| examples/examples.mk | $(shell find -L ...)  | 递归遍历 examples/ 目录树      |
| src/extra/extra.mk   | $(shell find -L ...)  | 递归遍历 extra/ 目录树（最大） |
| lv_drivers.mk        | $(wildcard ...) × 5   | 逐目录 glob 匹配               |
| 项目 Makefile        | $(wildcard ./src/*.c) | 扫描项目源码目录               |

每次 \$(shell find) 和 $(wildcard) 都会在 drvfs 上做 stat/opendir 系统调用，跨越 Windows/Linux 边界。三次 find 递归遍历数百个文件，累计上千次跨边界调用，导致 make 启动阶段卡顿 30+ 秒。

链接阶段卡顿原因：链接器从 build/obj/ 读取几百个 .o 文件并写出 build/bin/demo，全部在 drvfs 上完成。

## 优化方案

### 优化 1：预生成文件列表（消除 make 启动卡顿）

将 \$(shell find) 和 $(wildcard) 的结果缓存为静态文件列表，make 启动时直接读取列表，不再扫描目录。

生成命令（只需执行一次，LVGL 源码更新后重新执行）：

```bash
cd /mnt/d/YQ/code/4concurrency/lv_pic

find -L lvgl/demos -name '*.c' | sed 's/^/CSRCS += /' > .lvgl_files.mk
find -L lvgl/src/extra -name '*.c' | sed 's/^/CSRCS += /' >> .lvgl_files.mk
find -L lv_drivers -name '*.c' | sed 's/^/CSRCS += /' >> .lvgl_files.mk
```

注意：examples/ 目录被跳过，项目不需要 examples。

### 优化 2：修改 Makefile include 链

将原来的：

```
include $(LVGL_DIR)/lvgl/lvgl.mk
include $(LVGL_DIR)/lv_drivers/lv_drivers.mk
```

替换为：

```makefile
# 静态文件列表（替代 lvgl.mk 中的 shell find 和 lv_drivers.mk 的 wildcard）
include .lvgl_files.mk

# lvgl 各子模块（使用显式文件列表，不触发目录扫描）
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/core/lv_core.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/draw/lv_draw.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/draw/sw/lv_draw_sw.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/font/lv_font.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/hal/lv_hal.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/misc/lv_misc.mk
include $(LVGL_DIR)/$(LVGL_DIR_NAME)/src/widgets/lv_widgets.mk
```

说明：lvgl.mk 不再 include（因为它会触发 examples/examples.mk 的 find），lv_drivers.mk 也不再 include（文件列表已在 .lvgl_files.mk 中）。

### 优化 3：编译产物放到 WSL 原生文件系统（消除链接卡顿）

将 Makefile 中的 BUILD_DIR 从 drvfs 改到 WSL 原生 ext4：

```
BUILD_DIR = $(HOME)/lv_pic_build
```

这样所有 .o 文件和最终 demo 二进制都写在 ext4 上，只有读源码走 drvfs。编译产物随时可以删除重建，不影响源码。

### 优化 4：并行编译

```
make -j20
```

让多个编译任务同时运行，I/O 等待互相重叠，大幅缩短完整编译时间。

## 优化效果

| 场景                               | 优化前     | 优化后  | 提升  |
| :--------------------------------- | :--------- | :------ | :---- |
| 完整编译 (make clean && make -j20) | 4 分 36 秒 | 21.8 秒 | 12 倍 |
| 重链接 (touch main.c && make)      | 30+ 秒     | 3.5 秒  | 9 倍  |

剩余 3.5 秒的延迟来自编译 main.c 时从 drvfs 读取头文件（lvgl.h 等几十个 include），这是源码留在 /mnt/d/ 的固有开销，无法进一步消除。

## 尝试过但无效/负优化的方案

| 方案                                       | 结果                  |
| :----------------------------------------- | :-------------------- |
| dirmetadata = true (.wslconfig / wsl.conf) | 无明显改善            |
| MAKEFLAGS += -r                            | 无明显改善            |
| CFLAGS 加 -pipe                            | 无明显改善            |
| build/ 符号链接到 WSL 原生目录             | Makefile 路径解析出错 |
| ccache                                     | 交叉编译场景效果有限  |
| 修改 .wslconfig 分配更多内存/CPU           | 无明显改善            |
| Windows fsutil 关闭 8.3/lastaccess         | 无明显改善            |

## 踩坑记录

1. 符号链接 build/ → ~/lv_pic_build 会导致 Makefile 中 addprefix 生成畸形路径（build/obj//mnt/d/...），不可用
2. 一次性改太多配置无法判断哪个有效——应逐个改动并对比测试