# Claude Minecraft Smoke-Test Bootstrap

本项目由 BotVodka 使用 Claude Code 与 GPT-5.4 编写。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![README: 中文](https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87-blue.svg)](./README.md)
[![README: English](https://img.shields.io/badge/README-English-blue.svg)](./README.en.md)

一个面向 Windows Claude Code 用户的 Minecraft smoke-test bootstrap 仓库。

它的职责不是重新实现 `minecraft-smoke-test-kit`，而是把 **Claude 全局命令分发、Windows 安装引导、公共安全配置模板、环境自检** 这一层整理成可复用的公开入口，让任意用户都可以更低成本地接入跨项目 smoke-test 能力。

## 这个仓库解决什么问题

`minecraft-smoke-test-kit` 已经提供了中央 orchestration 脚本、Forge helper 安装器、模板和接入文档，但对一个新的 Windows Claude Code 用户来说，仍然有几个重复成本：

- 不知道 Claude 全局命令应该放在哪里
- 不知道 `MC_SMOKE_TEST_KIT_ROOT` 应该如何配置
- 不知道哪些配置可以公开，哪些不能提交
- 不知道如何把公开仓库资产安装到自己的 Claude 环境
- 不知道如何验证本地集成是否已经可用

这个仓库解决的就是这些 **bootstrap / integration / distribution** 问题。

## 双仓结构

### Repository A: `minecraft-smoke-test-kit`

负责 Minecraft smoke-test 领域能力本身：

- `scripts/mc_smoke_test.py`
- `scripts/install_forge_smoke_test.py`
- Forge helper 模板
- 未来的 NeoForge / Fabric 适配模板或 helper-generation 规则
- Minecraft smoke-test 领域文档

### Repository B: `claude-minecraft-smoke-test-bootstrap`

负责 Claude 侧的安装与集成：

- Windows-first bootstrap
- 全局 Claude command 分发
- 公共安全 settings 模板
- 安装与集成文档
- 本地环境 doctor / validation

> 关键边界：本仓库不是通用 workflow 框架，也不是 `minecraft-smoke-test-kit` 的替代品。

## 已实现的 MVP 能力

当前仓库已经具备以下可运行能力：

- `scripts/install.ps1`
  - Windows 安装入口
  - 自动寻找 Python 3 并转发参数到 Python bootstrap 脚本
- `scripts/bootstrap_claude_windows.py`
  - 检测 Claude 配置目录
  - 安装/更新 `commands/botvodka/*.md`
  - 合并公共安全 settings 模板
  - 设置 `MC_SMOKE_TEST_KIT_ROOT`
  - 支持 `--dry-run`
- `scripts/doctor.py`
  - 检查 Claude config 目录
  - 检查 `settings.json`
  - 检查 `MC_SMOKE_TEST_KIT_ROOT`
  - 检查 botvodka 命令安装状态
  - 检查中央 smoke-test 脚本与 Forge helper installer

## 快速开始

### 1. 克隆两个仓库

```bash
git clone https://github.com/BotVodka/claude-minecraft-smoke-test-bootstrap.git
git clone https://github.com/BotVodka/minecraft-smoke-test-kit.git
```

### 2. 运行 bootstrap 安装入口

默认安装：

```powershell
./scripts/install.ps1
```

显式指定 smoke-test kit 路径：

```powershell
./scripts/install.ps1 --kit-root "D:/projects/code/minecraft-smoke-test-kit"
```

仅预览，不写入文件：

```powershell
./scripts/install.ps1 --dry-run
```

### 3. 运行 doctor 验证

```bash
python3 ./scripts/doctor.py
```

如果要显式覆盖路径，也可以：

```bash
python3 ./scripts/doctor.py --kit-root "D:/projects/code/minecraft-smoke-test-kit"
```

## 安装行为说明

bootstrap 安装脚本会按以下优先级解析 `MC_SMOKE_TEST_KIT_ROOT`：

1. `--kit-root`
2. 现有 `settings.json` 中的 `env.MC_SMOKE_TEST_KIT_ROOT`
3. 仓库平级目录中的 `../minecraft-smoke-test-kit`

安装脚本会：

- 检测并创建 Claude 配置目录
- 安装或更新 `commands/botvodka/*.md`
- 合并 `templates/claude/settings.json.template`
- 写入 `env.MC_SMOKE_TEST_KIT_ROOT`
- 在更新现有 `settings.json` 前生成 `settings.json.bak`

安装脚本不会：

- 写入私有 token
- 写入私有 MCP 地址
- 静默猜测不存在的 kit 路径
- 复制 `minecraft-smoke-test-kit` 的领域逻辑进当前仓库

## 已安装命令

完成安装后，用户应至少拥有以下全局命令：

```text
/botvodka:mc-smoke-test
/botvodka:doctor
/botvodka:bootstrap-project
```

它们的职责分别是：

- `/botvodka:mc-smoke-test`
  - 调用中央脚本执行 `server` / `client` / `both` smoke-test
- `/botvodka:doctor`
  - 检查 Claude 配置、命令安装与 `MC_SMOKE_TEST_KIT_ROOT`
- `/botvodka:bootstrap-project`
  - 为目标 Minecraft 项目给出 helper 接入路径与集成建议

## 目标使用方式

在支持的 Minecraft 项目中，用户应能够直接使用：

```text
/botvodka:mc-smoke-test server
/botvodka:mc-smoke-test client
/botvodka:mc-smoke-test both
```

该命令会统一调用：

- `MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py`

并在已验证 Forge 1.20.1 环境中按需自动 bootstrap helper。

## 配置边界

### 可以公开分发的内容

- 命令模板
- `settings.json.template`
- `MC_SMOKE_TEST_KIT_ROOT` 这类路径型环境约定
- Windows-first 安装脚本
- 环境 doctor / validation 脚本

### 不应公开提交的内容

- API tokens
- 私有 MCP 地址
- 私有 base URLs
- 机器本地 secret 路径
- 私有 memory 内容
- 项目私有自动化数据

## 文档导航

- `docs/architecture.md`
- `docs/repo-boundaries.md`
- `docs/windows-installation.md`
- `docs/smoke-test-integration.md`

## 当前 MVP 范围

当前只规划并优先支持：

- Windows
- Claude Code
- `minecraft-smoke-test-kit` 集成
- 已验证 Forge 1.20.1 helper bootstrap 路径

暂不在本仓库中直接承担：

- 全 loader 全版本兼容实现
- macOS / Linux 安装流程
- 私有本地环境的完整公开化
- 通用插件系统

## 设计原则

- **KISS**：Bootstrap 层只负责安装、集成、校验，不复制领域逻辑
- **DRY**：中央 smoke-test 逻辑继续由 `minecraft-smoke-test-kit` 维护
- **YAGNI**：首版只解决 Windows Claude Code + Minecraft smoke-test 复用
- **SOLID**：命令入口、安装器、doctor、领域脚本职责分离

## License

MIT
