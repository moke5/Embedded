---
type: 踩坑
tags: [服务器, ssh, 阿里云, 网络, fail2ban]
status: 已完成
target: 流体
input: 新购阿里云 ECS 首次 SSH 登录
output: 端口级连通性排查流程、fail2ban 自封机制与解封步骤
review: 2026-11-17
created: 2026-10-22
updated: 2026-10-29
related: ["[[从零上手]]", "[[ssh]]", "[[配置记录]]", "[[从零上手]]"]
---
# SSH 连不上

> 场景：阿里云 ECS（Ubuntu 22.04，2 vCPU / 4 GiB）购买后未配置，本地 Windows 执行 `ssh root@<公网IP>` 超时，ping 正常。

## 现象

- `ping <公网IP>` 有回复，延迟约 20 ms。
- TCP 22 连接超时，无 `Connection refused`。
- 阿里云控制台 Workbench 可以登录。
- 同一网络访问 `github.com:22`、`portquiz.net:22` 同样超时。

## 环境

- 客户端：Windows 10/11，OpenSSH for Windows。
- 服务端：阿里云 ECS，Ubuntu 22.04，安全组规则未核对。
- 网络：本地宽带/校园网，出口 IP 见 [self/local.md](../../self/local.md)。

## 排查过程

1. `ping` 通，排除实例停机、路由中断与 ICMP 拦截。
2. 探测目标端口：22 超时，80/443 也超时，说明安全组未放行 Web 端口或服务未启动。
3. 做对照组，区分"实例问题"与"本地网络问题"：

| 探测目标 | 结果 | 含义 |
| --- | --- | --- |
| `portquiz.net:22` | 超时 | 出站 22 被本地网络拦截 |
| `portquiz.net:2222` | 通 | 高位端口未被拦截 |
| `portquiz.net:2552` | 通 | 同上 |
| `portquiz.net:443` | 通 | 443 正常 |
| `github.com:22` | 超时 | 二次确认 22 被拦截 |

4. Workbench 登入后检查 `ss -tulpn | grep ':22'` 与 `systemctl status ssh`，确认 sshd 监听 `0.0.0.0:22`。
5. 控制台安全组入方向已放行 22。三层服务端条件全部满足，只剩客户端出站一项不满足。

结论：服务端已确认 sshd 监听 `0.0.0.0:22`、安全组已放行 22，实例配置不构成阻断；**本地网络封锁出站 TCP 22** 是当前唯一未满足的条件。

## 根因

SSH 可达性由三个条件合取决定：

```text
可达(22) ⇔ 安全组放行(22) ∧ 系统防火墙放行(22) ∧ sshd 监听(0.0.0.0:22)
```

除此之外，客户端的出网策略与运营商策略是第四个独立变量。本例中客户端网络直接丢弃 22 端口的 SYN，表现为超时而非拒绝。

## 解决

按依赖顺序处理，任一路径可恢复登录。

**A. 绕开本地 22 封锁：换 SSH 端口**

```bash
# 服务器上（Workbench 内）
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo sed -i 's/^#\?Port .*/Port 2222/' /etc/ssh/sshd_config
sudo sshd -t
sudo systemctl restart ssh

# 系统防火墙
sudo ufw allow 2222/tcp
```

安全组入方向追加 `TCP 2222`，来源填当前出口 IP `/32`。本地客户端：

```text
Host <主机名>
    HostName <公网IP>
    User dev
    Port 2222
```

用 `ssh <主机名>` 验证。改端口只减少扫描噪声，认证仍必须走密钥。

本例按 A 执行后的实测结果：本地 TCP 2222 可达，banner 为 `SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.17`，未提供凭据时返回 `Permission denied (publickey,password)`；22 仍然超时。

**B. 换网络或使用控制台**

手机热点、VPN 可绕开本地 22 封锁；阿里云 Workbench 完全不经过本地 SSH，适合作为复位通道。

**C. 补齐登录凭据**

购买时未设置密码、未绑定密钥对时，端口通了也会得到 `Permission denied`。在控制台「重置实例密码」（重启生效）或绑定密钥对，再按 [[从零上手]] 第二、三节建立普通用户。

## 追加案例：fail2ban 封禁本机直连出口

### 现象

- 端口改为 2222 后曾可登录；安装宝塔面板后，本地 SSH 再次超时，ping 与面板端口正常。
- 服务端三层条件均满足：`sshd` 监听 `0.0.0.0:2222`，`ufw` 放行 2222，安全组 2222 来源为 `0.0.0.0/0`。
- `fail2ban-client status sshd` 显示封禁两个 IP；本地 HTTP 查询得到的出口 IP 与 SSH 实际源 IP 不同，导致第一轮排查误判。

### 证据

`tcpdump -ni any tcp port 2222` 只见入站 SYN，源 IP 与 `f2b-sshd` 链的 REJECT 规则逐条对应，无 SYN-ACK。客户端收不到响应，表现为超时。

`iptables -S f2b-sshd` 的拒绝动作为 `REJECT --reject-with icmp-port-unreachable`，返回的是 ICMP；`tcpdump` 的 `tcp port 2222` 过滤器不显示该回包，因此现场呈现为"有 SYN 无响应"。

### 根因

#### 封禁原因

`sshd` jail 的参数为 `maxretry = 5`、`findtime = 10m`、`bantime = 1h`：同一源 IP 在 10 分钟内累计 5 次认证失败，即被封禁 1 小时。

root 已设 `PermitRootLogin prohibit-password`，以 root 密码登录每次都会失败。此类尝试累计到阈值后，源 IP 被封。封禁对象是源地址，与账号、认证方式无关；同一出口下的所有用户与密钥一并被挡。

设 HTTP(S) 代理出口为 $A$，SSH 直连出口为 $B$。查询 IP 的请求走代理，返回 $A$；SSH 走直连，源地址为 $B$。当 $A \neq B$ 时，用 $A$ 核对封禁列表会得到"本机未被封"的错误结论。本例 $A \neq B$。

#### 解封后密钥登录恢复的原因

封禁发生在 TCP 握手阶段，早于认证：

```text
SYN → 安全组 → iptables INPUT → f2b-sshd → ufw → sshd
```

fail2ban 在 `f2b-sshd` 链插入：

```text
-A f2b-sshd -s <出口IP>/32 -j REJECT --reject-with icmp-port-unreachable
```

SYN 在此被拒绝，sshd 收不到连接，密钥没有机会提交。症状因此是连接超时，而非 `Permission denied`。

可达性由四个条件合取决定：

```text
可达(2222) ⇔ 安全组放行(2222) ∧ ¬fail2ban封禁(源IP) ∧ ufw放行(2222) ∧ sshd监听(2222)
```

`unbanip` 删除该 REJECT 规则，其余三项原本满足，连接与密钥认证随即恢复。`fail2ban-client status sshd` 只读取状态，不解封。

REJECT 回送 ICMP；`tcpdump` 的 `tcp port 2222` 过滤器看不到该回包，现场表现为"有 SYN、无 SYN-ACK"。

### 解封

```bash
# 1. 确认封禁列表
sudo fail2ban-client status sshd

# 2. 解封，可一次写多个 IP
sudo fail2ban-client set sshd unbanip <出口IP>

# 3. 确认规则已删除
sudo iptables -S f2b-sshd
sudo fail2ban-client status sshd
```

本地用密钥登录：

```powershell
ssh -p 2222 <用户>@<公网IP> -i $env:USERPROFILE\.ssh\id_ed25519 -o IdentitiesOnly=yes
```

可选白名单，写入 `/etc/fail2ban/jail.local` 的 `[sshd]` 段：

```ini
[sshd]
ignoreip = 127.0.0.1/8 ::1 <出口IP>
```

```bash
sudo systemctl restart fail2ban
```

白名单仅登记可信的静态出口；出口变化后及时更新。扫描器地址保持封禁。

不手动解封时，`bantime = 1h` 到期后自动解封。继续以 root 密码尝试会重新触发封禁。

## 预防

- 新实例先用 Workbench 登录，确认 sshd 状态，再折腾本地 SSH。
- 判断"服务器问题"前，先拿 `portquiz.net` 做同端口对照，成本一个命令。
- 查出口 IP 时注意代理：HTTP(S) 代理与 SSH 直连的源地址可能不同，以服务端 `tcpdump` 或 sshd 日志中的源 IP 为准。
- fail2ban 按地址和端口封禁：只有 SSH 失效而面板、Web 正常时，优先检查封禁列表。
- 安全组 SSH 来源限定为具体出口 IP `/32`；出口 IP 变化后先更新规则。
- 若两台实例共用一套安全组，改动端口规则会同时影响两台，先核对 `sg-` 编号。
- 每次操作写入 [[配置记录]]，记录目的、命令、结果与回滚方式。

## 相关笔记

- [[从零上手]]
