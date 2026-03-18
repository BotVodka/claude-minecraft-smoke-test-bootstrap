---
description: '检查 Windows Claude Code 与 Minecraft smoke-test bootstrap 环境是否配置正确'
allowed-tools: 'Bash, Read, Glob, AskUserQuestion'
---

# BotVodka Claude Smoke-Test Doctor

目标：
- 检查 Claude 配置目录是否存在
- 检查全局命令是否安装
- 检查 `MC_SMOKE_TEST_KIT_ROOT` 是否配置
- 检查中央脚本是否存在
- 输出可执行的修复建议

MVP 设计要求：
- 优先报告缺失项
- 不猜测私有路径
- 不写入私有配置
- 只输出诊断和后续动作
