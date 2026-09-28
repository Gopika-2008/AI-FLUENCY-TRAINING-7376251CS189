# Agentic AI: Foundations and Open-Source Practice
# Day 3 Lab – ReAct Agent: Build, Break, and Fix

## 1. Aim

The aim of this lab was to build a ReAct agent from scratch in plain Python using two tools: a safe calculator and a web-page/local-file reader. The agent was tested on normal questions and was then deliberately exposed to failure situations such as repeated tool calls, an unknown tool call, and a very large tool output.

Finally, guards were added to the agent to improve reliability and prevent unnecessary tool calls, excessive tool output, and runaway context usage.

---

## 2. Tools Used

### 2.1 Calculator

The `calculator(expression)` tool evaluates basic arithmetic expressions safely.

It uses Python's `ast` module instead of `eval()`. Only supported arithmetic operations are allowed.

For example:

```text
(12000 + 18000) * 0.9