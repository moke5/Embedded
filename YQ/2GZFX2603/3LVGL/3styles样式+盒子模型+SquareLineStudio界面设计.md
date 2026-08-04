# styles样式+盒子模型+SquareLineStudio界面设计

## styles样式+盒子模型

#### **一、LVGL对象的盒子模型**

```
LVGL 遵循 CSS 的 border-box 模型。 对象的“盒子”由以下部分构成：
边界(bounding)：元素的宽度/高度围起来的区域(整个盒子)。
边框(border)：边框有大小和颜色等属性(相当于盒子的厚度和它的颜色)。
填充(padding)：对象两侧与其子对象之间的空间(盒子的填充物)。
内容(content)：如果边界框按边框宽度和填充的大小缩小，则显示其大小的内容区域(盒子实际装东西的区域)。
轮廓(outline) ：LVGL中没有外边距(margin)的概念(盒子之间的距离)，确认代之的是轮廓(outline)。它是绘制于元素(盒子)周围的一条线，它不占据空间，位于边框边缘的外围，可起到突出元素(盒子)的作用。在浏览器里，当鼠标点击或使用Tab键让一个选项或者一个图片获得焦点的时候，这个元素就会多了一个轮廓框围绕。轮廓(outline) 。
LVGL的盒子模型是我们理解对象(部件)的组成，修改对象的样式，实现对对象的布局、处理对象排列等等的关键。
```



![image-20260718090414908](./img/image-20260718090414908.png)

#### **二、样式(Styles)**

##### **1. 简介**

```
Styles 用于设置对象的外观。
样式是一个 lv_style_t 变量，它可以保存边框宽度、文本颜色等属性。
将样式(变量)分配给对象就可以改变其外观。在赋值过程中，可以指定目标部分和目标状态。
一个样式可以给多个对象使用（正常样式）。
样式可以级联，也就是可以将多个样式分配给一个对象。所以，我们不用将所有属性都在一个样式中指定，可以通过多个样式组合的形式指定。 LVGL 会优先使用我们定义的样式，如果没有就会使用默认值。
后来添加的样式具有更高的优先级。也就是说如果在两种样式中指定了同一个属性，则将使用最后添加的样式。
如果对象中未指定某些属性（例如文本颜色），就会从父级继承。
上面说的是 “正常” 样式，对象还有本地样式，它比 “正常” 样式具有更高的优先级。
可以定义有过渡效果的样式。
默认有一个样式主题，我们也可以自己定义样式主题，作为默认的样式主题使用。
```

 

##### **2.初始化样式**

```
样式存储在 lv_style_t 变量中。样式变量应该是 静态 、全局或动态分配 的。 也就是它们不能是函数中的局部变量，因为当函数结束时它们会被销毁。样式初始化示例：
static lv_style_t style_obj;	
lv_style_init(&style_obj);
```

 

##### **3.设置样式属性**

```
当我们初始化好一个样式之后就可以设置它的样式属性了，接口函数是这样的格式：
lv_style_set_<property_name>(&style, <value>);
 
示例：
lv_style_set_bg_color(&style_obj, lv_color_hex(0x000000));   // 设置背景色
lv_style_set_bg_opa(&style_obj, LV_OPA_50);// 设置背景透明度
lv_style_set_....
```

 

##### **4.添加样式到对象**

```
当我们初始化并且设置好一个样式之后就可以将它添加到对象上面了，接口函数只有一个：
lv_obj_add_style(obj, &style, <selector>)
 
参数 “obj” 就是要添加到的对象，“style” 是指向样式变量的指针，<selector> 是应添加样式的部分和状态的 OR-ed 值 (不能是互斥，否则就是清除标志，没法合并)。
示例：
lv_obj_add_style(obj, &style_obj, 0);   // 默认(常用)
lv_obj_add_style(obj, &style_obj, LV_STATE_PRESSED);  // 在对象被按下时应用样式
 
案例：
    lv_obj_t*widget = lv_obj_create(lv_scr_act());
    lv_obj_set_size(widget,100,100);
    lv_obj_set_align(widget,LV_ALIGN_CENTER);
 
    //1、定义一个样式变量
    static lv_style_t style;
    //2、初始化变量
    lv_style_init(&style);
    //3、往样式变量中设置背景颜色
    lv_style_set_bg_color(&style,lv_color_hex(0xff0000));
    //4、将样式变量 添加到对象中
    lv_obj_add_style(widget,&style,0);
```



![image-20260718090439950](./img/image-20260718090439950.png)

##### **5.获取样式属性**

```
我们可以获取属性的最终值（考虑级联、继承、本地样式和转换），接口函数是这样的格式：
    lv_obj_get_style_<property_name>(obj, <part>);
    
函数使用对象的当前状态，如果没有更好的候选对象，则返回默认值。 例如：
    lv_color_t color = lv_obj_get_style_bg_color(obj, LV_PART_MAIN);
```

 

##### **6.删除样式**

```
删除对象的所有样式：
    lv_obj_remove_style_all(obj);
 
删除对象的特定样式：
    lv_obj_remove_style(obj, &style_obj, selector);
    
只有当 selector 与 lv_obj_add_style 中使用的 selector 匹配时，此函数才会删除 style
如果 style 是空，那么会根据给出的 selector 检查并删除所有匹配的样式
如果 selector 是 LV_STATE_ANY 或 LV_PART_ANY 就会删除具有任何状态或部分的样式。
下面这个效果和lv_obj_remove_style_all 的效果是一样的：
     lv_obj_remove_style(obj, NULL, LV_STATE_ANY | LV_PART_ANY );
```

 

##### **7.查看样式属性**

```
所有的可用的样式属性我们可以在文档或者代码中获取得到。
文档位置：
英文原版：https://docs.lvgl.io/8.1/overview/style-props.html
中文翻译：http://lvgl.100ask.net/8.1/overview/style-props.html
代码位置：
普通样式：lvgl/src/misc/lv_style_gen.h
本地样式：lvgl/src/core/lv_obj_style_gen.h
文档位置和代码位置可能在后续的版本更新中会发生变化，这里的方法只是提供参考，不需要死记硬背函数接口名。
```



![image-20260718090510278](./img/image-20260718090510278.png)



##### **8.背景部分的属性**

```
背景属性和我们前面学习的盒子模型关系很大，背景属性主要有一下这些：
背景(Background)
边界(Border)
轮廓(Outline)
阴影(Shadow)
填充(Padding)
宽度和高度变换
X和Y变换
```

 

##### **9.样式的状态和部分**

 **1）状态（status）**

```
对象可以处于以下状态的组合：
LV_STATE_DEFAULT (0x0000) 正常，释放状态
LV_STATE_CHECKED (0x0001) 切换或检查状态
LV_STATE_FOCUSED (0x0002) 通过键盘或编码器聚焦或通过触摸板/鼠标点击
LV_STATE_FOCUS_KEY (0x0004) 通过键盘或编码器聚焦，但不通过触摸板/鼠标聚焦
LV_STATE_EDITED (0x0008) 由编码器编辑
LV_STATE_HOVERED (0x0010) 鼠标悬停（现在不支持）
LV_STATE_PRESSED (0x0020) 被按下
LV_STATE_SCROLLED (0x0040) 正在滚动
LV_STATE_DISABLED (0x0080) 禁用状态
LV_STATE_USER_1 (0x1000) 自定义状态
LV_STATE_USER_2 (0x2000) 自定义状态
LV_STATE_USER_3 (0x4000) 自定义状态
LV_STATE_USER_4 (0x8000) 自定义状态
这些可能会随着lvgl的更新而不断增加，同学们可以阅读最新版本的文档获取最新资料。
```

 

**2）部分(part)**

```
对象可以有 部分(parts) ，它们也可以有自己的样式。LVGL 中存在以下预定义部分：
LV_PART_MAIN  类似矩形的背景
LV_PART_SCROLLBAR  滚动条
LV_PART_INDICATOR  指标，例如用于滑块、条、开关或复选框的勾选框
LV_PART_KNOB  像手柄一样可以抓取调整值
LV_PART_SELECTED  表示当前选择的选项或部分
LV_PART_ITEMS  如果小部件具有多个相似元素（例如表格单元格）
LV_PART_TICKS  刻度上的刻度，例如对于图表或仪表
LV_PART_CURSOR  标记一个特定的地方，例如文本区域或图表的光标
LV_PART_CUSTOM_FIRST 可以从这里添加自定义部件。
这些可能会随着lvgl的更新而不断增加，同学们可以阅读最新版本的文档获取最新资料。
```

 

##### **10.本地样式**

```
除了“普通” 样式外，对象还可以存储 本地样式(私有样式) 。
本地样式与普通样式类似，但是它不能在其他对象之间共享。如果使用本地样式，将自动分配局部样式，并在删除对象时释放。本地样式对于向对象添加本地自定义很有用。
本地样式的接口函数是这样的格式：
lv_obj_set_style_<property_name>(obj, <value>, <selector>);
 
示例：
lv_obj_set_style_bg_color(obj,  lv_color_hex(0xffffff), 0);   // 设置背景色
lv_obj_set_style_bg_opa(obj, LV_OPA_50, 0); // 设置背景透明度lv_style_set_style_....
 
删除本地样式的时候我们删除某一个样式：
v_obj_remove_local_style_prop(obj, LV_STYLE_..., selector);
LV_STYLE_...的取值请看： lvgl/src/misc/lv_style.h 中的 lv_style_prop_t
```

 

##### **11.样式继承**

```
某些属性（通常与文本相关）可以从父对象的样式继承。
只有没有在为对象设置样式属性的时候，才应用继承。 在这种情况下，如果这个属性是可继承的，那这个属性的值会在父类中检索，直到一个对象为该属性指定了一个值。父类将使用自己的状态来确定该值。 因此，如果按下按钮，并且文本颜色来自此处，则将使用按下的文本颜色。
```

 

##### **12.过渡特效**

```
默认情况下，当一个对象改变状态（例如它被按下）时，新状态的新属性会立即设置。但是，通过转换，可以在状态更改时播放动画。 例如，按下按钮时，其背景颜色可以在 300 毫秒内动画显示为按下的颜色。
demo体验
	https://docs.lvgl.io/8.1/overview/style.html#transition
	http://lvgl.100ask.net/8.1/overview/style.html#transition
这部分我们在后面课程再展开讨论
 
```

##### **13.样式主题**

```C
主题是风格的集合。如果存在活动主题，LVGL将其应用于每个创建的部件(对象)。 这将为UI提供一个默认外观，然后可以通过添加更多样式对其进行修改。
demo体验：	
https://docs.lvgl.io/8.1/overview/style.html#extending-the-current-theme
	http://lvgl.100ask.net/8.1/overview/style.html#extending-the-current-theme
这部分后面的课程再展开讨论。
 
    //得到当前屏幕的界面对象
    lv_obj_t*parent = lv_scr_act();
    int width = lv_obj_get_width(parent);
    int height = lv_obj_get_height(parent);
 
    lv_obj_t*btn1 = lv_btn_create(parent);
    lv_obj_set_size(btn1, 100, 100);
 
    lv_obj_t*btn2 = lv_btn_create(parent);
    lv_obj_set_size(btn2, 100, 100);
    lv_obj_align(btn2, LV_ALIGN_CENTER, 0, 0);
 
    //初始化样式
    static lv_style_t style;
    lv_style_init(&style);
    lv_style_set_bg_color(&style, lv_color_hex(0xff0000));
    lv_style_set_border_width(&style, 10);
    lv_style_set_border_color(&style, lv_color_hex(0x00ff00));
 
    //把设置好的样式生效于控件
    lv_obj_add_style(btn1, &style, LV_PART_MAIN);
    lv_obj_add_style(btn2, &style, LV_PART_MAIN);
```

 

练习：

设计一个按钮，设置其样式如下：

```
默认状态下背景是蓝色，字体黑色
按下状态下背景红色，字体白色
 
扩展：
    按下后突出边框，边框显示绿色
```

 

#### **三.LVGL的多界面编程**

##### **1、界面跳转原理**

界面跳转

![image-20260718090541117](./img/image-20260718090541117.png)

##### **2、代码实现**

```C
void login_handler(lv_event_t * e);
lv_obj_t *scr1;
lv_obj_t *scr2;
//返回按钮响应函数
void back_handler(lv_event_t * e) {
    //创建一个界面
    scr1 = lv_obj_create(lv_scr_act());
    //设置界面大小
    lv_obj_set_size(scr1, 800, 480);
    //在界面上创建一个按钮
    lv_obj_t *login_btn = lv_btn_create(scr1);
    //设置按钮的大小
    lv_obj_set_size(login_btn, 100, 100);
    //设置按钮的位置
    lv_obj_set_pos(login_btn, 100, 100);
    //设置登入按钮的响应函数
    lv_obj_add_event_cb(login_btn, login_handler, LV_EVENT_PRESSED, NULL);
    //加载第一个界面
    //lv_scr_load(scr1);
    //删除第二个界面
    lv_obj_del(scr2);
}
 
//登入按钮响应函数
void login_handler(lv_event_t * e) {
    //创建第二个界面
    scr2 = lv_obj_create(lv_scr_act());
    //设置界面大小
    lv_obj_set_size(scr2, 800, 480);
    //在界面上创建一个按钮
    lv_obj_t *back_btn = lv_btn_create(scr2);
    //设置按钮的大小
    lv_obj_set_size(back_btn, 100, 100);
    //设置按钮的位置
    lv_obj_set_pos(back_btn, 300, 100);
    //设置登入按钮的响应函数
    lv_obj_add_event_cb(back_btn, back_handler, LV_EVENT_PRESSED, NULL);
    //加载第二个界面
    //lv_scr_load(scr2);
 
    //删除第一个界面
    lv_obj_del(scr1);
}
 
 
//主函数代码
    //创建一个界面
   scr1 = lv_obj_create(lv_scr_act());
   //设置界面大小
   lv_obj_set_size(scr1, 800, 480);
   //在界面上创建一个按钮
   lv_obj_t *btn = lv_btn_create(scr1);
   //设置按钮的大小
   lv_obj_set_size(btn, 100, 100);
   //设置按钮的位置
   lv_obj_set_pos(btn, 100, 100);
   //设置登入按钮的响应函数
   lv_obj_add_event_cb(btn, login_handler, LV_EVENT_PRESSED, NULL);
```



## SquareLineStudio

LVGL软件组件编程



**1.问题的引入**

我们使用纯代码编写LVGL界面的方式比较麻烦，所以LVGL社区和第三方公司给LVGL开发出一些配套的UI设计工具，比如说squareLineStudio以及GUI Builder,允许用户以所见即所得的方式创建界面布局，然后导出为LVGL代码。本文主要介绍squareLineStudio软件的操作方式。

 GUI Builder

![image-20260718091428281](./img/image-20260718091428281.png)



squareLineStudio

![image-20260718091447153](./img/image-20260718091447153.png)

**2.squareLineStudio介绍**

SquareLine Studio是一款专业的Ul设计软件,它与LVGL（Light and Versatile Graphics Library,轻量级通用图形库）紧密集成。LVGL是一个轻量化的、开源的、在嵌入式系统中广泛使用的图形库，它提供了一套丰富的控件和组件，使得在资源受限的设备上创建高端的图形界面成为可能。

![image-20260718091507527](./img/image-20260718091507527.png)

SquareLineStudio具有直观的拖放界面，用户可以通过拖放组件来设计用户界面，无需编写复杂的代码。它支持多种组件和布局，并允许用户自定义样式、动画和行为。此外，SquareLineStudio也提供了丰富的模板供用户选择，用户可以根据需求快速创建各类设计项目，如海报、邀请函等。

除了UI设计功能，SquareLineStudio还具备二维制图、三维建模和参数化设计的能力。用户可以轻松创建各种建筑图纸，如平面图、立面图、剖面图等;也可以构建精确的三维模型以展示建筑空间和结构;同时，通过参数化设计，用户可以快速调整建筑模型的尺寸和形状，实现灵活的设计变更。

在SquareLineStudio中，用户还可以添加各种设计元素，如文本、图片、形状、图表等，并可以从图库中选择现成的设计元素。在编辑过程中，用户可以通过调整设计元素的大小、颜色、字体等属性进行个性化编辑。完成设计后，用户还可以预览整体效果，并导出为图片或PDF格式保存到本地。

 

不过，目前该软件只能支持30天试用，而且免费版的使用有诸多限制，所以需要开发复杂的界面还需要进行付费购买。

![image-20260718091526653](./img/image-20260718091526653.png)



**3.下载安装**

**1.下载**

点击https://squareline.io/，进行下载

![image-20260718091550439](./img/image-20260718091550439.png)



![image-20260718091558468](./img/image-20260718091558468.png)

**2.如何使用squareLineStudio**

对于如何使用该软件，最好的方式是查看官网文档 https://docs.squareline.io/docs/squareline

![image-20260718091618267](./img/image-20260718091618267.png)



**4. 创建工程**

安装完成之后，可以看到如图画面，点击创建工程

![image-20260718091634687](./img/image-20260718091634687.png)

![image-20260718091646105](./img/image-20260718091646105.png)

不过为了加快工程构建，颜色深度Color depth 选择16bit即可

创建出来之后，可以看到如图界面

![image-20260718091703115](./img/image-20260718091703115.png)

**5.操作使用**

 

**1.软件布局介绍**

![image-20260718091720183](./img/image-20260718091720183.png)

**2.设置工程导出路径**

我们使用该软件的目的就是为了导出UI设计器生成界面的C文件，所以要先进行设置工程导出的存储位置，以及导出的C文件包含的头文件

![image-20260718091737764](./img/image-20260718091737764.png)

![image-20260718091753407](./img/image-20260718091753407.png)

**3.添加PNG图像**

![image-20260718091808638](./img/image-20260718091808638.png)

此时可以看到添加成功

![image-20260718091821907](./img/image-20260718091821907.png)

这些图像可以作为界面的背景图片 或者 控件的背景图片

![image-20260718091842417](./img/image-20260718091842417.png)

**4.导出C文件**

![image-20260718091855142](./img/image-20260718091855142.png)

![image-20260718091906747](./img/image-20260718091906747.png)

【文件夹】

components文件夹：通常这个文件夹用于存放自定义组件的相关代码，这些组件是在SquareLine Studio中设计并自定义的，例如某些特殊的按钮样式、图表或其他复合控件。如果项目中包含了自定义组件，那么它们的实现代码将会在这个文件夹下。

 

fonts文件夹：存放字体资源，包括已转换为LVGL可读格式的字体文件，可能有预编译后的二进制字体数据文件，或者是原始的字体文件以及相关的加载和注册代码。

images文件夹：包含项目中使用的图像资源，如图标、背景图片等。这些图像经过处理后，通常是转换成C语言数组形式的二进制数据，可以直接被嵌入到应用程序中并在LVGL中显示。

screens文件夹：存储每个屏幕或页面的布局和组件信息。每个屏幕对应一个或多个C文件，其中包含了屏幕的初始化代码，即定义并创建UI界面上所有控件的代码。

 

【c文件】

ui.c和ui.h:

u.c是主要的UI实现文件，它包含了所有屏幕的初始化函数以及可能的全局变量声明和初始化。通过调用这些函数来实例化和连接UI界面的所有元素。

ui.h则是对应的头文件，包含了对外公开的函数声明和常量定义，以便在主程序或其他模块中引用和调用UI初始化及交互函数。

ui_events.c和ui_events.h:这些文件通常包含了对UI组件事件处理的代码，如按钮按下、滑动事件、输入框文本变化等。

ui_events.c实现具体的事件回调函数，而ui_events.h 则是对外部可见的事件处理函数声明。

ui_helpers.c和ui_helpers.h:这些文件用于存放辅助函数，用于简化UI组件的创建、更新和管理，或者是封装了一些通用的LVGL对象操作逻辑。这些函数有助于提高代码的可读性和复用性。

总结来说，SquareLine Studio导出的文件集合是为了方便用户直接将设计的Ul界面整合到嵌入式系统项目中，涵盖了所需的全部资源文件和实现代码，使得开发者能够快速地将设计成果部署到目标平台上运行。

 

**6.将导出的C文件合并到ARM-LVGL项目**

导出的C文件要进行简单修改，最终合并到LVGL项目中执行

1.SquareLine工程中要设置

![image-20260718091925571](./img/image-20260718091925571.png)



2.导出C文件

![image-20260718091940709](./img/image-20260718091940709.png)

导出之后，可以在LVGL工程下看到 已经包含了 squareLine 软件导出的所有C文件

![image-20260718091954602](./img/image-20260718091954602.png)

3.修改LVGL工程中的Makefile文件

现在我们将整个squareLine软件导出的文件 放入了LVGL工程中，所以需要在Makefile文件中指定导出的C源文件和对应的头文件

![image-20260718092007579](./img/image-20260718092007579.png)

4.在main.c函数中，添加头文件 和 直接调用 导出的C文件的函数 ui_init()

![image-20260718092019383](./img/image-20260718092019383.png)



![image-20260718092029963](./img/image-20260718092029963.png)

5.编译工程

如提示报错：

![image-20260718092042703](./img/image-20260718092042703.png)

解决方法：

![image-20260718092055816](./img/image-20260718092055816.png)

最后编译可以了

**7.显示汉字**

**1.添加字体文件到资源中**  

![image-20260718092114773](./img/image-20260718092114773.png)

成功如图所示  

![image-20260718092125894](./img/image-20260718092125894.png)

**2.添加中文字体**

![image-20260718092143235](./img/image-20260718092143235.png)

**3.设置中文字体**  

![image-20260718092201769](./img/image-20260718092201769.png)

**4.导出**

![image-20260718092214433](./img/image-20260718092214433.png)

编译工程并运行即可















