---
type: 工具
layer: X
domain: linux
tags:
- ssh
- linux
- 服务器
status: 进行中
target: 晶体
input: openssh 手册与服务器实操
output: 服务端安装、密钥登录、私钥选择、私钥口令、格式兼容、客户端别名、权限、空闲超时、fail2ban 封禁、加固与传文件
review: 2026-11-06
created: 2026-10-18
updated: '2026-11-06'
prereq:
- '[[端口与进程]]'
related:
- '[[从零上手]]'
- '[[端口与进程]]'
- '[[vscode]]'
---
# SSH

> SSH（Secure Shell）在不可信网络上提供服务器认证、用户认证、加密通道和完整性校验。客户端默认连接 TCP 22 端口，认证完成后可执行远程命令并传输文件。
> 买服务器后从登录到加固的完整流程见 [[从零上手]]。


## ubuntu

### 服务端

```shell
sudo apt update
sudo apt install openssh-server -y
```

安装完成后验证：

```bash
# 查看服务状态
systemctl status ssh
# 设置开机自启并立即启动
sudo systemctl enable --now ssh
# 查看22端口监听
ss -tulpn | grep 22
```

### 连接

```bash
ssh name@ip -p port
```

## 密钥登录

### 定义

SSH 中有两类非对称密钥，分别认证不同对象：

| 符号 | 名称 | 私钥持有端 | 公钥保存端 | 认证对象 |
| --- | --- | --- | --- | --- |
| $(H_s, H_p)$ | 主机密钥对 | 服务器 | 客户端 `known_hosts` | 服务器 |
| $(K_u, K_p)$ | 用户密钥对 | 客户端 | 服务器 `authorized_keys` | 登录用户 |
| $P$ | 私钥口令（passphrase） | 客户端本地 | 无 | 保护用户私钥文件 |
| $A_u$ | 用户 $u$ 的授权公钥集合 | 无 | 服务器 `authorized_keys` | 限制可登录公钥 |

### 协议模型

#### 1. 服务器认证

客户端连接服务器后，双方协商算法并执行密钥交换，得到共享会话密钥 $S$。服务器用主机私钥 $H_s$ 对交换参数签名：

$$
\sigma_H = \operatorname{Sign}_{H_s}(T_H)
$$

其中 $T_H$ 为密钥交换过程的握手转录。客户端用本地保存的主机公钥 $H_p$ 验证：

$$
\operatorname{Verify}_{H_p}(T_H, \sigma_H) = 1
$$

验证通过后，客户端确认对端持有 $H_s$。后续通信使用由 $S$ 派生的对称会话密钥保护。

#### 2. 用户公钥认证

设服务器生成随机挑战 $c$，客户端持有用户私钥 $K_u$。认证过程为：

$$
\sigma_u = \operatorname{Sign}_{K_u}(c)
$$

服务器根据 $K_p$ 验证：

$$
\operatorname{Verify}_{K_p}(c, \sigma_u) = 1
$$

公钥认证成功的条件为：

```text
Auth(u, K_p) = 1
    ⇔ PubkeyAuthentication = yes
    ∧ K_p ∈ A_u
    ∧ Verify_{K_p}(c, Sign_{K_u}(c)) = 1
    ∧ 主目录、~/.ssh、authorized_keys 与客户端私钥的权限检查通过
```

用户私钥 $K_u$ 和私钥口令 $P$ 均不发送给服务器。

#### 认证时序

图 1 给出主机密钥、用户密钥、私钥口令和授权公钥集合在协议中的位置。

```mermaid
sequenceDiagram
    box 客户端
        participant C as 客户端进程
        participant KH as known_hosts<br/>H_p
        participant KF as 私钥文件<br/>F = E_P(K_u)
    end

    box 服务器
        participant SRV as sshd
        participant AK as authorized_keys<br/>A_u
    end

    C->>SRV: TCP 连接 / 算法协商
    SRV-->>C: 密钥交换参数 + 主机签名 σ_H
    C->>KH: 检索 H_p
    KH-->>C: 主机公钥记录
    Note over C: Verify_H_p(T_H, σ_H) = 1
    C->>SRV: 密钥交换，派生会话密钥

    C->>SRV: 用户 u，公钥标识 K_p
    SRV->>AK: 判定 K_p ∈ A_u
    AK-->>SRV: 判定结果
    SRV-->>C: 随机挑战 c
    C->>KF: 输入私钥口令 P
    KF-->>C: K_u = D_P(F)
    C->>SRV: σ_u = Sign_K_u(c)
    Note over SRV: Verify_K_p(c, σ_u) = 1
    SRV-->>C: 认证结果
```

**图 1：SSH 主机认证与用户公钥认证时序**

图 1 给出三个边界条件：

1. $H_p$ 位于客户端 `known_hosts`，$H_s$ 位于服务器，二者用于认证服务器。
2. $K_u$ 位于客户端，$K_p$ 位于服务器的 $A_u$，二者用于认证用户。
3. $P$ 仅在客户端计算 $K_u=D_P(F)$ 时出现，不进入网络消息。

### 私钥口令

设私钥文件为 $F$。带口令保存时：

$$
F = E_P(K_u)
$$

客户端使用私钥前先在本地计算：

$$
K_u = D_P(F)
$$

因此，客户端软件请求两类输入的条件分别为：

| 软件请求 | 必要条件 | 用途 |
| --- | --- | --- |
| 私钥文件 | 软件需要 $K_u$ 生成签名 | 获得用户认证所需的签名材料 |
| 私钥口令 | $F$ 由 $P$ 加密 | 在本地解密 $F$，得到 $K_u$ |

$P=\epsilon$ 表示生成密钥时未设置口令。此时软件不请求私钥口令。私钥口令与服务器用户密码是两个独立凭证：前者保护本地私钥文件，后者由服务器在密码认证中验证。

### `.ssh` 目录的文件职责

| 文件 | 所在位置 | 内容 | 机密性 |
| --- | --- | --- | --- |
| `id_ed25519` | 客户端 `~/.ssh/` | 用户私钥 $K_u$ | 机密 |
| `id_ed25519.pub` | 客户端 `~/.ssh/` | 用户公钥 $K_p$ | 可公开 |
| `authorized_keys` | 服务器用户主目录 `~/.ssh/` | 授权公钥集合 $A_u$ | 决定访问权 |
| `known_hosts` | 客户端 `~/.ssh/` | 已确认的主机公钥 $H_p$ | 不保密 |
| `config` | 客户端 `~/.ssh/` | 主机别名、端口、用户名、私钥路径 | 可能含主机拓扑 |

### 密钥生成

密钥对在客户端生成，私钥 $K_u$ 留在客户端，公钥 $K_p$ 复制到服务器。在服务器上生成密钥对，用于该服务器主动连接其他主机（git、部署），与登录服务器本身无关。

`ssh-keygen` 的必填参数是算法类型 `-t`。参数含义如下：

| 参数 | 作用 | 取值或示例 |
| --- | --- | --- |
| `-t` | 密钥算法类型，必填 | `ed25519`、`rsa`、`ecdsa` |
| `-b` | 密钥位数，RSA 等算法使用 | `-t rsa -b 4096` |
| `-C` | 公钥注释，写入 `.pub` 末尾，用于标识持有者 | `-C "feng@laptop"` |
| `-f` | 私钥输出路径，同时决定公钥路径 | `-f ~/.ssh/id_ed25519_aliyun` |
| `-N` | 私钥口令 $P$，`-N ""` 表示 $P=\epsilon$ | `-N ""` |
| `-y` | 由私钥导出公钥 | `ssh-keygen -y -f id_ed25519` |
| `-l` | 输出私钥指纹 | `ssh-keygen -l -f id_ed25519` |

用户名不进入 `-t`。`-t` 只接受算法名；标识持有者用 `-C`；登录用户名由 `ssh <用户>@<IP>` 指定。三者的位置不同，混用会导致命令失败或注释错误。

Linux、macOS、Git Bash：

```bash
ssh-keygen -t ed25519 -C "feng"
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.ssh" | Out-Null
ssh-keygen.exe -t ed25519 -C "feng"
```

交互过程：

1. `Enter file in which to save the key`：直接回车使用默认路径 `~/.ssh/id_ed25519`；需要多套密钥时输入新路径。
2. `Enter passphrase`：输入私钥口令 $P$；留空则 $P=\epsilon$。
3. `Enter same passphrase again`：重复输入同一口令。

生成结果：

| 文件 | 内容 | 处理方式 |
| --- | --- | --- |
| `id_ed25519` | 私钥 $K_u$ | 留在客户端，权限 600 |
| `id_ed25519.pub` | 公钥 $K_p$ | 复制到服务器 `authorized_keys` |

常见参数错误：

| 命令 | 结果 | 原因 |
| --- | --- | --- |
| `ssh-keygen -t feng` | `unknown key type feng` | `-t` 只接受算法名，`feng` 是用户名 |
| `ssh-keygen -C feng` | 使用默认算法生成密钥 | 省略 `-t`；`feng` 仅作为注释 |
| `ssh-keygen -t ed25519 feng` | 报参数错误 | 用户名不能作为位置参数 |

### 公钥部署

Linux、macOS、Git Bash：

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub devuser@<IP>
```

Windows 无 `ssh-copy-id` 时，通过管道追加公钥：

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | ssh -p 2222 devuser@<IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

部署后验证公钥登录：

```bash
ssh -i ~/.ssh/id_ed25519 -p 2222 -o IdentitiesOnly=yes devuser@<IP>
```

确认公钥认证可用后，再关闭服务器密码认证；关闭前保留一个已登录会话，避免配置错误导致失去访问。

允许复制到服务器的是 `.pub` 公钥文件。无 `.pub` 后缀的文件为私钥。公钥丢失时，可由私钥重新导出：

```bash
ssh-keygen -y -f ~/.ssh/id_ed25519 > ~/.ssh/id_ed25519.pub
```

### 多账号与多密钥

密钥对与账号没有绑定关系。sshd 只为本次连接指定的账号检查公钥是否属于该账号的授权集合：

$$
\operatorname{Auth}(u, K_p)=1 \iff K_p \in A_u
$$

同一对密钥可以登录多个账号，前提是把同一个公钥追加到每个账号的 `authorized_keys`。一个账号也可以授权多个公钥。私钥文件只是客户端凭证，文件名与用户名没有强制对应关系。

共享私钥的代价是失去按人撤销和审计归属：日志只记录登录账号，无法区分实际操作人；一方私钥泄露时，所有授权该公钥的账号同时失守。推荐按下表生成和部署：

| 场景 | 密钥数量 | 部署位置 |
| --- | --- | --- |
| 两个人各用各的账号 | 每人一对 | 各自公钥加入各自账号 |
| 一个人管理多个账号 | 每个账号一对 | 各公钥加入对应账号 |
| 同一账号多台设备 | 每台设备一对 | 各公钥加入该账号 |

在已有默认密钥的机器上再次执行不带 `-f` 的 `ssh-keygen`，默认路径仍是 `~/.ssh/id_ed25519`。该文件已存在时，工具提示：

```text
/home/<用户>/.ssh/id_ed25519 already exists.
Overwrite (y/n)?
```

输入 `y` 覆盖原有私钥，依赖旧公钥的账号立即无法登录；输入 `n` 不生成任何文件。`-C` 只修改注释，不改变保存路径，也不会追加第二对密钥。新增密钥必须用 `-f` 指定不同路径。

多套密钥用 `-f` 区分文件，并在 `~/.ssh/config` 中按账号绑定：

```bash
ssh-keygen -t ed25519 -C "feng@laptop" -f ~/.ssh/id_ed25519_feng
ssh-keygen -t ed25519 -C "deploy@ci" -f ~/.ssh/id_ed25519_deploy
```

```text
Host ali-feng
    HostName <IP>
    User feng
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_feng
    IdentitiesOnly yes

Host ali-deploy
    HostName <IP>
    User deploy
    Port 2222
    IdentityFile ~/.ssh/id_ed25519_deploy
    IdentitiesOnly yes
```

撤销某个密钥时，从对应账号的 `authorized_keys` 中删除该公钥行，立即生效，无需重启 sshd。

### 显式指定私钥

`-i` 指定私钥路径；`IdentitiesOnly=yes` 限定本次连接只使用指定私钥和命令行或 `config` 中声明的密钥。

```bash
# Linux / macOS / Git Bash
ssh -i ~/.ssh/id_ed25519 -p 2552 -o IdentitiesOnly=yes <用户>@<服务器IP>

# Windows PowerShell
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" -p 2552 -o IdentitiesOnly=yes <用户>@<服务器IP>
```

`scp` 的端口参数为大写 `-P`：

```bash
scp -i ~/.ssh/id_ed25519 -P 2552 ./本地文件 <用户>@<服务器IP>:/home/<用户>/
```

若云厂商提供的 `.pem` 文件内容为用户私钥，同样通过 `-i` 指定：

```bash
ssh -i ~/.ssh/server.pem -p 2552 ubuntu@<服务器IP>
```

Windows 环境无 `ssh-copy-id` 时，可通过管道追加公钥：

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | ssh -p 2552 <用户>@<服务器IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### 权限要求

OpenSSH 对私钥和授权文件执行权限检查。Linux 常用权限为：

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519 ~/.ssh/config
chmod 644 ~/.ssh/id_ed25519.pub ~/.ssh/known_hosts

# 服务端
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Windows OpenSSH 可将私钥 ACL 收敛为当前用户只读：

```powershell
icacls "$env:USERPROFILE\.ssh\id_ed25519" /inheritance:r
icacls "$env:USERPROFILE\.ssh\id_ed25519" /grant:r "$($env:UserName):R"
```

### 私钥口令缓存

`ssh-agent` 保存解密后的用户私钥，用于当前会话内复用。

```powershell
# Windows：以管理员权限设置并启动服务
Set-Service ssh-agent -StartupType Automatic
Start-Service ssh-agent

# 加入私钥并查看已缓存密钥
ssh-add "$env:USERPROFILE\.ssh\id_ed25519"
ssh-add -l
```

Linux 客户端：

```bash
ssh-add ~/.ssh/id_ed25519
ssh-add -l
```

### 私钥格式

常见私钥容器格式如下：

| 文件头或特征 | 容器格式 | 典型支持范围 |
| --- | --- | --- |
| `-----BEGIN OPENSSH PRIVATE KEY-----` | OpenSSH | OpenSSH 与现代 SSH 客户端 |
| `-----BEGIN RSA PRIVATE KEY-----` | PEM RSA | 传统 SSH 客户端和旧库 |
| `-----BEGIN PRIVATE KEY-----` | PKCS#8 | 部分编程语言库和安全组件 |
| `PuTTY-User-Key-File` | PuTTY `.ppk` | PuTTY、WinSCP 及部分 Windows 客户端 |

客户端解析私钥成功的条件为：

```text
Parse(F) = 1
    ⇔ 首尾标记完整
    ∧ 文件未截断且换行有效
    ∧ 容器格式属于客户端支持集合
    ∧ 密钥算法属于客户端支持集合
    ∧ (P = ε ∨ 提供的 P 正确)
```

本机 `id_ed25519` 的首行是 `BEGIN OPENSSH PRIVATE KEY`，容器为 OpenSSH，算法为 Ed25519。堡塔终端旧版本曾存在 Ed25519 密钥兼容问题；基于 Paramiko 的终端读取加密私钥时，也必须取得正确口令。

私钥文件的有效性与口令状态可通过以下命令检查：

```powershell
# 输出指纹：文件可被 OpenSSH 解析
ssh-keygen -l -f "$env:USERPROFILE\.ssh\id_ed25519"

# 请求口令：私钥带口令；直接输出公钥：私钥无口令
ssh-keygen -y -f "$env:USERPROFILE\.ssh\id_ed25519"
```

兼容性受限时，为该软件生成独立 RSA/PEM 密钥，原有 Ed25519 密钥保持不变：

```powershell
ssh-keygen -t rsa -b 4096 -m PEM -f "$env:USERPROFILE\.ssh\bt_rsa" -C "bt-terminal"
```

部署规则：

1. 软件提供口令输入框时，可设置 $P\neq\epsilon$，并在软件中输入同一口令。
2. 软件无口令输入框时，令 $P=\epsilon$，生成无口令私钥；该文件的 ACL 必须限制为当前用户可读。
3. 将 `bt_rsa` 导入 BT-Terminal。
4. 将 `bt_rsa.pub` 追加到服务器 `~/.ssh/authorized_keys`。

粘贴私钥时，首尾标记、Base64 正文和换行必须完整。支持文件选择时，直接选择私钥文件。

## 客户端配置

`~/.ssh/config` 给每台机器起别名，之后 `ssh 别名` 即可，省去每次敲 IP、端口、用户名和私钥参数：

```text
Host myserver
    HostName <IP>
    User devuser
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

配置后，以下命令等价：

```bash
ssh myserver
ssh -i ~/.ssh/id_ed25519 -p 22 -o IdentitiesOnly=yes devuser@<IP>
```

若私钥使用默认文件名 `~/.ssh/id_ed25519`，客户端即使不写 `IdentityFile` 也会自动尝试；存在多套密钥或私钥文件名不是默认值时，必须显式配置。

### 认证排查

```bash
# 查看客户端实际提供了哪些密钥、服务器是否接受
ssh -v -i ~/.ssh/id_ed25519 -p 2552 -o IdentitiesOnly=yes <用户>@<服务器IP>
```

| 现象 | 直接原因 | 检查点 |
| --- | --- | --- |
| `Permission denied (publickey)` | 服务器没有接受客户端提供的公钥 | `authorized_keys` 是否含对应公钥；登录用户是否正确；服务端是否启用公钥认证 |
| `bad permissions` / `UNPROTECTED PRIVATE KEY FILE` | 私钥可被其他用户读取 | 按上一节收紧私钥权限 |
| `Load key ... invalid format` / 第三方软件提示“私钥格式错误” | 私钥文件损坏、容器格式或算法不受支持、粘贴内容缺行、指定路径指向公钥，或加密私钥未提供正确口令 | `-i` 指向无 `.pub` 后缀的私钥；执行 `ssh-keygen -l -f <私钥>`；客户端不支持时生成 RSA/PEM 独立密钥 |
| 出现 `Host key verification failed` | 目标主机公钥与 `known_hosts` 记录不一致 | 先通过云控制台等带外渠道确认主机身份；确认无误后执行 `ssh-keygen -R '[主机]:端口'` |
| 连接超时 | TCP 未到达 sshd | 安全组、防火墙、sshd 监听端口、客户端出站网络，详见 AI 库 `知识库/技术/SSH连不上` |

服务端确认公钥认证开关与生效配置：

```bash
sudo sshd -T | grep -E 'pubkeyauthentication|authorizedkeysfile|port'
```

## 服务端加固（sshd_config）

### 基础加固

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak   # 先备份
sudo vi /etc/ssh/sshd_config
#   PermitRootLogin no          禁止 root 交互登录
#   PasswordAuthentication no   关闭密码认证
#   Port 2222                   修改监听端口
sudo sshd -t
sudo systemctl restart ssh
```

### 空闲超时（ClientAlive）

`ClientAliveInterval` 是 sshd 的客户端存活探测间隔，单位为秒，记为 $I$。`ClientAliveCountMax` 是允许连续发送但未收到客户端响应的探测消息数，记为 $N$。无响应断开时间记为 $D$：

$$
\begin{aligned}
I = 0 &\Rightarrow \text{不发送客户端存活探测} \\
I > 0 \land N = 0 &\Rightarrow \text{不触发连接终止} \\
I > 0 \land N > 0 &\Rightarrow D \approx I \times N
\end{aligned}
$$

安全检查要求 $I \in [600, 900]$。若目标断开时间约为 600 秒，设置：

```ssh-config
ClientAliveInterval 600
ClientAliveCountMax 1
```

若目标断开时间约为 900 秒，设置：

```ssh-config
ClientAliveInterval 900
ClientAliveCountMax 1
```

图 2 给出存活探测与断开条件。

```mermaid
sequenceDiagram
    box 客户端
        participant C as SSH 客户端
    end

    box 服务器
        participant S as sshd
    end

    C->>S: 会话数据
    Note over C,S: t=0：sshd 重置接收计时器
    Note over C,S: 连续 I 秒未收到客户端数据

    S->>C: Client Alive 请求（加密通道）

    alt 客户端正常响应
        C-->>S: Client Alive 响应
        Note over C,S: 连接保持，探测计时器重置
    else 客户端连续 N 次无响应
        loop N 次
            S->>C: Client Alive 请求
        end
        Note over S: t ≈ I × N
        S->>C: 断开连接
    end
```

**图 2：SSH ClientAlive 探测时序**

图 2 的不变量为：`ClientAliveInterval` 决定探测周期，`ClientAliveCountMax` 决定无响应容忍次数；客户端正常响应时，即使用户没有键盘输入，连接仍保持。因此该参数检测的是客户端或传输层无响应，不等价于用户无输入超时。

应用与验证：

```bash
sudo vi /etc/ssh/sshd_config
sudo sshd -t
sudo systemctl restart ssh
sudo sshd -T | grep -Ei 'clientalive(interval|countmax)'
```

期望输出：

```text
clientaliveinterval 600
clientalivecountmax 1
```

回滚：

```bash
sudo cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config
sudo sshd -t
sudo systemctl restart ssh
```

配置变更前保留备份。配置导致连接失败时，通过云控制台 VNC 或救援控制台恢复备份。

外部可达性由系统防火墙与云厂商安全组共同决定；两者均需放行监听端口。排查流程见 AI 库 `知识库/技术/SSH连不上` 与 [[端口与进程]]。

## 仅密钥登录与 fail2ban 自动封禁

### 目标约束

设允许认证方法集合为 $A$，观察窗口为 $T$，源地址 $I$ 在窗口内的认证失败次数为 $n(I,T)$，封禁阈值为 $N$。目标条件为：

$$
A=\{\text{publickey}\}
$$

$$
n(I,T)\geq N\Rightarrow \operatorname{ban}(I)
$$

一次失败即封时取 $N=1$。

### sshd 配置

现代 OpenSSH 使用 drop-in 文件：

```bash
sudo tee /etc/ssh/sshd_config.d/99-only-pubkey.conf > /dev/null <<'EOF'
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
AuthenticationMethods publickey
PermitRootLogin prohibit-password
MaxAuthTries 3
EOF
sudo sshd -t
sudo systemctl reload ssh
```

旧版 OpenSSH 将 `KbdInteractiveAuthentication no` 替换为 `ChallengeResponseAuthentication no`。

### fail2ban 监狱

Debian / Ubuntu 使用 `/var/log/auth.log`；RHEL 系使用 `backend = systemd` 或 `/var/log/secure`。Debian / Ubuntu 配置：

```bash
sudo tee /etc/fail2ban/jail.d/sshd.local > /dev/null <<'EOF'
[sshd]
enabled = true
port = ssh
filter = sshd[mode=aggressive]
logpath = /var/log/auth.log
maxretry = 1
findtime = 10m
bantime = 1h
EOF
sudo fail2ban-client -t
sudo systemctl enable --now fail2ban
sudo systemctl restart fail2ban
```

自定义 SSH 端口时，将 `port = ssh` 改为实际端口。固定管理 IP 可在 `[DEFAULT]` 中设置 `ignoreip`。

### 封禁时序

```mermaid
sequenceDiagram
    participant C as 客户端
    participant S as sshd
    participant L as 认证日志
    participant F as fail2ban
    participant W as 防火墙

    C->>S: 发起非公钥认证
    S-->>C: 拒绝认证
    S->>L: 记录认证失败或预认证断开
    L->>F: sshd aggressive 过滤器匹配
    F->>W: 写入源地址封禁规则
    W-->>C: 后续连接被丢弃
```

**图 3：SSH 非公钥认证与 fail2ban 封禁**

图 3 的不变量为：封禁对象是源 IP，封禁动作由防火墙执行；关闭密码认证后，aggressive 模式也会匹配预认证断开和无效用户事件。

### 验证与回滚

验证密码认证关闭：

```bash
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no <用户>@<服务器地址>
```

查看监狱状态：

```bash
sudo fail2ban-client status sshd
```

手动解封：

```bash
sudo fail2ban-client set sshd unbanip <IP>
```

回滚时删除 `/etc/ssh/sshd_config.d/99-only-pubkey.conf` 与 fail2ban 监狱配置，再分别重载 sshd 和 fail2ban。

## 传文件

```bash
scp 本地文件 devuser@<IP>:/remote/path    # 本地 → 远程
scp devuser@<IP>:/remote/file ./           # 远程 → 本地
scp -r 目录 devuser@<IP>:/remote/path      # 目录加 -r
```

也可以 `sftp devuser@<IP>` 进入交互式传文件。

## 参考资料

- [OpenSSH sshd_config 手册：ClientAliveInterval 与 ClientAliveCountMax](https://manpages.ubuntu.com/manpages/focal/man5/sshd_config.5.html)
- [fail2ban 官方 jail 配置](https://github.com/fail2ban/fail2ban/blob/master/config/jail.conf)
- [fail2ban sshd 过滤器](https://github.com/fail2ban/fail2ban/blob/master/config/filter.d/sshd.conf)
- [堡塔终端客户端使用 ED25519 密钥报错的案例](https://www.bt.cn/bbs/thread-49742-1-1.html)
- [堡塔终端解析加密私钥时要求 passphrase 的案例](https://www.bt.cn/bbs/thread-142814-1-1.html)
- [宝塔面板 SSH 基础设置文档](https://docs.bt.cn/user-guide/security/ssh/basic-settings)

## 关联

- [[从零上手]]：买服务器后从登录、加固到部署的完整流程。
- AI 库 `知识库/技术/SSH连不上`：端口、安全组、fail2ban 与凭据失败的逐层排查。
- [[端口与进程]]：端口占用与连通性排查。
- [[vscode]]：用 remote-ssh 在编辑器里直连服务器。