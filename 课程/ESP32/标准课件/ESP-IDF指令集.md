# ESP-IDF指令集

[toc]

## **一、ESP idf.py常用指令详解及操作指南**

- 了解 idf.py 常用命令使用

- 明白为什么我们需要使用命令行来进行项目管理。

## **二、idf.py 全命令中文帮助**

```C
➜  Desktop idf.py --help
Usage: idf.py [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...
 
  ESP-IDF 命令行构建管理工具。对于 idf.py 未知的命令，将尝试将其作为构建系统目标执行。选择的目标：无
 
Options:
  --version                       显示 IDF 版本并退出。
  --list-targets                  打印支持的目标列表并退出。
  -C, --project-dir PATH          项目目录。
  -B, --build-dir PATH            构建目录。
  -w, --cmake-warn-uninitialized / -n, --no-warnings
                                  为项目目录内的 CMake 文件启用 CMake 未初始化变量警告。(--no-warnings 现在是默认值，不需要指定。)
                                  默认值可以通过 IDF_CMAKE_WARN_UNINITIALIZED 环境变量设置。
  -v, --verbose                   详细构建输出。
  --preview                       启用仍在预览中的 IDF 功能。
  --ccache / --no-ccache          在构建中使用 ccache。默认情况下禁用。默认值可以通过 IDF_CCACHE_ENABLE 环境变量设置。
  -G, --generator [Ninja|Unix Makefiles]
                                  CMake 生成器。
  --no-hints                      禁用解决错误和日志记录提示。
  -D, --define-cache-entry TEXT   创建一个 CMake 缓存条目。此选项最多只能全局使用一次，或在一个子命令中使用一次。
  -p, --port PATH                 串行端口。默认值可以通过 ESPPORT 环境变量设置。此选项最多只能全局使用一次，或在一个子命令中使用一次。
  -b, --baud INTEGER              闪存的波特率。如果未在本地定义，它还可以暗示监视器波特率。默认值可以通过 ESPBAUD 环境变量设置。
                                  此选项最多只能全局使用一次，或在一个子命令中使用一次。
  --help                          显示此消息并退出。
 
Commands:
  add-dependency               向清单文件添加依赖项。
  all                          别名：build。构建项目。
  app                          仅构建应用程序。
  app-flash                    仅刷新应用程序。
  bootloader                   仅构建引导加载程序。
  bootloader-flash             仅刷新引导加载程序。
  build-system-targets         打印构建系统目标列表。
  clang-check                  在当前文件夹下运行 clang-tidy 检查，将输出写入 "warnings.txt"。
  clang-html-report            通过读取 "warnings.txt" 生成 HTML 报告到 "html_report" 文件夹（可能需要几分钟）。此功能需要额外的依赖项 "codereport"。请通过运行 "pip install codereport" 安装。
  clean                        删除构建目录中的构建输出文件。
  confserver                   运行 JSON 配置服务器。
  coredump-debug               创建核心转储 ELF 文件并使用此文件运行 GDB 调试会话。
  coredump-info                打印崩溃任务的寄存器、调用栈、系统中可用任务列表、内存区域和核心转储中存储的内存内容（TCB 和堆栈）。
  create-component             创建新组件。
  create-manifest              为指定组件创建清单。
  create-project               创建新项目。
  create-project-from-example  从示例创建项目。
  delete-version               （已弃用）弃用！新 CLI 命令："compote component delete"。从组件注册表中删除指定版本的组件。
  docs                         用浏览器打开 ESP-IDF 文档。
  efuse-common-table           生成 IDF 的 eFuse 字段的 C 源代码。
  efuse-custom-table           生成用户 eFuse 字段的 C 源代码。
  encrypted-app-flash          仅刷新加密的应用程序。
  encrypted-flash              刷新加密的项目。
  erase-flash                  擦除整个闪存芯片。
  erase-otadata                擦除 otadata 分区。
  flash                        刷新项目。
  fullclean                    删除整个构建目录内容。
  gdb                          运行 GDB。
  gdbgui                       在默认浏览器中打开 GDB 用户界面。
  gdbtui                       运行 GDB TUI 模式。
  menuconfig                   运行 "menuconfig" 项目配置工具。
  monitor                      显示串行输出。
  openocd                      从当前路径运行 openocd。
  pack-component               （已弃用）弃用！新 CLI 命令："compote component pack"。创建组件归档并存储在 dist 目录中。
  partition-table              仅构建分区表。
  partition-table-flash        仅刷新分区表。
  post-debug                   读取异步调试操作的输出并停止它们的实用目标。
  python-clean                 删除 IDF 目录中生成的 Python 字节码。
  read-otadata                 读取 otadata 分区。
  reconfigure                  重新运行 CMake。
  save-defconfig               生成一个包含与默认配置不同选项的 sdkconfig.defaults。
  set-target                   设置要构建的芯片目标。
  show-efuse-table             打印 eFuse 表。
  size                         打印应用程序的基本大小信息。
  size-components              打印每个组件的大小信息。
  size-files                   打印每个源文件的大小信息。
  uf2                          生成包含所有二进制文件的 UF2 二进制文件。
  uf2-app                      仅为应用程序生成 UF2 二进制文件。
  update-dependencies          更新项目的依赖项。
  upload-component             （已弃用）弃用！新 CLI 命令："compote component upload"。将组件上传到组件注册表。如果注册表中不存在组件，它将自动创建。
  upload-component-status      （已弃用）弃用！新 CLI 命令："compote component upload-status"。通过作业 ID 检查组件上传状态。
 
```

## **三、idf.py 入门命令**

### **3.1 查看 idf 版本**

**idf.py –version**

1. 当我们需要知道当前使用的 idf 版本时可以使用改命令，例如从下图命令可知，我们知道当前使用的是 v5.2.2 。

```
➜  Desktop  idf.py --version
ESP-IDF v5.2.2-440-gd1ed3a8c5c
```

### **3.2 设置芯片目标**

**idf.py set-target**

1. 我们首先需要选择芯片平台是什么，如下是以 esp32c3 为例。

1. 如果不知道自己当前的模组是什么系列的芯片，可以查看 芯片概览。

```
idf.py set-target esp32c3 
```

### **3.3 构建命令**

**idf.py build/all**

1. 该命令将会把当前文件进行一次编译

1. 如下两种写法效果一样

```
idf.py all
idf.py build
```

### **3.4 烧录命令**

**idf.py flash**

1. 该命令将会把工程文件烧录进 esp32 。

1. 但是如果你还没有执行 idf.py build 进行编译。那么该命令将会将会自动编译，如果编译通过自动将程序烧录进入芯片。

1. 需要注意，如果电脑只插入了一个 esp32，只需要执行如下命令，自动将代码烧录。

```
idf.py flash
```

1. 如果电脑同时插入多个 esp32 那么我们需要指定端口。假设我们当前要将程序烧录进入 /dev/ttyUSB0 ，命令如下。

```
idf.py flash -p /dev/ttyUSB0
```

### **3.5 清除命令**

**3.3.1 idf.py clean**

1. 该命令会删除 build 目录中的生成文件和对象文件，但会保留某些缓存文件和配置文件。

1. 适用于需要重新构建项目但不想清除所有缓存和配置的情况。执行时间较短，因为它保留了一些缓存，可以加快后续的构建过程。

**3.3.2 idf.py fullclean**

1. 该命令会彻底清理构建目录，包括所有生成文件、对象文件、缓存文件和配置文件。适用于需要完全重置构建环境，确保没有任何遗留文件影响重新构建的情况。

### **3.6 工具命令**

**3.6.1 idf.py monitor**

1. 该命令会让芯片复位，并且显示串口信息。

1. 如果插入了一个 esp32，只需要执行如下命令。

```
idf.py monitor
```

1. 如果电脑同时插入多个 esp32 那么我们需要指定端口。

```
idf.py monitor -p /dev/ttyUSB0
```

**3.6.2 idf.py menuconfig**

1. 该命令能够设置一些 esp32 的配置信息，从而进行相应的处理。该功能是一个开源项目，在 linux 和 rtthread 上均有实现。

1. menuconfig 将会和 kconfig 配合。配置教程 : ESP32 之 ESP-IDF 教学（十八）—— 组件配置（KConfig）

## **四、idf.py 进阶命令**

### **4.1 分步构建**

**4.1.1 idf.py app**

1. 如果我们仅修改了 app 程序，为了加快开发，验证 app 程序是否能够正常编译，即可使用该命令。

1. 如果想要摸鱼，那么每次程序调整，都可以使用如下命令。那样每次验证都是重新开始，基本需要半分钟以上，项目大一点，可能需要一两分钟。

```
idf.py fullclean
idf.py flash monitor -p /dev/ttyUSB0
```

**4.1.2 idf.py bootloader**

1. 如果我们仅修改了 bootloader 程序，为了加快开发，验证 bootloader 程序是否能够正常编译，即可使用该命令。

1. 摸鱼套装同上。

**4.1.3 idf.py partition-table**

1. 该命令只会编译分区表相关信息。

1. 当我们调整了分区表，同时想看看分区表的分区信息，可调用该命令查看。

1. 通过下面的例子，我们知道当前分区表信息

| **名字**        | **类型** | **子类型** | **偏移** | **大小** | **标志**  |
| --------------- | -------- | ---------- | -------- | -------- | --------- |
| nvs             | data     | nvs        | 0x9000   | 24K      | /         |
| phy_init        | data     | phy        | 0xf000   | 4K       | /         |
| factory         | app      | factory    | 0x10000  | 2500K    | /         |
| assets          | data     | spiffs     | 0x281000 | 1000K    | /         |
| storage         | data     | spiffs     | 0x37b000 | 100K     | /         |
| esp_secure_cert | 63       | 6          | 0x394000 | 8K       | encrypted |
| fctry           | data     | nvs        | 0x396000 | 24K      | /         |



```C
➜  software git:(feature/zhangyixu) idf.py partition-table
Executing action: partition-table
Running ninja in directory ~/Desktop/esp-toothbrush/software/build
Executing "ninja partition-table"...
[1/1] cd ~/Desktop/esp-toothbrush/software...*******************************************************"
Partition table binary generated. Contents:
*******************************************************************************
# ESP-IDF Partition Table
# Name, Type, SubType, Offset, Size, Flags
nvs,data,nvs,0x9000,24K,
phy_init,data,phy,0xf000,4K,
factory,app,factory,0x10000,2500K,
assets,data,spiffs,0x281000,1000K,
storage,data,spiffs,0x37b000,100K,
esp_secure_cert,63,6,0x394000,8K,encrypted
fctry,data,nvs,0x396000,24K,
*******************************************************************************
 
Partition Table build complete. To flash, run:
 idf.py partition-table-flash
or
 idf.py -p PORT partition-table-flash
or
 python -m esptool --chip esp32c2 -b 460800 --before default_reset --after hard_reset write_flash 0x8000 build/partition_table/partition-table.bin
or from the "~/Desktop/esp-toothbrush/software/build" directory
 python -m esptool --chip esp32c2 -b 460800 --before default_reset --after hard_reset write_flash "@flash_args"
 
```

### **4.2 分步烧录**

**4.2.1 idf.py app-flash**

1. 改命令仅仅会将 app 程序烧录进芯片。这样可以加快开发速度。

1. 如果程序没有执行 idf.py app 。该命令将会自动执行 idf.py app 编译后烧录。

**4.2.2 idf.py bootloader-flash**

1. 改命令仅仅会将 bootloader 程序烧录进芯片。

1. 如果程序没有执行 idf.py bootloader 。该命令将会自动执行 idf.py bootloader 编译后烧录。

**4.2.3 idf.py partition-table-flash**

1. 改命令仅仅会将 partition 程序烧录进芯片。

1. 如果程序没有执行 idf.py partition 。该命令将会自动执行 idf.py partition 编译后烧录。

### **4.3 CMake 重新运行**

**4.3.1 idf.py reconfigure**

1. 当我们对 CMakeList 文件做了调整。需要使用命令重新运行 CMake 。

1. 如果我们使用摸鱼套件，那么就无需再使用改命令了。因为 idf.py fullclean 会将 CMake 相关配置信息删除，执行 idf.py flash 时会重新运行 CMake 。

```
idf.py fullclean
idf.py flash monitor -p /dev/ttyUSB0
```

### **4.4 信息查看命令**

**4.4.1 idf.py save-defconfig**

1. 该命令能够生成一个 sdkconfig.defaults 文件，该文件包含与默认选项不同的配置选项。

1. 使用该命令，我们可以即可知道需要调整那些 menuconfig 的配置项。

**4.4.2 idf.py size**

1. 打印应用程序的基本大小信息。

1. 下图为某个程序的打印结果。

```
Total sizes:
Used stat D/IRAM:  126058 bytes ( 195238 remain, 39.2% used)
      .data size:   13296 bytes
      .bss  size:   28320 bytes
      .text size:   84442 bytes
Used Flash size : 1091530 bytes
           .text:  895410 bytes
         .rodata:  193048 bytes
Total image size: 1189268 bytes (.bin may be padded larger)
```

**4.4.3 idf.py size-files**

1. 如果仅idf.py size-files，那么 shell 中将会打印每个源文件的大小信息。

1. shell 中看信息终究是有些许麻烦，因此我们可以将打印信息存储到 size-file.txt 文件中，那样利用文本阅读软件，方便进行内存优化。

```
idf.py size-files > size-file.txt
```

### **4.5 擦除命令**

**4.5.1 idf.py erase-flash**

1. 该命令将会擦除整个 flash 。

1. 当 esp32 配网建立时，相关信息会存储在 nvs 中。当程序不是很健全，而你使用 esp32 配网失败后，程序卡死。你调整代码，执行 idf.py flash 命令将依旧没有用。因为 **idf.py flash 命令不会自动擦除 NVS 分区中的数据，它只会将固件写入指定的闪存区域，而不会影响 NVS 中的内容**。

1. 如果遇到该问题，程序执行流程应当如下

```
# 擦除整个闪存芯片，包括 NVS 分区中的所有数据
idf.py erase-flash
# 烧录程序并打开监视器, -p 后面的值根据你当前配置而定
idf.py flash monitor -p /dev/ttyUSB0
```

## **五、高级用法**

**5.1 批量烧录**

1. 如下为一个8个设备同时烧录的脚本。

```bash
#!/bin/bash
 
# 遍历 /dev/ttyUSB0 到 /dev/ttyUSB7
for i in {0..7}
do
  port="/dev/ttyUSB$i"
  
  # 检查设备是否存在
  if [ -e "$port" ]; then
    echo "Flashing device on $port..."
    
    # 执行 idf.py flash -p 命令
    idf.py flash -p $port
    
    # 检查上一个命令的退出状态码
    if [ $? -eq 0 ]; then
      echo "Successfully flashed $port"
    else
      echo "Failed to flash $port"
    fi
    
  else
    echo "Device $port does not exist."
  fi
done
 
```

**5.2 批量烧录—部分数据不同**

1. 如果我们需要批量烧录程序，但有部分数据需要调整，那么烧录脚本将会有些许不同。

1. 如下为 gatt_server 的程序批量烧录方法。我们需要烧录相同的程序，但是每台设备的设备名要求不一样。那么我们就使用如下脚本

```bash
#!/bin/bash
 
#--------------------------------------------------------------------------------------
# 使用说明 ： 
# 1. SOURCE_FILE : 设置要进行宏替换源代码路径。
# 注意：源文件的 TEST_DEVICE_NAME 必须是 #define TEST_DEVICE_NAME      "DEVICE_NAME_PLACEHOLDER" 
SOURCE_FILE="./main/gatts_demo.c"
# 2. DEVICE_NAME_PREFIX : 从机设备的名字前缀
DEVICE_NAME_PREFIX="ESP_GATTS_DEMO_"
# 3. letter_map : 从机名字的后缀
declare -a letter_map=(a b c d e f g h i)
# 4. ttyUSB_start : /dev/ttyUSB* 的起始
ttyUSB_start=1
# 5. ttyUSB_start : /dev/ttyUSB* 的结束
ttyUSB_end=9
#--------------------------------------------------------------------------------------
# 注意事项 ： 
# 1. 该脚本必须存放在服务端工程根目录！！！
# 2. 如果该脚本失效，尝试在 SOURCE_FILE 的 main 函数中加入一个报错。测试该文件是否会被编译，如果不会
#    被编译，那么就可以查 CMakeLists.txt 是否把 BACKUP_FILE 过程文件加入了编译。导致源代码
#    SOURCE_FILE 中 main 函数被覆盖
#--------------------------------------------------------------------------------------
 
# 颜色定义
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'
 
# 设置脚本执行过程中的临时文件（脚本执行完成后该文件会被删除）
TEMP_FILE="./shell_tmp/gatts_demo_temp.c"
# 设置脚本执行过程中的备份文件（脚本执行完成后该文件会被删除）
BACKUP_FILE="./shell_tmp/gatts_demo_backup.c"
 
# 创建过程文件目录
echo -e "${YELLOW}Create the shell_tmp directory ${RESET}"
mkdir shell_tmp
# 备份原始文件
echo -e "${YELLOW}Backing up original file...${RESET}"
cp "$SOURCE_FILE" "$BACKUP_FILE"
 
# 创建临时文件
echo -e "${YELLOW}Touch TEMP_FILE...${RESET}"
cp "$SOURCE_FILE" "$TEMP_FILE"
 
echo -e "${YELLOW}for ... in ...${RESET}"
for i in $(seq "$ttyUSB_start" "$ttyUSB_end"); do
    port="/dev/ttyUSB$i"
    # 获取对应的字母
    device_name="${DEVICE_NAME_PREFIX}${letter_map[$((i-1))]}"
    
    # 创建临时文件，替换宏定义
    echo -e "${YELLOW}Replacing macro with DEVICE_NAME=${device_name} in $TEMP_FILE...${RESET}"
    sed "s/DEVICE_NAME_PLACEHOLDER/${device_name}/g" "$BACKUP_FILE"  "$TEMP_FILE"
    
    # 将临时文件替换为原始文件
    echo -e "${YELLOW}Replacing original file with the updated file...${RESET}"
    mv "$TEMP_FILE" "$SOURCE_FILE"
    
    # 打印下载命令并执行
    echo -e "${YELLOW}Running 'idf.py flash -p $port '...${RESET}"
    idf.py flash -p "$port" 
    
done
 
# 恢复原始文件
echo -e "${YELLOW}Restoring original file...${RESET}"
mv "$BACKUP_FILE" "$SOURCE_FILE"
# 删除过程文件
echo -e "${YELLOW}remove shell_tmp ${RESET}"
rm -rf shell_tmp
 
```

## **六、查看idf.py参考**

```
idf.py –help
```

 