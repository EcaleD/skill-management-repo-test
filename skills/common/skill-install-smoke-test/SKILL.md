---
name: skill-install-smoke-test
description: Verify that an Agent Skill was discovered and loaded correctly. Use when the user asks to run a Skill installation smoke test, verify a newly installed Skill, or confirm that the Skills catalog workflow works.
license: MIT
compatibility: No scripts, network access, or external dependencies are required.
metadata:
  com.example.product-line: common
  com.example.status: test
  com.example.version: "0.1.0"
---

# Skill Installation Smoke Test

## Purpose

Verify that this Skill is available to the current agent.

## Instructions

When the user asks to test, verify, or confirm this Skill:

1. Reply with exactly: `Skill installation smoke test passed.`
2. State the Skill name: `skill-install-smoke-test`.
3. Do not run commands, access files, use tools, or make network requests.
