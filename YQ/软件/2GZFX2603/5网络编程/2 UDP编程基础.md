#  UDP编程基础

[toc]

## UDP入门与应用

### **1. UDP简介**

UDP全称 User Datagram Protocol，即：用户数据报协议。是面向无连接的协议。通常，UDP 通信还会被冠以**不可靠**的头衔。这里的不可靠指的是：无法可靠地得知对方是否收到数据。

UDP有如下特征：

- 无连接：通信双方不需要事先连接
- 无确认：收到数据不给对方发回执确认
- 不保证有序、丢失不重发
- 采用帧同步的数据报通信方式（即通信双方每次的收发数据量相等）

![img](./img/wKgP3GId9rWAD7h0AARYhPCY9Gw248.png)
<center>
    寄信
</center>

简单来讲，UDP 类似于寄信，如果两个人除了信件之外没有任何别的通信方式，那么信件寄出去了之后，寄件人是无法得知收件人是否收到信件或者是否已经读取内容的。UDP 的特点是无需连接、无需确认、无需缓冲区和分包序列号，因此 UDP 的效率是比较高的。

- UDP适用情况
    - 发送小尺寸数据（如对DNS服务器进行IP地址查询时）
    - 在接收到数据，给出应答较困难的网络中使用UDP。（如：无线网络）
- 广播、组播模式
    - 即时通讯软件的点对点文本通讯以及音视频通讯
    - 流媒体、VOD、VoIP、IPTV等网络多媒体服务中的实时数据传输

### **2. UDP通信流程**

- 发送方：
    1. 创建 UDP 套接字： `int fd = socket();`
    2. 准备好接收方的地址：`struct sockaddr_in peerAddr;`
    3. 给对方发送 UDP 数据报：`sendto(fd, peerAddr);`
- 接收方：
    1. 创建 UDP 套接字：`int fd = socket();`
    2. 准备好自己的地址：`struct sockaddr_in addr;`
    3. 绑定套接字和地址：`bind(fd, addr);`
    4. 坐等各方发来的 UDP 数据报：`recvfrom(fd);`

### **3. 核心API解析**

#### **3.1 创建套接字**

这是最重要的核心API，通过 `socket()` 可以创建基于各种协议的套接字（也称套接口），后续所有的网络操作都是从套接字开始的。

```C
int socket(int domain, int type, int protocol);
```

- 参数
    - **domain** - 域，比如因特网AF_INET、UNIX本地域AF_LOCAL等
    - **type** - 套接字类型，比如字节流SOCKET_STREAM、数据报SOCKET_DGRAM等
    - **protocol** - 传输层协议，比如UDP协议IPPROTO_UDP、TCP协议IPPROTO_TCP等
- 返回值
    - 成功返回大于零的套接字文件描述符
    - 失败返回-1

#### **3.2 绑定地址**

对于服务端来说，由于其IP和端口必须固定（否则客户端无法找到），因此服务端一般都需要将套接字绑定到某个IP和端口上，IP和端口一般统称网络地址或地址。当然，有些特定的场合客户端的套接字也可以绑定地址。

```C
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```

- 参数
    - **sockfd** - 套接字文件描述符
    - **addr** - IP地址与端口号，注意需转换成标准地址结构体
    - **addrlen** - 地址长度
- 返回值
    - 成功返回0
    - 失败返回-1

#### **3.3 发送UDP数据**

对于UDP而言，由于没有连接，因此每次发送数据都必须携带对端的地址，就像写信，不管信封里面的内容长短，也不管是第几次寄信，每次寄信都必须写清楚对方的地址方可寄出。

```C
ssize_t sendto(int sockfd, const void *buf,size_t len, int flags, const struct sockaddr *dest_addr, socklen_t addrlen);
```

- 参数
    - **sockfd** - 套接字文件描述符
    - **buf** - 指向要发送的数据的首地址
    - **len** - 要发送的数据的长度（单位：字节）
    - **flags** - 发送标记，比如带外数据MSG_OOB等，一般设置为0
    - **dest_addr** - 目标地址，包括IP地址和端口号
    - **addrlen** - 目标地址长度
- 返回值
    - 成功返回已发送的数据（单位：字节）
    - 失败返回-1

#### **3.4 接收UDP数据**

对于UDP而言，由于对端发来的数据都是携带地址的，因此可以在以下函数中获取对端的地址信息，当然如果不需要对端的地址信息，可以将下面函数的最后两个参数写为 `NULL` 即可。

```C
ssize_t recvfrom(int sockfd,
                 void *buf,
                 size_t len,
                 int flags,
                 struct sockaddr *src_addr,
                 socklen_t *addrlen);
```

- 参数
    - **sockfd** - 套接字文件描述符
    - **buf** - 接收数据缓冲区
    - **len** - 接收数据缓冲区大小（单位：字节）
    - **flags** - 接收标记，比如带外数据MSG_OOB等，一般设置为0
    - **src_addr** - 源端地址，包括IP地址和端口号，不保存源端地址时可设置为NULL
    - **addrlen** - 源端地址长度，不保存源端地址时可设置为NULL
- 返回值
    - 成功返回已接收的数据（单位：字节）
    - 失败返回-1

### **4. UDP收发数据代码实现**

使用上述API，可以自己实现UDP协议的收发程序，核心代码如下：

#### **4.1 发送UDP数据**

```C
// 创建UDP套接字
int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

// 准备对方的IP地址和端口号
struct sockaddr_in addr;
bzero(&addr, sizeof(addr));
addr.sin_family = AF_INET;
addr.sin_addr.s_addr = inet_addr("192.168.1.123");
addr.sin_port = htons(50001);

// 向对方发送UDP数据
sendto(sockfd, "abc", 3, 0, (struct sockaddr *)&addr, len);
```

#### **3.2 接收UDP数据**

```C
// 创建UDP套接字
int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

// 准备接收UDP数据的地址
struct sockaddr_in addr;
bzero(&addr, sizeof(addr));
addr.sin_family = AF_INET;
addr.sin_addr.s_addr = htonl(INADDR_ANY);
addr.sin_port = htons(50001);

// 绑定地址
bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));

// 等待接收UDP数据
char buf[100] = {0};
recvfrom(sockfd, buf, 100, 0, NULL, NULL);
```

## 套接字属性

### **1. 基本概念**

套接字可以设定很多属性，比如数据缓冲区长度、广播、心跳测试、超时控制等等，下表展示了比较常见的套接字的属性：

**常用套接字属性列表**

|  属性层次  | 属性名称     | 数据格式       | 说明                               |
| :--------: | ------------ | -------------- | ---------------------------------- |
|  SOL_SOCK  | SO_DEBUG     | bool           | 使能网络调试信息                   |
|  SOL_SOCK  | SO_REUSEADDR | bool           | 允许关闭后可立即重用本地地址和端口 |
|  SOL_SOCK  | SO_BROADCAST | bool           | 广播                               |
|  SOL_SOCK  | SO_ERROR     | int            | 套接字错误信息                     |
|  SOL_SOCK  | SO_LINGER    | struct linger  | 延迟关闭连接                       |
|  SOL_SOCK  | SO_RCVBUF    | int            | 接收缓冲区大小                     |
|  SOL_SOCK  | SO_SNDBUF    | int            | 发送缓冲区大小                     |
|  SOL_SOCK  | SO_RCVLOWAT  | int            | 接收缓冲区下限                     |
|  SOL_SOCK  | SO_SNDLOWAT  | int            | 发送缓冲区下限                     |
|  SOL_SOCK  | SO_RCVTIMEO  | struct timeval | 数据接收超时                       |
|  SOL_SOCK  | SO_SNDTIMEO  | struct timeval | 数据发送超时                       |
| IPPROTO_IP | IP_OPTINOS   | int            | IP首部选项信息                     |
| IPPROTO_IP | IP_TOS       | int            | 服务质量                           |
| IPPROTO_IP | IP_TTL       | int            | 生存时间                           |

说明：

- 由于套接字的属性繁多，因此为了更加清晰，系统将这些不同的属性放置到各个 `Socket Option Level` 中，即属性层次SOL。
- 不同的属性的数据格式是不同的：
    - bool格式表示开关型属性，比如是否地址复用、是否使能广播等。
    - int格式表示数值型属性，比如缓冲区大小。
    - 还有一些属性拥有特定的数据格式，比如超时控制格式是 `struct timeval`

### **2. 相关API**

这些属性通过如下两个函数来获取和设定：

#### **2.1 获取套接字属性**

```
int getsockopt(int sockfd, int level, int optname,
               void *optval, socklen_t *optlen);
```

- 参数
    - **sockfd** - 套接字文件描述符
    - **level** - 属性所在层次，比如SOL_SOCKET
    - **optname** - 属性名，比如SOL_BROADCAST
    - **optval** - 属性值，不同属性的值的类型是不同的，比如有int、bool还有不同的结构体
    - **optlen** - 属性值的长度
- 返回值
    - 成功返回 0
    - 失败返回-1

#### **2.2 设定套接字属性**

```
int setsockopt(int sockfd, int level, int optname,
               const void *optval, socklen_t optlen);
```

- 参数
    - **sockfd** - 套接字文件描述符
    - **level** - 属性所在层次，比如SOL_SOCKET
    - **optname** - 属性名，比如SOL_BROADCAST
    - **optval** - 获取的属性值的存储区
    - **optlen** - 属性值存储区的长度
- 返回值
    - 成功返回0
    - 失败返回-1

### **3. 用法举例**

#### **3.1 举例：设定UDP广播属性**

**示例代码1：**（下载完整代码：[socketOpt-UDPbroadcast.c](http://vm.yueqian.com.cn:8886/group1/M00/12/7E/wKgP3GIXMrSAUwFjAAAEYrA2zww66299.c?token=null&ts=null&filename=socketOpt-UDPbroadcast.c)）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: socketOpt-UDPbroadcast.c
//  描述: 获取和设定UDP的广播属性
//
///////////////////////////////////////////////////////

// UDP套接字
int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

// 获取套接字的广播属性
int val;
int len = sizeof(val);
getsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &val, &len);

// 设定套接字的广播属性为真
int on = 1;
setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &on, sizeof(on));

// 再次获取套接字的广播属性
getsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &val, &len);
```

说明：在UDP广播、组播的情形中，都需要使能广播属性。

#### **3.2 举例：设定TCP数据缓冲区**

**示例代码2：**（下载完整代码：[socketOpt-TCPbuffer.c](http://vm.yueqian.com.cn:8886/group1/M00/12/7E/wKgP3GIXMrSAVsd5AAAFtjEid1U53285.c?token=null&ts=null&filename=socketOpt-TCPbuffer.c)）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: socketOpt-TCPbuffer.c
//  描述: 获取和设定TCP的数据缓冲区的大小
//
///////////////////////////////////////////////////////

// 创建TCP套接字
int sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

// 获取TCP默认的数据收发缓冲区大小
int sndbuf, rcvbuf;
int len1 = sizeof(sndbuf);
int len2 = sizeof(rcvbuf);
getsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &sndbuf, &len1);
getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &rcvbuf, &len2);

// 设定套接字的缓冲区
sndbuf = 1024;
rcvbuf = 2048;
setsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &sndbuf, sizeof(len1));
setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &rcvbuf, sizeof(len2));
```

说明：TCP协议具有数据丢失自动重发、数据水位线等特性，这些特性要求TCP的通信双方的套接字必然有数据缓冲区。在不同的系统中，这些读写缓冲区的大小可能不同。

#### **3.3 举例：设定套接字超时属性**

**示例代码3：**（下载完整代码：[socketOpt-timeout.c](http://vm.yueqian.com.cn:8886/group1/M00/12/7E/wKgP3GIXPWCAe8yhAAAF8JB0zR002203.c?token=null&ts=null&filename=socketOpt-timeout.c)）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: socketOpt-timeout.c
//  描述: 设置UDP套接字的读操作超时时长
//
///////////////////////////////////////////////////////

// 设定接收UDP数据3秒超时
struct timeval val = {.tv_sec  = 3,
                      .tv_usec = 0
                     };
setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &val, sizeof(val));

// 等待UDP数据，3秒钟后以下语句将超时出错返回
recvfrom(sockfd, buf, 10, 0, NULL, NULL);
```

说明：上述代码中的 `sockfd` 是一个绑定了地址的UDP服务端套接字，由于设定了 `SO_RCVTIMEO` 属性，在调用 `recvfrom()` 的瞬间开始倒计时，3秒内若还没收到数据则出错返回不再等待。

## 网络接口信息获取

### **1. 基本概念**

编程中经常需要程序自动获得某个指定网卡的地址信息，比如给定某网卡名称为 `ens33`、`eth0`，然后要根据这些网卡名称好获取其IP地址等信息，掌握下面的相关结构体和操作API，可以很方便得到上述目的。

#### **1.1 网络接口卡信息结构体**

```C
// 本机所有活跃网卡列表信息
struct ifconf
{
      int     ifc_len;     /* size of buffer */
      union {
        caddr_t ifcu_buf;
        struct  ifreq *ifcu_req;
      } ifc_ifcu;
};
```



```C
// 某一个网卡信息
struct ifreq
{
    union {
        char ifrn_name[IFNAMSIZ];    /* 某个网口的名称，比如 "ens33" */
    } ifr_ifrn;

    union {
        struct sockaddr ifru_addr;     // IP地址
        struct sockaddr ifru_dstaddr;  // 目标IP地址
        struct sockaddr ifru_broadaddr;// 广播地址
        struct sockaddr ifru_netmask;  // 子网掩码
        struct sockaddr ifru_hwaddr;   // 硬件MAC地址
        short int ifru_flags;
        int ifru_ivalue;
        int ifru_mtu;
        struct ifmap ifru_map;
        char ifru_slave[IFNAMSIZ];    /* Just fits the size */
        char ifru_newname[IFNAMSIZ];
        __caddr_t ifru_data;
    }ifr_ifru;
};
```

注意到，某网卡的相关信息被放在一个联合体中，换句话说不能一次性获取这些信息，而是要用如下宏来分别获取这些信息：

| 序号 | 宏             | ioctl参数     | 描述                          |
| :--: | -------------- | ------------- | ----------------------------- |
|  1   | SIOCGIFCONF    | struct ifconf | 获取所有活跃网卡的信息        |
|  2   | SIOCGIFADDR    | struct ifreq  | 获取指定网卡的IP地址信息      |
|  3   | SIOCGIFBRDADDR | struct ifreq  | 获取指定网卡的广播地址信息    |
|  4   | SIOCGIFHWADDR  | struct ifreq  | 获取指定网卡的硬件MAC地址信息 |

**获取网络接口卡相关信息**

```C
// 指定网口名称 ens33
struct ifreq ifr;
strcpy(ifr.ifr_ifrn.ifrn_name, "ens33");

// 1，获取指定网口IP地址
int ioctl(int fd, SIOCGIFADDR, &ifr);

// 2，获取指定网口广播地址
int ioctl(int fd, SIOCGIFBRDADDR, &ifr);

// 3，获取指定网口子网掩码
int ioctl(int fd, SIOCGIFNETMASK, &ifr);
```

**说明**
`ioctl()` 的功能由第二个参数 request 来指定：

- SIOCGIFADDR : 获取IP地址
- SIOCGIFBRDADDR : 获取广播地址
- SIOCGIFNETMASK: 获取子网掩码

更多的控制命令字可以到系统头文件 `ioctls.h` 中查阅.

**示例代码**（ [getIfaceInfo-ifreq.c](http://vm.yueqian.com.cn:8886/group1/M00/12/7E/wKgP3GIXMrSAA6YZAAAFLH7ol5k03322.c?token=null&ts=null&filename=getIfaceInfo-ifreq.c) ）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: getIfaceInfo-ifreq.c
//  描述: 获取指定网络接口的地址信息
//
///////////////////////////////////////////////////////

int main(int argc, char *argv[])
{
    // 获取指定网卡的各种基本信息
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    struct ifreq ifr;
    strcpy(ifr.ifr_ifrn.ifrn_name, "ens33");
    
    ioctl(sockfd, SIOCGIFADDR, &ifr);
    printf("IP: %s\n", inet_ntoa(((struct sockaddr_in *)&(ifr.ifr_ifru.ifru_addr))->sin_addr));

    ioctl(sockfd, SIOCGIFBRDADDR, &ifr);
    printf("广播地址: %s\n", inet_ntoa(((struct sockaddr_in *)&(ifr.ifr_ifru.ifru_broadaddr))->sin_addr));

    ioctl(sockfd, SIOCGIFNETMASK, &ifr);
    printf("子网掩码: %s\n", inet_ntoa(((struct sockaddr_in *)&(ifr.ifr_ifru.ifru_netmask))->sin_addr));

    return 0;
}
```

### **2. 网络信息检索**

在网络编程中，如下API都是比较常见且有用的：

| 序号 | API                  | 描述                         |
| :--: | -------------------- | ---------------------------- |
|  1   | gethostname( )       | 获取主机名                   |
|  2   | **getsockname( )**   | **获得本端套接字的地址信息** |
|  3   | **getpeername( )**   | **获得对端套接字的地址信息** |
|  4   | **gethostbyname( )** | **根据主机名取得主机信息**   |
|  5   | gethostbyaddr( )     | 根据主机地址取得主机信息     |
|  6   | getprotobyname( )    | 根据协议名取得主机协议信息   |
|  7   | getprotobynumber( )  | 根据协议号取得主机协议信息   |
|  8   | getservbyname( )     | 根据服务名取得相关服务信息   |
|  9   | getservbyport( )     | 根据端口号取得相关服务信息   |

上表中几个粗体显示的，是其中比较重要的几个API，他们更详细的说明如下：

#### **2.1 获取本端套接字的地址信息**

```C
#include <sys/socket.h>
int getsockname(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

- 参数
    - **sockfd** - 套接字文件描述符
    - **addr** - 存储套接字所绑定的地址信息
    - **addrlen** - 地址结构体长度
- 返回值
    - 成功返回 0
    - 失败返回-1

**说明**
如果套接字未绑定任何地址信息，那么调用以上函数将不会得到任何有效数据。

**示例代码1**（ [getsockname-localUDP.c](http://vm.yueqian.com.cn:8886/group1/M00/12/7E/wKgP3GIXMrSAGbqZAAAGV6i4xKA49649.c?token=null&ts=null&filename=getsockname-localUDP.c) ）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: getsockname-localUDP.c
//  描述: 获取本端UDP套接字的地址信息
//
///////////////////////////////////////////////////////

int main(int argc, char const *argv[])
{
    // 创建UDP套接字
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    struct sockaddr_in a = {0};
    socklen_t len = sizeof(a);

    // 获取本端套接字的地址信息
    // 此时获取到的信息将为空
    getsockname(sockfd, (struct sockaddr *)&a, &len);
    printf("本端UDP套接字绑定的IP: %s\n", inet_ntoa(a.sin_addr));
    printf("本端UDP套接字绑定的PORT: %hu\n", ntohs(a.sin_port));


    // 绑定IP和端口
    struct sockaddr_in addr;
    bzero(&addr, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = inet_addr("192.168.9.89");
    addr.sin_port = htons(50021);
    if(bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) == 0)
        printf("地址绑定成功\n");
    else
    {
        perror("地址绑定失败");
        exit(0);
    }

    // 重新获取与套接字绑定IP和端口信息
    getsockname(sockfd, (struct sockaddr *)&a, &len);
    printf("本端UDP套接字绑定的IP: %s\n", inet_ntoa(a.sin_addr));
    printf("本端UDP套接字绑定的PORT: %hu\n", ntohs(a.sin_port));

    return 0;
}
```

可见，未绑定地址的套接字本身是不包含地址信息的，但是 **绑定地址** 的动作不一定对应 `bind()` 函数，比如TCP客户端 `connect()` 成功后，套接字就不涉及所谓 **绑定** 的动作，但其返回的时候已经与对端达成连接状态，其地址信息是确定的。

**示例代码2**（ [getsockname-localTCP.c](http://vm.yueqian.com.cn:8886/group1/M00/14/05/wKgP3GIzAseAGD-cAAAGsckAjrY21592.c?token=null&ts=null&filename=getsockname-localTCP.c) ）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: getsockname-localTCP.c
//  描述: 获取本端TCP套接字的地址信息
//
///////////////////////////////////////////////////////

#define PORT 50021

int main(int argc, char **argv)
{
	// 创建TCP套接字
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);

	// 准备服务端地址结构体
	struct sockaddr_in addr;
	bzero(&addr, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = inet_addr("192.168.1.100"); // 服务端IP
	addr.sin_port = htons(PORT); // 服务器端口号


    // 本地套接字未绑定任何地址


    // 连接服务端
    connect(sockfd, (struct sockaddr *)&addr, sizeof(addr));

    // 如果连接成功，那么系统会为本客户端随机分配IP和端口号
    // 利用 getsockname() 来获取这些随机分配的信息
    struct sockaddr_in a = {0};
    socklen_t len = sizeof(a);
    getsockname(sockfd, (struct sockaddr *)&a, &len);
    printf("本端TCP套接字绑定的IP: %s\n", inet_ntoa(a.sin_addr));
    printf("本端TCP套接字绑定的PORT: %hu\n", ntohs(a.sin_port));

	return 0;
}
```

#### **2.2 获取对端套接字的地址信息**

```C
int getpeername(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```

- 参数
    - **sockfd** - 套接字文件描述符
    - **addr** - 对端网络IP地址和端口信息结构体
    - **addrlen** - 对端网络信息长度
- 返回值
    - 成功返回0
    - 失败返回-1

**说明**
既然是 **对端** 的信息，那就必须是已经 **连接** 了的套接字才有，一般而言只有基于TCP协议的通信两端才需要去获取 **对端** 的地址信息，基于UDP协议的通信则一般无此特性。

**示例代码**（ [getpeername-peerTCP.c](http://vm.yueqian.com.cn:8886/group1/M00/14/0B/wKgP3GIzCA6AENEfAAAGkufkAf423175.c?token=null&ts=null&filename=getpeername-peerTCP.c) ）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: getpeername-peerTCP.c
//  描述: 本端是TCP服务器，通过 getpeername() 获取对端
//        TCP客户端套接字的地址信息
//
///////////////////////////////////////////////////////

int main(int argc, char **argv)
{
	// 创建TCP套接字
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);

	// 准备本机（服务端）地址结构体
	struct sockaddr_in addr;
	bzero(&addr, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(INADDR_ANY); // 自动获取本机（服务端）IP
	addr.sin_port = htons(50021); // 端口号PORT

	bind(sockfd, (struct sockaddr *)&addr, sizeof(addr));
	listen(sockfd, 3);

    // 等待客户端连接...
	int connfd = accept(sockfd, NULL, NULL);

	// 获取对端套接字的地址信息
    struct sockaddr_in a = {0};
    socklen_t len = sizeof(a);
    getpeername(connfd, (struct sockaddr *)&a, &len);
    printf("对端TCP套接字的IP: %s\n", inet_ntoa(a.sin_addr));
    printf("对端TCP套接字的端口: %hu\n", ntohs(a.sin_port));

	close(connfd);
	close(sockfd);

	return 0;
}
```

### **3. 获取主机名（域名）的地址信息**

```C
#include <netdb.h>
extern int h_errno;

struct hostent *gethostbyname(const char *name);
```

- 参数
    - **name** - 指定主机名或域名
- 返回值
    - 成功返回结构体指针
    - 失败返回NULL

```C
// 结构体struct hostent信息
struct hostent
{
    char  *h_name;            /* official name of host */
    char **h_aliases;         /* alias list */
    int    h_addrtype;        /* host address type */
    int    h_length;          /* length of address */
    char **h_addr_list;       /* list of addresses */
};
```

**示例代码**（[gethostbyname.c](http://vm.yueqian.com.cn:8886/group1/M00/14/0D/wKgP3GIzCSqAfAQMAAADDc9cArA30135.c?token=null&ts=null&filename=gethostbyname.c)）

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: gethostbyname.c
//  描述: 获取指定域名的IP地址
//
///////////////////////////////////////////////////////


int main(int argc, char **argv)
{
    struct hostent *p;
    p = gethostbyname(argv[1]);

    // 列出指定域名的IP地址（列表）
    for(int i=0; p->h_addr_list[i] != NULL; i++)
        printf("%s\n", inet_ntoa(*(struct in_addr*)((p->h_addr_list)[i])));
}
```
