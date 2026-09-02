# systemV的IPC对象

[toc]

## 消息队列MSG

### **1. IPC对象概述**

各种不同的IPC其实是在不同时期逐步引入的，在UNIX伯克利版本system-V（念作系统五，V是罗马数字，是Unix伯克利分支的版本号）中引入的三种通信方式（消息队列、共享内存和信号量组）被称为IPC对象，它们有较多共同的特性：

- 在系统中使用所谓键值（KEY）来唯一确定，类似于文件系统中的文件路径。
- 当某个进程创建（或打开）一个IPC对象时，将会获得一个整型ID，类似于文件描述符。
- IPC对象属于系统，而不是进程，因此在没有明确删除操作的情况下，IPC对象不会因为进程的退出而消失。

![img](http://edu.yueqian.com.cn/group1/M00/0F/F7/wKgP3GHl8SOAV7ZSAABPdzCNtLs372.png?token=null&ts=null)
<center>
    系统IPC对象
</center>



### **2. IPC对象相关命令**

以下命令可以帮助更好了解系统IPC。

#### **2.1 查看IPC对象**

```
# 查看系统当前所有IPC对象
gec@ubuntu:~$ ipcs -a
------ Message Queues --------
key        msqid      owner      perms      used-bytes   messages    

------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status      
0x00000000 393216     gec        600        67108864   2          dest         
0x00000000 557057     gec        600        524288     2          dest         
0x00000000 655362     gec        600        524288     2          dest         
0x00000000 688131     gec        600        524288     2          dest         
0x51010451 8978436    gec        600        1024       1                       

------ Semaphore Arrays --------
key        semid      owner      perms      nsems     
```



```
# 查看系统当前所有的消息队列MSG对象
gec@ubuntu:~$ ipcs -q
------ Message Queues --------
key        msqid      owner      perms      used-bytes   messages    
```



```
# 查看系统当前所有共享内存SHM对象
gec@ubuntu:~$ ipcs -m
------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status      
0x00000000 393216     gec        600        67108864   2          dest         
0x00000000 557057     gec        600        524288     2          dest         
0x00000000 655362     gec        600        524288     2          dest         
0x00000000 688131     gec        600        524288     2          dest         
0x51010451 8978436    gec        600        1024       1                       
```



```
# 查看系统当前所有信号量组SEM对象
gec@ubuntu:~$ ipcs -s
------ Semaphore Arrays --------
key        semid      owner      perms      nsems   
```



#### **2.2 删除IPC对象**

```
ipcrm -Q key : 删除指定的消息队列
ipcrm -q id : 删除指定的消息队列

ipcrm -M key : 删除指定的共享内存
ipcrm -m id： 删除指定的共享内存

ipcrm -S key : 删除指定的信号量
ipcrm -s id： 删除指定的信号量
```



### **3. 消息队列**

#### **3.1 基本逻辑**

消息队列是system-V三种IPC对象之一，其最主要的特征是允许发送的数据携带类型，具有相同类型的数据在消息队列内部排队，读取的时候也要指定类型，然后依次读出数据。这使得消息队列用起来就像一个多管道集合，如下图所示：

![image-20260720091118981](./img/image-20260720091118981.png)
<center>
    消息队列基本逻辑
</center>



由于每个消息都携带有类型，相同的类型自成一队，因此读取方可以根据类型来“挑选”不同的队列，也因此MSG适用于所谓“多对一”的场景，经典案例是系统日志：多个不同的、不相关的进程向同一管道输入数据。

#### **3.2 应用场景**

消息队列最常见的应用场合是作为读写不同步的两个进程间的缓冲区，比如一个进程从文件读取数据，另一个进程将数据发送到网络，那么如果网络带宽环境较差，数据发送进程可能没办法及时将数据发出，这时数据读取进程就可以通过消息队列将未来得及发出去的数据缓冲区来，不耽误数据的读取，发送者那边根据实际情况从消息队列读取出去再发出去。

像这样通信双方读写速度不一致，需要的中间缓冲来协调的场合，在涉及硬件读写或网络读写时尤为明显，消息队列都可以作为非常好的中间过渡机制。**消息队列实现了对消息发送方和消息接收方的解耦，使得双方可以异步处理消息数据**，这是消息队列最重要的应用。

#### **3.3 函数接口**

**创建或打开MSG对象**
对消息队列的使用非常简单，由如下接口提供：

```C
// 创建（或打开）消息队列
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

int msgget(key_t key, int msgflg);
```

- 接口说明
    - 返回值：消息队列MSG对象ID
    - 参数key：键值，全局唯一标识，可由ftok()产生
    - 参数msgflg：操作模式与读写权限，与文件操作函数open类似。

示例代码：

```C
int main()
{
    // 以当前目录和序号1为系数产生一个对应的键值
    key_t key = ftok(".", 1);

    // 创建（若存在则报错）key对应的MSG对象
    int msgid = msgget(key, IPC_CREAT|IPC_EXCL|0666);
}
```

**注意：**
key实质上就是一个整数，但该整数一般应由 ftok() 产生而不应手写，因为key作为键值是 IPC 对象在系统中的唯一标识，万一误撞就会导致错乱。

ftok()的接口有时也容易使人糊涂：

```C
#include <sys/types.h>
#include <sys/ipc.h>
key_t ftok(const char *pathname/*路径*/, int proj_id/*序号*/);
```

- 对于ftok()函数参数，首先需要说明的一点是，路径和序号一样的情况下，产生的键值key也是一样的。那么，由于项目开发中，需要互联互通的进程一般会放在同一目录下，而其他无关的进程则不会放在一起，一起使用路径来产生键值是有效避免键值误撞的手段，序号是为了以防在某路径下需要产生多个IPC对象的情况。
- 最后需要再重申一点的是，ftok()函数参数中的路径仅仅是产生键值key的参数，与实际文件系统并无关系。
- 若 msgget() 中的key写成 IPC_PRIVATE，那意味着新建一个私有的IPC对象，该对象只在本进程内部可见，与外部的系统MSG对象不会冲突。

**向MSG对象发送消息**

```C
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

int msgsnd(int msqid, const void *msgp, size_t msgsz, int msgflg);
```

接口说明：

- msgqid：MSG对象的ID，由msgget()获取。
- msgp：一个指向等待被发送的消息的指针，由于MSG中的消息最大的特点是必须有一个整数标识，用以区分MSG中的不同的消息，因此MSG的消息会使用一个特别的结构体来表达，具体如下所示：

```C
struct msgbuf
{
    // 消息类型（固定）
    long mtype;

    // 消息正文（可变）
    // ...
};
```

因此一般而言，msgp就是一个指向上述结构体的指针。

- msgsz：消息正文的长度（单位字节），注意不含类型长度。
- msgflg：发送选项，一般有：
    - 0：默认发送模式，在MSG缓冲区已满的情形下阻塞，直到缓冲区变为可用状态。
    - IPC_NOWAIT：非阻塞发送模式，在MSG缓冲区已满的情形下直接退出函数并设置错误码为EAGAIN.

示例代码：

```C
struct message
{
	long mtype;
	char mtext[80];
};

int main(void)
{
	int msgid;
	msgid = msgget(ftok(".", 1), IPC_CREAT | 0666);

	struct message msg;
	bzero(&msg, sizeof(msg));

	// 消息类型
	msg.mtype = 1;
	// 消息内容
	fgets(msg.text, 80, stdin);

    // 发送消息
	msgsnd(msgid, &msg, strlen(msg.mtext), 0);
}
```

**从MSG对象接收消息**

```
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

ssize_t msgrcv(int msqid, void *msgp, size_t msgsz, long msgtyp, int msgflg);
```

接口说明：

- msgqid：MSG对象的ID，由msgget()获取。
- msgp：存放消息的内存入口。
- msgsz：存放消息的内存大小。
- msgtyp：欲接收消息的类型：
    - 0：不区分类型，直接读取MSG中的第一个消息。
    - 大于0：读取类型为指定msgtyp的第一个消息（若msgflg被配置了MSG_EXCEPT则读取除了类型为msgtyp的第一个消息）。
    - 小于0：读取类型小于等于msgtyp绝对值的第一个具有最小类型的消息。例如当MSG对象中有类型为3、1、5类型消息若干条，当msgtyp为-3时，类型为1的第一个消息将被读取。
- msgflg：接收选项：
    - 0：默认接收模式，在MSG中无指定类型消息时阻塞。
    - IPC_NOWAIT：非阻塞接收模式，在MSG中无指定类型消息时直接退出函数并设置错误码为ENOMSG.
    - MSG_EXCEPT：读取除msgtyp之外的第一个消息。
    - MSG_NOERROR：如果待读取的消息尺寸比msgsz大，直接切割消息并返回msgsz部分，读不下的部分直接丢弃。若没有设置该项，则函数将出错返回并设置错误码为E2BIG。

示例代码：

```C
struct message
{
	long mtype;
	char mtext[80];
};

int main(void)
{
	int msgid;
	msgid = msgget(ftok(".", 1), IPC_CREAT | 0666);

	struct message msgbuf;
	bzero(&msgbuf, sizeof(msgbuf));

	printf("等待消息...\n");
    int m = msgrcv(msgid, &msgbuf, sizeof(msgbuf)-sizeof(long), 1, 0);

	if(m < 0)
		perror("msgrcv()");
    else
	    printf("%s\n", msgbuf.text);

	msgctl(msgid, IPC_RMID, NULL);
	return 0;
}
```



**对MSG对象其余操作**
IPC对象是一种持久性资源，如果没有明确的删除掉他们，他们是不会自动从内存中消失的，除了可以使用命令的方式删除，可以使用函数来删除。比如，要想显式地删除掉MSG对象，可以使用如下接口：

```
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

int msgctl(int msqid, int cmd, struct msqid_ds *buf);
```

接口说明：

- msqid：MSG对象ID
- cmd：控制命令字
    - IPC_STAT：获取该MSG的信息，储存在结构体msqid_ds中
    - IPC_SET：设置该MSG的信息，储存在结构体msqid_ds
    - IPC_RMID：立即删除该MSG，并且唤醒所有阻塞在该MSG上的进程，同时忽略第三个参数

在程序中如果不再使用MSG对象，为了节省系统资源，应用如下代码删除：

```
msgctl(id, IPC_RMID, NULL);
```



## 共享内存SHM

### **1. 基本概念**

共享内存，顾名思义，就是通过不同进程共享一段相同的内存来达到通信的目的，由于SHM对象不再交由内核托管，因此共享内存SHM对象是众多IPC方式最高效的一种方式，但也因为这个原因，SHM一般不能单独使用，而需要配合诸如互斥锁、信号量等协同机制使用。

![image-20260720091315130](./img/image-20260720091315130.png)
<center>
    共享内存实现逻辑
</center>



#### **2. 函数接口**

使用共享内存的一般步骤是：

1. 获取共享内存对象的ID
2. 将共享内存映射至本进程虚拟内存空间的某个区域
3. 当不再使用时，解除映射关系
4. 当没有进程再需要这块共享内存时，删除它。

下面来详细介绍这些函数接口的用法。

#### **2.1 创建或打开SHM对象**

与消息队列类似，SHM对象的创建或打开也需要一个唯一的键值标识，并且需要指定内存的大小尺寸，具体接口如下：

```
#include <sys/ipc.h>
#include <sys/shm.h>

int shmget(key_t key, size_t size, int shmflg);
```



接口说明：

- 返回值：SHM对象ID
- 参数key：SHM对象键值
- 参数size：共享内存大小
- 参数shmflg：创建模式和权限
    - IPC_CREAT：如果key对应的共享内存不存在，则创建SHM对象
    - IPC_EXCL：如果该key对应的共享内存已存在，则报错
    - 权限与文件创建open类似，用八进制表示

示例代码：

```
int main(void)
{
	key_t key = ftok(".", 1);
	int shmid;

	// 创建或打开一个大小为1024自己的SHM对象，获取其ID
	shmid = shmget(key, 1024, IPC_CREAT|0666);
	if(shmid < 0)
	{
		perror("创建SHM对象失败");
	}

	// ...

	return 0;
}	
```



#### **2.2 映射 / 解除映射SHM对象**

有了SHM对象的ID之后，必须先将其映射到用户进程的内存空间之后方可使用，映射接口如下：

```
#include <sys/types.h>
#include <sys/shm.h>

void *shmat(int shmid, const void *shmaddr/*一般为NULL*/, int shmflg);
```



接口说明：

- 功能：
    - 将指定的共享内存，映射到本进程内存空间
- 参数：
    - shmid：指定的共享内存的ID
    - shmaddr：指定映射后的地址，因为是虚拟地址，分配的原则要兼顾诸如段对齐、权限分配等问题，因此用户进程是无法指定的，只能由系统自动分配，因此此参数一般为NULL，表示交由系统来自动分配。
    - shmflg：可选项
        - 0：默认，代表共享内存可读可写。
        - SHM_RDONLY：代表共享内存只读。
- 返回值：
    - 共享内存映射后的虚拟地址入口。

正确映射之后，命令ipcs -m查看SHM对象时，可从nattch列中看到已映射进程个数：

```
aidevelop@aidevelop-vm:~$ ipcs -m

------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status      
0x00000000 688132     aidevelop  600        67108864   2          dest         
0x00000000 688137     aidevelop  600        524288     2          dest         
0x00000000 688138     aidevelop  600        524288     2          dest         
0x00000000 688139     aidevelop  600        4389528    2          dest         
0x00000000 688142     aidevelop  600        524288     2          dest         
0x5101374a 20         aidevelop  600        1024       1                    
```



使用完SHM对象后，需要将其跟进程解除关联关系，即解除映射，函数接口如下：

```
#include <sys/types.h>
#include <sys/shm.h>

int shmdt(const void *shmaddr);
```



该函数接口非常简单，参数就是从 shmat() 返回的SHM对象的入口指针。

#### **2.3 其余操作**

与其他IPC对象一样，共享内存也有一个control函数，可用于设置SHM对象属性信息、获取SHM属性信息、删除SHM对象等其余操作，接口如下：

```
#include <sys/ipc.h>
#include <sys/shm.h>

int shmctl(int shmid, int cmd, struct shmid_ds *buf);
```



接口说明：

- shmid：指定的共享内存的ID
- cmd：一些命令字
    - IPC_STAT：获取共享内存 的一些信息，放入shmid_ds{ }中
    - IPC_SET：将 buf 中指定的信息，设置到本共享内存中
    - IPC_RMID：删除指定的共享内存，此时第三个参数 buf 将被忽略
- buf：用来存放共享内存信息的结构体

用的较多的就是删除SHM对象，示例代码如下：

```
shmctl(shmid, IPC_RMID, NULL);
```



## 信号量组SEM

### 1. **基本概念**

信号量SEM全称Semaphore，中文也翻译为信号灯。信号量跟MSG和SHM有极大的不同，SEM不是用来传输数据的，而是作为“旗语”，用来协调各进程或者线程工作的。

信号量本质上是一个数字，用来表征一种资源的数量，当多个进程或者线程争夺这些稀缺资源的时候，信号量用来保证他们合理地、秩序地使用这些资源，而不会陷入逻辑谬误之中。

#### 1.1 **红绿灯**

在一个繁忙的十字路口中，路口的通过权就是稀缺资源，并且是排他的，南北向的车辆用了，东西向的车辆就不能使用，就是通过十字路口的权限，为了避免撞车，一个方向通行时另外方向的车必须停下来等待，直到红绿灯变换为止。这就是最基本的资源协同。

![img](http://edu.yueqian.com.cn/group1/M00/05/36/wKgP3GDJXLWAfa7gAAAjDaPLLm0143.png?token=null&ts=null)
信号灯

#### 1.2 **信号量的分类**

在Unix/Linux系统中常用的信号量有三种：

- **IPC信号量组**
- POSIX具名信号量
- POSIX匿名信号量

本节课讲解的是第一种IPC信号量组，既然说到它是一个“组”，说明这种机制可以一次性在其内部设置多个信号量，实际上在其内部实现中，IPC信号量组是一个数组，里面包含N个信号量元素，每个元素相当于一个POSIX信号量。

#### 1.3 **基本概念**

- 临界资源（critical resources）
    - 多个进程或线程有可能同时访问的资源（变量、链表、文件等等）
- 临界区（critical zone）
    - 访问这些资源的代码称为临界代码，这些代码区域称为临界区
- P操作
    - 程序进入临界区之前必须要对资源进行申请，这个动作被称为P操作，这就像你要把车开进停车场之前，先要向保安申请一张停车卡一样，P操作就是申请资源，如果申请成功，资源数将会减少。如果申请失败，要不在门口等，要不走人。
- V操作
    - 程序离开临界区之后必须要释放相应的资源，这个动作被称为V操作，这就像你把车开出停车场之后，要将停车卡归还给保安一样，V操作就是释放资源，释放资源就是让资源数增加。


信号量组非常类似于停车场的卡牌，想象一个有N个车位的停车场，每个车位是立体的可升降的，能停n辆车，那么我们可以用一个拥有N个信号量元素，每个信号量元素的初始值等于n的信号量来代表这个停车场的车位资源——某位车主要把他的m辆车开进停车场，如果需要1个车位，那么必须对代表这个车位的信号量元素申请资源，如果n大于等于m，则申请成功，否则不能把车开进去。

![image-20260720091505930](./img/image-20260720091505930.png)
<center>
    停车场和信号量组
</center>



### 3. **函数接口**

#### 3.1 **创建（或打开）SEM**

与其他IPC对象类似，首先需要创建（或打开）SEM对象，接口如下：

```C
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

int semget(key_t key, int nsems, int semflg);
```

接口说明：

- key：SEM对象键值
- nsems：信号量组内的信号量元素个数
- semflg：创建选项
    - IPC_CREAT：如果key对应的信号量不存在，则创建之
    - IPC_EXCL：如果该key对应的信号量已存在，则报错
    - mode：信号量的访问权限（八进制，如0644）

创建信号量时，还受到以下系统信息的影响：

1. SEMMNI：系统中信号量的总数最大值。
2. SEMMSL：每个信号量中信号量元素的个数最大值。
3. SEMMNS：系统中所有信号量中的信号量元素的总数最大值。

Linux中，以上信息在 `/proc/sys/kernel/sem` 中可查看。
示例代码：

```C
int main()
{
     key_t key = ftok(".", 1);

     // 创建（若已有则打开）一个包含2个元素的信号量组
     int id = semget(key, 2, IPC_CREAT|0666);
}
```

#### 3.2 **PV操作**

对于信号量而言，最重要的作用就是用来表征对应资源的数量，所谓的P/V操作就是对资源数量进行 +n/-n 操作，既然只是个加减法，那么为什么不使用普通的整型数据呢？原因是：

- 整型数据的加减操作不具有原子性，即操作可能被中断
- 普通加减法无法提供阻塞特性，而申请资源不可得时应进入阻塞

对于原子性再做个简单的解释，即这种资源数量的加减法不能有中间过程，不管是成功还是失败都必须一次性完成。加减法看似简单，但在硬件层面上并非一个原子性操作，而是包含了多个寄存器操作步骤，因此不能作为P/V操作的手段。

在SEM对象中，P/V操作的函数接口如下：

```C
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

int semop(int semid, struct sembuf *sops, size_t nsops);
```

接口说明：

- 参数
    - semid：SEM对象ID
    - sops：P/V操作结构体sembuf数组
    - nsops：P/V操作结构体数组元素个数
- 返回值
    - 成功：0
    - 失败：-1

其中，所谓P/V操作结构体定义如下：

```
struct sembuf
{
    unsigned short sem_num;  /* 信号量元素序号（数组下标） */
    short		   sem_op;   /* 操作参数 */
    short		   sem_flg;  /* 操作选项 */
};
```



举例说明，假设有一个信号量组SEM对象，包含两个元素，现在要对第0个元素进程P操作（即减操作），对第1个元素进程V操作（即加操作），则代码如下：

```
int main()
{
     key_t key = ftok(".", 1);

     // 创建（若已有则打开）一个包含2个元素的信号量组
     int id = semget(key, 2, IPC_CREAT|0666);

     // 定义包含两个P/V操作的结构体数组
     struct sembuf op[2];
     op[0].sem_num = 0;  // 信号量元素序号
     op[0].sem_op  = -2; // P操作
     op[0].sem_flg = 0;  // 选项默认0

     op[1].sem_num = 1;  // 信号量元素序号
     op[1].sem_op  = +3; // V操作
     op[1].sem_flg = 0;  // 选项默认0

     // 同时对第0、1号信号量元素分别进行P、V操作
     semop(id, op, 2);
}
```



**注意：**

1. P操作是申请资源，因此如果资源数不够的话会导致进程阻塞，这正是我们想要的效果，因为资源数不可为负数。
2. V操作是释放资源，永远不会阻塞。
3. SEM对象的一大特色就是可以对多个信号量元素同时进行P/V操作，这也是跟POSIX单个信号量的区别。

#### **等零操作**

当操作结构体sembuf中的sem_op为0时，称为等零操作，即阻塞等待直到对应的信号量元素的值为零，示例代码如下：

```
struct sembuf op[1];
op[0].sem_num = 0;
op[0].sem_op  = 0; // 等零操作
op[0].sem_flg = 0;

// 若此时信号量组中的第0个元素的值不为零，则阻塞直到恢复零为止
semop(id, op, 1);
```



#### 3.3 **其余操作**

system-V的IPC对象都有类似的操作接口，SEM对象也有control函数，接口如下：

```
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

int semctl(int semid, int semnum, int cmd, ...);
```



接口说明：

- semid：信号量组的ID
- semnum：信号量组内的元素序号（从0开始）
- cmd：操作命令字：
    - IPC_STAT：获取信号量组的一些信息，放入semid_ds{ }中
    - IPC_SET：将 semid_ds{ } 中指定的信息，设置到信号量组中
    - **IPC_RMID**：删除指定的信号量组。
    - GETALL：获取所有的信号量元素的值。
    - SETALL：设置所有的信号量元素的值。
    - GETVAL：获取第semnum个信号量元素的值。
    - **SETVAL**：设置第semnum个信号量元素的值。

在上述常见控制命令中，以 **IPC_RMID** 和 **SETVAL** 用的最多。

**1. IPC_RMID**
其中，当命令字为IPC_RMID时，意为删除SEM对象，这操作与其他两种IPC对象一样，示例代码如下：

```
// 删除SEM对象
semctl(id, 0/*该参数将被忽略*/, IPC_RMID);
```



**2. SETVAL**
一般而言，SEM对象在刚被创建出来的时候需要进行初始化，该命令字可以执行初始化的操作，示例代码如下：

```C
// 操作联合体
union semun {
     int              val;    /* Value for SETVAL */
     struct semid_ds *buf;    /* Buffer for IPC_STAT, IPC_SET */
     unsigned short  *array;  /* Array for GETALL, SETALL */
     struct seminfo  *__buf;  /* Buffer for IPC_INFO */
};

int main()
{
    // 创建（或打开）SEM对象
    // 注意需要指定 IPC_EXCL 模式，因为要区分是否是新建的SEM对象
    int semid = semget(key, 1, IPC_EXCL|IPC_CREAT|0666);

    // 1，若SEM对象已存在，则重新打开即可
	  if(semid == -1 && errno == EEXIST)
		    semid = semget(key, 1, 0);

    // 2，若SEM对象为当前新建，则需进行初始化
	  else if(semid > 0) {
        union semun a;
        a.val = 1; // 假设将信号量元素初始值定为1

        semctl(semid, 0, SETVAL, a);
    }
}
```



**注意：**

1. semun是一个联合体，各成员对应不同的命令字。
2. 该联合体须由调用者自己定义。

**2. IPC_SET / IPC_STAT**
这两个命令字用来设置、获取SEM对象的相关属性信息，这些信息用如下结构体表达：

```C
struct semid_ds {
     struct ipc_perm sem_perm;  /* 所有者、权限*/
     time_t          sem_otime; /* 最后一次PV操作的时间 */
     time_t          sem_ctime; /* 最后一次IPC_SET的时间 */
     unsigned long   sem_nsems; /* 信号量元素个数 */
};
```



## QA

【1】问：信号量跟信号有什么关系？
【1】答：它们之间没有关系，只是名字相似。信号量有时也被翻译为信号灯。

【2】问：三种IPC对象基本语法都懂了，函数接口也都练习了一遍了，但还是不知道具体在什么场合下用什么对象，这是在钻牛角尖吗？
【2】答：不，你没在钻牛角尖，相反你提的问题很好。具体是这样的，MSG对象可以看做是一种增强型具名管道，它可以对每个数据标注类型，因此可以用在多对一通信的场合，而普通的管道由于对数据不加区分，因此只能用于一对一通信。

同时还应理解到，不管是普通管道还是MSG对象，通信数据都是被发往内核，由内核进行管理，这样一来自然就省却了很多数据管理的烦恼，比如无需担心会数据越界，也无需担心读到重复的数据，但代价是降低了性能，因为数据转手了两次。

SHM对象与此相对，不再由内核管理，而是直接给用户进程自己管理，因此在SHM中存取数据要比其他的IPC对象效率高得多，但也正因如此，SHM一般无法单独使用，因为我们必须使用诸如信号量、互斥锁等机制去协同各个进程或线程。

至于SEM对象，它纯粹就是一种进程线程间的旗语，它不是用来传输数据的，它的作用就是红绿灯，在实际应用项目中，凡是需要协同进程线程、控制它们的执行进度，一般都离不开信号量。

