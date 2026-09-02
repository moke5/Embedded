# Espressif-IDE环境搭建

[toc]

## **一、Espressif-IDE开发介绍**

Espressif-IDE 是一个基于 Eclipse CDT 的集成开发环境（IDE），专为 ESP-IDF 框架设计的物联网应用程序开发而打造。它作为一个独立且定制的 IDE，集成了 IDF Eclipse 插件、关键的Eclipse CDT 插件以及其他第三方插件，旨在提供全面支持以构建 ESP-IDF 应用程序。

Espressif-IDE 安装程序是一款便捷的离线安装工具，它集成了 ESP-IDF 应用开发所需的全部核心组件。这些组件包括嵌入式 Python、交叉编译器、开放 OCD、CMake 和 Ninja 构建工具、ESP-IDF 框架、Espressif-IDE 本身以及 Amazon Corretto OpenJDK。通过这一安装程序，您可以一次性获取所有必要的组件和工具，轻松完成安装，进而顺利开展方案开发。在 IDE 启动时，它会自动配置所有必需的构建环境变量和工具路径，无需您手动进行任何设置，极大地提升了开发效率。

## **二、IDE离线包安装**

**ESP-IDE安装包官网下载地址：**https://dl.espressif.cn/dl/esp-idf/?idf=4.4﻿

![img](./img/58009.png)

**💡注：如果只想用ESP-IDF+VSCode开发只下载第2个即可。**

### **1. 打开 espressif-ide 安装包**

**以管理员身份运行** **espressif-ide-setup-2.12.0-with-esp-idf-5.1.2.exe** **文件。**

![img](./img/57987.png)

### **2.选择安装语言界面，安装流程：一直下一步即可。**

![img](./img/58016.png)

 

### **3.安装前系统检查**

安装程序会检查你当前系统有没有打开"长路径支持"，因为 GNU 编译器产生的编译文件会有非常深的目录结构，如果不支持长路径，编译可能出现文件不存在，目录不存在等奇怪的错误。这里单击**应用修复**按钮，可以修复这个问题。在弹出的确认对话框中，选择是，开始修复。

![img](./img/58027.png)

**特殊情况：**如果修复不成功，一般情况是安装软件打开时没有使用管理员权限打开，可以手动修改注册表来支持长路径：打开注册表HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled 设置为 1。

![img](./img/58019.png)

 

### **4.配置安装路径**

安装程序默认的安装位置为 C:\Espressif，但这里我是安装在 D 盘，如果全部源码编译后可能产生几十 G 的大小占用，我们在 D 盘下创建 D:\Develop_Tool\esp-idf 文件夹来保存 ESP32-IDF 库安装过程中生成的文件。注意：这个安装路径非常重要，因为 VS Code 软件的 IDF 插件需要此路径来获取相关文件，所以开发者务必牢记该路径。

![img](./img/58042.png)

**工具安装目录介绍**

![img](./img/58035.png)

 **安装 USB 设备驱动程序** 

![img](./img/58031.png)

 

### **5.选择组件安装并完成**

设置安装路径后点击 “下一步”选项，进入确认安装组件界面，这里全部打勾。然后单击下一步。

![img](./img/58001.png)

 

### **6.选择组件安装并完成**

到这里软件已经安装完成了，由于勾选了“运行 ESP-IDF PowerShell 环境”和“运行 ESP-IDF 命令提示符环境”，所以会弹出这两个窗口，等待命令行出现“idf.py build”字样，后面就可以关闭窗口。这时候，就可以发现在桌面有三个新图标，如下图所示。

![img](./img/58039.png)

 

### **7.对 Espressif-IDE 工作区进行设置**

双击“Espressif-IDE”软件图标，准备启动软件，

![img](./img/58013.png)

稍等片刻，需要对 Espressif-IDE 工作区进行设置。使用工作区来存储首选项和开发过程中生成的文件，在这里根据自己实际情况进行选择即可。点击 Launch，即可进入到软件主界面

![img](./img/57994.png)

启动 Espressif-IDE 后，它会自动配置所需的环境变量并随即展示欢迎页面。为确保环境变量已正确配置，您可以进入“Window→Preferences→C/C++→Build→Environment”进行检查，相关显示页面如图所示。这样，您可以更加安心地进行后续的开发工作。

![img](./img/58024.png)

 

**注意：**安装好软件后，建议大家检查一下是否已正确设置所需的环境变量。如果环境变量存在，那么后续的新建工程和编译工程过程通常不会遇到问题。如果发现这些环境变量不存在，请检查系统的环境变量设置，以排除可能的冲突情况。（主要是检查 IDF_PATH 和 IDF_TOOLS_PATH 这两个环境变量是否存在冲突或不一致的问题。）

 

![img](./img/57990.png)

**💡注意：**如果 IDF_PATH 环境变量没有，需自己手动创建，并指定路径为 esp-idf 安装路径下的 frameworks\esp-idf-v5.3.1 。

![img](./img/57998.png)

 

### **8.Espressif_IDE 界面**

![img](./img/58005.png)

若在使用过程中遇到任何问题，查阅官方资料以获取更详细的指导，具体链接为：https://github.com/espressif/idf-eclipse-plugin/blob/master/README_CN.md#Installation﻿

 