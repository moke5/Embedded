#

[toc]

# 通用性分析

到目前为止，我们的顺序表或者链表都以存放整型数据为例，但在实际工作应用中，处理的对象不一定是一个整数，而是任意的数据类型。这要求我们对顺序表和链表的设计要做一个更加深入的理解。

### **1. 容器**

首先要理解，所有的数据结构本质上是一种容器，包括已经学习了的顺序表、链表，以及后续将会学习的栈、队列、二叉树等等。所谓容器，指的是只关心其内部数据之间的逻辑关系，并提供与这种逻辑关系相对应的操作的集合。容器不关心数据本身的类型，因为对于容器而言，不管是存储一个整数，还是存储一个进程，还是一个学生、一本图书，它们都被称为一个数据节点。

![img](http://edu.yueqian.com.cn/group1/M00/03/8B/wKgP3GCJD32Aau4rAAUU9J2WIh0655.png?token=null&ts=null)

### **2. 通用性**

容器提供的是数据处理的通用解决方案，即：提供一套可以处理任意数据类型的通用API，不管是什么数据，都可以统一处理。比如链表，不管处理什么数据，对它们的操作都是统一的：初始化、插入、删除、遍历、销毁等等。

目前，有两种常见的方式来获得通用性：

- 创建容器时，让用户提供数据的类型。典型应用案例是STL（一个C++的类库）
- 将数据从容器中剥离出去，让容器只提供逻辑。典型应用案例是Linux内核链表

由于C语言没有类，也不支持重载，受语言本身特性的限制，一般不使用第一种办法来设计通用容器，但在一些小型程序中，C语言也是可以实现通用性的，关键在于：让用户提供数据的类型。而容器本身只处理跟数据逻辑结构相关的操作，凡是涉及具体数据的操作，一律要让用户来提供。

下面以双向链表为例，使用上述第一种方法，将其改造成通用的容器。

### **3. 节点的设计**

```
// list.h

#ifndef DATATYPE
#define DATATYPE int
#endif

typedef DATATYPE datatype;

// 此处的节点是通用的
// 原理是将具体数据的类型让渡给用户自己去定义
typedef struct node
{
    datatype data;

    struct node *prev;
    struct node *next;
}listnode, *linklist;
```







以上代码有几处需要着重解释：

- 上述代码必须写在 *.h 头文件中，而不是 *.c 源文件
- 用户使用该容器的时候，定义 DATATYPE 为其所需要的数据类型

许多人比较困惑的地方在于，既然用户需要提供数据，那为什么不直接让用户定义datatype，而要去定义宏 DATATYPE 呢？原因是 typedef 无法跟宏一样，给用户提供一个默认的数据类型。

接下来，对于跟用户数据无关的操作，无需任何修改，直接就是通用的，比如初始化、判断是否为空：

```
// 注意以下内容必须放在头文件 list.h 中

// 初始化空链表，与用户实际数据无关
static node * initList()
{
    node * head = (node *)malloc(sizeof(node));

    if(head != 0)
    {
        head->prev = head;
        head->next = head;
    }

    return head;
}

// 判断链表是否为空，与用户实际数据无关
static bool isEmpty(node *head)
{
    return head->next == head;
}
```







**注意1：**
通用型算法一律都只能写到头文件 list.h 中，因为编译的时候 datatype 必须结合用户提供的 *.c 源文件才能确定切确的类型，如果单独编辑 list.c，那么在编译产生 list.o 的过程中就无法使用用户所指定的类型。

**注意2：**
通用型算法代码 list.h 的使用方法，就是直接作为头文件放在用户程序中即可，如果用户需要使用链表容器处理其特定的数据，那么就在包含头文件前自定义宏 DATATYPE，如：

```
#define DATATYPE xxx // xxx为用户自定义的任意数据类型
#include "list.h"
```







**注意3：**
为防止头文件被多个C文件包含而造成函数冲突，头文件中的所有函数必须被定义为静态存储类型。

### **4. 增删操作**

由于增删操作都涉及用户具体的数据，因此需要对之前的操作作出修改。以增删链表首部第一个节点为例，参考代码如下：

```
// 根据用户提供的数据，产生一个新节点
static linklist __newNode(datatype *newData)
{
    linklist new = malloc(sizeof(listnode));
    if(new != NULL)
    {
        new->data = *newData;
        new->prev = new;
        new->next = new;
    }

    return new;
}

// 将新节点new插入到链表的首部
void listAdd(linklist head, datatype *newdata)
{
    linklist new = __newNode(newdata);

    new->prev = head;
    new->next = head->next;

    head->next->prev = new;
    head->next = new;
}

// 将新节点new插入到链表的尾部
void listAddTail(linklist head, datatype *newdata)
{
    linklist new = __newNode(newdata);

    new->prev = head->prev;
    new->next = head;

    head->prev->next = new;
    head->prev = new;
}

// 将指定节点从链表中剔除出去
bool listDel(linklist p)
{
    if(p==NULL || isEmpty(p))
        return false;

    // 将原链表首节点剔除出链表
    p->prev->next = p->next;
    p->next->prev = p->prev;
    p->prev = p;
    p->next = p;

    return true;
}
```







> 提醒：
> 不对外的函数接口，一般使用下划线开头，比如 __newNode()

### **5. 查找节点**

在链表中查找某个节点也是一种常规操作，但查找操作与上述的增删操作有个很大的不同，节点的比对是跟节点本身数据密切相关的，比如整型数据可以直接使用等号来判断是否一致，而字符串则需要通过特定的函数才能判断，至于结构体，则无法使用任何现成的方式去判定，只能由用户根据其实际数据去判定。

因此，查找节点时，节点的判定接口必须由用户提供，链表只提供回调接口。具体代码如下：

```
// 查找指定的节点，并使用用户提供的钩子函数 equal 来判定节点是否相同
linklist find(linklist head, datatype data,
                bool (*equal)(datatype, datatype))
{
    for(linklist tmp=head->next; tmp!=head; tmp=tmp->next)
    {
        if(equal(tmp->data, data))
            return tmp;
    }
    return NULL;
}
```



### **6. 遍历链表**

与上述查找算法类似，容器只应提供跟通用性相关的操作，任何涉及用户数据的操作都是不能写的，否则就是去了通用性。之前对链表的遍历，就是将节点中的数据打印出来，这是一种特定的针对整型数据的操作，是不具备通用性的。

> 注意：
> 在实际应用中，遍历链表时对每个节点的访问操作不一定是将节点内部数据打印出来。
> 对节点的访问方式，应该交给用户去处理，只有用户才知道怎么处理。
> 容器本身必须且只能提供“挨个访问”每个节点的路径操作，而不能涉及任何数据本身。

对节点的操作，需将用户提供的特定操作函数 handle 以参数的方式传入给遍历函数，比如：

```
// 遍历链表，并使用用户提供的钩子函数 handle 处理节点
void listForEach(linklist head, void (*handle)(datatype *))
{
    if(isEmpty(head))
        return;

    for(linklist tmp=head->next; tmp!=head; tmp=tmp->next)
        handle(&tmp->data);
}
```



# 内核链表

## 1. 普通链表弊端

普通链表概念简单，操作方便，但存在有致命的缺陷，即：每一条链表都是特殊的，不具有通用性。因为对每一种不同的数据，所构建出来的链表都是跟这些数据相关的，所有的操作函数也都是数据密切相关的，换一种数据节点，则所有的操作函数都需要一一重写编写，这种缺陷对于一个具有成千上万种数据节点的工程来说是灾难性的。

### **1.1 问题分析**

比如下面的操作函数，函数只能操作指定的参数类型：

```
// 普通链表的插入函数，与数据节点node密切相关
// 换一种数据节点，该函数就无法使用了
void insert(node *head, node *new)
{
    // ...
}

// 普通链表的删除函数，与数据节点node密切相关
// 换一种数据节点，该函数就无法使用了
node * remove(node *head)
{
    // ...
}
```

![image-20260719150420999](./img/image-20260719150420999.png)
<center>
    形态各异的普通链表
</center>

在普通链表的节点设计中，不同的链表所使用的指针不同，就直接导致操作函数的参数不同，在C语言的环境下，无法统一这些所有的操作，这给编程开发带来了很大的麻烦，尤其在节点种类众多的场合。

### **1.2 原因分析**

分析上述问题，其产生的根本原因是链表节点的设计，没有把数据和逻辑分开，也就是将具体的数据与组织这些数据的链表揉在一起，导致链表的操作不得已绑定了某个固定类型的数据。

![image-20260719150452339](./img/image-20260719150452339.png)

<center>
    节点中的数据和逻辑
</center>



### **1.3 解决思路**

既然是因为数据和链表指针混在一起导致了通用性问题，那么解决的思路就是将它们分开。将链表逻辑单独抽出来，去掉节点内的具体数据，让节点只包含双向指针。这样的节点连接起来形成一条单纯的链表如下所示：

![image-20260719150543118](./img/image-20260719150543118.png)

接着，将这样的不含任何数据的链表，镶嵌在具体要用串起来的数据节点之中，这样一来，就可以将任何节点的链表操作完全统一了。

![image-20260719150554901](./img/image-20260719150554901.png)

<center>
    镶嵌了标准链表的用户节点
</center>



如上图所示，不管用户节点是什么类型的节点，也不管它里面包含什么数据，都跟链表本身没有关系。如下图所示，在 A 和 C 中插入 B 节点，和在 X 与 Z 中插入 Y 节点，完全可以用相同的函数来达到。此时，就已经成功地将数据与组织这些数据的逻辑分开了。这就是内核链表的基本思路。

![image-20260719150638807](./img/image-20260719150638807.png)

## 2. 内核链表

如前所述，内核链表解决通用性问题，大概分两步：

1. 设计标准节点
2. 针对标准节点，设计由标准节点构成的标准链表的所有操作

> 内核链表的标准节点及其所有操作，都被封装在内核源码中，具体来讲都被封装在一个名为 list.h 的文件中，该文件在内核中的位置是：
> kernel/linux/include/list.h

内核中的源码文件 list.h 实际上包含了两部分内容，一是内核链表，二是哈希链表。经过整理的、仅包含内核链表的文件：[kernel_list.h](http://vm.yueqian.com.cn:8886/group1/M00/05/6B/wKgP3GDUAySAFqdUAAAezxKdazg65527.h?token=null&ts=null&filename=kernel_list.h)

### **2.1 节点设计**

标准节点就是不包含任何数据的双向链表节点，如下所示：

```
// list.h

struct list_head
{
	struct list_head *next, *prev;
};
```







这个标准节点的用法，就是在实际用户数据节点中，镶嵌进去。为了表述简单，一般将用户的数据节点称为大结构体，将标准节点称为小结构体，例如：

```
struct node // 大结构体
{
    // 用户数据
    datatype data;
    ...

    // 标准链表
    struct list_head list; // 小结构体
};
```







### **2.2 初始化**

内核链表对节点的初始化与普通的双向链表节点无异，就是简单地让节点的前后向指针指向自身，其代码如下：

```
#define INIT_LIST_HEAD(ptr) do { \
	(ptr)->next = (ptr); (ptr)->prev = (ptr); \
} while (0
```

![image-20260719150654698](./img/image-20260719150654698.png)

<center>
    初始化了的标准节点
</center>





实际应用中，采用标准节点的内核链表都是带头结点的，其初始化代码如下所示：

```
struct node * initList()
{
    struct node * head = malloc(sizeof(struct node));
    if(head != NULL)
    {
        INIT_LIST_HEAD(&head->list);
    }
    return head;
}
```







### **2.3 大小结构体转换**

由于内核链表的所有操作都只针对标准的小结构体，与包裹它的大结构体没有关系，但是用户关心的是实际数据所在的大结构体，因此一个最基本的问题是：如何快速方便地转换大小结构体指针。

要搞清楚这个问题，首先必须清楚用户节点的细节。假设用户节点的类型为 type，小结构体在用户节点中的名称为 member，指向小结构体的指针为 ptr，现在要通过 ptr 求得指向用户节点的指针 p，它们的关系如下图所示：

![image-20260719150723936](./img/image-20260719150723936.png)

<center>
    内核链表的节点细节
</center>



由于用户数据都存储于大结构体中，因此只要求得指针 p 即可获取所有的用户数据。从图中很容易看到：

```
p = ptr - offset
```







ptr是已知的，关键是 offset，而这个偏移量就是：

```
&((type *)0)->member
```







唯一需要解释的中间的数值0，这个0代表：如果以0地址为起始，那么小结构体member的地址值就是它在大结构体中相对于大结构体起始地址的偏移量。

由于C语言特殊的语法，当我们对结构体中某个成员取地址时，那么程序并不需要操作内存中的任何数据，而只会根据大小结构体的相对位置，纯粹计算地址的值。因此，虽然宏中出现了0，但并不涉及任何内存数据的存取。

实际上，将这个内存地址0换成任意地址x都是可以的，只不过得到的就是相对于地址x的偏移量了，然后又要减掉x以求的小结构体在大结构体中的偏移量，这个操作无疑是多余的。

于是，用户节点指针等于：

```
p = ptr - &((type *)0)->member
```







最后，由于以上算式都是指针，为了让计算结果是字节，将所有的运算操作数强制类型转化为单字节运算的整数或者char型指针即可，其内核源码是：

```
#define list_entry(ptr, type, member) \
((type *)((char *)(ptr)-(unsigned long)(&((type *)0)->member)))
```







通过上面的宏，我们可以直接从标准链表中获取用户大结构体指针，从而访问用户数据：

### **2.4 插入节点**

内核练表的标准操作中，提供了头插法和尾插法，内核源码代码如下：

```
// 内部函数
// 将节点new插入到prev与next之间
// 注意，所有的指针都是标准节点指针，与用户数据无关
static inline void __list_add(struct list_head *new,
				struct list_head *prev,
				struct list_head *next)
{
	next->prev = new;
	new->next = next;
	new->prev = prev;
	prev->next = new;
}

// 将新节点new插入到链表head的首部
// 即:插入到head的后面
static inline void list_add(struct list_head *new, struct list_head *head)
{
	__list_add(new, head, head->next);
}

// 将新节点new插入到链表head的尾部
// 即:插入到head的前面
static inline void list_add_tail(struct list_head *new, struct list_head *head)
{
	__list_add(new, head->prev, head);
}
```







在实际应用中，用户针对大结构体中的标准节点去操作，比如：

```
// 用户节点（大结构体）
node *new = malloc(sizeof(node));

// 将该节点插入已有链表的首部或尾部
list_add(&new->list, &head->list);
list_add_tail(&new->list, &head->list);
```







### **2.5 遍历链表**

内核练表提供了向前、向后遍历链表的标准算法，源码如下：

```
// 向后遍历链表每一个节点
// 注意：
// 遍历过程不可删除节点
#define list_for_each(pos, head) \
for (pos = (head)->next; pos != (head); \
pos = pos->next)


// 安全版：
// 向后遍历链表的每一个节点
// 支持边遍历，边删除节点
#define list_for_each_safe(pos, n, head) \
for (pos = (head)->next, n = pos->next; pos != (head); \
pos = n, n = pos->next)


// 向后遍历链表的每一个节点并直接获得用户节点指针
// 注意：
// 遍历过程不可删除节点
#define list_for_each_entry(pos, head, member)                \
for (pos = list_entry((head)->next, typeof(*pos), member);    \
&pos->member != (head);                     \
pos = list_entry(pos->member.next, typeof(*pos), member))


// 安全版：
// 向后遍历链表的每一个节点并直接获得用户节点指针
// 支持边遍历，边删除节点
#define list_for_each_entry_safe(pos, n, head, member)            \
for (pos = list_entry((head)->next, typeof(*pos), member),    \
n = list_entry(pos->member.next, typeof(*pos), member);    \
&pos->member != (head);                     \
pos = n, n = list_entry(n->member.next, typeof(*n), member))


// 向前遍历链表的每一个节点
// 注意：
// 遍历过程不可删除节点
#define list_for_each_prev(pos, head) \
for (pos = (head)->prev; pos != (head); \
pos = pos->prev)
```



### **2.6 剔除节点**

与普通链表一致，剔除内核链表节点只是意味着将某指定节点脱离链表，并不意味着释放其内存。剔除节点的内核源码是：

```
// 内部函数
static inline void __list_del(struct list_head *prev, struct list_head *next)
{
	next->prev = prev;
	prev->next = next;
}

// 将指定节点 entry 从链表结构中剔除
// 并将其前后指针置空
static inline void list_del(struct list_head *entry)
{
	__list_del(entry->prev, entry->next);
	entry->next = (void *) 0;
	entry->prev = (void *) 0;
}

// 将指定节点 entry 从链表结构中剔除
// 并将其前后指针指向自身
static inline void list_del_init(struct list_head *entry)
{
	__list_del(entry->prev, entry->next);
	INIT_LIST_HEAD(entry);
}
```







比如，要将一条内核练表全部节点释放掉，参考代码如下：

```
// 初始化一条空链表
struct node *head = init();

// 插入若干用户节点
// ...

// 销毁链表，释放所有的节点
struct list_head *pos;
struct list_head *n;
list_for_each_safe(pos, n, &head->list)
{
    // 将当前节点剔除出链表
    list_del(pos);

    // 释放当前节点
    struct node *p = list_entry(pos, node, list);
    free(p);
}
```







### **2.7 移动节点**

移动节点的操作，实际上是先将节点剔除出链表，然后再插入某指定位置，内核源码如下：

```
// 将节点list，移动到指定位置head的后面
static inline void list_move(struct list_head *list,
                             struct list_head *head)
{
	__list_del(list->prev, list->next);
	list_add(list, head);
}

// 将节点list，移动到指定位置head的前面
static inline void list_move_tail(struct list_head *list,
                                  struct list_head *head)
{
	__list_del(list->prev, list->next);
	list_add_tail(list, head);
}
```





## QA

【1】问：通用性是什么意思？
【1】答：就是将链表理解为一个容器，这个容器提供诸如插入、删除、遍历等算法，如果这个容器可以存储任意类型的数据，那么就说这个链表是具有通用性的。

【2】问：大结构体和小结构体是什么？
【2】答：由于内核链表实现的机理，是将一个标准的无数据的节点镶嵌到一个用户数据节点中，因此形象地将标准节点称为小结构体，将用户节点称为大结构体。

【3】问：怎么理解 list_entry() ?
【3】答：宏`list_entry()`的源码如下：

```
/**
* list_entry – get the struct for this entry
* @ptr:    the &struct list_head pointer.
* @type:    the type of the struct this is embedded in.
* @member:    the name of the list_struct within the struct.
*/
#define list_entry(ptr, type, member) \
((type *)((char *)(ptr)-(unsigned long)(&((type *)0)->member)))
```







宏 `list_entry()` 的功能是在已知一个指向小结构体指针ptr的前提下，求得包裹这个小结构体的大结构体的指针，其基本的思路就是将ptr减去小结构体在大结构体中的偏移量。而这个偏移量就是：

```
&((type *)0)->member
```







唯一需要解释的中间的数值0，这个0代表：如果以0地址为起始，那么小结构体member的地址值就是它在大结构体中相对于大结构体起始地址的偏移量。

另外，由于C语言特殊的语法，当我们对结构体中某个成员取地址时，那么程序并不需要操作内存中的任何数据，而只会根据大小结构体的相对位置，纯粹计算地址的值。因此，虽然宏中出现了0，但并不涉及任何内存数据的存取。

实际上，将这个内存地址0换成任意地址x都是可以的，只不过得到的就是相对于地址x的偏移量了，然后又要减掉x以求的小结构体在大结构体中的偏移量，这个操作无疑是多余的。

