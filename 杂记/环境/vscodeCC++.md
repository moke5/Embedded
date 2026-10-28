---
type: 工具
tags: [杂记, 环境]
status: 进行中
created: 2026-10-13
updated: 2026-10-29
related: ["[[STM32 VS Code调试踩坑]]"]
---
# VS Code C/C++

[toc]



- `c_cpp_properties.json`

```json
{
    "configurations": [
        {
            "name": "STM32",
            "includePath": [
                "${workspaceFolder}/**"
            ],
            "defines": [
                "USE_HAL_DRIVER",
                "STM32F103xB"
            ],
            "compilerPath": "C:\\Users\\<用户>\\AppData\\Local\\stm32cube\\bundles\\gnu-tools-for-stm32\\14.3.1+st.2\\bin\\arm-none-eabi-gcc.exe", // arm-none-eabi-gcc.exe 的路径
            "cStandard": "gnu17",
            "cppStandard": "gnu++14",
            "intelliSenseMode": "gcc-arm"
        }
    ],
    "version": 4
}
```



1. `Ctrl+Shift+P` 调出命令面板
2. 输入：`C/C++: Reset IntelliSense Database`，回车重置数据库
3. 再输入：`Reload Window`，重载 VSCode 窗口

## 相关笔记

- [[STM32 VS Code调试踩坑]]
