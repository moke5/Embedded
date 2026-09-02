# cc-connect 企业微信接入 Claude Code

### 目录

[toc]



## 简介

cc-connect 是一个将 AI 编程代理（Claude Code、Cursor 等）桥接到消息平台的工具，支持企业微信、飞书、钉钉、Telegram 等。

项目地址：https://github.com/chenhg5/cc-connect

## 安装

```bash
npm install -g cc-connect
```

## 配置文件

位置：`~/.cc-connect/config.toml`

```toml
[log]
level = "info"

[[projects]]
name = "wechat"

[projects.agent]
type = "claudecode"

[projects.agent.options]
command = "claude"

[[projects.platforms]]
type = "wecom"

[projects.platforms.options]
mode = "webhook"
corp_id = "你的企业ID"
corp_secret = "应用密钥"
agent_id = "应用ID"
callback_token = "回调Token"
callback_aes_key = "回调AESKey"
port = "8081"
callback_path = "/wecom/callback"
enable_markdown = false
```

## 企业微信配置步骤

### 1. 注册企业微信

- 访问 https://work.weixin.qq.com/
- 选择「企业注册」→「其他组织」类型
- 个人可免费注册，不需要真实企业

### 2. 创建自建应用

- 登录管理后台 → 应用管理 → 自建 → 创建应用
- 记录 **AgentId** 和 **Secret**
- 在「我的企业」页面底部获取 **CorpId**（企业ID）

### 3. 配置接收消息

进入应用 → 接收消息 → 设置 API 接收：
- **URL**: `https://你的公网域名/wecom/callback`
- **Token**: 自定义字符串
- **EncodingAESKey**: 自定义或随机生成

### 4. 配置公网访问

使用 cloudflared（免费）暴露本地服务：

```bash
# 安装
winget install Cloudflare.cloudflared

# 启动（会生成临时公网 URL）
cloudflared tunnel --url http://localhost:8081
```

将输出的 `https://xxx.trycloudflare.com` 加上 `/wecom/callback` 填入企业微信回调 URL。

### 5. 添加可信 IP

企业微信会报错提示需要添加的 IP，按提示添加即可。

查看当前出口 IP：
```bash
curl.exe -s https://api.ipify.org
```

### 6. 关联个人微信（可选）

企业微信后台 → 我的企业 → 微信插件 → 扫码关联
关联后个人微信也能直接对话。
找不到机器人时，先在企业微信里给机器人发一条消息。

## 启动服务

```bash
# 终端 1：启动 cc-connect
cc-connect

# 终端 2：启动 cloudflared
cloudflared tunnel --url http://localhost:8081
```

## 注意事项

- cloudflared quick tunnel 每次重启会生成新 URL，需重新配置回调
- 长期使用建议注册 Cloudflare 账号创建固定 tunnel
- `enable_markdown = false` 时个人微信可正常显示，设为 true 仅企业微信应用内可渲染
- 可信 IP 可能会变化，如果突然无法收发消息，检查 IP 是否需要更新

## 常见问题

**Q: 发送消息无回复？**
检查 cc-connect 终端日志，常见原因是可信 IP 未配置或已变更。

**Q: 报错 60020？**
IP 不在白名单，按日志提示的 IP 添加到企业可信 IP。

**Q: cloudflared 重启后失效？**
每次重启会生成新 URL，需要重新配置企业微信回调 URL。



# 会话管理

● cc-connect 的会话机制：

  会话管理
  - 会话内保持历史（同一个对话上下文）
  - 空闲 30 分钟后自动轮换新会话（防止上下文漂移）
  - 手动控制：/new 新会话、/list 列出会话、/switch 切换

  与 Claude Code 的关系
  - 每条消息调用一次 claude 命令
  - 读取当前目录的 CLAUDE.md（跟你本地终端一样）
  - 记忆系统（~/.claude/projects/）共享，但每个会话是独立上下文
