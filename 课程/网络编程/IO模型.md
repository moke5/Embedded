# IO模型

[toc]

## **阻塞与轮询**

### **1. 问题的提出**

对于网络服务器，不管是基于UDP还是基于TCP，都需要处理多个客户端的问题，对于具体这两种协议，可以分开讨论：

**UDP**
UDP协议不需要连接，因此服务端只需要一个套接字便可与任意个客户端通信，但默认的套接字是阻塞型的，这意味着当远端客户端没有发来消息的时候，服务端冒然调用 `recvfrom()` 将会进入不限期阻塞而无法做别的事情。

**TCP**
对于TCP而言，每当有一个远端的客户端发起链接成功后，服务端这边都会新增一个已连接套接字与之匹对，那么随着客户端链接的越来越多，服务端要处理的套接字也随之增多，如何同时妥善处理这些套接字成为必须解决的问题。

#### **1.1 IO模型**

所谓服务器IO模型，指的是当一个服务端网络程序需要同时处理多个套接字时，采取什么策略去妥善处理它们。由于网络数据的到达是无法预见的，因此不能像读取本地数据那样直接读取，要考虑如果数据不能及时到达应该如何处理的问题。

一般而言，服务端IO模型包括：

1. 非阻塞轮询
2. 多任务并发
3. 异步信号
4. 多路复用

### **2. 服务器IO模型（一）：非阻塞轮询**

第一个可以想到的办法，就是将所有的套接字都设置为非阻塞，既然都是非阻塞了，那就不用担心对端迟迟不发出数据导致本端卡死的问题，但与此同时，非阻塞套接字也无法妥善地告知本端程序对端数据究竟何时到达，以至于本端需要不断地尝试读取对端数据，这就是非阻塞带来的 **轮询** 模式。

轮询并非一个好方案，不值得推荐，但我们需要知道如何设置阻塞、非阻塞，对这两种模式的设定要熟练掌握。

#### **2.1 将套接字设置为非阻塞**

核心代码如下：

```C
long state = fcntl(sockfd, F_GETFL);
state |= O_NONBLOCK;
fcntl(sockfd, F_SETFL, state);
```

**注意：**
一定要先用 `F_GETFL` 获取套接字已有属性，然后通过位或运算加上非阻塞属性 `O_NONBLOCK`，然后再用 `F_SETFL` 进行设定，不能直接设定，因为要保留原来的属性值。

设置了非阻塞属性的套接字，在接下去的操作中需要判断返回状态，当相关API函数返回出错时，必须要将非阻塞资源暂时不可得的错误单独挑出来。

以下以读取UDP数据为例，展示如何使用轮询：

**核心代码：**（[nonBlockUDP.c](http://vm.yueqian.com.cn:8886/group1/M00/00/FC/rBJlJmT32EeAB2V6AAAI0OBQVeU43933.c?token=null&ts=null&filename=nonblockUDP.c)）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: nonBlockUDP.c
//  描述: 基于UDP协议的非阻塞轮询方式，接收对端数据
//
///////////////////////////////////////////////////////

int main(int argc, char const *argv[])
{
    // 创建UDP套接字并绑定地址
    int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY); // 服务器IP
    addr.sin_port = htons(PORT); // 接收数据端口
    bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));

    // 将套接字设定位非阻塞
    long state = fcntl(sockfd, F_GETFL);
    state |= O_NONBLOCK;
    fcntl(sockfd, F_SETFL, state);

    // 轮询接收UDP数据
    char buf[100];
    while(1)
    {
        bzero(buf, 100);

        socklen_t len = sizeof(clientAddr);
        bzero(&clientAddr, len);

        // 等待UDP数据
        int n = recvfrom(sockfd, buf, 100, 0,(struct sockaddr *)&clientAddr, &len);

        // 资源暂时不可得
        if(n == -1 && errno == EAGAIN)
            continue;

        // 正常读到数据
        else if(n > 0)
            printf("收到：%s\n", buf);
    }

    close(sockfd);
    return 0;
}
```



编译并执行上述代码，可以注意到，在程序运行期间，系统CPU单核利用率达100%，这说明程序一直在做无用的循环，白白浪费系统资源，因此轮询的IO方式一般是不被采用的。

#### **2.2 将套接字设置为阻塞**

当要把套接字重新设置回阻塞状态时，可用如下代码达到目的：

```C
long state = fcntl(sockfd, F_GfETFL);
state &= ~O_NONBLOCK;
fcntl(sockfd, F_SETFL, state);
```



### **3. 总结**

不管是TCP还是UDP，亦或是其他文件描述符，轮询处理都不是一个明智的选择，只有在某些特定的场合下，才会使用非阻塞状态去试探性地获取资源。本章节掌握设置阻塞和非阻塞是重点。



## 多任务并发模型

### **1. 服务器IO模型（二）：多任务并发**

#### **1.1 基本概念**

多任务并发的IO模型，就是利用多进程或者多线程，来达到同时处理多个套接字的目的。一般而言，进程用于具有较完整逻辑块的整合，如果只是处理网络套接字的数据，那么一般使用多线程，以下以线程为例，展示多任务并发的IO模型实现方式。

#### **1.2 设计思路**

对于UDP而言，由于不存在连接的问题，因此服务端一个UDP套接字可以接收任意的客户端发来的数据，可直接将该套接字交由一条专用于收发数据的线程管理即可。

对于TCP而言，稍微复杂一点，首先需要一条专门的线程处理监听套接字，用来随时接受客户端的连接请求。另外由于每当有一个客户端连接成功，服务端都会产生一个新的连接套接字来与之通信，那么就应该每产生一个套接字就分配一条线程与之对应，便可形成所谓的 **多任务并发** 的服务器IO模型。

#### **1.3 实现代码**

核心代码如下：（[mutilThread-TCPserver.zip](http://vm.yueqian.com.cn:8886/group1/M00/15/19/wKgP3GJNYImALJdXAAAWObhP1_E975.zip?token=null&ts=null&filename=mutilThread-TCPserver.zip)）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: server.c
//  描述: 基于TCP协议的服务端，采用多线程IO模型
//
///////////////////////////////////////////////////////

// 客户端处理线程
void *clientRoutine(void *arg)
{
    // 代码略
}

int main(int argc, char **argv)
{
    // 准备相关TCP套接字资源
    // 代码略

    // 初始化用户链表
    struct user *clients = init_list();
    if(clients == NULL)
    {
        perror("初始化用户链表失败");
        exit(0);
    }

    // 主循环：每当来一个远程客户端，就分配一条专门的线程处理之
    while(1)
    {
        // 准备存储对端（客户端）的用户结构体
        struct user *newClient = calloc(1, sizeof(struct user));
        socklen_t len = sizeof(newClient->addr);

        if((newClient->connfd=accept(sockfd, (struct sockaddr *)&newClient->addr, &len)) < 0)
        {
            perror("accept失败");
            free(newClient);
            continue;
        }

        printf("[%s:%hu]连接成功\n", inet_ntoa(newClient->addr.sin_addr), ntohs(newClient->addr.sin_port));
        newClient->ID = randomID();

        // 将新客户端信息加入链表，并启动专用线程处理之
        list_add_tail(&newClient->list, &clients->list);

        pthread_t tid;
        pthread_create(&tid, NULL, clientRoutine, (void *)newClient);
    }

	return 0;
}
```



#### **1.4 总结**

总体而言，多线程处理服务端IO模型是比较简单的，注意几点：

- UDP没有连接，因此多线程模式一般用于TCP服务端
- 每个线程处理一个已连接套接字
- 线程一般要处于分离状态，避免产生僵尸



## 异步信号模型

### **1. 服务器IO模型（三）：异步信号驱动**

所谓信号驱动，即用信号来驱使服务器妥善处理多个远端套接字，信号方式的思路也很简单：每当远端有数据到达，那么就在本端触发信号，然后利用信号的异步特性来处理这些远端信息。

### **2. 适用场景**

首先明确一点，由系统套接字触发的是第29号信号：

```C
SIGIO
```

由于不管套接字收到何种数据，内核一律触发 `SIGIO`，因此这种看似很理想的方式，却不适用于 `TCP` 协议，因此在 `TCP` 中，当客户端发来连接请求、普通数据、数据回执，甚至是断开请求、断开请求的回执等等情况，都触发一样的信号，这就使得服务端光凭这一个信号无法知道下一步要做什么，因此信号驱动的服务器模型，一般**只适用于UDP协议**。

### **3. 代码实现**

要让 `UDP` 服务端工作在信号触发模式下，需要依次做如下步骤：

- 设置信号 `SIGIO` 的响应函数
- 设定信号 `SIGIO` 的属主进程
- 设定套接字工作在信号模式下

具体实现代码如下（假设sockfd是`UDP`套接字）:

```C
// 1. 捕捉信号 SIGIO
signal(SIGIO, f);

// 2. 设置信号的属主：指定信号的接受者的 PID
fcntl(sockfd, F_SETOWN, PID);

// 3. 将套接字设置为异步工作模式：
long state  = fcntl(sockfd, F_GETFL);
state |= O_ASYNC;
fcntl(sockfd, F_SETFL, state);
```

说明：
信号 `SIGIO` 默认会杀死目标进程，因此必须要设定其响应函数；信号`SIGIO`由内核针对套接字产生，而内核套接字可以在多个应用层程序中有效（例如父进程将套接字遗传给各个子进程），因此必须指定该信号的属主；默认情况下，套接字收到数据时不会触发 `SIGIO`，必须将套接字设定为异步工作模式，它才会触发该信号。

以下是关键代码示例：（[signalDriven-UDPserver.zip](http://vm.yueqian.com.cn:8886/group1/M00/15/19/wKgP3GJNbDeAWLGZAAAJCXDknfg337.zip?token=null&ts=null&filename=signalDriven-UDPserver.zip)）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: signalDriven-UDPserver.c
//  描述: 基于信号驱动IO模型的UDP服务端
//
///////////////////////////////////////////////////////

int sockfd;

// 收UDP数据
void f(int sig)
{
    struct sockaddr_in clientAddr;
    char buf[100];

    bzero(buf, 100);

    socklen_t len = sizeof(clientAddr);
    bzero(&clientAddr, len);

        // 等待UDP数据
    int n = recvfrom(sockfd, buf, 100, 0,
                            (struct sockaddr *)&clientAddr, &len);
    printf("[%s:%hu]:%s\n", inet_ntoa(clientAddr.sin_addr),
                            ntohs(clientAddr.sin_port), buf);
}

int main(int argc, char const *argv[])
{
    // 创建UDP套接字
    sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY); // 服务器IP
    addr.sin_port = htons(PORT); // 接收数据端口

    // 绑定上述地址
    bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));

    // 1. 捕捉信号 SIGIO
    signal(SIGIO, f);

    // 2. 设置信号的属主：指定信号的接受者的 PID
    fcntl(sockfd, F_SETOWN, getpid());

    // 3. 将套接字设置为异步工作模式：
    long state  = fcntl(sockfd, F_GETFL);
    state |= O_ASYNC;
    fcntl(sockfd, F_SETFL, state);

    // 主线程继续做其他事情...
    for(int i=0;;i++,i%=26)
    {
        fprintf(stderr, "%c", 'a'+i);
        usleep(200*1000);
    }
}
```



## 多路复用模型

### **1. 服务器IO模型（四）：多路复用**

所谓多路复用，指的是**通过某个特定的接口（比如 `select()`、`poll()` 等），来同时监听多路阻塞IO**，这就达到既无需多进程多线程，又可以同时处理多个阻塞套接字的目的。

### **2. 准备知识**

对于某套接字 `sockfd`，其就绪状态有三种：

- 读就绪
- 写就绪
- 异常就绪

**（一）** 当 `sockfd` 读状态未就绪时，执行以下函数试图读取该套接字数据就会阻塞：

```C
// 1. 读取 sockfd 的TCP数据
read(sockfd, ...);
recv(sockfd, ...); // 读取普通数据

// 2. 等待 sockfd 上的TCP连接请求
accept(sockfd, ...);

// 3. 读取 sockfd 上的UDP数据
recvfrom(sockfd, ...);
```

以上函数处于阻塞状态很容易理解，那代表了对应套接字上的数据尚未到达。

**（二）** 当 `sockfd` 写状态未就绪时，执行以下函数试图往该套接字写入数据就会阻塞：

```C
// 1. 往TCP套接字 sockfd 写入数据
write(sockfd, ...);
send(sockfd, ...);

// 2. 往TCP对端发送连接请求
connect(sockfd, ...);
```

通常，人们不会注意到以上函数默认情况下也是阻塞型函数，在一般的实验环境下，这些函数通常会 “立即” 返回，但这并不代表它们永远都可以 “立即” 返回，例如TCP缓冲区满时，或对端TCP响应连接的回执缓慢时，这些函数都将阻塞。

**（三）** 当 `sockfd` 异常状态未就绪时，执行以下函数试图读取该套接字的OOB数据时就会阻塞：

```C
recv(sockfd, buf, SIZE, MSG_OOB);
```

注意到，所谓异常并不是错误，套接字的异常状态是相当于普通读写就绪状态而言的，经典的场景就是 TCP 中的OOB带外数据：当接收端收到对端的 OOB 数据时，其对应的套接字就会处于异常就绪。

### **3. 多路复用接口**

多路复用，就是通过 `select()` 或 `poll()` 来同时监控多个套接字，当发现一个或多个套接字的某种状态就绪时，再调用相应的函数去处理的过程。

#### **3.1 `select()`**

```C
int select(int nfds,
           fd_set *readfds,
           fd_set *writefds,
           fd_set *exceptfds,
           struct timeval *timeout);
```

- 参数
    - **nfds** - 所有被监控的套接字的最大值+1
    - **readfds** - 读就绪套接字集合
    - **writefds** - 写就绪套接字集合
    - **exceptfds** - 异常就绪套接字集合
    - **timeout** - 超时控制结构体。如果为NULL，代表无限阻塞等待
- 返回值
    - 成功时返回处于某种就绪状态的套接字个数
    - 失败返回-1
- 注意：
    - 三个套接字集合分别关注三个不同的就绪状态，如果需要同时监控某个套接字sockfd的不同就绪状态，则需要将此套接字放入相应的套接字集合中；
    - 当 `select()` 返回时，三个集合中未处于就绪状态的套接字将被自动清零，因此如果要重复监控它们，则需要重新设置这些套接字集合。

下面是如何使用 `select()` 函数的核心代码：（[multiplexing-TCPserver.zip](http://vm.yueqian.com.cn:8886/group1/M00/15/19/wKgP3GJOVCSAeZmwAAAYj9hXGmc853.zip?token=null&ts=null&filename=multiplexing-TCPserver.zip)）

```C
// 假设 sockfd 是一个TCP监听套接字，需要监控它以便能及时处理远端连接请求。
// 假设 connfd 是一个TCP连接套接字，需要监控它以便能及时处理远端发来的普通数据和OOB数据。

// 设置套接字集合，并清零
fd_set rset;
fd_set eset;

FD_ZERO(&rset); // 清零
FD_ZERO(&eset); // 清零

// 将监听套接字放入 rset 中，监控其读就绪状态
FD_SET(sockfd, &rset);

// 将连接套接字放入 rset 中，监控其读就绪状态
FD_SET(connfd, &rset);

// 将连接套接字放入 eset 中，监控其异常就绪状态
FD_SET(connfd, &eset);

// 求得所有多路监控的套接字中的最大值
int maxfd = sockfd>connfd? sockfd : connfd;

// 调用select()，同时多路监控以上三种阻塞状态
select(maxfd+1, &rset, NULL, &eset, NULL);

// 当select()返回后，判定究竟发生了什么情况
// 1. 当sockfd在rset中未被清零时，代表sockfd处于读就绪状态
//    即有远端连接请求到达了，那么此时可以调accept()来处理
if(FD_ISSET(sockfd, &rset))
    accept(sockfd, ...);

// 2. 当connfd在rset中未被清零时，代表connfd处于读就绪状态
//    即有远端的普通数据达到了，那么此时可以调read()来处理
if(FD_ISSET(connfd, &rset))
    read(connfd, ...);

// 3. 当connfd在eset中未被清零时，代表connfd处于异常就绪状态
//    即有远端的OOB数据到达了，那么此时可以调recv()来处理
if(FD_ISSET(connfd, &rset))
    recv(connfd, buf, SIZE, MSG_OOB);
```

#### **3.2 `poll()`**

函数 `poll()` 实现与 `select()` 基于完全一样的功能，只是参数的组织形式不同，下面是该函数的详细接口说明：

```C
int poll(struct pollfd *fds,
         nfds_t nfds,
         int timeout);
```

- 参数
    - **fds** - 套接字监控数组
    - **nfds** - 套接字监控数组的元素个数
    - **timeout** - 超时控制，注意是整型，单位是毫秒。设置为-1代表阻塞
- 返回值
    - 成功时返回处于某种就绪状态的套接字个数
    - 失败返回-1

其中，关键结构体 `struct pollfd{}` 如下：

```C
struct pollfd
{
    int   fd;         /* file descriptor */
    short events;     /* requested events */
    short revents;    /* returned events */
};
```

`fd` 是要监控的套接字文件描述符，events是输入参数，标记了要监控该套接字的何种就绪状态，revents是输出参数，标记了 `poll()` 返回时何种就绪状态有效。

常见就绪状态如下：

- POLLIN: 读就绪
- POLLOUT: 写就绪
- POLLPRI: 异常就绪

这些就绪状态宏可以用位运算来设定和判定，比如：

```C
struct pollfd uni[1];
uni[0].fd = sockfd;
uni[0].events = (POLLIN | POLLPRI); // 同时监控sockfd的读就绪和异常就绪状态
```

下面是如何使用 `poll()` 函数的核心代码：（）

```C
// 假设 sockfd 是一个TCP监听套接字，需要监控它以便能及时处理远端连接请求。
// 假设 connfd 是一个TCP连接套接字，需要监控它以便能及时处理远端发来的普通数据和OOB数据。

struct pollfd fds[2];

fds[0].fd = sockfd;
fds[0].events = POLLIN; // 监控sockfd的读就绪状态

fds[1].fd = connfd;
fds[1].events = POLLIN|POLLPRI; // 监控connfd的读就绪和异常就绪状态

// 开始多路监听
int n = poll(fds, 2, -1);
if(n == -1)
{
    perror("select()失败");
}

// 1. 远端发来连接请求
if(fds[0].revents & POLLIN)
{
    accept(sockfd, ...);
}

// 2. 远端发来普通数据
if(fds[1].revents & POLLIN)
{
    read(connfd, ...);
}

// 3. 远端发来OOB数据
if(fds[1].revents & POLLPRI)
{
    char oob;
    recv(p->connfd, &oob, 1, MSG_OOB);
}
```



### epoll

**ppoll 扩展**

GNU定义了ppoll（非POSIX标准），可以支持设置信号屏蔽字，大家可参考poll模型自行实现C/S。

```C
#define _GNU_SOURCE /* See feature_test_macros(7) */
#include <poll.h>
int ppoll(struct pollfd *fds, nfds_t nfds, const struct timespec *timeout_ts, const sigset_t *sigmask);
```

**3.突破1024文件描述符的限制**

**3.1概念**

Unix和Linux内核（kernel）利用文件描述符（file descriptor）来访问文件。文件描述符是非负整数。打开现存文件或新建文件时，内核会返回一个文件描述符。读写文件也需要使用文件描述符来指定待读写的文件，类似于我们在生成定时器时返回的定时器ID。每打开一个文件就会生成一个对应的文件描述符，相关操作例如打开文件操作、建立socket连接操作、读写文件操作等等都依赖于文件描述符。

每打开一个文件就会占用一定的系统资源，因为我们系统的资源是有限的，所以会对文件描述符的数量有限制，但是系统的限制比较严格，可能把数值限制的比较小。所以在一个进程中，有可能会出现同一时间维护的tcp链接过多，导致linux的文件句柄达到上限，出现Too many open files的问题。所以我们需要调高文件描述符的数量限制，以便于更加充分地利用系统资源，那么我们如何来设定呢？

 

**3.2如何修改文件描述符数量限制**

第一种方法：

1）通过ulimit命令查看系统限制信息

```C
gec@ubuntu:~/桌面$ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 7483
max locked memory       (kbytes, -l) 65536
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 204800
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
 
```

其中：

```
open files                      (-n) 1024
```

可以看到 系统一个进程最多可以打开的文件描述符个数为1024

2）通过ulimit -n来修改数量限制，以10000为例

```
ulimit -n 100000
```

3） 该修改只对当前的终端有效，你可以把这个命令添加到配置脚本中

```
1、打开 ~/.bashrc
2、将上面的命令写到脚本中
3、保存并且退出，重启终端
```

第二种方法：

1）可以使用cat命令查看一个进程可以打开的socket描述符上限。该上限由当前主机性能（硬件环境）决定。

```
gec@ubuntu:~/桌面$ cat /proc/sys/fs/file-max 
9223372036854775807
 
```

2）修改limits.conf配置文件

```
sudo vim /etc/security/limits.conf
```

打开后，在文件最后添加：

```
* soft nofile 204800    
* hard nofile 204800
* soft nproc  204800
* hard nproc  204800
```

![img](./img/15372.png)

保存退出。

3)修改user.conf 和 system.conf文件

然后，在下面的两文件中加入：DefaultLimitNOFILE=204800

```
sudo vim /etc/systemd/user.conf
sudo vim /etc/systemd/system.conf
```

![img](./img/15373.png)

![img](./img/15374.png)

 

保存退出即可。

4）重启Ubuntu系统。

 

**4.多路复用epoll** 

**4.1概念**

epoll是Linux下多路复用IO接口select/poll的增强版本，它能显著提高程序在大量并发连接中只有少量活跃的情况下的系统CPU利用率，因为它会复用文件描述符集合来传递结果而不用迫使开发者每次等待事件之前都必须重新准备要被侦听的文件描述符集合，另一点原因就是获取事件的时候，它无须遍历整个被侦听的描述符集，只要遍历那些被内核IO事件异步唤醒而加入Ready队列的描述符集合就行了。

目前epoll是linux大规模并发网络程序中的热门首选模型。epoll除了提供select/poll那种IO事件的电平触发（Level Triggered）外，还提供了边沿触发（Edge Triggered），这就使得用户空间程序有可能缓存IO状态，减少epoll_wait/epoll_pwait的调用，提高应用程序效率。

**4.2epoll函数介绍**

**1）epoll_create**

```
#include <sys/epoll.h> 
int epoll_create(int size);		
```

函数作用：

创建一个epoll句柄，参数size用来告诉内核监听的文件描述符的个数，跟内存大小有关。

函数参数：

size：创建的红黑树的监听节点数量。（仅供内核参考）

返回值：

指向新创建的红黑树的根节点的fd.

失败 返回  -1  errno被设置

**2）epoll_ctl**

```
#include <sys/epoll.h> 
int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event); 
```

函数作用：

控制某个epoll监控的文件描述符上的事件：注册、修改、删除

函数参数：

​	epfd：	为epoll_create的句柄，也就是红黑树的根节点

​	op：	表示动作，用3个宏来表示：

​			EPOLL_CTL_ADD，添加fd到监听红黑树

​			EPOLL_CTL_MOD  修改fd在监听红黑树上的监听事件

​			EPOLL_CTL_DEL   从监听红黑树上删除结点，也就是取消该文件描述符的监听

 fd	:       待监听的文件描述符

​        event：	告诉内核需要监听的事件 ，传入struct epoll_event结构体 的地址

```
struct epoll_event { 
    __uint32_t events; /* Epoll events */ 
    epoll_data_t data; /* User data variable */ 
}; 
typedef union epoll_data { 
    void *ptr; 
    int fd;   //对应监听事件的fd 
    uint32_t u32; 
    uint64_t u64; 
} epoll_data_t;
 
Epoll events 有以下：
 
EPOLLIN ：	表示对应的文件描述符可以读（包括对端SOCKET正常关闭）
EPOLLOUT：	表示对应的文件描述符可以写
EPOLLPRI：	表示对应的文件描述符有紧急的数据可读（这里应该表示有带外数据到来）
EPOLLERR：	表示对应的文件描述符发生错误
EPOLLHUP：	表示对应的文件描述符被挂断；
EPOLLET： 	将EPOLL设为边缘触发(Edge Triggered)模式，这是相对于水平触发(Level Triggered)而言的
EPOLLONESHOT：只监听一次事件，当监听完这次事件之后，如果还需要继续监听这个socket的话，需要再次把这个socket加入到EPOLL队列里
```

**3）epoll_wait**

```
#include <sys/epoll.h> 
int epoll_wait(int epfd, struct epoll_event *events,int maxevents, int timeout); 
```

函数作用：

等待所监控的文件描述符上有事件的产生，类似于select()调用。	

函数参数：

epfd：		为epoll_creat的句柄

​	events：		用来存内核得到事件的集合 ，实际上就是结构体数组的地址

​	maxevents：	告之内核这个events有多大，这个maxevents的值不能大于创建epoll_create()时的size

​	timeout：	是超时时间

​				-1：		阻塞

​				0：		立即返回，非阻塞

​				>0：	指定毫秒

返回值：

​	成功返回有多少文件描述符就绪

时间到时返回0

出错返回-1

 

**4.3epoll多路复用服务器 实例**

```
#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <netinet/in.h> 
#include <arpa/inet.h> 
#include <sys/epoll.h> 
#include <errno.h> 
 
 
#define MAXLINE 80 
#define SERV_PORT 6666 
#define OPEN_MAX 1024
 
 
int main(int argc, char *argv[]) 
{ 
    	int i, j, maxi, listenfd, connfd, sockfd; 
    	int nready, efd, res; 
 ssize_t n; 
        char buf[MAXLINE], str[INET_ADDRSTRLEN]; 
 socklen_t clilen; 
    	int client[OPEN_MAX]; 
    	struct sockaddr_in cliaddr, servaddr; 
    	struct epoll_event tep, ep[OPEN_MAX]; 
 
	listenfd = socket(AF_INET, SOCK_STREAM, 0); 
 
        bzero(&servaddr, sizeof(servaddr)); 
	servaddr.sin_family = AF_INET; 
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
	servaddr.sin_port = htons(SERV_PORT); 
 
        bind(listenfd, (struct sockaddr *) &servaddr, sizeof(servaddr)); 
 
        listen(listenfd, 20); 
 
 
         for (i = 0; i < OPEN_MAX; i++) 
		client[i] = -1; 
	maxi = -1; 
 
    	//创建一颗监听红黑树
        efd = epoll_create(OPEN_MAX); 
        if (efd == -1) 
		perr_exit("epoll_create"); 
 
	tep.events = EPOLLIN; 
        tep.data.fd = listenfd;
        //将连接套接字 添加到 红黑树中 
 
	res = epoll_ctl(efd, EPOLL_CTL_ADD, listenfd, &tep); 
    	if (res == -1) 
		perr_exit("epoll_ctl"); 
 
         while (1) {
                 //阻塞监听 红黑树上的文件描述符 的状态 
		nready = epoll_wait(efd, ep, OPEN_MAX, -1); /* 阻塞监听 */ 
		if (nready == -1) 
			perr_exit("epoll_wait"); 
 
		for (i = 0; i < nready; i++) { 
			if (!(ep[i].events & EPOLLIN)) 
				continue;
                        //连接套接字 的状态发生变化，说明有新客户端连接 
			if (ep[i].data.fd == listenfd) { 
				clilen = sizeof(cliaddr); 
				connfd = accept(listenfd, (struct sockaddr *)&cliaddr, &clilen); 
				printf("received from %s at PORT %d\n", 
						inet_ntop(AF_INET, &cliaddr.sin_addr, str, sizeof(str)), 
						ntohs(cliaddr.sin_port)); 
				for (j = 0; j < OPEN_MAX; j++) { 
					if (client[j] < 0) { 
						client[j] = connfd; /* save descriptor */ 
						break; 
					} 
				} 
 
				if (j == OPEN_MAX) 
					perr_exit("too many clients"); 
				if (j > maxi) 
					maxi = j; 		/* max index in client[] array */ 
 
				tep.events = EPOLLIN; 
				tep.data.fd = connfd;
                                //将连接上来的新客户端文件描述符 加入到监听红黑树中 
				res = epoll_ctl(efd, EPOLL_CTL_ADD, connfd, &tep); 
				if (res == -1) 
					perr_exit("epoll_ctl"); 
			} else {
                               //红黑树中 有客户端发来数据 
				sockfd = ep[i].data.fd; 
				n = read(sockfd, buf, MAXLINE);
                                //客户端断开连接 
				if (n == 0) { 
					for (j = 0; j <= maxi; j++) { 
						if (client[j] == sockfd) { 
							client[j] = -1; 
							break; 
						} 
					} 
					res = epoll_ctl(efd, EPOLL_CTL_DEL, sockfd, NULL); 
					if (res == -1) 
						perr_exit("epoll_ctl"); 
 
					close(sockfd); 
					printf("client[%d] closed connection\n", j); 
				} else { 
					for (j = 0; j < n; j++) 
						buf[j] = toupper(buf[j]); 
					Writen(sockfd, buf, n); 
				} 
			} 
		} 
        }
        
        close(listenfd); 
        close(efd); 
        return 0; 
}
```

 

**5.epoll和select/poll的底层机制区别**

```
1.select,poll和epoll都需要不停地监控所有要监控地描述符,知道有描述符就绪为止,期间会有睡眠和唤醒地多次交替，但是epoll
在描述符就绪时,调用回调函数,把就绪地描述符放入就绪红黑树中,并唤醒epoll_wait的进程。虽然都有睡眠和唤醒的交替,但是select和poll
在唤醒后要去遍历所有监控的描述符,找出其中就绪的部分。而epoll唤醒后只需要读取就绪红黑树即可,节省了大量的操作。
2.select和poll在每次调用时都要把所有监控的描述符从用户态拷贝到内核态,而epoll只要拷贝一次(epoll_ctl)即可,这样也节省了不少开销
```

 

**6.网络超时处理**

​	IO多路复用自带超时功能，在普通的网络通信中如何实现超时。

socket属性中带有超时的设置影响(read recv recvfrom accept)

```
struct timeval tv;
tv.tv_sec = xxx;
tv.tv_usec = yyy;
setsockopt(sockfd,SOL_SOCKET,SO_RCVTIMEO,&tv,sizeof(tv));
```



## QA

【1】问：究竟什么时候该用哪种IO模型？
【1】答：每种IO模型都有其特点，根据其特点来选择。

- 阻塞与轮询：一般不推荐使用。
- 多任务并发：最常见的模型，常用于TCP服务端。
- 信号驱动：对UDP套接字很有用，简单易用。
- 多路复用：对于既不想要创建多线程多进程，又要同时处理多个套接字的场合很有用，在硬件资源特别紧张的场合下特别有用。

