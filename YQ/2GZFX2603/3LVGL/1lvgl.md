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

**解决方法就是把O_CLOEXEC 改成 FD_CLOEXEC，****因为当前编译器不支持** **O_CLOEXEC** **标志。对应需要修改的.c位置：**

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



## LVGL 图片显示+基本控件-软件组件编程

### **一、创建一个主画布（控件），默认是屏幕大小**

```
注意：画布称为界面窗口的控件载体（基类控件），后续可往画布中添加子类控件
创建画布的函数原型：不管是什么控件都是LVGL链表中的结点，所有控件对应的对象结构体都是统一的类型：lv_obj_t
    lv_obj_t * lv_obj_create(lv_obj_t * parent);
参数分析：
    参数1：
        parent:设置创建出来的的控件对应的父类控件，如果是第一次创建出来的画布，则没有父类控件填NULL
        NULL：指定父类控件指针，那为何要填 空，如果是第一次创建，则没有父类控件，所以填NULL
        
    参数类型：
        lv_obj_t * 是LVGL平台统一所有控件的对象类型
        
lv_obj_t * main_windows = lv_obj_create(NULL);  //控件被创建出来，生命周期肯定是长的，所以类似malloc返回堆空间
 
 main_windows：保存画布控件的首地址
```

### **二、常见的多控件适配函数** 

**1.常见的****适配**  **函数如下：**

```C
lv_obj_set_size() - 设置控件的大小。
lv_obj_set_align() - 设置控件的对齐方式。
lv_obj_set_pos() - 设置控件的位置。
lv_obj_center() - 设置控件居中
lv_scr_load()  - 加载显示控件
```

**2.lv_obj_set_size - 设置控件的大小**

```C
void lv_obj_set_size(lv_obj_t * obj, lv_coord_t w, lv_coord_t h)
obj:要设置的控件对象
w:宽
h:长
```

**3.lv_obj_set_align() - 设置控件的对齐方式**

```C
void lv_obj_set_align(lv_obj_t * obj, lv_align_t align)
obj:要设置的控件对象
align: 对齐方式，使用 lv_align_t 枚举类型，比如
    LV_ALIGN_LEFT_TOP: 控件对齐到父容器的左上角。
    LV_ALIGN_LEFT_MID: 控件对齐到父容器的左中部（垂直居中）。
    LV_ALIGN_LEFT_BOTTOM: 控件对齐到父容器的左下角。
    LV_ALIGN_CENTER: 控件在父容器中居中对齐。
    LV_ALIGN_RIGHT_TOP: 控件对齐到父容器的右上角。
    LV_ALIGN_RIGHT_MID: 控件对齐到父容器的右中部（垂直居中）。
    LV_ALIGN_RIGHT_BOTTOM: 控件对齐到父容器的右下角.
    LV_ALIGN_TOP_MID: 控件对齐到父容器的顶部中间（水平居中）。
    LV_ALIGN_BOTTOM_MID: 控件对齐到父容器的底部中间（水平居中）。
    LV_ALIGN_OUT_TOP_LEFT: 控件对齐到父容器的左上方，超出父容器顶部和左侧边界。
    LV_ALIGN_OUT_TOP_RIGHT: 控件对齐到父容器的右上方，超出父容器顶部和右侧边界。
    LV_ALIGN_OUT_BOTTOM_LEFT: 控件对齐到父容器的左下方，超出父容器底部和左侧边界。
    LV_ALIGN_OUT_BOTTOM_RIGHT: 控件对齐到父容器的右下方，超出父容器底部和右侧边界.
```

![image-20260716142524682](./img/image-20260716142524682.png)

**4.lv_obj_set_pos() - 设置控件的位置**

```C
lv_obj_set_pos(lv_obj_t * obj, lv_coord_t x, lv_coord_t y)
obj:控件对象
x: 对象在父容器中的 X 坐标。
y: 对象在父容器中的 Y 坐标。
```

**5.lv_obj_set_style_bg_color() --- 设置背景颜色**

```C
void lv_obj_set_style_bg_color(struct _lv_obj_t * obj, lv_color_t value, lv_style_selector_t selector);
obj - 控件对象
value - 颜色值 lv_color_hex(...);
selector - 颜色选择器,给0
```



```C
// 创建一个画布
    lv_obj_t * canvas = lv_obj_create(NULL);
    lv_obj_set_size(canvas, 800, 480);

    lv_obj_t * canvas1 = lv_obj_create(canvas);
    lv_obj_set_size(canvas1, 400, 200);
    lv_obj_set_align(canvas1, LV_ALIGN_CENTER);
    lv_obj_set_style_bg_color(canvas1, lv_color_hex(0x00ff00), 0); // 绿色

    lv_obj_t * canvas2 = lv_obj_create(canvas);
    lv_obj_set_size(canvas2, 200, 100);
    lv_obj_set_align(canvas2, LV_ALIGN_CENTER);
    lv_obj_set_style_bg_color(canvas2, lv_color_hex(0xff0000), 0); // 红色
    
    lv_scr_load(canvas);
```



### **三、如何显示图片**

**步骤 一、 显示图片等需要开启LVGL对标准IO的支持 -- 为了能让LVGL打开图片读取图像像素点**

![image-20260716142552271](./img/image-20260716142552271.png)

**步骤二、开启显示图片格式的接口与调大LVGL内存**

**1）开启图片格式**

![image-20260716142614108](./img/image-20260716142614108.png)

**2）调大内存**

![image-20260716142633897](./img/image-20260716142633897.png)

**步骤三、显示图片** **BMP jpg  PNG** 

显示bmp图片：屏幕出现no data,解决方法：

![image-20260716161321852](./img/image-20260716161321852.png)

![image-20260716161334618](./img/image-20260716161334618.png)

![image-20260716161348387](./img/image-20260716161348387.png)



```C
在 LittlevGL（LVGL）中，要显示图片，您可以使用 lv_img_create() 函数创建一个图像对象，并使用 lv_img_set_src() 函数设置图像的源。
以下是一个简单的示例代码，演示了如何在屏幕上显示一张图片：
lv_obj_t * img = lv_img_create(lv_scr_act());  // 在屏幕上创建一个图像对象
 
lv_img_set_src(img, "path/to/image.png");  // 设置图像的路径,直接显示图片
 
// 可选：设置图像对象的位置和大小
lv_obj_set_pos(img, x, y);
lv_obj_set_size(img, width, height);
```

**步骤四、显示** **GIF**

```C
1）创建gif控件的函数：
    lv_obj_t *gif_img = lv_gif_create(main_draw); // 创建一个gif图片对象用于显示 GIF 动画
    参数1：设置创建的gif图片对象的父类控件
    返回值：返回创建的gif对象的基地址
    
2）设置gif控件对象的gif图片路径函数：
    void lv_gif_set_src(lv_obj_t * obj, const void * src);
    
     参数1：要设置gif图片对象控件
     参数2：要设置gif图片开发板路径
     返回值：无
 

// 设置 GIF 图片对象的大小模式为正常大小,8.2版本只有一个显示图片的模式：一比一的比例显示，可以不用设置，默认一比一
lv_img_set_size_mode(gif_img, LV_IMG_SIZE_MODE_REAL);
 
 
// 将 GIF 图片对象在父类控件 中 居中
lv_obj_align(gif_img, LV_ALIGN_CENTER, 0, 0);
```

###  **三、基本控件**

#### **1. 常见的控件分析**

```
以下是 LVGL 中一些常见的控件：
    1）Label - 用于显示文本或标签。
    2）Button - 提供按钮功能，可以响应用户的点击操作。
    3）Image - 显示静态图片。
    4）Slider - 提供滑块控件，用户可以通过拖动滑块来选择值。
    5）Switch - 提供开关功能，用于切换两个状态（开/关）。
    6）Check Box - 提供复选框功能，用户可以选择多个选项。
    7）List - 提供列表视图，展示一组项，可以滚动和选择。
    8）Drop-down List - 提供下拉菜单，展示选择项。
    9）Text Area - 提供多行文本输入区域。
    10）Gauge - 用于显示仪表盘样式的仪表控件。
    11）Bar - 显示条形图，可以用来表示进度或数值。
    12）Arc - 显示圆弧，可以用来展示进度或计量。
    13）Canvas - 提供画布控件，可以进行自定义绘图。
    14）Table - 提供表格控件，用于显示数据表格。（数据库的视图控件）
    15）Calendar - 显示日历控件，用户可以选择日期。
    16）Keyboard - 提供虚拟键盘控件，用户可以输入文本。
```

#### **2. Button - 提供按钮功能，可以响应用户的点击操作**

**1）函数分析**

```C
创建按钮控件函数：lv_obj_t * lv_btn_create(lv_obj_t * parent)
parent：父类对象指针
返回值：返回创建的按钮控件对象指针
 
实例：创建100X100的按钮，居中显示
 
    lv_obj_t * main_draw = lv_obj_create(NULL);    //创建画布
    lv_obj_t * btn = lv_btn_create(main_draw);     //创建按钮
    lv_obj_set_size(btn,100,100);                  //设置按钮大小
    lv_obj_set_align(btn,LV_ALIGN_CENTER);         //设置按钮基于父类画布居中
 
    lv_scr_load(main_draw);                        //加载显示画布
    
//如果需要响应按钮点击，需要注册/添加事件
struct _lv_event_dsc_t * lv_obj_add_event_cb(lv_obj_t * obj, lv_event_cb_t event_cb, lv_event_code_t filter,
                                             void * user_data);
参数：
    obj - 添加事件的对象
    event_cb - 事件处理函数
    filter - 触发事件的动作(code)
    user_data - 传递的用户数据
    
事件动作是一个枚举
typedef enum {
    LV_EVENT_ALL = 0,
 
    /** Input device events*/
    LV_EVENT_PRESSED,             /**< 按下事件*/
    LV_EVENT_PRESSING,            /**< The object is being pressed (called continuously while pressing)*/
    LV_EVENT_PRESS_LOST,          /**< The object is still being pressed but slid cursor/finger off of the object */
    LV_EVENT_SHORT_CLICKED,       /**< The object was pressed for a short period of time, then released it. Not called if scrolled.*/
    LV_EVENT_LONG_PRESSED,        /**< Object has been pressed for at least `long_press_time`.  Not called if scrolled.*/
    LV_EVENT_LONG_PRESSED_REPEAT, /**< Called after `long_press_time` in every `long_press_repeat_time` ms.  Not called if scrolled.*/
    LV_EVENT_CLICKED,             /**< Called on release if not scrolled (regardless to long press)*/
    LV_EVENT_RELEASED,            /**< Called in every cases when the object has been released*/
    LV_EVENT_SCROLL_BEGIN,        /**< Scrolling begins*/
    LV_EVENT_SCROLL_END,          /**< Scrolling ends*/
    LV_EVENT_SCROLL,              /**< Scrolling*/
    LV_EVENT_GESTURE,             /**< A gesture is detected. Get the gesture with `lv_indev_get_gesture_dir(lv_indev_get_act());` */
    LV_EVENT_KEY,                 /**< A key is sent to the object. Get the key with `lv_indev_get_key(lv_indev_get_act());`*/
    LV_EVENT_FOCUSED,             /**< The object is focused*/
    LV_EVENT_DEFOCUSED,           /**< The object is defocused*/
    LV_EVENT_LEAVE,               /**< The object is defocused but still selected*/
    LV_EVENT_HIT_TEST,            /**< Perform advanced hit-testing*/
 
    /** Drawing events*/
    LV_EVENT_COVER_CHECK,        /**< Check if the object fully covers an area. The event parameter is `lv_cover_check_info_t *`.*/
    LV_EVENT_REFR_EXT_DRAW_SIZE, /**< Get the required extra draw area around the object (e.g. for shadow). The event parameter is `lv_coord_t *` to store the size.*/
    LV_EVENT_DRAW_MAIN_BEGIN,    /**< Starting the main drawing phase*/
    LV_EVENT_DRAW_MAIN,          /**< Perform the main drawing*/
    LV_EVENT_DRAW_MAIN_END,      /**< Finishing the main drawing phase*/
    LV_EVENT_DRAW_POST_BEGIN,    /**< Starting the post draw phase (when all children are drawn)*/
    LV_EVENT_DRAW_POST,          /**< Perform the post draw phase (when all children are drawn)*/
    LV_EVENT_DRAW_POST_END,      /**< Finishing the post draw phase (when all children are drawn)*/
    LV_EVENT_DRAW_PART_BEGIN,    /**< Starting to draw a part. The event parameter is `lv_obj_draw_dsc_t *`. */
    LV_EVENT_DRAW_PART_END,      /**< Finishing to draw a part. The event parameter is `lv_obj_draw_dsc_t *`. */
 
    /** Special events*/
    LV_EVENT_VALUE_CHANGED,       /**< The object's value has changed (i.e. slider moved)*/
    LV_EVENT_INSERT,              /**< A text is inserted to the object. The event data is `char *` being inserted.*/
    LV_EVENT_REFRESH,             /**< Notify the object to refresh something on it (for the user)*/
    LV_EVENT_READY,               /**< A process has finished*/
    LV_EVENT_CANCEL,              /**< A process has been cancelled */
 
    /** Other events*/
    LV_EVENT_DELETE,              /**< Object is being deleted*/
    LV_EVENT_CHILD_CHANGED,       /**< Child was removed, added, or its size, position were changed */
    LV_EVENT_CHILD_CREATED,       /**< Child was created, always bubbles up to all parents*/
    LV_EVENT_CHILD_DELETED,       /**< Child was deleted, always bubbles up to all parents*/
    LV_EVENT_SCREEN_UNLOAD_START, /**< A screen unload started, fired immediately when scr_load is called*/
    LV_EVENT_SCREEN_LOAD_START,   /**< A screen load started, fired when the screen change delay is expired*/
    LV_EVENT_SCREEN_LOADED,       /**< A screen was loaded*/
    LV_EVENT_SCREEN_UNLOADED,     /**< A screen was unloaded*/
    LV_EVENT_SIZE_CHANGED,        /**< Object coordinates/size have changed*/
    LV_EVENT_STYLE_CHANGED,       /**< Object's style has changed*/
    LV_EVENT_LAYOUT_CHANGED,      /**< The children position has changed due to a layout recalculation*/
    LV_EVENT_GET_SELF_SIZE,       /**< Get the internal size of a widget*/
 
    _LV_EVENT_LAST,               /** Number of default events*/
 
 
    LV_EVENT_PREPROCESS = 0x80,   /** This is a flag that can be set with an event so it's processed
                                      before the class default event processing */
} lv_event_code_t;
 
//事件处理函数
void btn_handler(lv_event_t * e);
//获取触发事件的code
lv_event_code_t lv_event_get_code(lv_event_t * e);
//获取触发事件的对象
lv_obj_t * lv_event_get_target(lv_event_t * e);
//获取注册事件时传递的参数
void * lv_event_get_user_data(lv_event_t * e);
```

**2）实例效果**

![image-20260716142701790](./img/image-20260716142701790.png)

#### **3. Label - 用于显示文本或标签**

**1）函数分析**

```
创建标签控件接口：lv_obj_t * lv_label_create(lv_obj_t * parent)
 
参数分析：
    parent：父类对象指针
    返回值：返回创建的标签控件对象指针
 
实例：给按钮添加标签
    lv_obj_t *label = lv_label_create(btn1);
    lv_label_set_text(label, "Button");
    lv_obj_center(label);//设置居中
```

**2）设置字体大小接口**

```
void lv_obj_set_style_text_font(struct _lv_obj_t * obj, const lv_font_t * value, lv_style_selector_t selector)
 
参数分析：
    obj：要设置字体的控件
    value:
        设置字体有多大，字号
        存放字体大小的结构体指针 lv_font_t * 实际为 struct _lv_font_t*
    selector：指定字体样式应用的状态。 类型的状态值通常包括  （默认状态）、        LV_STATE_PRESSED（按下状态）、LV_STATE_FOCUSED（获得焦点状态）等。
```

**3）lv_font_t 结构体成员分析 --- 提供拓展**

```
typedef struct _lv_font_t {
   函数指针，用于获取指定字符的描述信息（如宽度、高度、偏移量等）。返回 true 表示成功，false 表示失败。
    bool (*get_glyph_dsc)(const struct _lv_font_t *, lv_font_glyph_dsc_t *, uint32_t letter, uint32_t letter_next);
 
   函数指针，用于获取指定字符的位图数据。返回指向位图数据的指针。
    const uint8_t * (*get_glyph_bitmap)(const struct _lv_font_t *, uint32_t);
    
   
    /*Pointer to the font in a font pack (must have the same line height)*/
    lv_coord_t line_height;          //字体的实际行高，确保文本适应这一行高。
    lv_coord_t base_line;           /*从 line_height 顶部测量到基线的距离。*/
    uint8_t subpx  : 2;             /*表示是否支持子像素渲染（如抗锯齿）。值通常为 lv_font_subpx_t 枚举类型的一个值*/
 
    int8_t underline_position;      /*下划线距离基线的距离，负值表示下划线在基线以下。 (< 0 means below the base line)*/
    int8_t underline_thickness;     /*下划线的厚度，以像素为单位*/
 
    const void * dsc;               /*存储实现特定或运行时数据的指针，可用于缓存等*/
    const struct _lv_font_t * fallback;   /*指向回退字体的指针，用于在主字体缺失字符时递归使用其他字体 */
#if LV_USE_USER_DATA
    void * user_data;               /*存储自定义用户数据的指针，仅在启用了 LV_USE_USER_DATA 时可用.*/
#endif
} lv_font_t;
 
```

**3）开启设置字体字号大小宏定义**

```
如果要设置大小需要修改lv_conf.h,设置为1开启对应的字体大小，才能提供对应的lv_font_t字体类型
```

**开启宏定义**

![image-20260716142728973](./img/image-20260716142728973.png)

![image-20260716142738715](./img/image-20260716142738715.png)

**4）实例1：设置字体大小**

```
 
    lv_obj_t * main_draw = lv_obj_create(NULL); //
    lv_obj_t * btn = lv_btn_create(main_draw);
    lv_obj_t * label = lv_label_create(btn);
    lv_label_set_text(label, "Me");
    
    
    lv_obj_set_style_text_font(label, &lv_font_montserrat_20,LV_STATE_DEFAULT);
    
    lv_scr_load(main_draw);
```

 

**5）实例2：设置按下字体大小设置为20**

```
/*Create a Demo*/
    lv_obj_t * main_draw = lv_obj_create(NULL);
    lv_obj_t * btn = lv_btn_create(main_draw);
    lv_obj_t * label = lv_label_create(btn);
    lv_label_set_text(label, "Button");
    
    //在这里设置btn的字体大小，状态为LV_STATE_PRESSED按下状态
    lv_obj_set_style_text_font(btn, &lv_font_montserrat_20,LV_STATE_PRESSED);
    
    lv_scr_load(main_draw);
```

**4. Bar - 显示条形图，可以用来表示进度或数值**

**1）函数分析**

```
1）创建条形图函数：lv_obj_t * lv_bar_create(lv_obj_t * parent)
    参数分析：
        parent：父类控件对象
    返回值：返回创建的条形图控件对象指针
    
2）设置进度条进度值:void lv_bar_set_value(lv_obj_t * obj, int32_t value, lv_anim_enable_t anim)
    参数分析：
        obj：要设置的进度条对象
        value：进度值
         anim:
        类型: lv_anim_enable_t（通常是一个枚举类型）。
        描述: 这个参数用于指定是否启用动画。常见的取值有：
            LV_ANIM_ON：启用动画效果。在这种情况下，条形图的值将会平滑地过渡到新的值。
            LV_ANIM_OFF：不启用动画。值会立即更新，不会有过渡效果。
    
设置条形图 (bar) 的最小值和最大值范围：
        void lv_bar_set_range(lv_obj_t * obj, int32_t min, int32_t max)
```

**2）创建进度条设置值为70**

```
 
    lv_obj_t * main_draw = lv_obj_create(NULL);
    lv_obj_t * bar1 = lv_bar_create(main_draw);
    lv_obj_set_size(bar1, 200, 20);
    lv_obj_center(bar1);
    lv_bar_set_range(bar1,0,100);//设置进度条上限和下限值
    lv_bar_set_value(bar1, 70, LV_ANIM_OFF);
    lv_scr_load(main_draw);
```

**实例效果**

![image-20260716142820409](./img/image-20260716142820409.png)



**3）线程动态设置进度条值**

```
要使用互斥锁与LVGL进程去进入轮询心跳机制遍历控件哈希表进行互斥，
```

 **5  List - 提供列表视图，展示一组多项，可以滚动和选择**

**1）函数分析**

```
 
1）创建列表视图控件接口：lv_list_create(lv_obj_t * parent)
   参数分析：
        parent：父类控件对象
   返回值：返回创建的列表视图控件对象指针
   
 
2）如何在list中添加按钮：lv_obj_t * lv_list_add_btn(lv_obj_t * list, const char * icon, const char * txt)
        
       使用lv_list_add_btn(list对象,自带的图片像素数据,按钮上面要显示的文字); 
关于第二个形参：
        文件夹图标:LV_SYMBOL_DIRECTORY
        给list控件添加按钮，该函数返回按钮对象（lv_obj_t *）
        
        自带的图片像素数据：是LVGL提供内置的像素数据
        
 
```

**1）基本的LVGL内置图片宏定义**

：图

**2）实例1 创建固定大小的列表视图控件**

```
    lv_obj_t * main_draw = lv_obj_create(NULL);
    lv_obj_t * dir_list  = lv_list_create(main_draw); //创建列表控件
    lv_obj_set_size(dir_list,300,480);//设置大小
    lv_scr_load(main_draw); //加载主屏幕画布 （当基类控件显示了，里面的子类默认自动显示）
```

**实例效果**

**2）实例2 往列表控件中添加按钮**

```
    lv_obj_t * main_draw = lv_obj_create(NULL);
 
    lv_obj_t * dir_list  = lv_list_create(main_draw); //创建列表控件
    lv_obj_set_size(dir_list,300,480);//设置大小
    //              (list对象,自带的图片像素数据,按钮上面要显示的文字); 
    lv_obj_t * list_btn_1 = lv_list_add_btn(dir_list,LV_SYMBOL_WIFI,"Net-Work"); 
    lv_obj_t * list_btn_2 = lv_list_add_btn(dir_list,LV_SYMBOL_TRASH,"TRASH"); 
 
    lv_scr_load(main_draw); //加载主屏幕画布 （当基类控件显示了，里面的子类默认自动显示）
```

**实例效果**

**3）设置list中按钮点击事件(普通的btn也是一样的)**

```
添加注册按钮的中断函数：
lv_obj_add_event_cb(lv_obj_t * obj, lv_event_cb_t event_cb, lv_event_code_t filter,
                                             void * user_data)
参数分析：
    形参1：obj指定要添加中断函数的控件对象（按钮对象）
    形参2：lv_event_cb_t event_cb 任务函数
        在LVGL8.2版本中发现是一个函数指针类型：
            typedef void (*lv_event_cb_t)(lv_event_t * e);
        可推理出该函数指针指向的函数返回值为void,形参为记录中断事件的结构体lv_event_t * e
    形参3：
        事件过滤：事件触发的状态过滤，填LV_EVENT_SHORT_CLICKED按下去之后触发
    形参4：自定义传参传给你的中断函数，如果不想传填NULL
    
中文分析：lv_obj_add_event_cb(按钮对象中断函数的名字,LV_EVENT_SHORT_CLICKED，（void*）传参)
 
在要调用函数里面使用lv_event_get_user_data获取传进来的数据
 
 void xxxx(lv_event_t *event) //event 保存当前触发的事件中产生的数据，比如你传进来的数据
 {
         event->user_data：void *类型，需要强转成实际的数据类型
        char *str = (char *)lv_event_get_user_data()
       
        // 处理按钮点击事件和关联的数据
        // ...
        
 }
 
考核项目中list控件的更新目录核心（一开始默认显示根目录中的目录项）：进入新的目录，删除上一个list控件，再创建新的list:
     lv_obj_del(控件对象); 
     
小工具：
    lv_obj_get_parent(e->current_target)：获取控件的父类控件指针
    event->current_target：获取当前控件指针
```

 **实例：按对应的按钮输出指定的语句，用来判断按钮了那个按钮**

```
void Btn_Handler(lv_event_t * e)
{
 
    printf("你按下了%s按钮\n",e->user_data);
 
    return ;
}
 
lv_obj_t * main_draw = lv_obj_create(NULL);
 
    lv_obj_t * dir_list  = lv_list_create(main_draw); //创建列表控件
    lv_obj_set_size(dir_list,300,480);//设置大小
    //              (list对象,自带的图片像素数据,按钮上面要显示的文字); 
    lv_obj_t * list_btn_1 = lv_list_add_btn(dir_list,LV_SYMBOL_WIFI,"Net-Work"); 
    lv_obj_t * list_btn_2 = lv_list_add_btn(dir_list,LV_SYMBOL_TRASH,"TRASH"); 
 
    
    //给按钮1按下中断函数
    lv_obj_add_event_cb(list_btn_1,Btn_Handler,LV_EVENT_SHORT_CLICKED,"Net-Work");
    lv_obj_add_event_cb(list_btn_2,Btn_Handler,LV_EVENT_SHORT_CLICKED,"TRASH");
 
```

**LVGL日志**

 lvgl也有日志和调试打印的功能，需要在编译配置时开启

在lvgl_conf.h文件中选择使用日志以及设置lvgl的日志级别

![image-20260716143200387](./img/image-20260716143200387.png)

然后再代码中调用输出日志的接口来打印日志

```
LV_LOG_USER
LV_LOG_ERROR
LV_LOG_WARN
.....
```

 **6. Check Box - 提供复选框功能，用户可以选择多个选项**

**1)函数接口分析**

```
1）创建复选框： lv_checkbox_create(main_draw);
2）设置复选框的文本：lv_checkbox_set_text(lv_obj_t * obj, const char * txt);
 
3）设计布局流向：lv_obj_set_flex_flow(lv_obj_t * obj, lv_flex_flow_t flow)
可以定义子对象的排列方式：
    LV_FLEX_FLOW_ROW：子对象按行排列。
    LV_FLEX_FLOW_COLUMN：子对象按列排列。
    LV_FLEX_FLOW_ROW_REVERSE：子对象按行反向排列。
    LV_FLEX_FLOW_COLUMN_REVERSE：子对象按列反向排列。
    LV_FLEX_FLOW_WRAP：子对象超出容器时换行或换列。
 
4）设计布局中的对齐方式：void lv_obj_set_flex_align(lv_obj_t * obj, lv_flex_align_t main_place, lv_flex_align_t cross_place,
                           lv_flex_align_t track_place)
                           
align_self: 设置该对象的对齐方式，即它自己在其容器中的对齐方式。取值可以是：
    LV_FLEX_ALIGN_START：对齐到容器的开始边（顶部或左侧）。
    LV_FLEX_ALIGN_CENTER：对齐到容器的中心。√
    LV_FLEX_ALIGN_END：对齐到容器的结束边（底部或右侧）。
    LV_FLEX_ALIGN_STRETCH：拉伸以填充容器的剩余空间。
 
align_start: 设置容器内所有子对象在主轴方向上的对齐方式。取值可以是：
    LV_FLEX_ALIGN_START：对齐到主轴的开始边。√
    LV_FLEX_ALIGN_CENTER：对齐到主轴的中心。
    LV_FLEX_ALIGN_END：对齐到主轴的结束边。
    LV_FLEX_ALIGN_STRETCH：拉伸以填充主轴方向的剩余空间。
 
align_end: 设置容器内所有子对象在交叉轴方向上的对齐方式。取值可以是：
    LV_FLEX_ALIGN_START：对齐到交叉轴的开始边。
    LV_FLEX_ALIGN_CENTER：对齐到交叉轴的中心。√
    LV_FLEX_ALIGN_END：对齐到交叉轴的结束边。
    LV_FLEX_ALIGN_STRETCH：拉伸以填充交叉轴方向的剩余空间。
    
主轴（Main Axis）
    主轴是Flex容器中子元素的主要排列方向。它可以是水平的（从左到右或从右到左），也可以是垂直的（从上到下或从下到上），这取决于Flex容器的flex-direction属性。
    当flex-direction为row或row-reverse时，主轴是水平的。
    当flex-direction为column或column-reverse时，主轴是垂直的。
交叉轴（Cross Axis）
    交叉轴是垂直于主轴的轴。它决定了子元素在主轴排列方向上的垂直（如果主轴是水平的）或水平（如果主轴是垂直的）位置。
    
5）设置复选按钮中断：struct _lv_event_dsc_t * lv_obj_add_event_cb(lv_obj_t * obj, lv_event_cb_t event_cb, lv_event_code_t filter,void * user_data)
 
参数分析：
    obj：要设置中断事件的控件
    event_cb：事件回调函数的指针。这是一个用户定义的函数，函数签名通常是 void event_cb(lv_event_t * e)
    lv_event_code_t filter:事件过滤器，指定要监听的事件类型。可以是特定的事件代码，如 
    LV_EVENT_CLICKED:
    LV_EVENT_VALUE_CHANGED:
        滑块（Slider）：当滑块的值被调整时，LV_EVENT_VALUE_CHANGED 事件会被触发。
        开关（Switch）：当开关的状态改变（开或关）时，LV_EVENT_VALUE_CHANGED 事件会被触发。
        文本输入框（Text area）：当文本输入框的内容发生变化时，会触发这个事件。
    LV_EVENT_ALL:所有事件类型 复选框使用这个状态
    
    user_data：用户数据，可以传递任何额外信息到事件回调函数中。这在需要在回调中使用特定数据时很有用。
```

**2)实例1：简单创建复选框**

```
    lv_obj_t * main_draw = lv_obj_create(NULL);
 
    lv_obj_t * select_box = lv_checkbox_create(main_draw);
    lv_checkbox_set_text(select_box,"Yes");
    lv_obj_center(select_box);
 
    lv_scr_load(main_draw); //加载主屏幕画布 （当基类控件显示了，里面的子类默认自动显示）
```

**3）复选框  实例：**

```
/*中断任务函数 复选框的函数基本目的要获取复选框的选择状态*/
static void event_handler(lv_event_t * e)
{
    lv_event_code_t code = lv_event_get_code(e);//获取当前的按钮控件对象触发事件状态
    lv_obj_t * obj = lv_event_get_target(e); //获取当前触发的复选控件
    
    //为了软件进行稳定的判断
    if(code == LV_EVENT_VALUE_CHANGED) {//判断状态是否发生改变 对应复选框控件来讲状态是必变的
                                当前状态                  打勾状态
        const char * state = lv_obj_get_state(obj) & LV_STATE_CHECKED ? "勾了" : "没勾";
       
        const char * txt = lv_checkbox_get_text(obj);
        printf("%s---%s\n",txt,state);
    }
}
 
主函数：
lv_obj_t * main_draw = lv_obj_create(NULL);
lv_obj_set_flex_flow(main_draw, LV_FLEX_FLOW_COLUMN);//设置排成一列
lv_obj_set_flex_align(main_draw, LV_FLEX_ALIGN_CENTER, LV_FLEX_ALIGN_START, LV_FLEX_ALIGN_CENTER);
 
lv_obj_t * cb_1;  //没打勾 支持点击
cb_1 = lv_checkbox_create(main_draw);//创建第一个复选控件
lv_checkbox_set_text(cb_1, "Apple"); //设置字体
lv_obj_add_event_cb(cb_1, event_handler, LV_EVENT_ALL, NULL);//添加任务函数  LV_EVENT_ALL：状态发生改变就触发调用event_handler
 
lv_obj_t * cb_2;//有打勾 支持点击
cb_2 = lv_checkbox_create(main_draw);//创建第二个复选控件
lv_checkbox_set_text(cb_2, "Banana");
lv_obj_add_state(cb_2, LV_STATE_CHECKED);//设置状态已被按下,如果不设置默认是没打勾
lv_obj_add_event_cb(cb_2, event_handler, LV_EVENT_ALL, NULL);
 
lv_obj_t * cb_3;  //没打勾 不支持点击
cb_3 = lv_checkbox_create(main_draw);//创建第三个复选控件
lv_checkbox_set_text(cb_3, "Lemon");
lv_obj_add_state(cb_3, LV_STATE_DISABLED);//设置点击关闭
 
lv_obj_t * cb_4; //有打勾  不支持点击
cb_4 = lv_checkbox_create(main_draw);//创建第四个复选控件
lv_obj_add_state(cb_4, LV_STATE_CHECKED | LV_STATE_DISABLED);
lv_checkbox_set_text(cb, "Melon\nand a new line");
lv_obj_add_event_cb(cb, event_handler, LV_EVENT_ALL, NULL);
 
lv_obj_update_layout(cb);
 
lv_scr_load(main_draw);
```

**7 Slider - 提供滑块控件，用户可以通过拖动滑块来选择值**  

```
    //滑动块
    lv_obj_t *slider = lv_slider_create(main_win);
    lv_obj_center(slider);
    lv_obj_set_size(slider, 200, 20);
    lv_bar_set_range(slider,0,100);//设置进度条上限和下限值
    lv_bar_set_value(slider, 70, LV_ANIM_OFF);
    //滑动事件处理
    lv_obj_add_event_cb(slider, slider_event_handler, LV_EVENT_VALUE_CHANGED, NULL);
```

 

**利用样式去实现修改背景颜色**

![image-20260716143243845](./img/image-20260716143243845.png)





