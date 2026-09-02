## docker



### command

#### 一、镜像操作

| 功能 | 命令 |
| ---- | ---- |
| 查看本地镜像 | docker images |
| 下载镜像 | docker pull 镜像名:标签 |
| 删除镜像 | docker rmi 镜像ID/镜像名 |

#### 二、容器查看

| 功能 | 命令 |
| ---- | ---- |
| 查看运行中容器 | docker ps |
| 查看所有容器（含已停止） | docker ps -a |

#### 三、创建&运行容器

| 功能 | 命令 |
| ---- | ---- |
| 新建交互式容器（命名，长期使用） | docker run -it --name my-ubuntu ubuntu:latest |
| 新建临时容器（退出自动删除） | docker run -it --rm ubuntu:latest |

#### 四、容器启停&登录

| 功能 | 命令 |
| ---- | ---- |
| 启动已存在容器 | docker start my-ubuntu |
| 停止运行容器 | docker stop my-ubuntu |
| 重启容器 | docker restart my-ubuntu |
| 强制关闭容器 | docker kill my-ubuntu |
| 进入正在运行的容器终端 | docker exec -it my-ubuntu /bin/bash |

#### 五、容器清理

| 功能 | 命令 |
| ---- | ---- |
| 删除单个已停止容器 | docker rm 容器ID |
| 清空所有已停止容器 | docker container prune |
| 清理全部闲置资源 | docker system prune |
| 清理闲置资源+无用镜像 | docker system prune -a |

#### 六、文件&日志

| 功能 | 命令 |
| ---- | ---- |
| 查看容器日志 | docker logs 容器名 |
| 实时查看日志 | docker logs -f 容器名 |
| 容器文件拷到本机 | docker cp 容器名:容器路径 本地路径 |
| 本机文件拷到容器 | docker cp 本地路径 容器名:容器路径 |

---
#### 固定使用流程（直接照敲）

1. 首次创建容器（仅执行一次）
`docker run -it --name my-ubuntu ubuntu:latest`

2. 后续重复使用
```bash
docker start my-ubuntu
docker exec -it my-ubuntu /bin/bash
```



### 例子

```bash
# 查所有监听端口
netstat -ano | findstr "LISTENING"

tasklist | findstr pid
taskkill /F /PID pid
```



```bash
# mysql
docker run -d \
  --name mysql \
  -p 3307:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  mysql:8.0

docker run -d --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0
docker exec -it mysql mysql -uroot -p123456
```



## cloudflared

```
# 停止隧道
docker stop cloudflared

# 重启隧道
docker restart cloudflared

# 删除容器（更新镜像/更换token时用）
docker rm -f cloudflared

# 停止日志输出：按键盘 Ctrl + C
```



## sbx

### 常用操作

```
# 查看版本，正常会输出版本号
sbx version

# 直接输 sbx，会显示所有命令
sbx
```

#### 1）起一个空沙箱（shell）

```
# 把当前目录挂载进沙箱，进入交互式 shell
sbx run shell .
```

- `.` 代表**当前目录**，会被挂载到沙箱里
- 进去后是一个独立的 Linux 环境，可随便造，**不影响主机**

#### 2）运行 AI 智能体（如 claude）

```
# 在当前项目下运行 claude code 智能体
sbx run claude .
```

首次运行会让你选**网络策略**（默认选严格即可）。

#### 3）查看沙箱列表

```
sbx ls
```

显示：名称、状态、运行时间。

#### 4）停止 / 删除沙箱

```
# 停止（保留状态）
sbx stop <沙箱名>

# 删除（彻底销毁）
sbx rm <沙箱名>
```

### 和 Docker Desktop 的区别

- **sbx**：给 AI 智能体用的**微虚拟机沙箱**，自带独立内核 + Docker，**不用装 Docker Desktop**
- **docker**：传统容器，共享主机内核，需要 Docker Desktop/Engine



网络报错：检查代理 / VPN，sbx 会走主机代理

想卸载：

```
winget uninstall Docker.sbx
```



**日常开发、联网装包 / 拉代码** → 选 **2 Balanced（平衡模式）**（推荐，兼顾安全和使用便利）

需要完整外网访问、测试网络功能 → 选 **1 Open（开放模式）**

仅本地运行、完全不需要联网 → 选 **3 Locked Down（严格隔离）**



### command

```
# 查看所有沙箱
sbx ls
```

