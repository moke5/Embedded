# 1 实时时钟

## 1.1 概述

  实时时钟的缩写是RTC(Real Time Clock)。RTC是集成电路，通常称为时钟芯片。

  实时时钟芯片是日常生活中应用最为广泛的消费类电子产品之一。它为人们提供精确的实时时间，或者为电子系统提供精确的时间基准，目前实时时钟芯片大多采用精度较高的晶体振荡器作为时钟源，常见频率为32.768KHz。有些时钟芯片为了在主电源掉电时，还可以工作，需要外加电池供电。


![img](./img/rBJlJmKQlHOABaTsAARHOVDQWC8775.png)

  在许多的单片机系统中，通常进行一些与时间有关的控制，这就需要使用实时时钟。

  传统的数据记录方式是隔时采样或定时采样，没有具体的时间记录，因此，只能记录数据而无法准确记录其出现的时间；若采用单片机计时，一方面需要采用计数器，占用硬件资源，另一方面需要设置中断、查询等，同样耗费单片机的资源，而且某些测控系统可能不允许。在系统中采用实时时钟芯片能很好的解决这个问题。

**早期RTC**

  早期RTC产品实质是一个带有计算机通讯口的分频器。它通过对晶振所产生的振荡频率分频和累加，得到年、月、日、时、分、秒等时间信息并通过计算机通讯口送入处理器处理。

  这一时期RTC的特征如下：在控制口线上为并行口；功耗较大；采用普通CMOS工艺；封装为双列直插式；芯片普遍没有现代RTC所具有的万年历及闰年月自动切换功能，也无法处理2000年问题。现在已经被淘汰。

**中期RTC**

  在20世纪90年代中期出现了新一代RTC，它采用特殊CMOS工艺；功耗大为降低，典型值约0.5μA以下；供电电压仅为1.4V以下；和计算机通讯口也变为串行方式，出现了诸如三线SIO/四线SPI，部分产品采用2线I2C总线；包封上采用SOP/SSOP封装，体积大为缩小；

  功能上：片内智能化程度大幅提高、具有万年历功能，输出控制也变得灵活多样。其中日本RICOH推出的RTC甚至已经出现时基软件调校功能（TTF）及振荡器停振自动检测功能而且芯片的价格极为低廉。目前，这些芯片已被客户大量使用中。

**最新一代RTC**

  最新一代RTC产品中，除了包含第二代产品所具有的全部功能，更加入了复合功能，如低电压检测，主备用电池切换功能，抗印制板漏电功能，更甚至已经集成到ARM芯片的内部。

  操作系统每个文件都具有创建时间、修改时间、访问时间的记录，都依赖了实时时钟。


![img](./img/rBJlJmKQlHOAN3PQAAJQHzwYJrc785.png)

## 1.2 晶振

  电子行业里，晶振这一行最常听到的晶振频率就是32.768KHz、77.503KHz、60.003KHz、40.003KHz、8MHZ、12MHz、14MHz、16MHz、24MHz等等。32.768KHz是最常用的频率，在日常生活中不可或缺。32.768KHz比较容易分频以便于产生1秒的时钟频率，因为32768等于2的15次方。我们每天用的手表、手机、电脑上显示作用的钟就是由它演变过来的。


![img](./img/rBJlJmKQlHKAfPq3AADcTBGp1fE655.png)

# 2 BCD编码

  二进制编码的十进制数，简称BCD码（Binary Coded Decimal）。这种方法是用4位二进制码的组合代表十进制数的0，1，2，3，4，5，6 ，7，8，9十个数符。4位二进制数码有16种组合，原则上可任选其中的10种作为代码，分别代表十进制中的0，1，2，3，4，5，6，7，8，9这十个数符。最常用的BCD码称为8421BCD码，8、4、2、1分别是4位二进数的位取值。

**示例：**


![img](./img/rBJlJmKQlHKAJwr1AAARCyd4l6s392.png)

下表为十进制数和BCD（8421）编码的对应关系：

| 十进制 | BCD（8421）编码 |
| :----: | :-------------: |
|   0    |      0000       |
|   1    |      0001       |
|   2    |      0010       |
|   3    |      0011       |
|   4    |      0100       |
|   5    |      0101       |
|   6    |      0110       |
|   7    |      0111       |
|   8    |      1000       |
|   9    |      1001       |

**优点**

  BCD码这种编码形式利用了四个位元来储存一个十进制的数码，使二进制和十进制之间的转换得以快捷的进行。这种编码技巧最常用于会计系统的设计里，因为会计制度经常需要对很长的数字串作准确的计算。相对于一般的浮点式记数法，采用BCD码，既可保存数值的精确度，又可免去使计算机作浮点运算时所耗费的时间。此外，对于其他需要高精确度的计算，BCD编码亦很常用。

# 3 夏令时

  夏时制，又称“日光节约时制”（Daylight Saving Time），是一种为节约能源而人为规定地方时间的制度，在这一制度实行期间所采用的统一时间称为“夏令时”。一般在天亮早的夏季人为将时间提前一小时，可以使人早起早睡，减少照明量，以充分利用光照资源，从而节约照明用电。各个采纳夏时制的国家具体规定不同。全世界有近110个国家每年要实行夏令时。

| 时间节点 | 非夏令时 | 夏令时  |     日出日落     |
| :------: | :------: | :-----: | :--------------: |
| 起床时间 | 7:00 AM  | 6:00 AM | 日出时间 5:30 AM |
| 上班时间 | 9:00 AM  | 8:00 AM | 日出时间 5:30 AM |
| 下班时间 | 5:00 PM  | 4:00 PM | 日落时间 6:30 PM |
| 睡觉时间 | 10:00 PM | 9:00 PM | 日落时间 6:30 PM |

比如人们在7点起床，在实行夏令时之后，就把起床实行在6点。

特别说明：从1986年开始，中国便是实行了夏令时，最后到了1992年被暂停。

原因：

  我国不光是南北跨度大，东西跨度也相当之大，由东到西跨了5个时区，虽然全国有着统一的时间，以东八区为准，但以黑龙江地区以及新疆地区为例，如果按照北京时间正午12点来看，但其实新疆地区还是9点多10点左右，如果再度实行夏令时的话，对于东八区的住民可能没什么影响，但对于其他时区的住民影响可就相当大了，指不定早上天还没有亮，按照夏令时上面的时间，就要去学校了。

  还有一点不得不提的就是，西北地区还有不少昼夜温差大的地区，有时候甚至就是这一个小时的区别，一天之内足以出现两种截然不同的温度。

# 4 内部结构

  RTC就是实时时钟，详细英文 Real Time Clock。

  实时时钟 (RTC) 是一个独立的 BCD 定时器/计数器。RTC 提供一个日历时钟、两个可编程闹钟中断，以及一个具有中断功能的周期性可编程唤醒标志。RTC 还包含用于管理低功耗模式的自动唤醒单元。

  两个 32 位寄存器包含二进码十进数格式 (BCD) 的秒、分钟、小时（12 或 24 小时制）、星期几、日期、月份和年份。此外，还可提供二进制格式的亚秒值。
系统可以自动将月份的天数补偿为 28、29（闰年）、30 和 31 天。并且还可以进行夏令时补偿。

  其它 32 位寄存器还包含可编程的闹钟亚秒、秒、分钟、小时、星期几和日期。此外，还可以使用数字校准功能对晶振精度的偏差进行补偿。

  上电复位后，所有 RTC 寄存器都会受到保护，以防止可能的非正常写访问。无论器件状态如何（运行模式、低功耗模式或处于复位状态），只要电源电压保持在工作范围内，RTC 便不会停止工作。


![img](./img/rBJlJmKQlHKAF51fAAGQY2busbc498.png)

  使用两个预分频器时，推荐将异步预分频器配置为较高的值，以最大程度降低功耗。

  要使用频率为 32.768 kHz 的 LSE 获得频率为 1 Hz 的内部时钟 (ck_spre)，需要将异步预分频系数设置为 128，并将同步预分频系数设置为 256。


![img](./img/rBJlJmKQlHKAE3LKAABdo77tpLc697.png)

# 5 供电

  当主电源 VDD 断电时，要保留 RTC 备份寄存器和备份 SRAM 的内容并为 RTC 供电，可以将 VBAT 引脚连接到通过电池或其它电源供电的可选备用电压。

  VBAT 电源的开关由复位模块中内置的掉电复位电路进行控制。如果应用中未使用任何外部电池，建议将 VBAT 引脚连接到并联了 100 nF 外部去耦陶瓷电容的VDD。


![img](./img/rBJlJmKQlHKARZH2AAHBA2fmGlI080.png)

# 6 中断配置注意事项

《stm32f4xx中文参考手册》P585有如下内容：

1. 所有 RTC 中断均与 EXTI 控制器相连。

1. 要使能 RTC 闹钟中断，需按照以下顺序操作：

- 将 EXTI 线 17 配置为中断模式并将其使能，然后选择上升沿有效。
- 配置 NVIC 中的 RTC_Alarm IRQ 通道并将其使能。
- 配置 RTC 以生成 RTC 闹钟（闹钟 A 或闹钟 B）。

1. 要使能 RTC 唤醒中断，需按照以下顺序操作：

- 将 EXTI 线 22 配置为中断模式并将其使能，然后选择上升沿有效。
- 配置 NVIC 中的 RTC_WKUP IRQ 通道并将其使能。
- 配置 RTC 以生成 RTC 唤醒定时器事件。

# 7 STM32CubeMX

## 7.1 唤醒中断

### 1、配置过程

1.在“categories”类别中就选择RCC。


![img](./img/rBJlJmKQlHOAIH6FAAAUy5z-Q-o920.png)

2.在“Low Speed Clock（LSE）”下拉菜单“Crystal/Ceramic Resonator”。


![img](./img/rBJlJmKQlHKAO1g0AAAdBgVp_78857.png)

3.在“Categories”选中RTC。


![img](./img/rBJlJmKQlHOAXXvWAAAS2X1rrOs247.png)

4.勾选“Activate Clock Source”激活时钟源。勾选“Activate Calendar”激活日历功能。“WakeUp”选中“Internal WakeUp”。


![img](./img/rBJlJmKQlHKAfambAAAkHc19mRA233.png)

5.详细配置RTC相关参数。


![img](./img/rBJlJmKQlHOAVRbEAABbjynbglU959.png)

6.使能RTC的唤醒中断。


![img](./img/rBJlJmKQlHOAeXE_AAAkpzPWCsE840.png)

### 2、示例代码

1.rtc.c

```
RTC_HandleTypeDef hrtc;

/* RTC init function */
void MX_RTC_Init(void)
{
	RTC_TimeTypeDef sTime = {0};
	RTC_DateTypeDef sDate = {0};

	/** Initialize RTC Only */
	hrtc.Instance = RTC;
	hrtc.Init.HourFormat = RTC_HOURFORMAT_24;	//24小时格式
	hrtc.Init.AsynchPrediv = 127;				//异步分频值127+1
	hrtc.Init.SynchPrediv = 255;				//同步分频值255+1
	hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;		//禁止使能（唤醒中断、闹钟A/闹钟B）输出控制RTC_AF1引脚；如果使能了，可以通过引脚控制继电器/蜂鸣器等。
	hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;//若hrtc.Init.OutPut使能，则RTC_AF1引脚输出高电平
	hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;	//若hrtc.Init.OutPut使能，则RTC_AF1引脚开漏输出，也可以选择为推挽输出。
	if (HAL_RTC_Init(&hrtc) != HAL_OK)
	{
		Error_Handler();
	}

	/* USER CODE BEGIN Check_RTC_BKUP */

	/* USER CODE END Check_RTC_BKUP */

	/** Initialize RTC and set the Time and Date */
	sTime.Hours = 0x10;	//时：10
	sTime.Minutes = 0x30;	//分：30
	sTime.Seconds = 0x45;	//秒：45
	sTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;	//不使能日光时间。可设置冬季时间减少1小时；可设置夏季时间增加1小时；
	sTime.StoreOperation = RTC_STOREOPERATION_RESET;//用户可对此位执行写操作以记录是否已对夏令时进行更改，现不对夏令时进行更改。	
	
	if (HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BCD) != HAL_OK)//设置时间
	{
		Error_Handler();
	}
	
	sDate.WeekDay = RTC_WEEKDAY_WEDNESDAY;//星期：三
	sDate.Month = RTC_MONTH_MARCH;//月：三
	sDate.Date = 0x25;//日：25
	sDate.Year = 0x21;//年：2021

	if (HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BCD) != HAL_OK)//设置日期
	{
		Error_Handler();
	}
	
	/** Enable the WakeUp */
	__HAL_RTC_WAKEUPTIMER_CLEAR_FLAG(&hrtc, RTC_FLAG_WUTF);
	if (HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, 0, RTC_WAKEUPCLOCK_CK_SPRE_16BITS) != HAL_OK)//使能唤醒中断
	{
		Error_Handler();
	}
}
```







2.stm32f4xx_it.c

（1）RTC_WKUP_IRQHandler中断服务函数

```
void RTC_WKUP_IRQHandler(void)
{
  HAL_RTCEx_WakeUpTimerIRQHandler(&hrtc);
}
```







（2）HAL_RTCEx_WakeUpTimerIRQHandler函数

```
void HAL_RTCEx_WakeUpTimerIRQHandler(RTC_HandleTypeDef *hrtc)
{
  /* Get the pending status of the WAKEUPTIMER Interrupt */
  if(__HAL_RTC_WAKEUPTIMER_GET_FLAG(hrtc, RTC_FLAG_WUTF) != (uint32_t)RESET)
  {
    /* WAKEUPTIMER callback */
#if (USE_HAL_RTC_REGISTER_CALLBACKS == 1)
    hrtc->WakeUpTimerEventCallback(hrtc);
#else
    HAL_RTCEx_WakeUpTimerEventCallback(hrtc);
#endif /* USE_HAL_RTC_REGISTER_CALLBACKS */

    /* Clear the WAKEUPTIMER interrupt pending bit */
    __HAL_RTC_WAKEUPTIMER_CLEAR_FLAG(hrtc, RTC_FLAG_WUTF);
  }

  /* Clear the EXTI's line Flag for RTC WakeUpTimer */
  __HAL_RTC_WAKEUPTIMER_EXTI_CLEAR_FLAG();

  /* Change RTC state */
  hrtc->State = HAL_RTC_STATE_READY;
}
```







（3）在rtc.c中添加RTC唤醒事件回调函数

```
//手动添加:RTC唤醒事件回调函数
void HAL_RTCEx_WakeUpTimerEventCallback(RTC_HandleTypeDef *hrtc)
{
    g_rtc_wakeup_event=1;
}
```







3.演示

  当将程序成功烧录到STM32F429开发板后，通过串口调试助手观察到RTC每1秒唤醒一次，时间也随之更新，详细显示如下：


![img](./img/rBJlJmKQlHOAWEBYAABYnTasjQE568.gif)

# 「课堂练习1」

  RTC使用LSI，每1秒触发一次唤醒中断。

## 7.2 闹钟中断

### 1、配置过程

1.在原来基础上使能闹钟A，即“Alarm A” 选中“Internal Alarm”。


![img](./img/rBJlJmKQlHKAbcljAAAjf5WnjsY241.png)

2.配置闹钟A相关参数。


![img](./img/rBJlJmKQlHOAVD7IAABTP9NI3Kw575.png)

3.使能闹钟中断。



![img](./img/rBJlJmKQlHOAMQmrAAArjn7sdm0321.png)

### 2、示例代码

1.rtc.c

(1)RTC初始化。

```
RTC_HandleTypeDef hrtc;

/* RTC init function */
void MX_RTC_Init(void)
{
	RTC_TimeTypeDef sTime = {0};
	RTC_DateTypeDef sDate = {0};
	RTC_AlarmTypeDef sAlarm = {0};

	/** Initialize RTC Only */
	hrtc.Instance = RTC;
	hrtc.Init.HourFormat = RTC_HOURFORMAT_24;	//24小时格式
	hrtc.Init.AsynchPrediv = 127;				//异步分频值127+1
	hrtc.Init.SynchPrediv = 255;				//同步分频值255+1
	hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;		//禁止使能（唤醒中断、闹钟A/闹钟B）输出控制RTC_AF1引脚；如果使能了，可以通过引脚控制继电器/蜂鸣器等。
	hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;//若hrtc.Init.OutPut使能，则RTC_AF1引脚输出高电平
	hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;	//若hrtc.Init.OutPut使能，则RTC_AF1引脚开漏输出，也可以选择为推挽输出。
	if (HAL_RTC_Init(&hrtc) != HAL_OK)
	{
		Error_Handler();
	}

	/* USER CODE BEGIN Check_RTC_BKUP */

	/* USER CODE END Check_RTC_BKUP */

	/** Initialize RTC and set the Time and Date*/
	sTime.Hours = 0x10;		//时：10
	sTime.Minutes = 0x30;	//分：30
	sTime.Seconds = 0x45;	//秒：45
	sTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;	//不使能日光时间变更。可设置冬季时间减少1小时；可设置夏季时间增加1小时；
	sTime.StoreOperation = RTC_STOREOPERATION_RESET;//用户可对此位执行写操作以记录是否已对夏令时进行更改，现不对夏令时进行更改。	
	
	
	if (HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BCD) != HAL_OK)//设置时间
	{
		Error_Handler();
	}
	
	sDate.WeekDay = RTC_WEEKDAY_WEDNESDAY;//星期：三
	sDate.Month = RTC_MONTH_MARCH;//月：三
	sDate.Date = 0x25;//日：25
	sDate.Year = 0x21;//年：2021

	
	if (HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BCD) != HAL_OK)//设置日期
	{
		Error_Handler();
	}
	
	/** Enable the Alarm A */
	sAlarm.AlarmTime.Hours = 0x10;				//时：10
	sAlarm.AlarmTime.Minutes = 0x30;			//分：30
	sAlarm.AlarmTime.Seconds = 0x50;			//秒：50
	sAlarm.AlarmTime.SubSeconds = 0x0;			//亚秒：0
	sAlarm.AlarmTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;	//不使能日光时间变更。
	sAlarm.AlarmTime.StoreOperation = RTC_STOREOPERATION_RESET;	//用户可对此位执行写操作以记录是否已对夏令时进行更改，现不对夏令时进行更改。
	sAlarm.AlarmMask = RTC_ALARMMASK_NONE;						//不使能闹钟掩码，则日期/星期比较生效
	sAlarm.AlarmSubSecondMask = RTC_ALARMSUBSECONDMASK_ALL;		//使能亚秒掩码，即亚秒比较无效，目前用不到
	sAlarm.AlarmDateWeekDaySel = RTC_ALARMDATEWEEKDAYSEL_DATE;	//进行日期比较
	sAlarm.AlarmDateWeekDay = 0x25;								//比较日期：25
	sAlarm.Alarm = RTC_ALARM_A;									//使能闹钟A
	
	if (HAL_RTC_SetAlarm_IT(&hrtc, &sAlarm, RTC_FORMAT_BCD) != HAL_OK)//使能闹钟A中断
	{
		Error_Handler();
	}
	/** Enable the WakeUp*/
	__HAL_RTC_WAKEUPTIMER_CLEAR_FLAG(&hrtc, RTC_FLAG_WUTF);
	if (HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, 0, RTC_WAKEUPCLOCK_CK_SPRE_16BITS) != HAL_OK)
	{
		Error_Handler();
	}

}
```







(2)RTC低级初始化。

```
void HAL_RTC_MspInit(RTC_HandleTypeDef* rtcHandle)
{
  if(rtcHandle->Instance==RTC)
  {
    __HAL_RCC_RTC_ENABLE();

    HAL_NVIC_SetPriority(RTC_WKUP_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(RTC_WKUP_IRQn);
    HAL_NVIC_SetPriority(RTC_Alarm_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(RTC_Alarm_IRQn);
  }
}
```







（3）添加RTC闹钟A回调函数。

```
void HAL_RTC_AlarmAEventCallback(RTC_HandleTypeDef *hrtc)
{
	g_rtc_alarm_a_event=1;
}
```







2.stm32f4xx_it.c

（1）RTC_Alarm_IRQHandler中断服务函数

```
void RTC_Alarm_IRQHandler(void)
{
	HAL_RTC_AlarmIRQHandler(&hrtc);
}
```







3.演示

  当将程序成功烧录到STM32F429开发板后，通过串口调试助手观察到RTC每1秒唤醒一次，时间也随之更新，过一会后，闹钟A事件发生，详细显示如下：


![img](./img/rBJlJmKQlHOAbVJvAAA3wYrlGHk331.gif)

# 「课堂练习2」

  RTC使能闹钟B中断，5秒后触发。

# 8 RTC 备份寄存器

## 8.1 概述

  备份寄存器 (RTC_BKPxR) 包括20 个 32 位寄存器，用于存储 80 字节的用户应用数据。这些寄存器在备份域中实现，可在 VDD 电源关闭时通过 VBAT 保持上电状态。备份寄存器不会在系统复位或电源复位时重置，也不会在器件从待机模式唤醒时复位。

  为了防止每次复位重置RTC时间，可以利用RTC自带的备份寄存器来实现。步骤如下：

- 初始化RTC时间的时候，接着去设置RTC备份寄存器的值。
- 复位的时候，去读取RTC备份寄存器的值，判断是否跟之前的值是否一致，若一致，则执行普通的时钟、电源、中断初始化。
- 发生入侵检测事件时，将复位备份寄存器。

## 8.2 函数接口

1.写备份寄存器函数

```
//用于建立重启标志，是否需要重置RTC的时间
HAL_RTCEx_BKUPWrite(&hrtc,RTC_BKP_DR0,0x8888);
```







2.读备份寄存器函数

```
uint32_t rt = HAL_RTCEx_BKUPRead(&hrtc,RTC_BKP_DR0)
```







# 「课堂练习3」

  基于RTC备份寄存器的使用，避免复位后被重置日期与时间。

# 9 应用领域

1. 桌面闹钟


![img](./img/rBJlJmKQlHKATcyqAAHqsSr21aQ617.png)

1. 智能手表


![img](./img/rBJlJmKQlHOAJZzbAAEh-mRg_8c269.png)

1. 智能定时夜灯