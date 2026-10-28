#!/usr/bin/env python3
"""校验笔记 frontmatter、命名与敏感信息。

用法：
    python script/notes_lint.py            # 全量扫描
    python script/notes_lint.py --strict   # 缺少 frontmatter 也算错误
    python script/notes_lint.py --changed  # 只检查暂存区（供 pre-commit 调用）

退出码：0 无错误；1 有错误；2 环境或 git 调用失败。
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    print("缺少 PyYAML：python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = ("type", "tags", "status", "created", "updated")
TYPES = {
    "概念", "课程", "实验", "踩坑", "读书", "项目", "对比",
    "自测", "练习", "复习", "MOC", "工具",
}
STATUSES = {"进行中", "已完成", "待整理"}
TARGETS = {"流体", "晶体"}

TEXT_SUFFIXES = {
    ".md", ".sh", ".ps1", ".py", ".json", ".yaml", ".yml",
    ".txt", ".conf", ".ini", ".toml", ".env",
}
SKIP_DIRS = {".git", "self", "img", ".obsidian", ".trash", "node_modules", ".skills", "log"}
SKIP_PREFIXES = ("script/log/",)
EXEMPT_NAMES = {
    "README.md", "readme.md", "AGENTS.md", "CLAUDE.md",
    "模板说明.md", "README模板.md",
}
EXEMPT_TOP_DIRS = {"模板"}

NAME_WHITELIST = {
    "ai", "api", "adc", "dac", "pwm", "uart", "usart", "i2c", "spi", "can",
    "rs485", "modbus", "zigbee", "ble", "wifi", "lorawan", "nbiot", "coap",
    "mqtt", "mqttx", "emqx", "http", "https", "tcp", "udp", "ip", "dns",
    "dhcp", "ntp", "tls", "ssl", "ota", "gdb", "jtag", "swd", "openocd",
    "make", "cmake", "gcc", "clang", "keil", "mdk", "iar", "stlink", "jlink",
    "linux", "ubuntu", "debian", "centos", "arch", "kali", "wsl", "vmware",
    "virtualbox", "hyperv", "windows", "powershell", "cmd", "bash", "zsh",
    "fish", "vim", "neovim", "emacs", "tmux", "screen", "curl", "wget",
    "grep", "sed", "awk", "find", "tar", "zip", "unzip", "crontab", "systemd",
    "docker", "git", "nginx", "redis", "mysql", "sqlite", "tomcat", "java",
    "python", "node", "npm", "yaml", "json", "toml", "xml", "html", "css",
    "javascript", "typescript", "react", "vue", "lvgl", "stm32", "esp32",
    "esp8266", "cc2530", "freertos", "rtos", "stm32cubemx", "cubemx",
    "vscode", "typora", "katex", "markdown", "obsidian", "excel", "word",
    "pdf", "ssh", "scp", "sftp", "ftp", "samba", "nfs", "vpn", "proxy",
    "clash", "v2ray", "frp", "ngrok", "gitlab", "github", "gitee",
    "jenkins", "ansible", "terraform", "k8s", "kubernetes", "podman",
    "claude", "cc-connect",
}
# 这些目录属于资料/附件，数字前缀不算违规。
MATERIAL_DIRS = {"资料", "附件", "开题报告", "任务书"}

FM_RE = re.compile(r"\A\ufeff?---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
RELATED_RE = re.compile(r"^\[\[.+\]\]$")

PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |PGP )?PRIVATE KEY-----"
)
TOKEN_RES = (
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{20,}=*"),
)
ASSIGN_RE = re.compile(
    r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key)\b"
    r"[\"']?\s*[:=]\s*[\"']?([^\s\"'`]+)"
)
PHONE_RE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
ID_RE = re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")
IPV4_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
IP_CONTEXT_RE = re.compile(
    r"(?i)(公网|服务器|主机|ssh|scp|sftp|root@|部署|host|server)"
)
IP_SKIP_RE = re.compile(
    r"(?i)(dns|nameserver|resolv|示例|example|掩码|子网|广播|组播|ntp|地址范围|网段)"
)
PLACEHOLDER_RE = re.compile(
    r"(?i)(your|example|placeholder|changeme|redacted|todo|\*\*\*|<[^>]+>|\{[^}]+\}|\.\.\.)"
)

def rel_posix(path: Path) -> str:
    return path.as_posix()


def is_skipped(rel: Path) -> bool:
    if any(part in SKIP_DIRS for part in rel.parts):
        return True
    return rel_posix(rel).startswith(SKIP_PREFIXES)


def parse_date(value):
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def parse_frontmatter(text: str):
    match = FM_RE.match(text)
    if not match:
        return None, None
    try:
        data = yaml.safe_load(match.group(1))
    except (yaml.YAMLError, ValueError) as exc:
        return None, str(exc).replace("\n", " ")
    if not isinstance(data, dict):
        return None, "frontmatter 不是键值映射"
    return data, None


def check_frontmatter(rel: Path, text: str, is_new: bool, strict: bool):
    issues = []
    if rel.suffix.lower() != ".md":
        return issues
    exempt = rel.name in EXEMPT_NAMES or (rel.parts and rel.parts[0] in EXEMPT_TOP_DIRS)
    if exempt:
        return issues

    data, error = parse_frontmatter(text)

    if data is None:
        if error:
            issues.append(("ERROR", rel, 1, f"frontmatter YAML 解析失败：{error}"))
        elif is_new or strict:
            issues.append(("ERROR", rel, 1, "笔记缺少 frontmatter"))
        else:
            issues.append(("WARN", rel, 1, "缺少 frontmatter"))
        return issues

    for key in REQUIRED:
        if key not in data or data[key] is None or (
            isinstance(data[key], str) and not data[key].strip()
        ):
            severity = "ERROR" if (is_new or strict) else "WARN"
            issues.append((severity, rel, 1, f"缺少必填字段 {key}"))

    type_value = data.get("type")
    if type_value is not None and (
        not isinstance(type_value, str) or type_value not in TYPES
    ):
        issues.append(("ERROR", rel, 1, f"type 取值无效：{type_value!r}"))

    status_value = data.get("status")
    if status_value is not None and (
        not isinstance(status_value, str) or status_value not in STATUSES
    ):
        issues.append(("ERROR", rel, 1, f"status 取值无效：{status_value!r}"))

    tags = data.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            issues.append(("ERROR", rel, 1, "tags 应为列表"))
        elif not tags:
            issues.append(("ERROR" if is_new else "WARN", rel, 1, "tags 为空"))
        elif any(not isinstance(tag, str) or not tag.strip() for tag in tags):
            issues.append(("ERROR", rel, 1, "tags 含空值或非字符串"))

    created = parse_date(data.get("created"))
    updated = parse_date(data.get("updated"))
    if data.get("created") is not None and created is None:
        issues.append(("ERROR", rel, 1, "created 不是 YYYY-MM-DD"))
    if data.get("updated") is not None and updated is None:
        issues.append(("ERROR", rel, 1, "updated 不是 YYYY-MM-DD"))
    if created and updated and updated < created:
        issues.append(("WARN", rel, 1, "updated 早于 created"))

    target = data.get("target")
    if target not in (None, ""):
        if not isinstance(target, str) or target not in TARGETS:
            issues.append(("WARN", rel, 1, f"target 取值不在 {{流体, 晶体}}：{target!r}"))

    review = data.get("review")
    if review not in (None, ""):
        if parse_date(review) is None:
            issues.append(("WARN", rel, 1, "review 不是 YYYY-MM-DD"))

    related = data.get("related")
    if related not in (None, []):
        if not isinstance(related, list):
            issues.append(("ERROR", rel, 1, "related 应为字符串列表，例如 [\"[[笔记]]\"]"))
        else:
            for item in related:
                if not isinstance(item, str):
                    issues.append(("ERROR", rel, 1, "related 含非字符串项"))
                elif not RELATED_RE.match(item.strip()):
                    issues.append(("WARN", rel, 1, f"related 项不是 [[双链]]：{item!r}"))

    for key in ("input", "output"):
        value = data.get(key)
        if value not in (None, "") and not isinstance(value, str):
            issues.append(("WARN", rel, 1, f"{key} 应为字符串"))

    return issues


def scan_secrets(rel: Path, text: str):
    issues = []
    lines = text.splitlines()
    for lineno, line in enumerate(lines, 1):
        if PRIVATE_KEY_RE.search(line) and "`" not in line:
            window = "\n".join(lines[lineno:lineno + 5])
            if re.search(r"[A-Za-z0-9+/=]{40,}", window):
                issues.append(("ERROR", rel, lineno, "疑似私钥"))
                continue

        for pattern in TOKEN_RES:
            if pattern.search(line):
                issues.append(("ERROR", rel, lineno, "疑似访问令牌"))
                break

        for match in ASSIGN_RE.finditer(line):
            key = match.group(1).lower().replace("-", "_")
            value = match.group(2).strip()
            low = value.lower()
            if (
                len(value) < 6
                or PLACEHOLDER_RE.search(value)
                or any(ord(ch) > 127 for ch in value)
                or low.startswith((
                    "$", "${", "os.environ", "getenv", "env.",
                    "null", "none", "undefined", "nil", "true", "false",
                ))
                or re.match(r"[A-Za-z_][A-Za-z0-9_]*\s*\(", value)
            ):
                continue
            if key in {"token", "api_key", "access_key"}:
                if not re.fullmatch(r"[A-Za-z0-9._~+/=-]{20,}", value):
                    continue
            issues.append(("ERROR", rel, lineno, f"疑似明文凭据：{key}"))
            break

        if PHONE_RE.search(line):
            issues.append(("ERROR", rel, lineno, "疑似手机号"))
        if ID_RE.search(line):
            issues.append(("ERROR", rel, lineno, "疑似身份证号"))

        if not IP_CONTEXT_RE.search(line) or IP_SKIP_RE.search(line):
            continue

        for match in IPV4_RE.finditer(line):
            parts = [int(part) for part in match.group().split(".")]
            if any(part > 255 for part in parts):
                continue
            if re.match(r"-\d+\.(?:el|fc|rh|noarch|x86_64|src)", line[match.end():]):
                continue
            first, second = parts[0], parts[1]
            if first == 255:
                continue
            if (
                first in (10, 127)
                or (first == 192 and second == 168)
                or (first == 172 and 16 <= second <= 31)
                or (first == 169 and second == 254)
                or (first == 198 and second in (18, 19))
                or (first == 192 and second == 0)
                or (first == 203 and second == 0)
                or match.group() in ("0.0.0.0", "255.255.255.255")
            ):
                continue
            issues.append((
                "WARN", rel, lineno,
                f"公网 IP {match.group()}：确认非敏感，或移入 self/",
            ))
    return issues


def check_name(rel: Path):
    issues = []
    if rel.suffix.lower() != ".md":
        return issues
    if rel.parts and rel.parts[0] in EXEMPT_TOP_DIRS:
        return issues

    stem = rel.stem
    if re.fullmatch(r"[a-z0-9._-]+", stem) and stem not in NAME_WHITELIST:
        issues.append((
            "WARN", rel, 0,
            "英文小写文件名：通用词应改中文，专名需可判定",
        ))

    has_material = any(part in MATERIAL_DIRS for part in rel.parts[:-1])
    if not has_material:
        for part in rel.parts[:-1]:
            if re.match(r"^\d+[-_]", part):
                issues.append((
                    "WARN", rel, 0,
                    f"目录含数字前缀：{part}",
                ))
                break
    return issues


def iter_all():
    try:
        raw = subprocess.run(
            ["git", "ls-files", "-z", "-co", "--exclude-standard"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"git 调用失败：{exc}", file=sys.stderr)
        sys.exit(2)

    for part in sorted(raw.split(b"\0")):
        if not part:
            continue
        rel = Path(part.decode("utf-8", "replace"))
        if rel.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if is_skipped(rel) or not (ROOT / rel).is_file():
            continue
        yield rel


def staged_files():
    cmd = [
        "git", "diff", "--cached", "--name-status", "-z",
        "--diff-filter=ACMR",
    ]
    try:
        raw = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"git 调用失败：{exc}", file=sys.stderr)
        sys.exit(2)

    parts = raw.split(b"\0")
    items = []
    index = 0
    while index < len(parts) and parts[index]:
        status = parts[index].decode("utf-8", "replace")
        index += 1
        if status[:1] in ("R", "C"):
            index += 1  # 旧路径
        if index >= len(parts):
            break
        path = parts[index].decode("utf-8", "replace")
        index += 1
        if Path(path).suffix.lower() in TEXT_SUFFIXES:
            items.append((path, status[:1] == "A"))
    return items


def read_staged(path: str) -> str:
    try:
        raw = subprocess.run(
            ["git", "show", f":{path}"],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        return raw.decode("utf-8-sig", "replace")
    except (OSError, subprocess.CalledProcessError):
        return (ROOT / path).read_text(encoding="utf-8-sig", errors="replace")


def category(message: str) -> str:
    prefixes = (
        "缺少必填字段", "缺少 frontmatter", "frontmatter YAML",
        "tags 为空", "公网 IP", "英文小写文件名", "目录含数字前缀",
        "related", "target", "review", "updated", "input", "output",
    )
    for prefix in prefixes:
        if message.startswith(prefix):
            return prefix
    return message.split("：", 1)[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="校验笔记 frontmatter 与敏感信息")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--changed", action="store_true", help="只检查暂存区")
    group.add_argument("--all", action="store_true", help="全量扫描（默认）")
    parser.add_argument("--strict", action="store_true", help="缺少 frontmatter 也算错误")
    parser.add_argument("--quiet", action="store_true", help="只输出汇总")
    args = parser.parse_args()

    issues = []
    if args.changed:
        targets = [(Path(p), s) for p, s in staged_files()]
    else:
        targets = [(rel, False) for rel in iter_all()]

    for rel, is_new in targets:
        if is_skipped(rel):
            continue
        text = read_staged(rel.as_posix()) if args.changed else (
            ROOT / rel
        ).read_text(encoding="utf-8-sig", errors="replace")

        file_issues = check_frontmatter(rel, text, is_new, args.strict)
        file_issues += scan_secrets(rel, text)
        file_issues += check_name(rel)
        issues.extend(file_issues)

    errors = sum(1 for item in issues if item[0] == "ERROR")
    warnings = len(issues) - errors

    if not args.quiet:
        for severity, rel, lineno, message in issues:
            location = f"{rel.as_posix()}:{lineno}" if lineno else rel.as_posix()
            print(f"[{severity}] {location}  {message}")

    print(f"\n扫描 {len(targets)} 个文件：错误 {errors}，警告 {warnings}")
    if issues:
        counts = Counter(category(message) for _, _, _, message in issues)
        detail = "，".join(f"{name} {count}" for name, count in counts.most_common())
        print(f"分类：{detail}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
