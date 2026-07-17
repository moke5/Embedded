# SSH

## ubuntu



- 服务端

```shell
sudo apt update
sudo apt install openssh-server -y
```



- 安装完成后验证

```bash
# 查看服务状态
systemctl status ssh
# 设置开机自启并立即启动
sudo systemctl enable --now ssh
# 查看22端口监听
ss -tulpn | grep 22
```