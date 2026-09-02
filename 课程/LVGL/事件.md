# 事件 event

[toc]



当对象状态发生变化时，就会触发某个事件，比如某个按钮被点击、滑动条发生滚动、下拉列表被选中等等，我们可以给某个感兴趣的事件设定回调函数，令其在该事件发生时被自动调用。

## **1.事件的特点**

- 一个事件回调函数可以同时绑定多个不同的事件

- 一个对象不同的状态改变可以绑定不同的回调函数

- 一个对象相同的状态改变可以多次绑定同一个回调函数，以便传入不同的参数，这些回调函数将以绑定的次序被依次调用

- 通过给对象设置“冒泡”标签，可以将对象的事件传递给其父对象

    

## **2.事件的种类**

- 输入设备事件(Input device events)
- 绘图事件(Drawing events)
- 其他事件(Special events)
- 特殊事件(Other events)
- 自定义事件(Custom events)
    具体而言，每一类事件都包含很多不同的组件状态变更，比如：
- 单击：LV_EVENT_PRESSED
- 长按：LV_EVENT_LONG_PRESSED
- 滚动：LV_EVENT_SCROLL
- 数值变更：LV_EVENT_VALUE_CHANGED
- 子对象被创建：LV_EVENT_CHILD_CREATED
- 子对象被删除：LV_EVENT_CHILD_DELETED
    在文件 lvgl/src/core/lv_event.h 中可以查到不同的事件代号（宏）：

![img](./img/rBJlJmfg12KACzAYAAEElD_skZ4792.jpg)

## **3.事件的一般处理流程**

- 编写事件回调函数，比如希望当一个按钮被点击时，自动调用如下函数：

```
static void my_event_cb(lv_event_t * event)
{
    printf("Clicked\n");
} 
```







- 添加事件到对象。用户可以为对象指定回调函数，比如：

```
lv_obj_t * btn = lv_button_create(lv_screen_active());
lv_obj_add_event_cb(btn, my_event_cb, LV_EVENT_CLICKED, NULL);
```







- 获得触发回调函数的具体事件code，以便于在同一个回调函数中针对不同事件做不同处理。比如：

```
static void event_cb(lv_event_t * e)
{
    lv_event_code_t code = lv_event_get_code(e);
    lv_obj_t * label = lv_event_get_user_data(e);

    switch(code) {
        case LV_EVENT_PRESSED:
            lv_label_set_text(label, "The last button event:\nLV_EVENT_PRESSED");
            break;
        case LV_EVENT_CLICKED:
            lv_label_set_text(label, "The last button event:\nLV_EVENT_CLICKED");
            break;
        case LV_EVENT_LONG_PRESSED:
            lv_label_set_text(label, "The last button event:\nLV_EVENT_LONG_PRESSED");
            break;
        case LV_EVENT_LONG_PRESSED_REPEAT:
            lv_label_set_text(label, "The last button event:\nLV_EVENT_LONG_PRESSED_REPEAT");
            break;
        default:
            break;
    }
}
```







## **4.事件冒泡**

如果启用了 `lv_obj_add_flag(obj, LV_OBJ_FLAG_EVENT_BUBBLE)`，所有事件也将发送到对象的父级。如果父级也启用了`LV_OBJ_FLAG_EVENT_BUBBLE`，则事件也将发送到其父级，依此类推。