# 一些命令

[toc]



### ps



#### 查看单个进程

```bash
ps -o pid,stat,cmd -p PID
```



### top

```

```



### grep



```
grep -rn "malloc" . --exclude-dir=.git --exclude-dir=build

find . \
-path "./build" -prune -o \
-name "*.c" -print \
| xargs grep "malloc"
```



### find



```
find . -type f -executable

.
当前目录

-type f
普通文件

-executable
具有执行权限
```



- 排除指定目录

```
find . -type f -name "*.c" -not -path "./build/*" -not -path "./.git/*"

找到：
    普通文件
    名字是 *.c

排除：
    ./build/*
    ./.git/*
```



```
find . -path "./build" -prune -o -name "*.c" -print

遇到 build
    ↓
跳过，不进入

其他目录
    ↓
继续查找 .c 文件

find . \
-path "./build" -prune -o \
-path "./.git" -prune -o \
-name "*.c" -print
```



- 查看正在运行程序的位置

```
ps aux | grep [exe]
----> pid
ls -l /proc/[pid]/exe
```

