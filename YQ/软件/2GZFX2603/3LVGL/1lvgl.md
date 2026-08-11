# LVGL

[toc]





### **LVGL简介**

LVGL（Light and Versatile Graphics Library）是一个开源的图形用户界面库，旨在提供轻量级、可移植、灵活和易于使用的图形用户界面解决方案。开源网址：https://github.com/lvgl

![image-20260716090810079](./img/image-20260716090810079.png)

它适用于嵌入式系统，可以在不同的操作系统、微控制器和图形加速器上运行。LVGL的核心代码是用C语言编写的，支持多种显示设备和输入设备，包括液晶显示屏、OLED显示屏、触摸屏、按键和编码器等。
LVGL提供了一系列组件和小部件，例如文本框、按钮、滑动条、表格、菜单等，可以快速构建交互式用户界面。LVGL还具有高度自定义的能力，用户可以根据需要修改或扩展库的功能。总之，LVGL是一个功能强大、易于使用的图形用户界面库，可以帮助开发人员在嵌入式系统中实现各种交互式应用程序。

#### **[LVGL代码特性](https://lvgl.io/features)**

1. **部件多**

LVGL带有30多个内置小部件，例如Arc、Bar、Calendar、Chart、Checkbox、下拉列表、键盘、仪表、消息框、开关、表格、Tabview、文本区域等等。

有了这些小部件，在手机应用程序中常见的内容也可以通过LVGL实现。

这些小部件可以实时创建和删除。这样就可以通过仅动态创建当前可见的屏幕和小部件来节省内存了。

2. **渲染功能**

![image-20260716091008827](./img/image-20260716091008827.png)

LVGL带有强大的软件渲染引擎，可以使用最少的资源以矢量图形方式绘制抗锯齿小部件。

\- 带半径的矩形
\- 带半径的边框
\- 水平和垂直梯度
\- 盒子阴影
\- 斜线
\- 弧线
\- 缩放和旋转图像或任何小部件

3. **丰富的style**

![image-20260716090954057](./img/image-20260716090954057.png)

我们可以从100多个样式属性中进行选择，以设置小部件运行时的样式。它可以动态更改UI的主题，甚至可以为样式设置动画。它还非常节省Flash存储空间，可以说是又便宜又好用。

小部件可以在任何状态下设置样式，如按下、检查、聚焦、禁用等。小部件的任何部分也可以自定义。例如，滑块由主、指示器和旋钮部分组成，其外观可以自由调整。

最重要的是，通过使用所做的转换，LVGL可以在状态更改时自动为样式设置动画。



4. **布局**

![image-20260716091049784](./img/image-20260716091049784.png)

通过使用强大的内置布局，不必手动定位小部件。
flex 布局允许根据设置的策略快速排列数百个项目。

网格布局有助于将小部件添加到用户定义的网格的单元格中，并根据需要对齐它们。
简单地将小部件与其父级的任意一侧对齐或使用百分比单位也有助于轻松创建响应式 UI。

更改任何内容、大小或位置，所有这些布局都会自动更新。



5. **字体和多语言支持**

可以使用 FreeType（适用于 MPU）或 TinyTTF（适用于 MCU）使用 1、2、4、8 位/像素字体、压缩字体、从 TTF 渲染字形或 WOFF 文件

所有字符串均采用 UTF-8 解码，LVGL 的类型设置引擎支持阿拉伯语、波斯语、希伯来语、泰语、中文、日语、韩语和许多其他语言。甚至可以混合从右到左和从左到右的书写方向。

还支持回退字体和表情符号。



6. **转换**

![image-20260716091146673](./img/image-20260716091146673.png)

任何库都可以转换图像，但在 LVGL 中，我们将其更进一步。

不仅可以旋转或缩放 LVGL 绘制的任何小部件。甚至 children 也支持嵌套转换。

触摸手势会针对小组件进行转换，例如，列表会沿其旋转方向滚动。



7. **滚动**

![image-20260716091226092](./img/image-20260716091226092.png)

流畅的滚动对于打造令人印象深刻、用户友好、类似智能手机的用户体验至关重要。

在 LVGL 中，滚动非常简单：如果 widget 的子项超出 widget 的边界框，则该 widget 将是可滚动的。就是这样。不需要特殊的可滚动容器或任何额外的技巧。

支持对齐、弹性滚动、滚动动量、滚动链接。

#### **LVGL商业特性**

- 完全开源，LVGL不属于任何个体，一旦下载，由你掌控。
- 遵循MIT开源协议，你可以使用、修改、发布，用于商业用途也不需要付任何费用。

#### **LVGL官方文档**

[LVGL官方文档](https://docs.lvgl.io/8.1/index.html)



## 下载

#### **LVGL源码下载--lvgl-8.2**



**下载** **lvgl-v8.2**

![image-20260716094110219](./img/image-20260716094110219.png)

![image-20260716094126385](./img/image-20260716094126385.png)



#### **下载arm Linux开发板fb0的源码主框架:**

 **LVGL 配置为使用标准 Linux 帧缓冲区**

**先进入主目录：**

![image-20260716094223983](./img/image-20260716094223983.png)

**进入主目录之后进行搜索lv_port_linux**

![image-20260716094911738](./img/image-20260716094911738.png)

**点击上面的lv_port_linuxr,然后下载：**

![image-20260716095011329](./img/image-20260716095011329.png)



#### **下载LVGL的驱动源码：**

**用于 LVGL 嵌入式 GUI 库的 TFT 和触摸板驱动程序**

```
lv_drivers是为LVGL提供的TFT（薄膜晶体管（Thin-Film Transistor）的缩写，它是一种用于液晶显示器（LCD）的技术）和
触摸屏驱动程序集合，包括了多种不同的嵌入式平台和显示屏接口的驱动程序。

```

**先进入主目录：**

**进入主目录之后进行搜索：**

![image-20260716095119035](./img/image-20260716095119035.png)



![image-20260716095132531](./img/image-20260716095132531.png)



### **源码框架整合搭建的细节操作**

①将lv_drivers-release-v8.2.zip解压后目录内的所有内容拷贝到lv_port_linux_release-v8.2.zip解压后内部的lv_drivers

②将lv-release-v8.2.zip解压后目录内的所有内容拷贝到lv_port_linux_release-v8.2.zip解压后内部的lvgl



![image-20260716095443668](./img/image-20260716095443668.png)



## LVGL main函数中接口分析



**一、LVGL 8.2 main函数如下：**

```C
int main(void)
{
    /*LittlevGL init*/
    lv_init();
 
    /*Linux frame buffer device init*/
    fbdev_init();
 
    /*A small buffer for LittlevGL to draw the screen's content*/
    static lv_color_t buf[DISP_BUF_SIZE];
 
    /*Initialize a descriptor for the buffer*/
    static lv_disp_draw_buf_t disp_buf;
    lv_disp_draw_buf_init(&disp_buf, buf, NULL, DISP_BUF_SIZE);
 
    /*Initialize and register a display driver*/
    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.draw_buf   = &disp_buf;
    disp_drv.flush_cb   = fbdev_flush;
    disp_drv.hor_res    = 800;
    disp_drv.ver_res    = 480;
    lv_disp_drv_register(&disp_drv);
 
    evdev_init();
    static lv_indev_drv_t indev_drv_1;
    lv_indev_drv_init(&indev_drv_1); /*Basic initialization*/
    indev_drv_1.type = LV_INDEV_TYPE_POINTER;
 
    /*This function will be called periodically (by the library) to get the mouse position and state*/
    indev_drv_1.read_cb = evdev_read;
    lv_indev_t *mouse_indev = lv_indev_drv_register(&indev_drv_1);
 
 
    /*Set a cursor for the mouse*/
    LV_IMG_DECLARE(mouse_cursor_icon)
    lv_obj_t * cursor_obj = lv_img_create(lv_scr_act()); /*Create an image object for the cursor */
    lv_img_set_src(cursor_obj, &mouse_cursor_icon);           /*Set the image source*/
    lv_indev_set_cursor(mouse_indev, cursor_obj);             /*Connect the image  object to the driver*/
 
 
    /*Create a Demo*/
    lv_demo_widgets();
 
    /*Handle LitlevGL tasks (tickless mode)*/
    while(1) {
        lv_timer_handler();
        usleep(5000);
    }
 
    return 0;
}
```

 

```C
lvgl初始化函数：lvgl_init() 设计理念
    初始化lvgl的各种基本核心功能比如链表初始化（lvgl核心数据结构是哈希链表）内存，用去存放控件
    
    lvgl心跳节拍（它自己设置每个时间段，会实时检索链表中的每一个控件中是否触发事件：控件有没有被删除。控件没有被触摸等事件）
    
 
fb0帧缓存框架初始化：fbdev_init()
    初始化显示缓冲区,在使用 LVGL 创建 GUI 应用程序时，通常需要配置和初始化显示缓冲区以实现双缓冲或多缓冲绘图.这个函数允许用户指定用于绘制的缓冲区，以及缓冲区的大小和数量等参数。
    
显示器驱动器初始化:lv_disp_drv_init()
    用于初始化显示器驱动器。在使用 LVGL 创建 GUI 应用程序时，需要将显示器的驱动器配置为 LVGL 能够识别和使用的格式。这个函数允许用户设置显示器驱动器的各种属性，包括显示器的分辨率、刷新率、像素格式、像素布局等。
 
注册已配置的显示驱动器:lv_disp_drv_register()
    用于注册已配置的显示驱动器，使其可以在 LVGL 库中被使用来渲染(显示算法)和显示图形界面
 
输入事件设备驱动初始化:evdev_init和lv_indev_drv_init()
        Linux系统中初始化 EVDEV（Event Device）驱动程序。EVDEV驱动程序是Linux内核中用于处理输入设备事件的一个子系统，它允许用户空间应用程序通过读取特定的设备文件来获取输入设备（如键盘、鼠标、触摸屏）产生的事件（读取坐标）。
        
注册已配置的输入设备驱动器:lv_indev_drv_register()
        你需要使用 lv_indev_drv_register 函数将对应的输入设备驱动注册到LVGL库中，以便LVGL能够正确识别和使用该输入设备。
   
 启动调用lvgl自带的例程：lv_demo_widgets();
            
// 进入你的应用程序主循环，例如：
while(1) {
    lv_task_handler(); // 处理LVGL的任务 lvgl心跳节拍
    usleep(5000);
}
```

**二、理解思路图**

![image-20260716101558284](./img/image-20260716101558284.png)



## LVGL 编码编译运行

#### **一、源码目录的搭建移动**

**① 移动编译**

```
把lvgl_release_v8.2和lv_drivers-release-v8.2中的源码移动到lv_port_linux_里面的lvgl和lv_drivers_release-v8.2中后，进入lv_port_linux_release_v8.2
输入：
    make进行编译
```

**② 修改Makefile中的编译器选项**

![image-20260716101812112](./img/image-20260716101812112.png)

**③ 编译可能出错的问题**

**编译如果出现以下错误**

![image-20260716101832833](./img/image-20260716101832833.png)

**解决方法就是把O_CLOEXEC 改成 FD_CLOEXEC，**因为当前编译器不支持*O_CLOEXEC** **标志。对应需要修改的.c位置：**

**lv_drivers/indev/evdec.v的145行**



![image-20260716101850728](./img/image-20260716101850728.png)

**编译可能出现以下错误：error: unrecognized command line option** **‘-Wshift-negative-value****’ ，arm-linux-gcc 编译器不支持，去掉这个参数**

```
-Wshift-negative-value 是 GCC 编译器选项之一，用于启用关于左移赋值的警告。在 LVGL（Light and Versatile Graphics Library）的 Makefile 中，这个选项可能会被用来确保代码中没有意外的左移负值的情况，因为这可能会导致未定义的行为或错误的结果。通过启用这个警告，可以帮助开发者及时发现潜在的问题并进行修复。
```



![image-20260716101928672](./img/image-20260716101928672.png)

**③ make 成功的部分截图**

![image-20260716101945492](./img/image-20260716101945492.png)

**使用file命令查看程序的文件属性是不是ARM32位的ARM平台**

![image-20260716102001251](./img/image-20260716102001251.png)

**④ 烧写程序到开发板**

**查看Makefile中，得知编译之后生成的程序的路径：**

![image-20260716102019715](./img/image-20260716102019715.png)

**⑤ 烧写到开发板里面运行**



#### **二、默认开启LVGL触摸屏功能  主要设置功能宏的有两个头文件**

**设置触摸屏坐标范围 在主目录中的lv_drv_conf.h**

![image-20260716102047266](./img/image-20260716102047266.png)

#### **三、修改帧率FPS，**

**30改成10，可以1秒刷新100次，****主要看硬件支持**

![image-20260716102105914](./img/image-20260716102105914.png)

#### **四、开启显示帧率功能，对应宏改成1即可**

![image-20260716102123775](./img/image-20260716102123775.png)



