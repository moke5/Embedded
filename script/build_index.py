#!/usr/bin/env python3
"""从 frontmatter 生成知识分层索引。

用法：
    python script/build_index.py           # 生成 知识地图/*.md
    python script/build_index.py --check   # 只校验，不写文件

退出码：0 无错误；1 有非法 layer/domain；2 环境失败。
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
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
OUT_DIR = ROOT / "知识地图"
FM_RE = re.compile(r"\A\ufeff?---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
WIKI_RE = re.compile(r"\[\[([^\[\]]+?)\]\]")

SKIP_DIRS = {
    ".git", "self", "img", ".obsidian", ".trash", "node_modules",
    ".skills", "log", "temp", "规范", "本机", "模板", "script", "知识地图",
}
SKIP_NAMES = {
    "README.md", "readme.md", "AGENTS.md", "CLAUDE.md",
    "模板说明.md", "README模板.md",
}

LAYERS = [
    ("L0", "物理与电路", "能读电路图、选元件、画 PCB、焊接与调试硬件"),
    ("L1", "芯片与外设", "能配置时钟、GPIO、中断、定时器、ADC、DMA 与总线"),
    ("L2", "驱动与固件", "能写寄存器/HAL 驱动并做分层封装与状态管理"),
    ("L3", "实时与内核", "能用 RTOS 调度/同步，理解 Linux 进程、线程、IPC、VFS"),
    ("L4", "系统编程与构建", "能用 C/数据结构/编译链接/构建工具组织可维护代码"),
    ("L5", "网络与协议", "能实现 socket 通信并接入常见应用协议与无线链路"),
    ("L6", "应用与交互", "能完成 GUI、上位机、小程序与云端交互"),
    ("L7", "集成与产品", "能软硬协同、测试、部署并交付完整项目"),
    ("X", "工具与方法", "能用工具链、服务器、AI 与规范提升效率"),
]
DOMAINS = [
    ("hardware", "硬件"),
    ("mcu", "MCU"),
    ("rtos", "RTOS"),
    ("linux", "Linux"),
    ("network", "网络"),
    ("gui", "GUI"),
    ("tool", "工具"),
    ("project", "项目"),
]
LAYER_CODES = {code for code, _, _ in LAYERS}
DOMAIN_CODES = {code for code, _ in DOMAINS}


def iter_notes():
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if rel.name in SKIP_NAMES:
            continue
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        match = FM_RE.match(text)
        if not match:
            continue
        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        if data.get("type") == "MOC":
            continue
        yield rel, data


def link(rel: Path, title: str | None = None) -> str:
    target = rel.with_suffix("").as_posix()
    label = title or rel.stem
    return f"[[{target}|{label}]]"


def sorted_notes(notes):
    return sorted(notes, key=lambda item: item[0].as_posix())


def build_layer_index(notes) -> str:
    lines = [
        "# 层级索引",
        "",
        "> 由 `script/build_index.py` 从 frontmatter 生成，请勿手工修改。",
        "",
    ]
    for code, name, desc in LAYERS:
        lines.append(f"## {code} {name}")
        lines.append("")
        lines.append(f"> {desc}")
        lines.append("")
        items = [n for n in notes if n[1].get("layer") == code]
        if items:
            for rel, data in sorted_notes(items):
                lines.append(
                    f"- {link(rel)} — `{data.get('domain', '未标注')}` / {data.get('type', '')}"
                )
        else:
            lines.append("- （暂无）")
        lines.append("")
    unmarked = [n for n in notes if not n[1].get("layer")]
    lines.append("## 未标注")
    lines.append("")
    if unmarked:
        for rel, _ in sorted_notes(unmarked):
            lines.append(f"- {link(rel)} — 待补 `layer` / `domain`")
    else:
        lines.append("- （无）")
    lines.append("")
    return "\n".join(lines)


def build_domain_index(notes) -> str:
    lines = [
        "# 领域索引",
        "",
        "> 由 `script/build_index.py` 从 frontmatter 生成，请勿手工修改。",
        "",
    ]
    for code, name in DOMAINS:
        items = [n for n in notes if n[1].get("domain") == code]
        lines.append(f"## {name}（`{code}`）")
        lines.append("")
        if items:
            for rel, data in sorted_notes(items):
                lines.append(
                    f"- {link(rel)} — `{data.get('layer', '未标注')}` / {data.get('type', '')}"
                )
        else:
            lines.append("- （暂无）")
        lines.append("")
    unmarked = [n for n in notes if not n[1].get("domain")]
    lines.append("## 未标注")
    lines.append("")
    if unmarked:
        for rel, _ in sorted_notes(unmarked):
            lines.append(f"- {link(rel)} — 待补 `domain`")
    else:
        lines.append("- （无）")
    lines.append("")
    return "\n".join(lines)


def build_dependency_index(notes) -> str:
    by_target = {}
    for rel, data in notes:
        by_target[rel.with_suffix("").as_posix()] = (rel, data)
        by_target.setdefault(rel.stem, (rel, data))

    node_ids = {rel.as_posix(): f"n{idx}" for idx, (rel, _) in enumerate(notes)}
    lines = [
        "# 依赖关系",
        "",
        "> 由 `prereq` 生成；箭头 `A --> B` 表示 A 依赖 B。",
        "",
        "```mermaid",
        "graph TD",
    ]
    edges = []
    for rel, data in notes:
        prereqs = data.get("prereq") or []
        if not isinstance(prereqs, list):
            continue
        for item in prereqs:
            match = WIKI_RE.match(str(item).strip())
            if not match:
                continue
            target = match.group(1).split("|")[0].split("#")[0].strip()
            found = by_target.get(target)
            if not found:
                continue
            source_id = node_ids[rel.as_posix()]
            target_id = node_ids[found[0].as_posix()]
            source_label = rel.stem.replace('"', "'")
            target_label = found[0].stem.replace('"', "'")
            edges.append(
                f'    {source_id}["{source_label}"] --> {target_id}["{target_label}"]'
            )
    if edges:
        lines.extend(edges)
    else:
        lines.append("    empty[暂无 prereq 关系]")
    lines.extend(["```", ""])
    return "\n".join(lines)


def check(notes) -> int:
    errors = 0
    for rel, data in notes:
        layer = data.get("layer")
        if layer not in (None, "") and layer not in LAYER_CODES:
            print(f"ERROR {rel}: layer 取值无效 {layer!r}")
            errors += 1
        domain = data.get("domain")
        if domain not in (None, "") and domain not in DOMAIN_CODES:
            print(f"ERROR {rel}: domain 取值无效 {domain!r}")
            errors += 1
    unmarked = sum(1 for _, data in notes if not data.get("layer"))
    print(f"扫描 {len(notes)} 篇；未标注 layer {unmarked} 篇；错误 {errors}")
    return 1 if errors else 0


def write_indexes(notes) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    files = {
        OUT_DIR / "层级索引.md": build_layer_index(notes),
        OUT_DIR / "领域索引.md": build_domain_index(notes),
        OUT_DIR / "依赖关系.md": build_dependency_index(notes),
    }
    for path, content in files.items():
        path.write_text(with_frontmatter(path, content), encoding="utf-8")
        print(f"写入 {path.relative_to(ROOT)}")

    moc = OUT_DIR / "MOC.md"
    moc_lines = [
        "# 知识地图 MOC",
        "",
        "> 由 `script/build_index.py` 生成，请勿手工修改。",
        "",
        "## 索引",
        "",
        "- [[知识地图/层级索引|层级索引]] — 按 L0–L7、X 分组",
        "- [[知识地图/领域索引|领域索引]] — 按 domain 分组",
        "- [[知识地图/依赖关系|依赖关系]] — 由 prereq 生成的 Mermaid 图",
        "",
        "## 层级入口",
        "",
    ]
    layer_entries = [
        ("L1-芯片与外设/MOC", "L1 芯片与外设"),
        ("L2-驱动与固件/MOC", "L2 驱动与固件"),
        ("L3-实时与内核/MOC", "L3 实时与内核"),
        ("L4-系统编程与构建/MOC", "L4 系统编程与构建"),
        ("L5-网络与协议/MOC", "L5 网络与协议"),
        ("X-工具与方法/MOC", "X 工具与方法"),
    ]
    for rel, label in layer_entries:
        if (ROOT / f"{rel}.md").exists():
            moc_lines.append(f"- [[{rel}|{label}]]")
    moc_content = "\n".join(moc_lines) + "\n"
    moc.write_text(with_frontmatter(moc, moc_content), encoding="utf-8")
    print(f"写入 {moc.relative_to(ROOT)}")


def with_frontmatter(path: Path, body: str) -> str:
    created = "2026-11-06"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^created:\s*(\d{4}-\d{2}-\d{2})\s*$", text)
        if match:
            created = match.group(1)
    updated = dt.date.today().isoformat()
    return (
        "---\n"
        "type: MOC\n"
        "tags: [知识地图, 生成]\n"
        "status: 进行中\n"
        f"created: {created}\n"
        f"updated: {updated}\n"
        "---\n"
        + body
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="生成知识分层索引")
    parser.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = parser.parse_args()

    notes = list(iter_notes())
    if args.check:
        return check(notes)

    write_indexes(notes)
    return check(notes)


if __name__ == "__main__":
    sys.exit(main())
