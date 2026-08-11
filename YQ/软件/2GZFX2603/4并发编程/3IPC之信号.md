# IPC之信号

[toc]



|          | pipe               | signal           |
| -------- | ------------------ | ---------------- |
| 类型     | 数据通信           | 事件通知         |
| 传输内容 | 字节流             | 信号编号         |
| 同步性   | 通常同步           | 异步             |
| 是否阻塞 | read/write可能阻塞 | 不阻塞等待       |
| 数据量   | 大                 | 极少             |
| 典型用途 | 父子进程传数据     | 告诉进程发生事件 |

> [!note] 
>
> pipe解决“进程之间怎么传递信息”，signal解决“进程怎么知道有事情发生”。

## 标准信号处理

程序在被CPU加载的过程中形成的动态过程叫做进程。在这个过程中，我们希望是可控的，也就是可以手动去控制这个进程的各个状态。所以需要制定出一套机制或者命令，比如把停止命令发送给进程时，进程能够接受这个来自外部的“请求命令”，做出相应的停止进程默认动作。这一套机制或者命令叫做信号。

### **1. 信号基本概念**

信号相对其他IPC（IPC的全称是**Inter-Process Communication**，即进程间通信）而言，其最大的特点是所谓的异步性，**异步的含义是事件的发生和处理没有事先协同**，一般情况下，进程什么时候会收到信号、收到什么信号是无法事先预料的（就像你家的门铃，你不知道它什么时候会响，但是门铃响的时候我们可以下楼开门(处理)）

**同步性（synchronous）和异步性（asynchronous）主要描述“通信双方是否需要等待对方”**。

sync:一个动作发生时，调用者需要等待结果，流程被阻塞。

async:发起操作后，不等待结果，继续执行，结果以后通知。

![img](http://edu.yueqian.com.cn/group1/M00/13/CB/wKgP3GIsa2OASYCbAAI6MUBeSGg030.png?token=null&ts=null)

<center>
    信号与门铃
</center>

**2. 标准信号处理**

Linux/Unix系统下，信号总共分成两大类，一类是最常用的标准信号，另一类是后面引入的实时信号，可以使用如下命令查看：

```
# 查看当前系统所支持的所有信号
gec@ubuntu:~$ kill -l
 1) SIGHUP	 2) SIGINT	 3) SIGQUIT	 4) SIGILL	 5) SIGTRAP
 6) SIGABRT	 7) SIGBUS	 8) SIGFPE	 9) SIGKILL	10) SIGUSR1
11) SIGSEGV	12) SIGUSR2	13) SIGPIPE	14) SIGALRM	15) SIGTERM
16) SIGSTKFLT	17) SIGCHLD	18) SIGCONT	19) SIGSTOP	20) SIGTSTP
21) SIGTTIN	22) SIGTTOU	23) SIGURG	24) SIGXCPU	25) SIGXFSZ
26) SIGVTALRM	27) SIGPROF	28) SIGWINCH	29) SIGIO	30) SIGPWR
31) SIGSYS	34) SIGRTMIN	35) SIGRTMIN+1	36) SIGRTMIN+2	37) SIGRTMIN+3
38) SIGRTMIN+4	39) SIGRTMIN+5	40) SIGRTMIN+6	41) SIGRTMIN+7	42) SIGRTMIN+8
43) SIGRTMIN+9	44) SIGRTMIN+10	45) SIGRTMIN+11	46) SIGRTMIN+12	47) SIGRTMIN+13
48) SIGRTMIN+14	49) SIGRTMIN+15	50) SIGRTMAX-14	51) SIGRTMAX-13	52) SIGRTMAX-12
53) SIGRTMAX-11	54) SIGRTMAX-10	55) SIGRTMAX-9	56) SIGRTMAX-8	57) SIGRTMAX-7
58) SIGRTMAX-6	59) SIGRTMAX-5	60) SIGRTMAX-4	61) SIGRTMAX-3	62) SIGRTMAX-2
63) SIGRTMAX-1	64) SIGRTMAX


例如：
19) SIGSTOP
信号值)SIG+信号名字

其实信号的名字与信号值是等价的，它们是宏定义来的，被定义在一个头文件：
/usr/include/asm-generic/signal.h
 
#define SIGHUP		 1
#define SIGINT		 2
#define SIGQUIT		 3
#define SIGILL		 4
```

![image-20260721112331506](./img/image-20260721112331506.png)

![image-20260721112349634](./img/image-20260721112349634.png)

- 标准信号：前31个信号，它们是从Unix系统继承下来的经典系统元素，他们有如下的特点：
    - 不排队，信号的响应会相互嵌套。
    - 如果目标进程没有及时响应，那么随后到达的相同信号将会被丢弃。
    - 每个信号都对应一个系统事件（除了SIGUSR1和SIGUSR2），当这个事件发生时，将产生这个信号。
    - 在进程的挂起信号中，进程会优先响应实时信号。
- 实时信号：后31个信号，它们是Linux系统新增的实时信号，也被称为“可靠信号”，这些信号的特征是：
    - 实时信号的响应次序按接收顺序排队，不嵌套。
    - 即使相同的实时信号被同时发送多次，也不会被丢弃，而会依次挨个响应。
    - 实时信号没有特殊的系统事件与之对应。

下面以标准信号入手，详细了解信号的各种特性。

#### **2.1 信号的生命周期**

所谓信号的生命周期，指的是信号从产生到被响应完毕的整个过程，这个过程可被描述为：

![image-20260720090358444](./img/image-20260720090358444.png)
<center>
    信号的生命周期
</center>

- 信号的产生
    信号既可以由特定的事件产生（比如发生了内存访问异常导致产生信号SIGSEGV），也可由用户主动发起（比如调用了kill()函数），不管是哪种方式产生的信号，其本质都是触发了内核的信号发生器，并向特定进程（即目标进程）递送的过程。
- 信号的挂起
    每个进程都保留有一个挂起信号集，所有被发送到这个进程的信号首先被放入这个信号集，挂起信号集存储了进程的待处理信号，这些信号必须要等到进程被系统调度，真正执行的时候才能被进一步响应。
- 信号的响应
    信号的响应总共有如下四种方式：
    - 屏蔽：也称为阻塞，即延缓对信号的响应，直到解除对该信号的屏蔽为止。
    - 捕捉：执行一个预先设置的与信号相关联的响应函数。
    - 默认：按信号默认的情况处理。
    - 忽略：直接丢弃该信号。

设置阻塞之后，来了阻塞的指定信号，并不是将信号丢弃，而是将信号挂起，等到解除阻塞之后才去响应这个信号。比如说你（进程）正在接待客户，此时朋友（信号1）过来找你，正确的做法是让朋友（信号1）在接待厅进行等待，而不是让其滚出去（丢弃）。如果此时陆续有多个朋友（多个信号）到来，那么需要将多个信号设置成阻塞状态。如何将多个信号设置成阻塞状态，也就是如何管理多个信号呢，需要用到信号集操作。

 

注意：9) SIGKILL	和    19) SIGSTOP   这两个信号不能被忽略，阻塞、捕捉。必须是执行默认动作

##### **信号集**

1、什么是信号集？

信号集是一个集合，而每一个成员都是一个信号，通过将信号加入到信号集中，再设置阻塞状态给信号集，那么整个信号集里面所有的信号都会变成阻塞的状态。

2、信号阻塞与信号忽略有什么区别？

信号响应： 收到信号之后，会响应信号的动作。

信号忽略： 收到信号之后，直接丢弃这个信号。

信号阻塞： 进程在阻塞某一个信号前提下，收到了这个信号，不会马上响应，而是要等到解除阻塞之后，才会响应这个信号。

（这个信号没有被响应时，不会丢弃，而是放在一个挂起队列中）



**信号集处理函数**

1、 信号集如何定义？

信号集其实就是一个变量，数据类型是： sigset_t。

定义信号集： sigset_t set

```C
#include <signal.h>
 
int sigemptyset(sigset_t *set);   清空信号集
int sigfillset(sigset_t *set); 将linux下所有的信号都加入到信号集中
int sigaddset(sigset_t *set, int signum); 在指定的信号集set中，添加一个指定的信号signum
int sigdelset(sigset_t *set, int signum);在指定的信号集set中，删除一个指定的信号signum
int sigismember(const sigset_t *set, int signum); 测试某一个信号是不是在集合中
```

参数：

set：需要判断的信号集的地址

signum： 需要测试的信号

返回值：

成功：0

失败：-1

sigismember 函数 在集合中返回 1  不在集合中返回 0  失败返回 -1

 

2、例题1： 写一个程序，先清空信号集，再把SIGUSR1加入到集合中，判断信号是不是在集合中。

```C
int main(int argc, char*argv[]) // ./a.out 3445
{
    //1）先定义一个信号集变量 
    sigset_t  set;
    //2) 初始化（清空）
    sigemptyset(&set); //清空信号集
    //3）将信号 添加到集合中 SIGUSR1  SIGUSR2
    sigaddset(&set,SIGUSR1); //在指定的信号集set中，添加一个指定的信号signum到集合中
    sigaddset(&set,SIGUSR2); 
    
    //4) 判断 SIGUSR2信号是否在集合中，如果在打印yes  ，否则 打印 no
    // sigismember 信号在集合中 返回1  否则 返回 0
    if(sigismember(&set, SIGUSR2))
        printf("yes\n");
    else 
        printf("no\n");
    
    return 0;
}
```

 

**4.如何设置信号集为阻塞状态？  -> sigprocmask()  -> man 2 sigprocmask**



```
#include <signal.h>
int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);
```

参数：

how：

SIG_BLOCK   -> 设置为阻塞的属性

SIG_UNBLOCK -> 解除阻塞	

set： 你要设置哪个信号集，将这个信号集的地址传递过来

oldset：保留之前状态的指针，如果不关心，则填NULL。

返回值：

成功：0

失败：-1

例如：

```
sigset set;
信号  -> set
sigprocmask(SIG_BLOCK,&set,NULL);  -> 设置为阻塞
...
sigprocmask(SIG_UNBLOCK,&set,NULL);  -> 解除阻塞
```

 

```C
#include<stdio.h>
#include <sys/types.h>
#include <signal.h>
 
void signalHandle(int arg)
{
    printf("%d signalHandle\n",arg);
}
 
int main(int argc, char*argv[]) // ./a.out 3445
{
    //将SIGUSR1信号   设置 一个信号响应函数 
    signal(SIGUSR1, signalHandle);
    
    
    //1）先定义一个信号集变量 
    sigset_t  set;
    //2) 初始化（清空）
    sigemptyset(&set); //清空信号集
    //3）将信号 添加到集合中 SIGUSR1  
    sigaddset(&set,SIGUSR1); //在指定的信号集set中，添加一个指定的信号signum到集合中
    
    //4) 判断 SIGUSR1信号是否在集合中，如果在打印yes  ，否则 打印 no
    // sigismember 信号在集合中 返回1  否则 返回 0
    if(sigismember(&set, SIGUSR1))
        printf("yes\n");
    else 
        printf("no\n");
    
    //将信号集中的所有的信号设置为 阻塞状态 
    //注意：设置的对象是信号，而不是进程，所以调用这个函数之后，程序还是会往下面走
    sigprocmask(SIG_BLOCK,&set,NULL);
    
    sleep(20);//延时20S 
    
    //再解除阻塞，也就是说，上面的20S之内，如果收到了信号SIGUSR1，那么进程会将这个信号挂起来，等到解除阻塞之后再执行信号响应函数
    sigprocmask(SIG_UNBLOCK,&set,NULL);
    
    return 0;
}
```



#### **2.2 信号的产生**

除了由特定事件触发的信号外，信号的产生均可由用户调用如下接口来主动触发：

```
#include <sys/types.h>
#include <signal.h>

int kill(pid_t pid, int sig);
```



其中：

- pid是接收信号的进程PID，称为目标进程。
- sig是信号的编号。

比如，下面的代码实现向指定PID的进程发送2号信号SIGINT（该信号就是平时按ctrl+c产生的键盘中断信号：

```C
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int main(int argc, char **argv)
{
    if(argc == 2)
    	kill(atoi(argv[1]), SIGSEGV);
    
    return 0;
}
```



**注意：**
由于函数接口kill的两个参数都是整型数据，因此如果不小心写错了它们的顺序，编译器是无法区分的，这个细节在写代码的时候要分外注意。

当然，有时候我们会在终端中直接使用kill命令来发送信号：

```C
# 向PID号为1234的进程发送2号信号：
gec@ubuntu:~$ kill -2 1234

# 向PID号为1234的进程发送信号SIGKILL：
gec@ubuntu:~$ kill -s SIGKILL 1234

# 向名称为example的所有进程发送信号SIGTERM：
gec@ubuntu:~$ killall example 
```



#### **2.3 信号的响应方式**

如前所述，信号的响应有四种方式，下面来详细分析。

##### **2.3.1 信号的屏蔽**

屏蔽信号实际上就是暂缓对信号的响应，采用如下函数进行对信号的屏蔽：

```
#include <signal.h>
int sigprocmask(int how, const sigset_t *set, sigset_t *oldset);
```



参数简析：

- how：操作命令字，比如阻塞、解除阻塞等
- set：当前要操作的信号集
- oldset：若为非空，则将原有阻塞信号集保留到该oldset中

注意到，该函数的操作参数不是单个信号，而是信号集（sigset_t），这意味着我们可以同时对多个信号设置阻塞或解除阻塞。

```C
// 信号集操作函数组
#include <signal.h>
int sigemptyset(sigset_t *set);   // 清空信号集set
int sigfillset(sigset_t *set);    // 将所有信号加入信号集set中
int sigaddset(sigset_t *set, int signum);         // 将信号signum添加到信号集set中
int sigdelset(sigset_t *set, int signum);         // 将信号signum从信号集set中剔除
int sigismember(const sigset_t *set, int signum); // 测试信号signum是否在信号集set中
```



另外，how是具体的操作命令字，可以有如下取值：

- SIG_BLOCK：阻塞set中的信号（原有正在阻塞的信号保持阻塞）。
- SIG_SETMASK：阻塞set中的信号（原有正在阻塞的信号自动解除）。
- SIG_UNBLOCK：解除set中的信号。

例如，想要对1、2号信号进行阻塞操作，首先要将这两个信号添加到一个信号集中，操作接口如下：

```C
// 将1、2号信号加入信号集
sigset_t sig;
sigemptyset(&sig);
sigaddset(&sig, SIGHUP); // 加入1号信号
sigaddset(&sig, SIGINT); // 加入2号信号

// 阻塞1、2号信号
setprocmask(SIG_SETMASK, &sig, NULL);
```



##### **2.3.2 信号的捕捉**

所谓信号的捕捉，实际就是在信号到达之前，给信号关联一个指定的响应函数，让其到达之后自动运行该函数。

给信号指定关联函数的接口是：

```
#include <signal.h>
void (*signal(int sig, void (*func)(int)))(int);
```



该函数接口比较复杂，下面是其返回值和参数详解：

- 返回值类型：void (*)(int);
- 返回值含义：返回一个指向原有的与指定信号关联的函数
- 参数：
    - sig: 指定要关联的信号
    - func：指定要关联的响应函数

注意到，使用这种方式关联的响应函数的接口是固定的，如下所示：

```
// 标准信号响应函数接口
void func(int sig)
{
    // ...
}
```



显然，func中的参数sig就是触发该响应函数的信号，以下示例代码展示了如何捕捉信号SIGINT：

```C
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

void func(int sig) {
    printf("捕获到信号:%d\n", sig);
}

int main(int argc, char **argv) {
    // 指定信号SIGINT关联函数
    signal(SIGINT, func);

    // 持续响应信号
    while(1)
        pause();

    return 0;
}
```



> 提示：
>
> 1. 函数pause会在信号响应结束后退出，为了让程序可以持续响应信号，上述程序将pause函数放在while循环中。
> 2. 由于上述代码捕捉了SIGINT，因此按ctrl+c将无法中断程序，此时可以按ctrl+\（触发另一个信号SIGQUIT）来退出程序的无限循环。

##### **2.3.3 信号的默认处理**

如果程序没有对信号做任何预先准备，那么当信号达到时，则会按照信号的默认规则进行响应，具体默认规则可使用如下命令查阅：

```bash
gec@ubuntu:~$ man 7 signal

# 会得到类似如下的表格：
       ...
       Signal     Value     Action   Comment
       ──────────────────────────────────────────────────────────────────────
       SIGHUP        1       Term    Hangup detected on controlling terminal
                                     or death of controlling process
       SIGINT        2       Term    Interrupt from keyboard
       SIGQUIT       3       Core    Quit from keyboard
       SIGILL        4       Core    Illegal Instruction
       SIGABRT       6       Core    Abort signal from abort(3)
       SIGFPE        8       Core    Floating-point exception
       SIGKILL       9       Term    Kill signal
       SIGSEGV      11       Core    Invalid memory reference
       SIGPIPE      13       Term    Broken pipe: write to pipe with no
                                     readers; see pipe(7)
       ...
```



列表中的 Action 一列就是系统对信号的默认处理规则，m默认规则如下：

- Term：中断目标进程。
- Core：中断目标进程，且产生核心转储文件core。
- Stop：暂停目标进程，直到收到信号SIGCONT
- Cont：恢复目标进程运行
- Ign：忽略信号

其中需要说明的是：

1. Term和Core都是中断程序，但Core处理方式还会产生转储文件core，core文件即程序在被中断的瞬间其内存映像的快照，用来给后续的调试提供追踪信息。但一般情况下系统是禁止生成所谓转储文件的，放开此项限制的命令是：

```C
# 查看当前系统对 core 文件的限制
gec@ubuntu:~$ ulimit -a
core file size          (blocks, -c) 0  # core 文件大小被限制为0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 0
file size               (blocks, -f) unlimited
pending signals                 (-i) 7635
max locked memory       (kbytes, -l) 16384
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) 7635
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
gec@ubuntu:~$ 

# 将 core 文件的大小设置为“不限制”
gec@ubuntu:~$ ulimit -c unlimited
```



1. Ign是默认就会被忽略的信号，典型的例子是SIGCHLD，此信号是子进程在状态转变时（比如变成僵尸时）自动发给其父进程的信号。
2. SIGKILL和SIGSTOP这两个信号只能采取默认处理，不能阻塞、捕捉，也不能忽略。

##### **2.3.4 忽略信号**

忽略信号就是直接将收到的信号丢弃，做法如下：

```C
int main() {
    // 忽略信号SIGINT
    signal(SIGINT, SIG_IGN);
}
```



## 扩展信号处理

### **1. 问题起源**

仔细观察标准信号的处理过程容易发现，其信号的发送和接收是无法传递额外信息的，即发送者除了可以将信号发送给接收者之外，无法传递其他信息，对于接收者而言，收到某个信号的时候也无法很方便地得知发送进程是哪个，更无法得知控制发送者用户的信息。

#### **1.1 标准信号处理与扩展信号处理**

上一节中的信号发送接口和信号响应函数接口是kill和signal，实际上除了这一对函数对应关系之外，还有扩展的配套函数：

![image-20260720090237748](./img/image-20260720090237748.png)

#### **1.2 标准信号处理**

也就是说，这四个函数的两两配对的。当使用kill发送信号时，由于不会携带任何额外的信息，因此对方只需使用signal来处理相应的信号即可，使用signal关联的响应函数称为标准响应函数，它们的协作示例代码如下所示：

```C
// 信号发送者程序sender.c
int main()
{
    kill(PID, SIGINT);
}
```



```C
// 信号接收者程序receiver.c
void func(int sig) {
    // sig 是触发本函数的信号值
}
int main() {
    signal(SIGINT, func);
    pause();
}
```



#### **1.3 扩展信号处理**

倘若要在发送信号的同时携带别的信息，那么就得用另一套相应的函数：

```C
// 信号发送者程序sender2.c
int main() {
    union sigval val;
    val.sival_int = 100;

    // 发送一个携带额外信息的信号
    sigqueue(PID, SIGINT, val);
}
```



```C
// 信号接收者程序receiver2.c
void func(int sig, siginfo_t *info, void *arg) {
    // sig 是触发本函数的信号值
}
int main()
{
    struct sigaction act;
    bzero(&act);

    // 指定函数响应函数
    act.sa_sigaction = func;
    act.sa_flags |= SA_SIGINFO;

    sigaction(SIGINT, &act, NULL);
    pause();
}
```



### **2. 函数接口**

#### **2.1 sigqueue函数接口**

该函数的功能与kill一样，都是向指定进程发送信号，但sigqueue在发送信号的同时会携带很多额外信息，其接口如下：

```C
#include <signal.h>
int sigqueue(pid_t pid, int sig, const union sigval value);
```



该函数的前两个参数与kill完全一样，不再赘述。第三个参数是一个联合体：

```C
union sigval {
    int   sival_int;
    void *sival_ptr;
};
```

由此联合体可见，系统允许发送者发送一个自定义的整型数据或者一个指针，当然，如果接受者与发送者不在同一个进程内，那么发送地址是无效的，只有当一个进程内部的线程间发送信号时，发送的地址才有效。

#### **2.2 sigaction函数接口**

该函数的功能与signal一样，都可以为指定信号关联其响应函数，但sigaction除了可以指定标准响应函数外，还可以指定扩展响应函数，以便接受从sigqueue发来的携带额外参数的信号：

```C
#include <signal.h>
int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);
```

上述函数接口中，第2、3个参数都是如下结构体（该结构体名称恰好与函数名称一样）：

```C
struct sigaction
{
    void     (*sa_handler)(int);
    void     (*sa_sigaction)(int, siginfo_t *, void *);
    sigset_t   sa_mask;
    int        sa_flags;
    void     (*sa_restorer)(void);
};
```

- sa_handler：标准响应函数指针
- sa_sigaction：扩展响应函数指针
- sa_mask：临时信号阻塞掩码
- sa_flags：配置标签
- sa_restorer：已废弃

关注点：

1. sa_handler和sa_sigaction一个指向标准函数，一个指向扩展函数，二者只能取其一。
2. sa_mask是一个信号集，里面所包含的信号将在本函数所关联的响应函数执行期间被临时阻塞。
3. sa_flags可以用来配置选择标准响应模式、扩展响应模式，具体而言，可通过如下设置来使能扩展模式：

```
sa_flags |= SA_SIGINFO;
```

4. sa_restorer是一个已废弃的接口，无需关注。



## QA

【1】问：一个进程收到信号时，是会跳转到signal语句地方去执行吗？
【1】答：不，不会。这是很多同学的误解，比如下面这段简单的代码：

```C
void func(int sig) {
    printf("收到信号%d\n", sig);
}

int main()
{
    signal(SIGINT, func);
    for(int i=0;;i++) {
        printf("%d\n", i);
        sleep(1);
    }
}
```



很多人没有认真理解signal函数的作用，把它错当做“接收信号”的函数，以为程序会在for循环中收到信号时往上跳到signal去执行相关响应函数，这个想法是错误的，signal函数只是对信号和函数func做了关联，做完之后就没他什么事了，程序也不可能会跳回到第8行。

程序之所以会在收到信号时跳转到函数func处，是因为内核对进程的执行流程做了中断处理，函数func是典型的回调函数，是由内核主动调用的。