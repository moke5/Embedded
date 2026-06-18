# MQTT

[toc]



**EMQX 是服务端（MQTT 服务器 / Broker）**

**MQTTX 是客户端（MQTT 调试工具）**

二者是**服务端 ↔ 客户端**的配对关系，缺一不可。



## **EMQX**

> admin
>
> admin 默认密码：public

服务管理：

D:\app\program\emqx\bin

```shell
emqx start / stop / emqx_ctl status
```

EMQX Dashboard 管理控制台:

```url
http://localhost:18083/
```



## MQTTX



### 客户端连接

配置并建立 MQTT 连接。点击 + 新建连接 进入配置页面，您只需配置：



•**名称**：连接名称，如 MQTTX_Test；

•**服务器地址**： emqx@127.0.0.1

•**端口**：1833

![image-20260525203512809](./img/image-20260525203512809.png)





