# port



##### 查看所有正在运行端口 + 进程

```shell
netstat -ano
```



##### 只看**占用端口**（常用）

```shell
netstat -ano | findstr "LISTENING"
```



##### 查指定端口

```shell
netstat -ano | findstr "8081"
```



##### 通过 PID 查看是哪个程序

```shell
tasklist | findstr "PID号"
```



##### 直接杀死占用端口进程

```shell
taskkill /F /PID pid
```



#### 服务



##### 运行服务

- 需要管理员权限

```shell
net start mysql
```

