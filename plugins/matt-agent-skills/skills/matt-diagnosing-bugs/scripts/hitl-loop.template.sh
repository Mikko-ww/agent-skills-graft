#!/usr/bin/env bash
# Human-in-the-loop 复现循环（可选模板，Agent 无关）。
# 复制本文件，编辑下方步骤后运行。
# Agent 跑脚本；用户在自己的终端按提示操作。
#
# Usage:
#   bash hitl-loop.template.sh
#
# 两个 helper：
#   step "<instruction>"          → 显示指令，等 Enter
#   capture VAR "<question>"      → 显示问题，读入 VAR
#
# 结束时以 KEY=VALUE 打印捕获值，供 Agent 解析。
#
# `capture` 会把值打回终端（Agent 从中读取），
# 因此捕获观察；登录等敏感步骤留给用户作为 `step`。

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- edit below ---------------------------------------------------------

step "Open the app at http://localhost:3000 and sign in."

capture ERRORED "Click the 'Export' button. Did it throw an error? (y/n)"

capture ERROR_MSG "Paste the error message (or 'none'):"

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
