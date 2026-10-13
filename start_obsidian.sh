#!/bin/bash
# WSL2 Ubuntu 启动当前目录作为 Obsidian 库
# 获取当前目录在 Windows 的路径（wslpath 转换）
VAULT_WIN_PATH=$(wslpath -m "$PWD")

# Obsidian.exe Windows 路径
OBSIDIAN_EXE="/mnt/d/app/notes/Obsidian/Obsidian.exe"

LOG_DIR="./log"
LOG_FILE="${LOG_DIR}/obsidian.log"

# 判断日志目录，不存在则创建
if [ ! -d "${LOG_DIR}" ]; then
	mkdir -p "${LOG_DIR}"
fi

# 判断日志文件是否存在
if [ ! -d "${LOG_FILE}" ]; then
	touch "${LOG_FILE}" 
fi

# 获取当前脚本PID
SCRIPT_PID=$$
MSG="脚本自身进程 PID:${SCRIPT_PID}"
# 输出到终端
echo "${MSG}"
# 写入日志
echo "[$(date +'+%Y-%m-%d %H:%M:%S')] ${MSG}" > "${LOG_FILE}"

# 检查Windows 侧Obsidian是否已启动
# tasklist /nh 列出进程，findstr 查找Obsidian.exe
if cmd.exe /c tasklist /nh | grep -qi "Obsidian.exe"; then
	INFO="检测到 Obsidian 已在Windows 运行，无需启动"
	echo "${INFO}"
	echo "[$(date +'+%Y-%m-%d %H:%M:%S')] ${INFO}" >> "${LOG_FILE}"
	exit 0
fi

# 启动 Obsidian，打开当前仓库
"$OBSIDIAN_EXE" "$VAULT_WIN_PATH" >> "${LOG_FILE}" 2>&1 &
OBS_PID=$!
MSG_OBS="Obsidian 后台子进程 PID（WSL侧）:${OBS_PID}" 
echo "${MSG_OBS}"
echo "[$(date +'+%Y-%m-%d %H:%M:%S')] ${MSG_OBS}" >> "${LOG_FILE}"
