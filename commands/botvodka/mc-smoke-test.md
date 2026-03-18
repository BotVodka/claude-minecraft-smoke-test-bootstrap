---
description: '全局 Minecraft smoke-test 工作流命令，自动检测 helper、按需 bootstrap 并执行中央脚本'
allowed-tools: 'Bash, Read, Glob, Grep, AskUserQuestion'
argument-hint: '[server|client|both] [--project-root <path>] [--no-bootstrap]'
# examples:
#   - /botvodka:mc-smoke-test server
#   - /botvodka:mc-smoke-test client --project-root "D:/projects/code/minecraftMods"
#   - /botvodka:mc-smoke-test both
#   - /botvodka:mc-smoke-test server --no-bootstrap
---

$ARGUMENTS

# BotVodka Global Minecraft Smoke Test

这是一个**可直接调用**的全局工作流命令。

目标：
- 以全局 command 作为唯一入口
- 统一调用中央脚本 `MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py`
- 自动检测 helper 是否存在
- 在已验证 Forge 1.20.1 项目中按需自动安装 helper
- 输出统一的 smoke-test 结果摘要

## 默认行为

### 参数约定

- 第一个位置参数可选：`server` | `client` | `both`
  - 默认：`server`
- `--project-root <path>`
  - 可选，默认使用当前工作目录
- `--no-bootstrap`
  - 可选，传入后不会自动安装 helper

### 执行规则

1. 解析参数，确定：
   - 目标 side
   - 项目根目录
   - 是否允许 bootstrap helper
2. 校验：
   - `MC_SMOKE_TEST_KIT_ROOT` 已配置
   - 中央脚本存在：`$MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py`
3. 对每个目标 side 执行：
   - `server` -> `runServer`
   - `client` -> `runClient`
4. 调用中央脚本：

```bash
python3 "$MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py" \
  --project-root "<project-root>" \
  --task <runServer|runClient> \
  --side <server|client> \
  [--bootstrap-helper]
```

5. 中央脚本内部负责：
   - helper 已存在 -> 直接执行
   - helper 缺失且项目属于已验证 Forge 1.20.1 -> 自动安装 helper
   - helper 缺失但项目不在已验证范围 -> 明确失败并要求走 `docs/helper-generation-prompt.md`

## 执行流程

### Step 1: 解析用户参数

按以下优先级处理：

- 若 `$ARGUMENTS` 为空 -> 默认运行 `server`
- 若包含 `server` / `client` / `both` -> 采用指定 side
- 若包含 `--project-root` -> 使用指定项目路径
- 若包含 `--no-bootstrap` -> 本次运行不传 `--bootstrap-helper`

如果 side 无法从参数中明确识别，则使用：
- `server`

如果参数格式明显不合法，先指出正确用法，再停止执行。

### Step 2: 预检

执行前必须检查：

- 环境变量 `MC_SMOKE_TEST_KIT_ROOT`
- 文件 `$MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py`
- 目标项目目录存在

若任一条件不满足，立即失败，并给出明确修复建议。

### Step 3: 执行 smoke-test

#### server

运行：

```bash
python3 "$MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py" \
  --project-root "<project-root>" \
  --task runServer \
  --side server \
  [--bootstrap-helper]
```

#### client

运行：

```bash
python3 "$MC_SMOKE_TEST_KIT_ROOT/scripts/mc_smoke_test.py" \
  --project-root "<project-root>" \
  --task runClient \
  --side client \
  [--bootstrap-helper]
```

#### both

先运行 server，成功后再运行 client。

如果 server 已失败：
- 默认不要继续跑 client
- 直接输出聚合结果与失败原因

## 输出要求

每次执行结束后，都要向用户输出如下结构。

### 单 side 输出

```markdown
## Smoke Test Result

- Project: <project-root>
- Script Source: Central
- Task: <gradle-task>
- Side: <server|client>
- Marker: <marker>
- Stop Strategy: <strategy>
- Result: Passed | Failed

### Evidence
- helper status: <existing|installed>
- loader: <loader-or-unknown>
- minecraft version: <version-or-unknown>
- marker seen: <true|false>
- exit code: <code>
- reason: <reason>

### Notes
- <next action if unsupported or helper generation is needed>
```

### both 输出

```markdown
## Smoke Test Results

### Server
- Result: Passed | Failed
- Evidence: <one-line summary>

### Client
- Result: Passed | Failed | Skipped
- Evidence: <one-line summary>

### Overall
- Project: <project-root>
- Script Source: Central
- Summary: <overall conclusion>
```

## 失败处理

以下情况必须明确报错，不得猜路径、不得静默失败：

- `MC_SMOKE_TEST_KIT_ROOT` 未配置
- 中央脚本不存在
- 目标项目目录不存在
- 项目不在已验证 Forge 1.20.1 支持范围内
- helper 缺失且无法识别 `base package` / `mod class`

## 实施要求

执行这个命令时，不要只解释应该怎么做。

你应当：
- 直接解析参数
- 直接运行必要的检查与中央脚本
- 直接返回结果摘要

只有在以下情况才先询问用户：
- 用户要求跑 `both` 但项目路径看起来不是当前仓库且参数又没给清楚
- 参数无法解析
- 执行被权限或环境阻止且需要用户决策
