# C/C++

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
            "compilerPath": "C:\\Users\\xun\\AppData\\Local\\stm32cube\\bundles\\gnu-tools-for-stm32\\14.3.1+st.2\\bin\\arm-none-eabi-gcc.exe", // arm-none-eabi-gcc.exe 的路径
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



