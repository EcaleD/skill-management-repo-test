# GitHub / GitLab Skills Catalog 管理指南

本仓库将 GitHub 或 GitLab 作为 Skill Catalog：创作者在 `skills/` 中维护 Skill 源文件，仓库管理者通过 PR/MR 与 CI 管理发布，终端用户通过 `npx skills add` 安装到 AI Agent。

本仓库当前地址：

```text
https://github.com/EcaleD/skill-management-repo-test
```

## 1. 目录与命名规则

统一采用两级 Catalog 目录：

```text
skills/<产品线或能力域>/<skill-name>/SKILL.md
```

当前示例：

```text
skills/
└── docs-platform/
    ├── technical-doc-translation/
    │   ├── SKILL.md
    │   ├── references/
    │   └── assets/
    └── markdown-translation-change-review/
        ├── SKILL.md
        └── scripts/
```

规则：

- 一级目录是产品线或共享能力域，例如 `docs-platform`、`modelark`、`seedance`、`common`。
- 二级目录是一个可独立安装的 Skill。
- `SKILL.md` frontmatter 中的 `name` 必须等于二级目录名。
- Skill 名必须在整个仓库内唯一，使用小写字母、数字和连字符。
- `references/`、`scripts/`、`assets/` 都归属到具体 Skill，不应放在产品线目录根部。
- 不要在 `skills/` 下再嵌套第三层产品目录；标准布局应保持为 `skills/<category>/<skill-name>/SKILL.md`。

## 2. Skill 创作者工作流

### 2.1 新建或修改 Skill

创建分支：

```bash
git checkout main
git pull --ff-only
git checkout -b feat/docs-platform-new-skill
```

以新增 ModelArk Skill 为例：

```bash
mkdir -p skills/modelark/ark-api-integration/{references,scripts,assets}
```

最小 `SKILL.md`：

```md
---
name: ark-api-integration
description: Build and troubleshoot ModelArk API integrations. Use when users ask about authentication, SDK initialization, request payloads, Responses API, or production integration patterns.
---

# ModelArk API Integration

## Workflow

1. Identify the API operation and SDK language.
2. Confirm authentication and endpoint requirements.
3. Provide a minimal runnable example.
4. Validate error handling and secret management.
```

### 2.2 本地验证

```bash
python3 scripts/validate_skills.py
npx skills add . --list
```

本地安装到 TRAE 项目进行持久化测试：

```bash
npx skills add . \
  --skill technical-doc-translation \
  --agent trae \
  --copy \
  --yes
```

验证完成后删除测试安装：

```bash
npx skills remove technical-doc-translation --agent trae
```

### 2.3 提交 Pull Request / Merge Request

```bash
git add skills scripts README.md SKILLS_MANAGEMENT.md MANIFEST.json .github
git commit -m "feat(skills): add docs platform skill"
git push -u origin feat/docs-platform-new-skill
```

在 GitHub 创建 PR，或在 GitLab 创建 MR。PR/MR 描述应包含：

- Skill 的名称和所属产品线。
- 新增或修改的触发场景。
- 是否新增可执行脚本、网络访问或敏感操作。
- 本地验证命令与结果。

## 3. 仓库管理者工作流

### 3.1 审查范围

仓库管理者应检查：

1. 目录符合 `skills/<category>/<skill-name>/SKILL.md`。
2. `name` 与二级目录名称一致，且不与现有 Skill 重名。
3. `description` 能清楚描述能力和触发场景。
4. 详细文档在 `references/`，确定性操作在 `scripts/`，模板在 `assets/`。
5. 新增或修改脚本不存在凭据泄露、破坏性命令或未经说明的网络上传行为。
6. README、MANIFEST、示例命令和路径已同步更新。

### 3.2 CI 校验

本仓库的 GitHub Actions workflow 会在 PR、main 分支 push 和手动触发时运行：

```bash
python3 scripts/validate_skills.py
npx skills add . --list
```

CI 应阻止以下问题进入 `main`：

- 错误目录层级。
- 缺少 `name` 或 `description`。
- Skill 名与目录名不一致。
- 重复 Skill 名。
- Skills CLI 无法发现 catalog 中的 Skill。

### 3.3 合并与发布

合并前确认 CI 通过，然后合并到 `main`。

需要版本记录时，在 `main` 上执行：

```bash
git checkout main
git pull --ff-only

python3 scripts/validate_skills.py
npx skills add . --list

git tag -a v0.2.0 -m "Organize skills by product line"
git push origin v0.2.0
```

随后在 GitHub Release 或 GitLab Release 中记录：

- 新增、修改或弃用的 Skill。
- 触发条件或行为变化。
- 脚本行为和兼容性变化。
- 升级注意事项。

## 4. 终端消费者使用方式（TRAE）

### 4.1 查看仓库中可安装的 Skill

```bash
npx skills add EcaleD/skill-management-repo-test --list
```

### 4.2 项目级安装

在目标项目根目录执行：

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill technical-doc-translation \
  --agent trae \
  --yes
```

项目级安装面向当前项目；TRAE 会在其项目 Skill 目录中发现已安装内容。

安装翻译变更判断 Skill：

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill markdown-translation-change-review \
  --agent trae \
  --yes
```

### 4.3 全局安装

需要在多个 TRAE 项目复用时：

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill technical-doc-translation \
  --agent trae \
  --global \
  --yes
```

### 4.4 已安装 Skill 的管理

```bash
# 查看已安装 Skill
npx skills list

# 检查是否有上游更新
npx skills check

# 更新指定 Skill
npx skills update technical-doc-translation

# 删除 Skill
npx skills remove technical-doc-translation --agent trae
```

新增 Skill 不会自动安装到消费者本地；消费者需要再次执行 `npx skills add <repo> --skill <new-skill>`。

## 5. 当前仓库的测试命令

```bash
# 验证 catalog 结构与 YAML frontmatter
python3 scripts/validate_skills.py

# 发现当前仓库中的两个 Skill
npx skills add . --list

# 测试正文内容变化：预期 translation_required 为 true
python3 skills/docs-platform/markdown-translation-change-review/scripts/check_translation_trigger.py \
  --baseline examples/translation-trigger/baseline.md \
  --updated examples/translation-trigger/updated-content-change.md \
  --english examples/translation-trigger/english.md

# 测试仅 frontmatter 变化：预期 translation_required 为 false
python3 skills/docs-platform/markdown-translation-change-review/scripts/check_translation_trigger.py \
  --baseline examples/translation-trigger/baseline.md \
  --updated examples/translation-trigger/updated-frontmatter-only.md \
  --english examples/translation-trigger/english.md
```

## 6. 参考资料

- Skills CLI: https://github.com/vercel-labs/skills
- Agent Skills Specification: https://agentskills.io/specification
- GitHub Actions: https://docs.github.com/actions
- GitLab CI/CD: https://docs.gitlab.com/ci/
