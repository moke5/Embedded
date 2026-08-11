# TCP编程基础

[toc]

## TCP编程基础

### **1. TCP概览**

TCP全称 Transmition Control Protocol，即：传输控制协议。是面向连接的协议。通常，TCP 通信还会被冠以 **可靠传输协议** 的头衔。但请注意，这里的**可靠**并非指发出去的数据对方一定能收到（这是不可能的），而仅指TCP能使发送方可靠地知道对方是否收到了数据。

#### **1.1 TCP基本特征**

- 有连接：通信双方需要事先连接成功，方可传输数据
- 有确认：一方收到对端的任何数据，都会给另一方发回执确认
- 保证数据有序、不重复、丢失会重发
- 如果网络拥堵，会自动调节发送量
- 采用帧异步的流式通信方式（即通信双方每次的收发数据量不必相等）

简单来讲，TCP 类似于打电话，说话前需要花一定的时间接通电话，等到对方接听了之后双方才能开始通信，通信的过程中每个数据的传送，接收方都会给发送方回执确认，断开的时候也会互相通知以便于释放各自相关的资源。可以看出来，TCP 相对于 UDP 而言资源开销更大，提供更丰富的功能，TCP适合用在如下情形：

- 传输质量要求较高，不能丢失数据
- 大数据量的通信，以至于通信前后的连接和断开的开销可以忽略不计
- 用户登录、账户管理等相关的功能

#### **1.2 TCP通信流程基本原理**

TCP的通信流程跟打电话是几乎一样的，因此可以将通信的过程细分为主动发起连接者（客户端）和被动接受连接者（服务端）两方来分别讨论。

**被动的服务端**

1. 建立TCP套接字sockfd，即通信端点
2. 绑定套接字sockfd与网络地址，即IP+端口
3. 设定套接字sockfd进入被动监听状态，即将套接字设定为监听套接字
4. 静静等待远程客户端的连接请求
5. 收到连接请求后，得到一个专用于收发数据的连接套接字connfd
6. 使用连接套接字connfd与客户端通信

**主动的客户端**

1. 建立TCP套接字sockfd，即通信端点
2. 对服务端发起连接请求
3. 若连接成功，则直接通过套接字sockfd与服务端通信

上述两者的互动，可以用一下手绘草图来简单表达：

![img](./img/wKgP3GIwW-KAUpL1AAIAQuBVOAo783.png)
TCP通信流程

**注意点：**

- 在服务端中，监听套接字和连接套接字是严格区分的，不可混用
- 服务端所绑定的地址（IP+PORT）需要对外公开，否则客户端无法发起连接
- 客户端在发起连接前一般无需绑定地址，此时系统会为此连接自动分配恰当的地址资源

### **2. TCP通信代码实现**

#### **2.1 基本C/S代码（Client客户端、Server服务端）**

要演示TCP的通信过程，只需要写一个服务端和客户端即可，服务端负责建立被动监听套接字，客户端负责主动发起连接。下面通过一个简单的**消息反弹**服务器（即将客户端发来的消息直接原样反弹回去）来了解TCP通信的基本流程和所涉及的API。

**服务端核心代码**

```C
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: TCP-reflectionServer.c
//  描述: 基于TCP协议的“消息反弹”服务器，即：将客户端发来
//        的消息，原样发回给客户端。
//        本版本仅支持一个客户端的连接。
//
///////////////////////////////////////////////////////

int main(int argc, char **argv)
{
	// 1. 创建TCP套接字
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);

	// 2. 将套接字与IP和端口绑定
	struct sockaddr_in addr;
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(INADDR_ANY); // 自动获取本机IP
	addr.sin_port = htons(50021); // 端口号PORT
	bind(sockfd, (struct sockaddr *)&addr, len);

	// 3. 将sockfd设置为被动监听套接字
	listen(sockfd, 3);

	// 4. 等待客户端的连接
	int connfd = accept(sockfd, NULL, NULL);

	char buf[100];
	while(1)
	{
		bzero(buf, 100);
		read(connfd, buf, 100);
		printf("收到客户端消息: %s", buf);
C
		// 4. 将消息原样回弹给客户端
		write(connfd, buf, strlen(buf));
	}

	close(connfd);
	close(sockfd);

	return 0;
}
```



**客户端核心代码**

```
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: TCP-reflectionClient.c
//  描述: 基于TCP协议的“消息反弹”客户端，即：本程序发送给
//        服务器的消息，都将被原样发回来。
//
///////////////////////////////////////////////////////

int main(int argc, char **argv)
{
	// 1. 准备TCP套接字
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);

	// 准备服务器的地址
	struct sockaddr_in addr;
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = inet_addr(服务器IP);
	addr.sin_port = htons(50021);

	// 对服务器发起连接请求...
	connect(sockfd, (struct sockaddr *)&addr, sizeof(addr));

	char sendbuf[100];
	char recvbuf[100];
	while(1)
	{
		bzero(sendbuf, 100);
		fgets(sendbuf, 100, stdin);

		// 向服务器发送数据
		write(sockfd, sendbuf, strlen(sendbuf));

		// 接收TCP回弹服务器发回的消息
		bzero(recvbuf, 100);
		if(read(sockfd, recvbuf, 100) > 0 )
			printf("服务器回弹：%s", recvbuf);
	}

	close(sockfd);
	return 0;
}
```



服务端代码下载：[TCP-reflectionServer.c](http://vm.yueqian.com.cn:8886/group1/M00/13/9D/wKgP3GIqCeCAKR1hAAAKclmDLVs97038.c?token=null&ts=null&filename=TCP-reflectionServer.c)
客户端代码下载：[TCP-reflectionClient.c](http://vm.yueqian.com.cn:8886/group1/M00/13/9D/wKgP3GIqCeCAC-GPAAAG5MD3aj445676.c?token=null&ts=null&filename=TCP-reflectionClient.c)

#### **2.2 核心API解析**

**(1) 地址绑定**

```
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```



- 功能
    - 将套接字 `sockfd` 与指定的IP和端口绑定
    - 注意，对于绑定了某个协议套接字的地址，不能重复绑定。
- 参数
    - **sockfd** - 套接字文件描述符
    - **addr** - 地址结构体，包含了IP+PORT
    - **addrlen** - 地址结构体长度
- 返回值
    - 成功返回 0
    - 失败返回-1

一般而言，TCP服务端套接字都需要绑定IP和端口，否则客户端无法发起连接。另外，除非要指定客户端的地址信息，TCP客户端套接字无需绑定IP和端口。

注意到，一条成功建立的TCP连接，由服务端和客户端两对IP和端口过程，例如：

- `<IP1:PORT1, IP2:PORT2>`
- `<192.168.1.100:5443, 192.168.1.200:50001>`
- `<10.0.0.213:52212, 202.33.12.23:2383>`

一条TCP连接由上述双方四个参数构成，其中任意一个参数差异都可以形成一条新的连接

**(2) 设置监听**

```
int listen(int sockfd, int backlog);
```



- 功能
    - 将套接字的状态设置为被动监听状态
    - 设定该套接字的最大等待连接数为backlog
- 参数
    - **sockfd** - 套接字文件描述符
    - **backlog** - 等待连接数最大值
- 返回值
    - 成功返回 0
    - 失败返回-1

套接字被设定为被动监听状态后，该套接字sockfd只能被动接收连接，不能再主动发起连接。backlog规定的是最大等待连接数，而不是最大连接数，在Linux中，如果backlog被设定为0，实质的最大等待连接数为4，也就是最多允许同时处理4个远端请求。在Linux中，backlog的最大值被限定在文件 `/proc/sys/net/core/somaxconn` 中。

另外要注意，要将该函数与阻塞等待对端连接的`accecpt()`区分开，`listen()`只是设置套接字状态以及设定backlog数目，它本身是不阻塞的，不能望文生义，以为 `listen` 就是监听等待对方，该函数的名字很容易产生歧义。

**(3) 等待连接请求**

```
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
```



- 功能
    - 阻塞等待TCP连接请求
- 参数
    - **sockfd** - 套接字文件描述符
    - **addr** - 客户端地址信息结构体，可设定为NULL
    - **addrlen** - 地址结构体长度指针，可设定为NULL
- 返回值
    - 成功返回一个新的非负连接套接字描述符
    - 失败返回-1
- 详解
    - 该函数默认会阻塞等待客户端连接请求
    - 当不需要保存客户端地址信息时，后两个参数都可以被设定为NULL
    - 成功返回一个新的连接套接字，是专用于与客户端通信的、能收发数据的套接字

**重点说明**
由 `accept()` 函数返回的套接字，称为 **已连接套接字**，这与其第一个参数 `sockfd` **被动监听套接字** 不同，前者专用于与对端进行读/写操作，后者专用于接收对端的连接请求，它们职责分明，不可混用。

**(4) 发起连接请求**

```
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
```



- 功能
    - 对指定地址的TCP服务端发起连接请求
- 参数
    - **sockfd** - 套接字文件描述符
    - **addr** - 服务端地址信息结构体
    - **addrlen** - 地址结构体长度
- 返回值
    - 成功返回 0
    - 失败返回-1

该函数会向指定服务器发送连接请求SYN，正常情况下服务器会返回应答ACK和SYN2，然后该函数再返回一个ACK2给服务器，此过程就是著名的TCP三次握手。连接的建立是需要一定时间的，在网络环境较差的条件下时间可能会比较长，也就是说 `connect()` 函数在网络不通畅的情形下会阻塞。



## TCP状态及相关概念

### **1. TCP通信状态**

#### **1.1 TCP有限状态机**

与UDP不同的是，TCP套接字有不同的状态，正是这些不同的状态的转换，保证了TCP协议的正常运转。在下图中，**红色实线**箭头代表的是TCP**客户端**套接字的状态转换，**绿色虚线**箭头代表的是TCP**服务端**套接字的状态转换：

![img](./img/wKgP3GIwW_mAfEi3AAVJc8nZVII172.png)
<center>
    TCP有限状态机
</center>



上图中的英文术语说明：

- **SYN**: synchronous，同步，同步请求，连接请求
- **ACK**: acknowledgement，回执，确认
- **RST**: reset，重置
- **FIN**: finish，结束，结束请求，关闭请求

#### **1.2 TCP三次握手**

从起点 `CLOSED` 到 `ESTABLISHED` 的过程，就是TCP建立连接的过程，在这个过程中：

- 客户端
    - 通过 `connect()` 向服务端发送 `SYN` 同步请求数据
    - 收到 `SYN/ACK` 并回送 `ACK` 后处于 `ESTABLISHED` 状态
- 服务端
    - 通过函数 `listen()` 将TCP套接字设置为 `LISTEN` 状态
    - 在收到客户端的 `SYN` 请求并回送 `SYN/ACK` 后处于 `SYN_RCVD` 状态
    - 最后收到客户端的 `ACK` 后与客户端一并处于 `ESTABLISHED` 状态
- 至此，TCP建立完毕，这个过程就是著名的 **三次握手** 的详细过程，如下图所示：

![img](./img/wKgP3GIwW_mAShHoAA4uVxTlOKI024.png)
<center>
    TCP协议三次握手
</center>



与三次握手相关的应用层核心代码：
**客户端**

```
// 该函数发起连接请求 SYN
// 并等待对端的ACK和SYN后，再发送ACK给对端
// 并最终将sockfd的状态调整为 ESTABLISHED
connect(sockfd, &srvaddr, len);
```



**服务端**

```
// 该函数发起连接请求 SYN
// 并等待对端的ACK和SYN后，再发送ACK给对端
// 并最终将sockfd的状态调整为 ESTABLISHED
int connfd = accept(listenfd, NULL, NULL);
```



客户端和服务端互相来回发送 `SYN` 和 `ACK` 的三次握手的过程，就发生在 `connect()` 和 `accept()` 这两个函数之间。

#### **1.3 connect卡顿优化**

由于数据包在网络中的传输是需要时间的，并且会因为网络拥塞的原因导致接收延时，因此三次握手并非一瞬间就能完成，比如客户端很有可能由于网络不畅导致迟迟不能得到服务端的确认，那么有时为了更好的用户体验和必要的逻辑控制，一般要给 `connect()` 套接字加上连接进度和超时控制，以便于在无法连接或者缓慢连接服务器的场景下，提供更好的使用体验。

**connect卡顿优化核心代码**

```
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: connectingDelay.c
//  描述: TCP连接的进度和超时控制
//
///////////////////////////////////////////////////////

void *connecting_host(void *arg)
{
	pthread_detach(pthread_self());

	fprintf(stderr, "正在连接远端服务器");
	while(g_connecting == CONNECTING)
	{
		fprintf(stderr, ".");
		usleep(100*1000);
	}
	printf("%s", g_connecting==CONNECT_SUCCESS ? "[OK]\n": "[FAIL]\n");
	sem_post(&s);

	pthread_exit(NULL);
}

int main(int argc, char **argv)
{
    // DNS查询，取得站点主机IP
	struct hostent *he = gethostbyname(argv[1]); 
	struct in_addr **addr_list = (struct in_addr **)(he->h_addr_list);

	struct sockaddr_in srvaddr;
	socklen_t addrlen = sizeof(srvaddr);
	bzero(&srvaddr, addrlen);
	srvaddr.sin_family = AF_INET;
	srvaddr.sin_port   = htons(80);
	srvaddr.sin_addr   = *addr_list[0];
    
    // 创建TCP套接字并将套接字设置为非阻塞，以便于进行连接进度控制
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);
	long state = fcntl(sockfd, F_GETFL);
	state |= O_NONBLOCK;
	fcntl(sockfd, F_SETFL, state);

    // 连接进度显示辅助
	sem_init(&s, 0, 0);
	g_connecting = CONNECTING;
    pthread_t t;
	pthread_create(&t, NULL, connecting_host, NULL);

    // 对服务器发起连接请求...
	if((connect(sockfd, (struct sockaddr *)&srvaddr, addrlen) == -1)
		&& (errno==EINPROGRESS || errno==EAGAIN))
	{
		fd_set wset;
		FD_ZERO(&wset);
		FD_SET(sockfd, &wset);

        // 将套接字重新设置为阻塞模式，以便于进行超时控制
		long state = fcntl(sockfd, F_GETFL);
		state &= ~O_NONBLOCK;
		fcntl(sockfd, F_SETFL, state);

		// 设置5秒超时
		struct timeval tv = {5, 0};
		int n = select(sockfd+1, NULL, &wset, NULL, &tv);
		if(n == 0)
		{
			g_connecting = CONNECT_FAIL;
			sem_wait(&s);
			fprintf(stderr, "连接超时.\n");
			exit(0);
		}
		else if(FD_ISSET(sockfd, &wset))
		{
            int err;
            int len = sizeof(err);
            getsockopt(sockfd, SOL_SOCKET, SO_ERROR, &err, &len);

            if(err == 0)
            {
                printf("[OK]\n");
                exit(0);
            }
		}
	}
    else 
        printf("[OK]\n");

	exit(0);
}
```



完整代码下载：[connectionDelay.c](http://vm.yueqian.com.cn:8886/group1/M00/13/CB/wKgP3GIrH8OAJPfxAAAMVXIlrAw17273.c?token=null&ts=null&filename=connectingDelay.c)

可以用上述代码来测试国内外站点的访问速度：

```
gec@ubuntu-20:~/tcp$ ./connectingDelay www.qq.com
正在连接远端服务器.[OK]
gec@ubuntu-20:~/tcp$ ./connectingDelay www.github.com
正在连接远端服务器...[OK]
```



```
gec@ubuntu-20:~/tcp$ ./connectingDelay www.google.com
正在连接远端服务器............................................[FAIL]
连接超时
gec@ubuntu-20:~/tcp$
```



对上述核心代码，核心的步骤归结起来是：

- **(1)** 将待连接TCP套接字设置为非阻塞

```
long state = fcntl(sockfd, F_GETFL);
state |= O_NONBLOCK;
fcntl(sockfd, F_SETFL, state);
```



- **(2)** 尝试连接服务器，并对网络不畅引起的连接延迟做出判断

```
if((connect(sockfd, (struct sockaddr *)&srvaddr, addrlen) == -1)
		 && (errno==EINPROGRESS || errno==EAGAIN))
{
    ...
}
```



- **(4)** 若的确发生了连接延迟，则将套接字重新设置为阻塞模式并设置超时

```
// 将套接字重新设置为阻塞模式，以便于进行超时控制
long state = fcntl(sockfd, F_GETFL);
state &= ~O_NONBLOCK;
fcntl(sockfd, F_SETFL, state);

// 设置5秒超时
struct timeval tv = {5, 0};
int n = select(sockfd+1, NULL, &wset, NULL, &tv);
```



在上述代码中，涉及多路复用IO函数 `select()` ，这将在《服务器IO模型》中详细讲解。

#### **1.4 四次挥手**

与 **三次握手** 类似，在TCP断开连接的时候，客户端和服务器也会相互发送断开请求和确认，而又因为允许一方断开读端或写端而保持另一端的通畅，因此两端的关闭请求可以不必同时发生，因此中间的 `FIN` 和 `ACK` 就不像连接时那样经常合并在一起，而是常常分开传输，因此断开连接的过程通常体现为**四次挥手**，如下图所示：

![img](./img/wKgP3GIwW_mAboKnAA6Agm1cQ2U504.png)
<center>
    TCP协议四次挥手
</center>



**关闭连接核心代码**

```
// 客户端主动发起断开请求核心代码
close(sockfd);

// 服务端处理断开请求核心代码
if(read(sockfd, buf, size) == 0)
{
	close(sockfd);
}
```



注意到，对于TCP服务端而言，`read()`返回0意味着对端已关闭了连接，此时服务端就可以关闭套接字了。

#### **1.5 特殊状态`TIME_WAIT`**

在上图中，四次挥手所涉的几种TCP状态里面，左下角的客户端 `TIME_WAIT` 显得有些特别，因为当客户端处于该状态时，客/服双方都均已收到对方的断开请求`FIN`并已发出确认`ACK`，那么客户端在此之后又处于 `TIME_WAIT` 状态而不立即置位的原因是什么呢？而这个状态的持续时间是2倍的 `MSL`（即数据包最大存活时间）又是为什么呢？

首先，客户端发出最后断开确认 `ACK` 后仍处于 `TIME_WAIT` 的原因有两个：

- 防止最后一个 `ACK` 丢失后，服务端由于迟迟收不到而重发的 `FIN` 无人接收。
- 防止客户端中立刻重用了相同IP和端口的程序（通常被称为网络分身）收到来自上一任连接的对端的数据。

其次，假设最后一个 `ACK` 恰好丢失，那么服务器将会由于迟迟收不到最后一个 `ACK` 而重发 `FIN`，这两个一来一回的数据包的最长传输时间，就是从客户端发出最后一个 `ACK` 算起的2倍数据包存活时间，如果客户端在2倍的 `MSL` 都没收到服务器的 `FIN`，就说明服务器已收到了最后的 `ACK`，客户端就可以安心将套接字状态切环为 `CLOSE` 并且释放地址资源。

**注意1**
仔细深究还会发现：即便客户端等待2倍的数据包存活时间也无法保证服务端正确地收到最后一个 `ACK` 而正常关闭了套接字，因为还可能是最后一个 `ACK`丢失并且服务端因此而重发的最后一个 `FIN` 也同时丢失，因此通信协议并不能 100% 消除网络异常，但能极大地降低出现异常的概率。

**注意2**
由于套接字的状态是由系统内核决定的，套接字也是由内核管理的，因此在应用程序退出之后，由于上述规则，套接字及其状态会继续存在并保留一段时间（2倍 `MSL`），在此期间内无法再重复绑定或使用相同的IP和端口，如果程序需要内核跳过 `TIME_WAIT` 状态立即释放这些地址资源，可以用以下代码达成：

```
// 使套接字sockfd关联的地址在套接字关闭后立即释放
int on = 1;
setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));
```



### **2. TCP协议简析**

TCP之所以可以自动进行数据包的丢失重传、自动充足、保证有序，甚至可以对网络拥塞做出自动调整数据发送量，原因是TCP有一个表征了所有这些信息的头部，即所谓的TCP协议头，它被装载到每一个TCP数据段上，就像这样：

![img](./img/wKgP3GIwW_mALCw5AAOibccDVVs795.png)
<center>
    TCP协议头
</center>



从上图可以很清晰地看到，IP包由IP首部和IP数据部分组成，而IP数据部分又由TCP首部和TCP数据部分组成，因此：`IP包 = IP首部+TCP首部+TCP数据`。可见，这些协议信息都是以这样一层套一层的形式，封装在真正的网络数据外面，对于TCP首部来说，主要核心的字段有：

- 端口：
    - 源端端口：即发送方套接字的端口号。
    - 目的端端口：即接收方套接字的端口号。
- 序号：
    - 即序列号（`sequence number`），用来标记已发送的数据量，单位为字节。
    - 当TCP数据段携带SYN请求时，序列号实际上是初始序列号（ISN），第一个数据字节是ISN+1。
    - 当TCP数据段净载荷（不含TCP首部）为12字节且序列号为SN1时，那么下一次发送时（假定数据被正常接收）SN2 = SN1+12。
- 确认号
    - 即TCP应答、TCP回执（`Acknowledgment`），用来标记已接收的数据量，单位为字节。
    - 这个值表示一个准备接收的包的序列码。
    - 当发生数据丢失时，确认号可以让发送方重新发送接收方未接收到的数据。
- 数据偏移
    - 实际上就是TCP首部的长度，跳过TCP首部就是TCP数据
    - 数据偏移字段栈4比特位，取值范围是`0-15`，单位是4字节（注意不是1字节）
    - TCP首部最短20字节。
- 标志位
    - `URG`：置位时代表当前TCP数据段包含紧急（带外）数据，此时紧急指针有效
    - `ACK`：置位时代表当前TCP数据段包含应答，此时确认号有效
    - `PSH`：置位时代表发送端缓存中已没有待发送数据，接收端应尽快将数据交由应用层处理。
    - `RST`：该标志用于复位相应TCP连接，通常在发生异常或错误时会触发复位TCP连接。
    - `SYN`：置位时代表当前TCP数据段包含同步请求，该标志仅在三次握手时有效。
    - `FIN`：置位时代表当前TCP数据段包含结束请求，该标志仅在四次握手时有效。
- 窗口
    - 这是一个16位的字段，指示了从`ACK`开始还愿意接收多少字节的数据量，也即用来表示当前接收端的接收窗还有多少剩余空间。
    - 该字段用于TCP的流量控制。
- 校验和
    - 接收端校验失败时会丢弃这个数据包。
    - 校验成功并不能代表数据比特位100%正确，严格的校验需要应用层自己添加校验算法。
- 紧急指针
    - 用来指示`OOB`数据在`TCP`数据部分的偏移量。
    - 在标志位`URG`置位时有效。



## 缓冲区与带外数据

### **1. TCP数据缓冲区**

在 TCP 通信当中，发送方和接收方都有所谓的缓冲区，发送方的缓冲区用来为数据的丢失重发做准备，接收方的缓冲区配合水位线可以用来规范接收数据块的大小。

#### **1.1 发送缓冲区**

对于发送缓冲区，可以用如下代码来检测和设置：（完整代码下载：[TCP-sendBuffer.c](http://vm.yueqian.com.cn:8886/group1/M00/13/CF/wKgP3GIu5eCAENrvAAAFhg7dRc404664.c?token=null&ts=null&filename=TCP-sendBuffer.c) ）

```
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: TCP-sendBuffer.c
//  描述: 检测、设置TCP的发送缓冲区
//
///////////////////////////////////////////////////////

int main(int argc, char **argv)
{
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);

    int bufSize = 0;
    int len = sizeof(bufSize);

    // 设定发送缓冲区大小
    scanf("%d", &bufSize);
    len = sizeof(bufSize);
    setsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &bufSize, len);

    // 检测发送缓冲区大小
    bufSize = 0;
    len = 0;
    getsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &bufSize, &len);
    printf("发送缓冲区大小: %d\n", bufSize);

	close(sockfd);
	return 0;
}
```



在Linux下，TCP的发送缓冲区大小一般介于 `4608-425984` 之间，不同主机的检测结果可能有所不同。发送缓冲区的基本作用，是当接收方发现数据丢失要求发送方重发时，发送方有备份数据可以重新发送。注意，这里提到的发现数据丢失、要求重发等行为，是TCP协议本身的自动机制，不需要应用层软件参与。

#### **1.2 接收缓冲区**

对于接收缓冲区，可以用如下代码来检测和设置：（完整代码下载：[TCP-recvBuffer.c](http://vm.yueqian.com.cn:8886/group1/M00/13/CF/wKgP3GIu5eCAfDZ6AAAFhLY2Ypg74885.c?token=null&ts=null&filename=TCP-recvBuffer.c) ）

```
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: TCP-recvBuffer.c
//  描述: 检测、设置TCP的接收缓冲区
//
///////////////////////////////////////////////////////

int main(int argc, char **argv)
{
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);

    int bufSize = 0;
    int len = sizeof(bufSize);

    // 设定接收缓冲区大小
    scanf("%d", &bufSize);
    len = sizeof(bufSize);
    setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &bufSize, len);

    // 检测接收缓冲区大小
    getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &bufSize, &len);
    printf("接收缓冲区大小: %d\n", bufSize);

	close(sockfd);
	return 0;
}
```



在Linux下，TCP的接收缓冲区大小一般介于 `2304-425984` 之间，不同主机的检测结果可能有所不同。接收缓冲区的最初概念，是套接字从网络接收到的数据在暂存区，尤其当传输的数据是结构化数据时，设定特定大小的缓冲区就特别有用，比如收发大小为100个字节的结构体，那么为了保证接收方每次收到的都是完整的100个字节的整块数据，可以将接收缓冲区设定为100。核心代码如下所示：

```
// 设定接收缓冲区为100个字节
int bufSize = 100;
int len = sizeof(bufSize);
setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &bufSize, len);
```



但执行上述代码会发现，就算设定了接收缓冲区为100，发送方发送1个字节的数据时接收方也会立即 `read()` 出来，达不到我们想要每次完整接收100个字节的数据块目的，这是怎么回事呢？ 问题出在下面要讲的水位线的概念上。

#### **1.3 水位线**

水位线是个很形象的说法，TCP将接收缓冲区视为一个水池，原则上只有等水池的水满了（接收的数据填满了缓冲区），应用层才能读取到数据，但为了更灵活，TCP增加了一个叫水位线的概念，规定：当接收数据量超过水位线时，就触发套接字的 **读就绪** 状态，使得应用层的 `read()` 函数可以正常读取数据。

![img](./img/wKgP3GIwXAiAIa0MAAAYscrIgko958.png)

**设置TCP缓冲区水位线**（完整代码下载：[TCP-lowat.c](http://vm.yueqian.com.cn:8886/group1/M00/13/CF/wKgP3GIvAS-ABwH0AAAFo2XSc9s47259.c?token=null&ts=null&filename=TCP-lowat.c)）

```
////////////////////////////////////////////////////////
//
//  Copyright(C), 2005-2022, GEC Tech. Co., Ltd.
//  www.yueqian.com.cn  ALL RIGHT RESERVED
//
//  文件: TCP-lowat.c
//  描述: 检测、设置TCP的接收缓冲区水位线
//
///////////////////////////////////////////////////////

int main(int argc, char **argv)
{
	int sockfd = socket(AF_INET, SOCK_STREAM, 0);

    int rcvLowat = 0;
    int len = sizeof(rcvLowat);

    // 设定接收缓冲区水位线
    scanf("%d", &rcvLowat);
    setsockopt(sockfd, SOL_SOCKET, SO_RCVLOWAT, &rcvLowat, len);

    // 检测接收缓冲区水位线
    getsockopt(sockfd, SOL_SOCKET, SO_RCVLOWAT, &rcvLowat, &len);
    printf("接收缓冲区水位线: %d\n", rcvLowat);

	close(sockfd);
	return 0;
}
```



### **2. OOB带外数据**

考虑这样一种情形：接收方设置了较大的缓冲区（比如10000字节）和较高的水位线（比如100字节），由于接收的数据量必须要达到水位线（默认是1字节）才能使套接字读就绪，因此在接收较少数据（比如80个字节）时，发送方发出的数据就会滞留在接收方的缓冲区中，若此时恰好有一些比较紧急的数据（比如一些控制信息），那这些数据就会被被迫滞留在缓冲区中无法被接收方读取，造成逻辑上的缺憾。

解决这个问题的办法是：将紧急数据设定为 **带外数据**，通过特殊的标志位，让其抵达接收方后可以冲破缓冲区和水位线的限制，让接收方可以优先读取。这种机制就是 TCP 的 OOB（Out of Band） 数据。

#### **2.1 OOB的基本性质**

- OOB 数据指的是在 TCP 通信中的一种特殊数据，它能冲破接收端缓冲区和水位线的限制。
- OOB 数据的到达会触发对端套接字产生 SIGURG 信号。
- OOB 数据的到达会使得对端套接字处于异常就绪状态，可以通过 select 监测到。
- OOB 数据每次只能发送 1 个字节，但是可以发送多次。
- OOB 数据只能使用 `recv()` 和 `send()` 来收发。

#### **2.2 OOB的基本操作**

- 发送：通过 `send()` 并加上 MSG_OOB 标记

```
send(sockfd, "x",   1, MSG_OOB); // 将x标记为带外数据OOB发送给对端
send(sockfd, "xyz", 3, MSG_OOB); // 将z标记为带外数据OOB发送给对端
```



- 接收：有两种方式接收 OOB
    - 方式一：利用 OOB 自动触发信号 SIGURG 来接收
    - 方式二：利用 OOB 触发的异常就绪状态来接收

**示例代码**

```
// 方式1：
signal(SIGURG, recvOOB); // 捕捉信号 SIGURG
fcntl(sockfd, F_SETOWN, getpid());  // 指定信号的接收者（属主）

void recvOOB(int sig)
{
    char oob;
    recv(sockfd, &oob, 1, MSG_OOB); //接收对端的OOB带外数据
}
```



```
// 方式2：
fd_set eset;
FD_ZERO(&eset);
FD_SET(sockfd, &eset); // 将套接字加入描述符集合中
select(sockfd+1, NULL, NULL, &eset, NULL); // 监听 OOB
if(FD_ISSET(sockfd, &eset))
{
    char oob;
    recv(sockfd, &oob, 1, MSG_OOB); //接收对端的OOB带外数据
}
```



## 网络超时控

### **1. 基本概念**

超时实际上是一种介于阻塞与非阻塞之间的折中等待的方案：

- 阻塞操作，意味着如果条件不满足时需要一直等待，等待的最长时间是：∞∞
- 非阻塞操作，意味着如果条件不满足时立即放弃，等待最长时间是：00

以上两种方式都比较极端，有时候我们需要等待某个资源，但又不想等太久，这时就需要用到所谓超时控制：

- 超时控制，意味着如果条件不满足时等待时间可以自定义为：x*x*

### **2. 超时控制实现办法**

在套接字操作中，超时控制有三种方式：

1. 直接设置套接字的超时属性，简单易用，童叟无欺。
2. 利用 select 函数自带的超时属性，群体控制，也挺好用。
3. 利用 SIGALRM 和它的搭档 alarm() 函数，自定闹钟，也能达到目的。

#### **2.1 套接字超时属性**

不管是TCP还是UDP，还是别的类型的套接字，他们本身就有超时属性，我们可以通过 `setsockopt()` 来直接设置超时属性，比如：

```
struct timeval tv;
tv.tv_sec  = 3;
tv.tv_usec = 0;
setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
```



在上述核心代码中，套接字sockfd被设置了**接收超时**（SO_RCVTIMEO）为3秒，这意味着：

- 如果 `sockfd` 是一个待连接监听套接字，那么其等待对端连接最多等3秒钟。
- 如果 `sockfd` 是一个已连接套接字，那么其等待对端数据最多等3秒钟。

#### **2.2 设置 select 的超时属性**

在多路复用IO中，函数 `select()` 也可以在多路监听的同时设置超时：

```
struct timeval tv;
tv.tv_sec  = 3;
tv.tv_usec = 0;

select(maxfd+1, &rset, NULL, NULL, &tv);
```



关于 `select()` 函数的具体详解，请参阅《第4章-服务器IO》相关章节。

#### **2.3 利用 SIGALRM 和 alarm()**

在众多的系统信号中，信号 `SIGALRM` 可由定时器函数 `alarm()` 触发，因此可以很方便地进行超时控制。

**核心示例代码**

```
int main()
{
    struct sigaction act;
    bzero(&act, sizeof(act));
    act.sa_handler = f;
    act.sa_flags  &= ~SA_RESTART; // 在信号响应完毕时，不要自动重启该系统函数。

    sigaction(SIGALRM, &act, NULL);

    alarm(3); // 3秒之后，自动触发SIGALRM
    read(connfd, buf, 100); // 该函数会一直阻塞，直到读取到数据或者被信号中断
}
```





