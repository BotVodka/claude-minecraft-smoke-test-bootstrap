---
description: '为目标 Minecraft 项目引导 smoke-test helper 接入与全局命令使用方式'
allowed-tools: 'Read, Glob, Grep, Bash, AskUserQuestion'
argument-hint: '[--project-root <path>]'
---

$ARGUMENTS

# BotVodka Bootstrap Project

目标：
- 判断当前项目是否已具备 smoke-test helper
- 引导接入 `minecraft-smoke-test-kit`
- 在已验证 Forge 1.20.1 环境下建议使用 helpers-only / global-mode
- 对未知环境给出 helper-generation 路径

MVP 设计要求：
- 先检查项目结构
- 再决定给出哪条接入路径
- 不把 Repository B 变成 smoke-test 领域逻辑实现层
