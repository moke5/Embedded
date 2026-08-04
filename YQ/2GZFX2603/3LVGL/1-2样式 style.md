# 样式 style

[toc]

## 样式 style

### **1. 样式的局部和状态**

在 `lvgl/src/core/lv_obj.h` 文件中描述：

```
// 样式起作用的部分
LV_PART_MAIN
LV_PART_SCROLLBAR
LV_PART_INDICATOR
LV_PART_KNOB 
LV_PART_SELECTED 
LV_PART_ITEMS 
LV_PART_TICKS  
LV_PART_CURSOR  
LV_PART_CUSTOM_FIRST 
LV_PART_ANY 
// 样式起作用的的状态：
LV_STATE_DEFAULT  
LV_STATE_CHECKED  
LV_STATE_FOCUSED  
LV_STATE_FOCUS_KEY  
LV_STATE_EDITED     
LV_STATE_HOVERED   
LV_STATE_PRESSED  
LV_STATE_SCROLLED 
LV_STATE_DISABLED 
LV_STATE_USER_1  
LV_STATE_USER_2  
LV_STATE_USER_3  
LV_STATE_USER_4    
LV_STATE_ANY
```







### **2. 样式的特点**

1. 一个样式可以给多个对象使用（正常样式）样式可以级联，也就是可以将多个样式分配给一个对象。所以，我们不用将所有属性都在一个样式中指定，可以通过多个样式组合的形式指定。 LVGL 会优先使用我们定义的样式，如果没有就会使用默认值。

2. 后来添加的样式具有更高的优先级。也就是说如果在两种样式中指定了同一个属性，则将使用最后添加的样式。

3. 如果对象中未指定某些属性（例如文本颜色），就会从父级继承。

4. 对象可以有“本地样式”，它比普通样式具有更高的优先级。

5. 可以定义有过渡效果的样式。

6. 默认有一个样式主题，我们也可以自己定义样式主题，作为默认的样式主题使用。

    

### **3. 使用样式三板斧**

一、初始化样式：样式存储在`lv_style_t`变量中。样式变量应该是 静态 、全局或动态分配 的。 也就是它们不能是函数中的局部变量，因为当函数结束时它们会被销毁。

```
static lv_style_t style;
lv_style_init(&style);
```







二、设置样式属性：样式就是控件外观的表达，其属性多种多样，他们的API接口函数通常如下所示：

```
lv_style_set_xxxxxx();
```







在文件 lvgl/src/misc/lv_style_gen.h 中可以查到不同的样式设置函数：

![img](./img/rBJlJmfdKHiAY00zAAWZrUejcL8277.jpg)

三、将样式添加到指定对象：当我们初始化并且设置好一个样式之后就可以将它添加到对象上面了，接口函数是：

### **4. 样式应用举例1**

| 1. 在界面创建一个对象，设置其背景色、背景透明度、阴影宽度、阴影颜色等样式，并令其呈现如右边效果： | ![img](./img/rBJlJmfdLXmAUtvLAAAzC7YPq-A990.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------ |
|                                                              |                                                  |

代码：

```
// 初始化样式
static lv_style_t style;
lv_style_init(&style);

// 设置圆角、透明度、背景色、阴影等样式属性
lv_style_set_radius(&style, 5);
lv_style_set_bg_opa(&style, LV_OPA_COVER);
lv_style_set_bg_color(&style, lv_palette_lighten(LV_PALETTE_GREY, 1));
lv_style_set_shadow_width(&style, 55);
lv_style_set_shadow_color(&style, lv_palette_main(LV_PALETTE_BLUE));

// 将样式添加到obj
lv_obj_t * obj = lv_obj_create(lv_scr_act());
lv_obj_add_style(obj, &style, 0);
```







### **5. 样式应用举例2**

| 在界面创建两个按钮，第一个按钮设置背景、字体、圆角、阴影、边框等属性，第二个按钮在第一个按钮属性的基础上更改背景、字体和边框，令其呈现如右效果： | ![img](./img/rBJlJmfdLtSAC2e8AAAjLmmQN1I448.jpg) |
| ------------------------------------------------------------ | ------------------------------------------------ |
|                                                              |                                                  |

代码：

```
/*A base style*/
static lv_style_t style_base;
lv_style_init(&style_base);
lv_style_set_bg_color(&style_base, lv_palette_main(LV_PALETTE_LIGHT_BLUE));
lv_style_set_border_color(&style_base, lv_palette_darken(LV_PALETTE_LIGHT_BLUE, 3));
lv_style_set_border_width(&style_base, 2);
lv_style_set_radius(&style_base, 10);
lv_style_set_shadow_width(&style_base, 10);
lv_style_set_shadow_ofs_y(&style_base, 5);
lv_style_set_shadow_opa(&style_base, LV_OPA_50);
lv_style_set_text_color(&style_base, lv_color_white());
lv_style_set_width(&style_base, 100);
lv_style_set_height(&style_base, LV_SIZE_CONTENT);

/*Set only the properties that should be different*/
static lv_style_t style_warning;
lv_style_init(&style_warning);
lv_style_set_bg_color(&style_warning, lv_palette_main(LV_PALETTE_YELLOW));
lv_style_set_border_color(&style_warning, lv_palette_darken(LV_PALETTE_YELLOW, 3));
lv_style_set_text_color(&style_warning, lv_palette_darken(LV_PALETTE_YELLOW, 4));

/*Create an object with the base style only*/
lv_obj_t * obj_base = lv_obj_create(lv_scr_act());
lv_obj_add_style(obj_base, &style_base, 0);
lv_obj_align(obj_base, LV_ALIGN_LEFT_MID, 20, 0);

lv_obj_t * label = lv_label_create(obj_base);
lv_label_set_text(label, "Base");
lv_obj_center(label);

/*Create another object with the base style and earnings style too*/
lv_obj_t * obj_warning = lv_obj_create(lv_scr_act());
lv_obj_add_style(obj_warning, &style_base, 0);
lv_obj_add_style(obj_warning, &style_warning, 0);
lv_obj_align(obj_warning, LV_ALIGN_RIGHT_MID, -20, 0);

label = lv_label_create(obj_warning);
lv_label_set_text(label, "Warning");
lv_obj_center(label);
```







### **6. 样式应用举例3**

| 在界面创建一个对象，设定器: | ![img](./img/rBJlJmfdL62AL_J5AAKs5WkEFWc219.jpg) |
| --------------------------- | ------------------------------------------------ |
|                             |                                                  |

代码：

```
// 数组props，用于指定背景色、边框色和边框宽度三个属性将在过渡期间被修改
static const lv_style_prop_t props[] = {LV_STYLE_BG_COLOR, LV_STYLE_BORDER_COLOR, LV_STYLE_BORDER_WIDTH, 0};

// 过渡持续时间（100毫秒），即过渡动画完成所需的时间
// 延迟时间（200毫秒），表示在状态改变后，过渡动画开始前需要等待的时间
static lv_style_transition_dsc_t trans_def;
lv_style_transition_dsc_init(&trans_def, props, lv_anim_path_linear, 100, 200, NULL);

/* A special transition when going to pressed state
 * Make it slow (500 ms) but start  without delay*/
static lv_style_transition_dsc_t trans_pr;
lv_style_transition_dsc_init(&trans_pr, props, lv_anim_path_linear, 500, 0, NULL);

static lv_style_t style_def;
lv_style_init(&style_def);
lv_style_set_transition(&style_def, &trans_def);

static lv_style_t style_pr;
lv_style_init(&style_pr);
lv_style_set_bg_color(&style_pr, lv_palette_main(LV_PALETTE_RED));
lv_style_set_border_width(&style_pr, 6);
lv_style_set_border_color(&style_pr, lv_palette_darken(LV_PALETTE_RED, 3));
lv_style_set_transition(&style_pr, &trans_pr);

/*Create an object with the new style_pr*/
lv_obj_t * obj = lv_obj_create(lv_scr_act());
lv_obj_add_style(obj, &style_def, 0);
lv_obj_add_style(obj, &style_p r, LV_STATE_PRESSED);

lv_obj_center(obj);
```



