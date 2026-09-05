# FreeRTOS_常用函数接口

[toc]

## **一、任务管理**

**1. xTaskCreatePinnedToCore**

```C
BaseType_t xTaskCreatePinnedToCore(
    TaskFunction_t pvTaskCode,
    const char * const pcName,
    const uint32_t usStackDepth,
    void * const pvParameters,
    UBaseType_t uxPriority,
    TaskHandle_t * const pxCreatedTask,
    const BaseType_t xCoreID
);
```

- **功能**：在ESP32-S3上创建一个新任务，并指定该任务运行在哪个CPU核心上。这是ESP-IDF中创建任务的标准方式，相比于标准FreeRTOS的xTaskCreate，增加了核心亲和性控制，允许开发者将关键任务绑定到特定核心，优化缓存利用率和任务隔离。

- **参数**：

- pvTaskCode：任务函数指针，任务函数必须定义为void vTaskFunction(void *pvParameters)形式，且不能返回（内部应包含无限循环）。

- pcName：任务名称字符串，主要用于调试目的，长度不超过configMAX_TASK_NAME_LEN。

- usStackDepth：任务栈大小，单位是**字（word）**，在ESP32-S3上1个字等于4字节。例如设置为2048，则实际栈大小为8192字节。需要根据任务中局部变量、函数调用嵌套深度等因素合理分配。

- pvParameters：传递给任务函数的参数指针，可为NULL。

- uxPriority：任务优先级，数值越大优先级越高。范围0 ~ configMAX_PRIORITIES-1。在ESP-IDF中，建议使用tskIDLE_PRIORITY、configMAX_PRIORITIES-1等宏定义。

- pxCreatedTask：用于返回创建的任务句柄，后续操作（如删除、挂起）需要用到。如果不需要，可传入NULL。

- xCoreID：指定任务运行的核心ID，可选值为0或1（对应ESP32-S3的两个核心），或tskNO_AFFINITY表示由调度器自由调度。

- **返回值**：

- pdPASS：任务创建成功。

- pdFAIL：任务创建失败，通常原因是堆内存不足（TCB或栈分配失败）。

- **注意事项**：如果使用xTaskCreate（不带PinnedToCore），系统内部会调用本函数并将xCoreID设为tskNO_AFFINITY（表示‌**不绑定特定 CPU 核心**‌，允许调度器自由决定任务在哪个核心运行及动态迁移 ）。在ESP32-S3上，优先使用xTaskCreatePinnedToCore以明确任务的核心分配策略。

**英文词汇：**

**Pinned，**英/pɪnd/，固定。

**AFFINITY，**英/əˈfɪnəti/，亲和。

**2. vTaskDelete**

```C
void vTaskDelete(TaskHandle_t xTaskToDelete);
```

- **功能**：删除一个已存在的任务，回收其任务控制块（TCB）和栈内存。当任务被删除后，将不再参与调度。

- **参数**：

- xTaskToDelete：待删除任务的句柄（即创建时返回的pxCreatedTask）。如果传入NULL，则表示删除当前正在执行的任务（即调用者自身）。

- **返回值**：无

- **注意事项**：

- 删除当前任务时，该任务会立即停止执行，不再返回。

- 为确保安全，删除任务前应确保该任务不再持有任何互斥锁、信号量等资源，否则可能导致死锁或资源泄漏。

- 从空闲任务（Idle Task）中会回收被删除任务的资源，因此确保空闲任务有足够的CPU时间。

**3. vTaskSuspend**

```C
void vTaskSuspend(TaskHandle_t xTaskToSuspend);
```

- **功能**：挂起指定任务，使其进入挂起态（Suspended）。挂起态的任务不会被调度器选中运行，无论其优先级多高。挂起操作是全局的，与CPU核心无关。

- **参数**：

- xTaskToSuspend：待挂起任务的句柄。如果传入NULL，表示挂起当前任务自身。

- **返回值**：无

- **注意事项**：

- 被挂起的任务需要通过vTaskResume来恢复，不能通过延时或等待事件自动唤醒。

- 挂起自身时，当前任务会在调用后立即停止执行，直到被其他任务恢复。

**4. vTaskResume**

```C
void vTaskResume(TaskHandle_t xTaskToResume);
```

- **功能**：将一个处于挂起态的任务恢复到就绪态（Ready），使其可以参与调度。

- **参数**：

- xTaskToResume：待恢复任务的句柄。

- **返回值**：无

- **注意事项**：

- 只能恢复通过vTaskSuspend挂起的任务。

- 如果任务原本处于阻塞态（Blocked）等待某个事件，恢复后仍会保持在阻塞态，直到事件发生。

- 不能在中断服务程序（ISR）中调用此函数，中断中应使用vTaskResumeFromISR。

**5. vTaskDelay**

```C
void vTaskDelay(const TickType_t xTicksToDelay);
```

- **功能**：使当前任务进入阻塞态，持续指定的系统时钟节拍数。在延时期间，任务会让出CPU使用权，调度器可以运行其他任务。

- **参数**：

- xTicksToDelay：延时的节拍数。可用pdMS_TO_TICKS(毫秒数)将毫秒转换为节拍数。例如vTaskDelay(pdMS_TO_TICKS(100))延时100毫秒。

- **返回值**：无

- **注意事项**：

- 实际延时时间可能存在±1个tick的误差，取决于系统时钟精度。

- 延时是从调用时刻开始计算的绝对时间，不受系统时间调整影响。

- 延时0个tick会立即返回，相当于让出CPU一次。

## **二、时间与时钟**

**6. pdMS_TO_TICKS**

```C
#define pdMS_TO_TICKS(xTimeInMS) ((TickType_t)(((TickType_t)(xTimeInMS) * (TickType_t)configTICK_RATE_HZ) / (TickType_t)1000))
```

- **功能**：宏定义，将以毫秒为单位的时间值转换为系统时钟节拍数。用于统一时间单位，提高代码可移植性。

- **参数**：

- xTimeInMS：需要转换的毫秒数。

- **返回值**：对应的系统节拍数（TickType_t类型）。

- **注意事项**：在ESP-IDF中，configTICK_RATE_HZ通常配置为100（即每10ms一个tick），但可调整。使用该宏可避免硬编码，确保代码在不同Tick频率下仍正确。

**7. xTaskGetTickCount**

```C
TickType_t xTaskGetTickCount(void);
```

- **功能**：获取系统从启动到当前时刻运行的总Tick计数。

- **参数**：无

- **返回值**：当前Tick计数值，类型为TickType_t（在ESP32-S3上通常为32位无符号整数）。

- **注意事项**：该值会在系统运行约49.7天后（Tick频率100Hz时）发生溢出（回绕到0）。如果需要长时间计时，应使用xTaskGetTickCountFromISR的中断安全版本，并注意溢出处理。

## **三、信号量（Semaphore）**

**8. xSemaphoreCreateBinary**

```C
SemaphoreHandle_t xSemaphoreCreateBinary(void);
```

- **功能**：创建一个二进制信号量，初始状态为"空"（即不可用）。二进制信号量通常用于任务间同步，表示"某个事件已发生"。

- **参数**：无

- **返回值**：

- 成功：返回信号量句柄（SemaphoreHandle_t类型）。

- 失败：返回NULL，通常是内存不足导致。

- **注意事项**：

- 创建后，需要通过xSemaphoreGive先给出一次，然后才能被xSemaphoreTake获取。

- 二进制信号量与互斥锁不同，不具有优先级继承机制。

- 在中断中可使用xSemaphoreGiveFromISR。

**9. xSemaphoreCreateCounting**

```C
SemaphoreHandle_t xSemaphoreCreateCounting(
    UBaseType_t uxMaxCount,
    UBaseType_t uxInitialCount
);
```

- **功能**：创建一个计数信号量，用于管理多个同类资源（例如：连接池中有N个可用连接）。计数信号量维护一个计数值，取值范围为0到uxMaxCount。

- **参数**：

- uxMaxCount：信号量的最大计数值，即资源总数。

- uxInitialCount：信号量的初始计数值，即初始可用资源数，通常设置为uxMaxCount。

- **返回值**：

- 成功：返回信号量句柄。

- 失败：返回NULL。

- **注意事项**：

- 每次xSemaphoreTake成功，计数值减1；每次xSemaphoreGive成功，计数值加1。

- 当计数值为0时，xSemaphoreTake会阻塞等待。

- 计数值不会超过uxMaxCount。

**10. xSemaphoreTake**

```C
BaseType_t xSemaphoreTake(
    SemaphoreHandle_t xSemaphore,
    TickType_t xTicksToWait
);
```

- **功能**：获取（消耗）一个信号量。如果信号量当前可用（计数值>0），则立即返回成功并递减计数值；如果不可用，任务进入阻塞态等待。

- **参数**：

- xSemaphore：信号量句柄（二进制或计数信号量，也适用于互斥锁）。

- xTicksToWait：等待超时时间（节拍数）。设置为portMAX_DELAY表示无限等待直到获取成功。

- **返回值**：

- pdTRUE：成功获取信号量。

- pdFALSE：等待超时仍未获取到。

- **注意事项**：

- 对于互斥锁，xSemaphoreTake同样适用，且会触发优先级继承。

- 中断中应使用xSemaphoreTakeFromISR，但通常不建议在中断中阻塞等待。

**11. xSemaphoreGive**

```C
BaseType_t xSemaphoreGive(SemaphoreHandle_t xSemaphore);
```

- **功能**：释放（给予）一个信号量，使计数值增加。如果有任务正在等待该信号量，则唤醒最高优先级的等待任务。

- **参数**：

- xSemaphore：信号量句柄。

- **返回值**：

- pdPASS：释放成功。

- pdFAIL：释放失败（例如计数信号量已达最大值，或互斥锁不是由当前任务持有）。

- **注意事项**：

- 对于互斥锁，**必须由持有该锁的任务释放**，否则行为未定义。

- 中断中应使用xSemaphoreGiveFromISR。

## **四、互斥锁（Mutex）**

**12. xSemaphoreCreateMutex**

```C
SemaphoreHandle_t xSemaphoreCreateMutex(void);
```

- **功能**：创建一个互斥锁（互斥量），用于保护共享资源，防止多任务同时访问。互斥锁具有**优先级继承**特性，可避免优先级反转问题。

- **参数**：无

- **返回值**：

- 成功：返回互斥锁句柄。

- 失败：返回NULL（内存不足）。

- **注意事项**：

- 互斥锁本质上是二进制信号量，但增加了优先级继承机制，因此开销略大于二进制信号量。

- 必须在任务上下文中使用，不能在中断中使用（中断中应使用信号量）。

- 获取和释放必须成对出现，且由同一个任务完成。

**13. xSemaphoreCreateRecursiveMutex**

```C
SemaphoreHandle_t xSemaphoreCreateRecursiveMutex(void);
```

- **功能**：创建一个递归互斥锁，允许同一个任务多次获取该锁而不会导致死锁。每次获取时计数器加1，每次释放时计数器减1，当计数器归零时锁才真正释放。

- **参数**：无

- **返回值**：

- 成功：返回递归互斥锁句柄。

- 失败：返回NULL。

- **注意事项**：递归互斥锁适用于函数递归调用或同一任务的不同函数间需要先后获取同一锁的场景。

**14. xSemaphoreTakeRecursive**

```C
BaseType_t xSemaphoreTakeRecursive(
    SemaphoreHandle_t xMutex,
    TickType_t xTicksToWait
);
```

- **功能**：递归获取互斥锁。如果当前任务已经持有该锁，则直接返回成功，同时内部持有计数器加1；如果未持有，则尝试获取并等待。

- **参数**：

- xMutex：递归互斥锁句柄。

- xTicksToWait：等待超时时间（节拍数）。

- **返回值**：

- pdPASS：获取成功。

- pdFAIL：超时失败。

- **注意事项**：获取次数必须与释放次数匹配，否则锁永远不会完全释放。

**15. xSemaphoreGiveRecursive**

```C
BaseType_t xSemaphoreGiveRecursive(SemaphoreHandle_t xMutex);
```

- **功能**：递归释放互斥锁。内部持有计数器减1，如果减到0，则真正释放锁，唤醒其他等待任务。

- **参数**：

- xMutex：递归互斥锁句柄。

- **返回值**：

- pdPASS：释放成功。

- pdFAIL：释放失败（例如当前任务并未持有该锁）。

- **注意事项**：释放次数必须等于获取次数，才能完全释放锁。

## **五、事件标志组（Event Group）**

**16. xEventGroupCreate**

```C
EventGroupHandle_t xEventGroupCreate(void);
```

- **功能**：创建一个事件标志组，用于任务间的同步。事件组内部维护一个24位（或32位，取决于配置）的位掩码，每一位可以代表一个独立事件。

- **参数**：无

- **返回值**：

- 成功：返回事件组句柄。

- 失败：返回NULL（内存不足）。

- **注意事项**：在ESP32-S3上，默认支持24个事件位（configUSE_24_BIT_EVENT_GROUPS为1），可同时等待多个事件。

**17. xEventGroupSetBits**

```C
EventBits_t xEventGroupSetBits(
    EventGroupHandle_t xEventGroup,
    const EventBits_t uxBitsToSet
);
```

- **功能**：在任务中设置（置1）事件组中的指定事件位。如果设置后满足了某些任务的等待条件，则唤醒相应任务。

- **参数**：

- xEventGroup：事件组句柄。

- uxBitsToSet：位掩码，指定哪些位需要置1。例如(BIT0 | BIT1)表示将第0位和第1位置1。

- **返回值**：设置后事件组的完整值（所有位的状态），可用于调试。

- **注意事项**：中断中应使用xEventGroupSetBitsFromISR，该函数会通过中断安全的队列机制在任务上下文中执行设置操作。

**18. xEventGroupWaitBits**

```C
EventBits_t xEventGroupWaitBits(
    EventGroupHandle_t xEventGroup,
    const EventBits_t uxBitsToWaitFor,
    const BaseType_t xClearOnExit,
    const BaseType_t xWaitForAllBits,
    TickType_t xTicksToWait
);
```

- **功能**：让当前任务等待一个或多个事件位被置位。支持"等待所有指定位"或"等待任意指定位"两种模式。

- **参数**：

- xEventGroup：事件组句柄。

- uxBitsToWaitFor：需要等待的位掩码。

- xClearOnExit：如果为pdTRUE，则在条件满足后自动清除这些位；为pdFALSE则保留状态。

- xWaitForAllBits：如果为pdTRUE，需要所有指定位都置1才满足条件；为pdFALSE，则任意一位置1即满足。

- xTicksToWait：超时时间（节拍数），portMAX_DELAY表示无限等待。

- **返回值**：返回条件满足时事件组的完整值。可以通过检查返回值判断哪些位触发了条件。

- **注意事项**：

- 调用前若条件已满足，函数会立即返回。

- 自动清除（xClearOnExit = pdTRUE）是原子操作，不会丢失事件。

## **六、消息队列（Queue）**

**19. xQueueCreate**

```C
QueueHandle_t xQueueCreate(
    UBaseType_t uxQueueLength,
    UBaseType_t uxItemSize
);
```

- **功能**：创建一个消息队列，用于任务间传递数据。队列采用拷贝传递方式，发送时将数据拷贝到队列内部缓冲区，接收时从队列拷贝到用户缓冲区，保证数据安全。

- **参数**：

- uxQueueLength：队列最大长度，即最多可存储的消息数量

- uxItemSize：每个消息的大小（字节数）。如果传递的是指针，则设为sizeof(void*)。

- **返回值**：

- 成功：返回队列句柄。

- 失败：返回NULL（内存不足）。

- **注意事项**：消息大小不宜过大，否则拷贝开销会较大。如需传递大数据，通常传递指针而非数据本身。

**20. xQueueSend / xQueueSendToBack**

```
BaseType_t xQueueSend(
    QueueHandle_t xQueue,
    const void * pvItemToQueue,
    TickType_t xTicksToWait
);
```

- **功能**：向队列尾部发送一个消息（xQueueSend等效于xQueueSendToBack）。消息内容会从pvItemToQueue指向的缓冲区拷贝到队列内部。

- **参数**：

- xQueue：队列句柄。

- pvItemToQueue：指向要发送数据的指针。

- xTicksToWait：队列满时的最大等待时间（节拍数），portMAX_DELAY表示无限等待。

- **返回值**：

- pdPASS：发送成功。

- errQUEUE_FULL：队列已满且等待超时。

- **注意事项**：中断中应使用xQueueSendFromISR（或xQueueSendToBackFromISR）。

**21. xQueueReceive**

```C
BaseType_t xQueueReceive(
    QueueHandle_t xQueue,
    void * pvBuffer,
    TickType_t xTicksToWait
);
```

- **功能**：从队列头部接收一个消息，并将该消息从队列中移除。接收到的数据会被拷贝到pvBuffer指向的缓冲区。

- **参数**：

- xQueue：队列句柄。

- pvBuffer：指向接收缓冲区的指针，大小至少为队列创建时指定的uxItemSize。

- xTicksToWait：队列空时的最大等待时间（节拍数），portMAX_DELAY表示无限等待。

- **返回值**：

- pdPASS：接收成功。

- errQUEUE_EMPTY：队列为空且等待超时。

- **注意事项**：如果只需要查看队首消息而不移除，可使用xQueuePeek。中断中应使用xQueueReceiveFromISR。

**22. xQueueSendFromISR（中断安全版本示例）**

```C
BaseType_t xQueueSendFromISR(
    QueueHandle_t xQueue,
    const void * pvItemToQueue,
    BaseType_t * pxHigherPriorityTaskWoken
);
```

- **功能**：在中断服务程序中向队列发送消息，是xQueueSend的中断安全版本。

- **参数**：

- xQueue：队列句柄。

- pvItemToQueue：指向要发送数据的指针。

- pxHigherPriorityTaskWoken：如果发送操作导致一个更高优先级的任务从阻塞态变为就绪态，此参数会被设为pdTRUE，指示需要在中断退出时进行上下文切换。

- **返回值**：

- pdPASS：发送成功。

- errQUEUE_FULL：队列已满。

- **注意事项**：中断中所有涉及FreeRTOS对象的操作都应使用FromISR版本，并根据返回值决定是否在ISR结束时调用portYIELD_FROM_ISR()。

## **七、队列集（Queue Set）**

**23. xQueueCreateSet**

```C
QueueSetHandle_t xQueueCreateSet(const UBaseType_t uxEventQueueLength);
```



- **功能**：创建一个队列集（Queue Set），允许一个任务同时等待多个队列或信号量中的任意一个变为可用。队列集在需要"多路复用"多个通信对象时很有用。

- **参数**：

- uxEventQueueLength：事件队列长度，**必须等于**所有将要添加到集合中的队列长度之和，加上所有信号量的数量（每个信号量计为1）。这个值用于确保集合不会丢失任何事件。

- **返回值**：

- 成功：返回队列集句柄。

- 失败：返回NULL（内存不足或参数无效）。

- **注意事项**：队列集的长度计算需要非常精确，否则可能导致事件丢失。如果不确定，可保守地设置为所有队列长度之和加上信号量数量的2倍。

**24. xQueueAddToSet**

```C
BaseType_t xQueueAddToSet(
    QueueSetMemberHandle_t xQueueOrSemaphore,
    QueueSetHandle_t xQueueSet
);
```



- **功能**：将一个已创建的队列或信号量添加到队列集中。

- **参数**：

- xQueueOrSemaphore：队列或信号量的句柄。

- xQueueSet：队列集句柄。

- **返回值**：

- pdPASS：添加成功。

- pdFAIL：添加失败（常见原因：该队列或信号量已被添加到其他集合，或者添加时队列/信号量不为空）。

- **注意事项**：**被添加的队列或信号量必须为空**（即没有待处理的消息或信号量计数值为0），否则添加会失败。添加后，该队列/信号量就专属于该集合，不能再单独使用。

**25. xQueueSelectFromSet**

```C
QueueSetMemberHandle_t xQueueSelectFromSet(
    QueueSetHandle_t xQueueSet,
    TickType_t xTicksToWait
);
```

- **功能**：在队列集上等待，当集合中任一成员（队列或信号量）变为可用时，返回该成员的句柄。

- **参数**：

- xQueueSet：队列集句柄。

- xTicksToWait：等待超时时间（节拍数），portMAX_DELAY表示无限等待。

- **返回值**：

- 成功：返回可用成员（队列或信号量）的句柄。

- NULL：等待超时。

- **注意事项**：

- 返回句柄后，需要调用对应的接收函数（如xQueueReceive或xSemaphoreTake）来获取数据/资源。

- 队列集**不能嵌套**，即不能将队列集添加到另一个队列集中。

## **八、内存管理（ESP32-S3特有）**

**26. xTaskCreateWithCaps**

```C
BaseType_t xTaskCreateWithCaps(
    TaskFunction_t pvTaskCode,
    const char * const pcName,
    const uint32_t usStackDepth,
    void * const pvParameters,
    UBaseType_t uxPriority,
    TaskHandle_t * const pxCreatedTask,
    const uint32_t ulStackCaps
);
```

- **功能**：ESP32-S3特有API，创建任务并指定栈内存的分配属性（例如分配在PSRAM或内部SRAM中）。

- **参数**：

- 前6个参数与xTaskCreatePinnedToCore相同。

- ulStackCaps：内存属性标志，例如MALLOC_CAP_SPIRAM表示从PSRAM分配栈，MALLOC_CAP_INTERNAL表示从内部SRAM分配（默认）。

- **返回值**：

- pdPASS：创建成功。

- pdFAIL：创建失败。

- **注意事项**：将任务栈分配到PSRAM可以节省内部SRAM，但访问速度稍慢，适合对速度不敏感但对内存容量有要求的场景。

## **九、中断安全通用规则**

几乎所有FreeRTOS对象（队列、信号量、事件组）的操作在中断中都有对应的FromISR版本，其使用模式遵循：

1. 调用XXXFromISR函数。

1. 检查函数的pxHigherPriorityTaskWoken参数是否被设为pdTRUE。

1. 如果是，则在ISR退出前调用portYIELD_FROM_ISR()请求上下文切换。

