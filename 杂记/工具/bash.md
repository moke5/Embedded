---
type: 工具
tags: [bash, linux, shell]
status: 进行中
target: 晶体
input: bash 官方手册（man bash）、写脚本时的实际调试
output: 引号与展开规则表 + 语法速查 + .bashrc 配置说明
review: 2026-10-20
created: 2026-10-13
updated: 2026-10-23
related: ["[[基础命令速查]]", "[[终端中文乱码]]", "[[vim]]"]
---

# bash

[toc]

> Linux 默认的 shell， 也是写自动化脚本最常用的解释器。日常敲的零散命令（ls、grep、find 那一批）见 [基础命令速查](../Linux/基础命令速查.md)，这篇记的是把它当语言用的部分：变量、引号、判断、循环、函数，以及 `.bashrc` 怎么配。
> bash 有个特点——报错少、静默错多。写错了不会像 C 那样编译不过，经常是变量为空、路径带空格这类问题悄悄跑完。所以「引号与展开」这一节值得先看。

## 一、使用

### 脚本骨架

```bash
#!/usr/bin/env bash
set -euo pipefail          # 出错就停、未定义变量报错、管道中任一环节失败即失败

main() {
    echo "hello"
}

main "$@"
```

三处值得解释：

- `#!/usr/bin/env bash`（shebang）：告诉系统用 bash 解释这个文件。用 `env` 而不是直接写 `/bin/bash`，是为了在不同机器上都找得到 bash。
- `set -euo pipefail`：三个开关合起来写，让脚本尽早暴露问题，而不是带着错误值一路跑到底。
  - `-e`：命令返回非 0 就退出；
  - `-u`：用了没赋值的变量直接报错，防手滑写错变量名；
  - `pipefail`：管道里任意一段失败，整条管道算失败（默认只看最后一段）。
- `"$@"`：把脚本收到的参数原样传进去，含空格也不会被拆开。

### 怎么运行

| 方式 | 命令 | 特点 |
| --- | --- | --- |
| 交给 bash 跑 | `bash 脚本.sh` | 不需要执行权限，在子 shell 里执行 |
| 当程序跑 | `chmod +x 脚本.sh` 后 `./脚本.sh` | 靠 shebang 决定用哪个解释器 |
| 在当前 shell 里执行 | `source 脚本.sh` 或 `. 脚本.sh` | 不新开进程，变量、`cd`、函数都会留在当前终端 |

`source` 和另外两种的区别容易踩：脚本里 `cd` 到别的目录，用 `bash 脚本.sh` 跑完终端还在原地；用 `source` 跑完就真的换了目录，因为它在当前 shell 里执行。

### 脚本自身路径

```bash
self_path=$(readlink -f "${BASH_SOURCE[0]}")
self_dir=$(dirname "$self_path")
```

- `${BASH_SOURCE[0]}`：当前脚本的调用路径；
- `readlink -f`：规范化为绝对路径；
- `dirname`：取脚本所在目录。

`realpath`、`readlink -f`、`realpath -m` 等路径命令的适用条件见 [[基础命令速查]]。

### 核心机制：先展开，再分词

bash 处理一行脚本的顺序，决定了引号为什么这么重要。

```mermaid
flowchart LR
    L["读入一行"] --> E["展开<br/>变量 $var / 命令替换 $(...) / 算术 $(( ))<br/>通配符 *.txt"]
    E --> S["分词：按空格（IFS）切成一个个词"]
    S --> X["执行第一条命令"]
    X --> R["返回退出码 $?"]
    R -.->|0 成功，非 0 失败| L
```

关键在于「展开」发生在「分词」之前：一个变量里存着带空格的内容，不加引号时展开后会被当成多个参数传下去。所以规则很简单——**展开出来的内容一律用双引号包住**，`"$var"`、`"$@"`、`"$(命令)"`。

### 调试手段

```bash
bash -n 脚本.sh        # 只做语法检查，不执行（写完先跑这个）
bash -x 脚本.sh        # 打印每条实际执行的命令，看变量被展开成了什么
```

脚本里也可以临时开关：`set -x` 打开、`set +x` 关闭，只把可疑的那一段圈起来跟踪，输出不至于刷屏。

## 二、常用操作

### 变量与引号

```bash
name="张三"            # 赋值时等号两边不能有空格
echo "$name"           # 取值加 $
readonly 常量=1        # 只读，再赋值会报错
unset name             # 删除变量
```

引号的区别是 bash 最容易出错的地方，一张表说清：

| 写法 | 变量 / 命令替换 | 通配符 | 适合 |
| --- | --- | --- | --- |
| `'内容'` | 不展开，原样输出 | 不展开 | 固定字符串、正则、含 `$` 的文本 |
| `"内容"` | 展开 | 不展开 | 含变量的字符串（最常用） |
| `\` 转义 | `\$` 表示字面 `$` | 转义的字符失去特殊含义 | 单个字符 |
| 不加引号 | 展开 | 展开 | 基本不用，容易出分词问题 |

```bash
file="a b.txt"
cat $file          # 错：被拆成两个参数 a 和 b.txt
cat "$file"        # 对
```

### 展开与替换（参数扩展）

都是 `${}` 里的写法，处理字符串时比调 `sed`/`basename` 快：

```bash
${var:-默认值}       # var 为空或未定义时用默认值，不改变 var
${var:=默认值}       # 同上，但把默认值赋给 var
${var:?错误提示}     # 为空就报错并退出，用来做参数校验
${#var}              # 字符串长度
${var#前缀}          # 从开头删掉最短匹配的前缀
${var##前缀}         # 删最长匹配
${var%后缀}          # 从结尾删掉最短匹配的后缀
${var%%后缀}         # 删最长匹配
${var/旧/新}         # 替换第一处
${var//旧/新}        # 替换全部
```

文件名处理里最常用的两个：

```bash
path="/etc/nginx/nginx.conf"
echo "${path##*/}"    # nginx.conf   最后一个 / 之前全删
echo "${path%/*}"     # /etc/nginx   最后一个 / 之后全删
echo "${path%.*}"     # /etc/nginx/nginx  去掉扩展名
```

### 条件判断

```bash
if [[ -f "$file" && "$mode" == "prod" ]]; then
    echo "生产环境的普通文件"
elif [[ "$n" -gt 10 ]]; then
    echo "大于 10"
else
    echo "其他"
fi
```

`[[ ]]` 是 bash 的关键字，能用 `&&` `||`，字符串比较不必引号包裹也不会分词，正则用 `=~`。老的 `[ ]`（即 `test` 命令）逻辑要用 `-a` `-o`，且变量必须加引号，新脚本一律用 `[[ ]]`。

常用判断项：

| 写法 | 判断内容 |
| --- | --- |
| `-f` / `-d` / `-e` | 普通文件 / 目录 / 存在 |
| `-z` / `-n` | 字符串为空 / 非空 |
| `==` `!=` / `=~` | 字符串相等 / 正则匹配 |
| `-eq` `-ne` `-gt` `-lt` | 整数比较（字符串比较用 `==`，别混） |
| `-x` `-r` `-w` | 可执行 / 可读 / 可写 |

### 循环

```bash
# 遍历固定列表
for name in a b c; do
    echo "$name"
done

# 遍历文件（路径含空格时关键是 "${arr[@]}" 的引号）
files=(*.log)
for f in "${files[@]}"; do
    echo "$f"
done

# 逐行读文件：read -r 防止反斜杠被吃掉，IFS= 保住行首空格
while IFS= read -r line; do
    echo "$line"
done < input.txt

# 计数循环
for ((i = 1; i <= 5; i++)); do
    echo "$i"
done
```

### 数组、算术、退出码

```bash
arr=(one two three)
echo "${arr[0]} ${arr[@]}"     # 第一个元素 / 全部元素
echo "${#arr[@]}"              # 元素个数
echo "${arr[@]:1:2}"           # 从下标 1 取 2 个

declare -A map                 # 关联数组，像字典
map[key]="value"

n=$((3 + 4 * 2))               # 算术扩展，只支持整数
((n++))                        # 自增，条件位上用时要注意返回值
```

退出码 `$?`：0 表示成功，非 0 表示失败，是脚本里串联命令的基础。

```bash
grep -q "error" "$log" && echo "有报错" || echo "没有"
```

这写法当简单的二元判断可以，一旦后面还有分支就该换 `if`——`&& ... || ...` 在后面那条失败时会继续执行 `||` 后面的内容，容易和预期不符。

### 函数

```bash
# 参数靠 $1 $2 取，返回靠 return（只能是 0-255 的整数）
log() {
    local level="$1"          # local 让变量只在这个函数里有效
    shift                     # 丢掉第一个参数，剩下的再传出去
    printf '[%s] %s\n' "$level" "$*"
}

log INFO "启动完成"
```

函数里想返回字符串，用 `echo` 输出再由调用方 `$( )` 接走，比全局变量干净。

### 重定向与管道

```bash
cmd > out.txt              # 覆盖输出
cmd >> out.txt             # 追加
cmd 2> err.txt             # 只接标准错误
cmd > out.txt 2>&1         # 标准输出和错误合并进同一个文件
cmd > /dev/null 2>&1       # 什么都不显示（定时任务里常用）

cat <<EOF > config.txt     # here-doc：把多行内容写进文件
key=value
EOF

while read -r l; do ... done < <(cmd)   # 进程替换，把命令输出当文件读
```

`|` 管道把前一条的输出接到后一条的输入，中间出错默认不报错，所以脚本开头的 `pipefail` 有必要。

### 几个常用内置命令

```bash
echo "$x"          # 简单输出
printf '%s\n' "$x" # 带格式，脚本里更稳
read -r -p "输入: " ans
export PATH="$PATH:/opt/bin"
source other.sh
```

## 三、配置

### 配置文件的加载顺序

bash 分两种启动方式，读的文件不一样：

| 启动方式 | 读什么 |
| --- | --- |
| 登录 shell（`ssh` 登录、`su -`） | `/etc/profile` → `~/.bash_profile`（找不到就找 `~/.bash_login`、`~/.profile`） |
| 交互式非登录 shell（打开终端、WSL 起窗口） | `~/.bashrc` |

`~/.bash_profile` 里一般会写一句 `source ~/.bashrc`，这样登录 shell 也能拿到别名和提示符设置。日常在桌面终端里改东西，改 `~/.bashrc` 就对了。

注意脚本（非交互）默认这两个文件都不读。脚本要用的配置走显式 `source`，或者把变量写进脚本本身，别指望 `.bashrc` 生效。

### 常用配置

```bash
# ~/.bashrc
alias ll='ls -alh'
alias gs='git status -s'

export EDITOR=vim
export PATH="$PATH:$HOME/.local/bin"

PS1='\u@\h:\w\$ '            # 提示符：用户@主机:目录$
```

`alias` 只对交互式命令行有用，脚本里不会被展开，需要长期用的一组操作就写成函数放到 `.bashrc` 里。

### 改完怎么生效

```bash
source ~/.bashrc      # 当前终端立即生效
```

或者关掉重开一个终端。`.bashrc` 写坏导致终端启动就报错时，先用 `/bin/sh` 或 `bash --norc` 起一个干净 shell，把文件改回去。

## 四、小结

1. 出问题先想「展开 → 分词」的顺序：变量、命令替换的结果一律加双引号，`"$var"`、`"$@"`、`"$(命令)"`。
2. 脚本开头写 `set -euo pipefail`，写完先 `bash -n` 查语法、再用 `bash -x` 看展开结果。
3. 字符串处理优先用 `${var#...}` `${var%...}` 这类参数扩展，少调外部命令。
4. 判断用 `[[ ]]`，配置改 `~/.bashrc`（交互式）或 `~/.bash_profile`（登录），改完 `source` 一下。

## 自测

- Q：`file="a b.txt"; cat $file` 为什么报"文件不存在"？
  A：展开发生在分词之前，`$file` 里的空格把内容切成了 `a` 和 `b.txt` 两个参数。写成 `cat "$file"`。
- Q：单引号和双引号什么时候用哪个？
  A：内容里有变量、命令替换需要展开就用双引号；固定字符串、正则、含 `$` 的字面文本用单引号，它什么都不展开。
- Q：`grep -q err log && echo 有 || echo 无` 什么时候会出意外？
  A：两种情况混在一起时判断会歪——这是二元写法，分支多了改用 `if`，因为 `&&` 后面的命令失败也会触发 `||`。
- Q：为什么脚本里读 `.bashrc` 里定义的别名没效果？
  A：别名只对交互式 shell 生效，而且非交互脚本根本不读 `.bashrc`。要用就写成函数，或在脚本里显式 `source`。

## 关联

- [基础命令速查](../Linux/基础命令速查.md)：ls / grep / find 这些命令的用法，脚本里调的就是它们。
- [bash快捷键](./bash快捷键.md)：交互式命令行里的行内编辑键位（删除、光标移动、剪切环、历史搜索）。
- [终端中文乱码](../环境/终端中文乱码.md)：脚本往终端输出中文时的编码问题，和 `locale`、`PYTHONIOENCODING` 有关。
- [vim](./vim.md)：改 `.bashrc`、写脚本时用得上。
