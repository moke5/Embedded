# ESP-IDF 新建工程

[toc]



## **一、引言**

在前面的章节中，我们已经简要介绍了ESP32-S3的基础知识和ESP-IDF的基本概念，并详细阐述了VS Code IDE环境的搭建以及Espressif插件的安装流程。现在，基于这些前期准备，我们将在本章搭建一个ESP-IDF基础工程，以后的例程都是基于此基础例程为模版来编写的。

## **二、快速搭建工程**

此方法参考ESP32提供的官方例程，可快速创建新工程。

### **2.1 查看官方提供的工程示例**

找到esp-idf软件安装路径，在安装路径下存在官方提供的示例：你电脑的路径下\Espressif\frameworks\esp-idf-v5.2.2\examples

![img](./img/57980.png)

### **2.2 使用官方示例**

拷贝 Espressif\frameworks\esp-idf-v5.2.2\examples路径下的sample_project工程，此工程就是最简单的工程模板，后续代码可在此基础模板上改动。

![img](./img/57967.png)

### **2.3 修改工程配置**

#### **2.3.1 改工程目录名**

![img](./img/57974.png)

**注意：工程名不能有中文，否则无法识别。**

#### **2.3.2 配置工程芯片**

切换到工程目录下，配置ESP32的芯片型号：

```
cd D:\esp32_code\led_project    #切换led_project工程目录下
idf.py set-target esp32s3       #设置工程芯片型号为esp32s3
```

![img](./img/57971.png)

配置成功后，会生成build目录和sdkconfig配置文件。

![img](./img/57977.png)

#### **2.3.6 编译工程**

```
idf.py build    #编译命令
```

 

 