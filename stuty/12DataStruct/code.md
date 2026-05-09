# 随笔

[toc]



### 单链表



#### 创建

```c
typedef struct node
{
    int data;
    struct node *next;
} Node;

Node *Init_list_node()
{
    Node *head = (Node *)malloc(sizeof(Node));
    if (head == NULL)
    {
        fprintf(stdout, "malloc failed : %s\n", strerror(errno));
        return NULL;
    }

    head->data = -1;
    head->next = NULL;
    return head;
}

Node *add_node(int data)
{
    Node *this = (Node *)malloc(sizeof(Node));
    if (this == NULL)
    {
        perror("add node malloc failed");
        return NULL;
    }

    this->data = data;
    this->next = NULL;
    return this;
}
```





#### 头插

```c
int add_head(Node *head, int data)
{
    if (head == NULL)
    {
        perror("add head faile");
        return -1;
    }

    Node *p = add_node(data);
    if (p == NULL)
    {
        perror("add node failed");
        return -1;
    }

    p->next = head->next;
    head->next = p;
    return 1;
}
```



#### 遍历

```c
void for_earch(const Node *head)
{
    if (head == NULL)
    {
        fprintf(stdout, "for earch head is NULL\n");
        return;
    }
    if (head->next == NULL)
    {
        fprintf(stdout, "list is NULL!\n");
        return;
    }

    Node *p = head->next;
    while (p != NULL)
    {
        printf("%d ", p->data);
        p = p->next;
    }
    
    printf("\n");
}
```



#### 逆转

```c
int node_reversal(Node *head)
{
    if(head == NULL)
    {
        fprintf(stdout, "node reversal failed : list is NULL\n");
        return -1;
    }
    if (head->next == NULL || head->next->next == NULL)
    {
        return 1;
    }
    
    Node *p = head->next, *q = p->next;
    while (p->next != NULL)
    {
        p->next = q->next;
        q->next = head->next;
        head->next = q;
        q = p->next;
    }
    
    return 1;    
}
```















