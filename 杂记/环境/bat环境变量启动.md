# 使用不同的环境变量

## 比如JAVA

启动文件: start.bat

```cmd
@echo off
cd /d %~dp0
set "JAVA_HOME=JDK-8"
set "PATH=%JAVA_HOME%\bin;%PATH%"
java -jar Digital.jar
```



```batch
cd /d %~dp0
```

> **把批处理的工作目录，强制切换到「这个 bat 脚本自己所在的文件夹」。**



创建快捷方式指向这个启动脚本

```cmd
cmd /d "绝对path"
```

- `/c`：运行 bat 后自动关闭 CMD 窗口





