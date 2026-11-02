# AGENTS.md

> 本文件面向所有进入本仓库的 AI 助手（Claude Code / Codex / Cursor / OpenCode / Trae / 网页端模型等）。
> 本文件是入口契约：先读本文件，再按索引打开需要的细则，不必一次读完全部。

## 1. 作用域与优先级

个人技术学习笔记仓库：Markdown + YAML，Obsidian 兼容，Git 管理；主线为嵌入式 Linux、C/C++、STM32、ESP32、物联网。远程为 GitHub + Gitee，配图放同级 `img/` 且不入库；配套 AI 知识库在 `D:/git/AI`。

本文件只在本仓库生效；跨项目的个人规则放在用户级 `~/.claude/CLAUDE.md` 或 `~/.config/opencode/AGENTS.md`。冲突时按“安全与隐私 > 用户明确指令 > 本文件 > 默认文风”取舍；仍冲突时先询问用户。

## 2. 硬约束

- 敏感信息写入 `self/`，不入库；不写真实 IP、token、凭据、账号明细。
- 安装、下载、修改系统配置、写凭据前征得用户同意。
- 未经要求不提交、不推送、不删除、不移动、不批量重命名。
- 向 `D:/git/AI` 写入前读目标库 `CLAUDE.md`；只归档本次会话产物，不整批复制本仓库笔记。
- 大规模目录重命名前，提醒用户关闭 Obsidian、Typora 等可能锁定文件的应用。
- 全盘文件检索、打开本机文件或操作本机软件前，先读 [本机/能力清单.json](./本机/能力清单.json) 或运行 `.\script\local.ps1 list`。
- `AI/` 是本仓库的 AI 学习笔记；`D:/git/AI` 是独立会话记忆库，两者不混用。

## 3. 目录地图

| 目录 | 内容 | 入口 |
| --- | --- | --- |
| `课程/` | 课程系统笔记 | [课程/MOC.md](./课程/MOC.md) |
| `项目/` | 实践项目 | [项目/MOC.md](./项目/MOC.md) |
| `杂记/` | 工具、环境、Linux、技术专题 | [杂记/MOC.md](./杂记/MOC.md) |
| `AI/` | AI/Agent 学习主线 | [AI/MOC.md](./AI/MOC.md) |
| `本机/` | 本机能力清单与适配器 | [本机/MOC.md](./本机/MOC.md) |
| `规范/` | 写作、校验、Agent 协作与信息架构 | [规范/MOC.md](./规范/MOC.md) |
| `模板/` | 笔记模板与 frontmatter | [模板/模板说明.md](./模板/模板说明.md) |
| `script/` | 校验、适配器与本地脚本 | 不要求 MOC |

`self/` 不入库；`.skills/`、`.cursor/`、`.obsidian/` 为工具配置目录。

## 4. 常用命令

```bash
python script/notes_lint.py --strict      # 全量校验，告警视为错误
python script/notes_lint.py --changed     # 暂存区，供 pre-commit 使用
.\script\local.ps1 list                   # 列出本机能力，可按 tag 过滤
git status --short                        # 提交前检查改动范围
```

脚本依赖 Python 3 与 PyYAML：`python -m pip install pyyaml`。

## 5. 写入门禁

- 新笔记必须包含 `type`、`tags`、`status`、`created`、`updated`；完整字段见 [模板说明](./模板/模板说明.md)。
- 新笔记加入所属 `MOC.md`；重命名或删除时同步更新 MOC 与正文双链。
- 笔记正文用双链 `[[笔记名]]`；入口文件与 README 用相对 Markdown 链接。
- 命名以中文为主，技术专名保留英文；禁止英文小写碎片（如 `url.md`、`code.md`）；图片放同级 `img/`。
- 摘录必须用自己的话重写；命名、文风、图、证据的完整规则见 [写作与笔记规范](./规范/写作与笔记规范.md)。
- 完成任务前运行 `python script/notes_lint.py --strict`；提交规则见 [校验与提交规范](./规范/校验与提交规范.md)。

## 6. 规范索引

| 需要 | 打开 |
| --- | --- |
| 命名、文风、配图、新建流程 | [写作与笔记规范](./规范/写作与笔记规范.md) |
| frontmatter 字段与模板选择 | [模板说明](./模板/模板说明.md) |
| lint、pre-commit、分支、提交、推送 | [校验与提交规范](./规范/校验与提交规范.md) |
| 工具适配、权限、本机能力、跨库、Skill | [Agent协作规范](./规范/Agent协作规范.md) |
| 本机能力字段与适配器契约 | [本机/规范.md](./本机/规范.md) |
| 信息架构与迁移方案 | [仓库信息架构](./规范/仓库信息架构.md) |

## 7. 工具适配

- Claude Code：[CLAUDE.md](./CLAUDE.md)，只指向本文件与规范索引。
- Cursor：[.cursor/rules/本机能力.mdc](./.cursor/rules/本机能力.mdc)，只放本机能力调用。
- 仓库 Skill：[.skills/embedded-knowledge-sync/SKILL.md](./.skills/embedded-knowledge-sync/SKILL.md)，只放知识沉淀流程。

工具文件只做薄适配，不重复本文件与 `规范/` 的规则。规则变更先改主文件或对应规范，再同步工具文件。

## 8. 冲突与例外

- 规则冲突时按第 1 节的优先级处理；无法判断时先询问用户。
- 用户明确要求的例外，在对应规范或项目记录中登记原因与范围。
- 发现规则过时或互相矛盾时，报告位置和影响，不自行扩大解释。
