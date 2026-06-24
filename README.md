# Agent Skills Catalog

这是一个面向技术文档工作流的公共 Agent Skills 测试目录。仓库使用 Git 管理 Skill 源文件，并允许终端用户通过 [`npx skills`](https://github.com/vercel-labs/skills) CLI 发现和安装 Skill。

## 简介

编程 Agent 需要项目特定的指令、可靠的工作流和最新的领域知识。本仓库将这些上下文封装为可复用的 Agent Skills：每个 Skill 都是一个目录，其中包含 `SKILL.md`，并可按需包含参考文档、脚本或资源文件。

本仓库用于演示如何通过 GitHub 或 GitLab 创建、评审、发布、安装和更新 Skills。

## 本仓库中的 Skills

| 产品线 | Skill | 说明 |
| :--- | :--- | :--- |
| `docs-platform` | [`technical-doc-translation`](skills/docs-platform/technical-doc-translation/) | 翻译或润色中文 Markdown 技术文档，同时保留代码块、URL、frontmatter、HTML、API 标识符和 Markdown 结构。 |
| `docs-platform` | [`markdown-translation-change-review`](skills/docs-platform/markdown-translation-change-review/) | 判断中文 Markdown 文档的修改是否需要触发英文翻译更新。 |

## 安装

以下示例使用 [TRAE](https://www.trae.ai/) 作为目标 Agent。使用其他受支持的 Agent 时，请将 `trae` 替换为对应的 Agent 名称。

### 查看可用 Skills

```bash
npx skills add EcaleD/skill-management-repo-test --list
```

### 安装到当前 TRAE 项目

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill technical-doc-translation \
  --agent trae \
  --yes
```

### 为 TRAE 全局安装

```bash
npx skills add EcaleD/skill-management-repo-test \
  --skill technical-doc-translation \
  --agent trae \
  --global \
  --yes
```

### 更新已安装的 Skills

```bash
# 更新当前项目中安装的全部 Skills。
npx skills update --project --yes

# 更新当前项目中的一个指定 Skill。
npx skills update technical-doc-translation --project --yes
```

当仓库新增 Skill 时，请显式执行 `npx skills add <repo> --skill <skill-name>`。`update` 只会刷新已安装的 Skill，不会自动安装仓库中新增加的 Skill。

## 本地开发

克隆仓库后，请在创建 Pull Request 前校验 catalog：

```bash
git clone https://github.com/EcaleD/skill-management-repo-test.git
cd skill-management-repo-test

# 校验 catalog 目录结构和必填 frontmatter。
python3 scripts/validate_skills.py

# 仅发现本地 Skills，不执行安装。
npx skills add . --list
```

如需在 TRAE 中进行持久化本地测试，可安装一个项目级复制副本：

```bash
npx skills add . \
  --skill technical-doc-translation \
  --agent trae \
  --copy \
  --yes
```

请修改 `skills/` 下的源文件，而不是已安装的副本。测试完成后可删除该测试安装：

```bash
npx skills remove technical-doc-translation --agent trae
```

## 仓库目录结构

```text
skills/
└── <产品线>/
    └── <skill-name>/
        ├── SKILL.md
        ├── references/  # 可选：长篇参考说明
        ├── scripts/     # 可选：确定性辅助脚本
        └── assets/      # 可选：模板和示例文件
```

本 catalog 采用以下必需目录结构：

```text
skills/<category>/<skill-name>/SKILL.md
```

- `category` 表示产品线或共享能力域，例如 `docs-platform`、`modelark`、`seedance` 或 `common`。
- `skill-name` 在全仓库内唯一，只能使用小写字母、数字和连字符。
- `SKILL.md` 中的 `name` 字段必须与 `skill-name` 目录完全一致。
- 参考文档、脚本和资源文件应保存在所属 Skill 的目录中。

不要将 `.trae/skills/` 用作仓库源目录。该目录是 TRAE 的安装目标；可发布的源文件应位于 `skills/` 下。

## 新增 Skill

1. 创建目录，例如 `skills/modelark/ark-api-integration/`。
2. 添加 `SKILL.md`，并在 frontmatter 中提供必需的 `name` 和 `description`。
3. 仅在 Skill 确实需要时再添加 `references/`、`scripts/` 或 `assets/`。
4. 运行 `python3 scripts/validate_skills.py` 和 `npx skills add . --list`。
5. 同步更新 `README.md`；如仓库继续保留 `MANIFEST.json`，按需同步其中的文件清单。
6. 创建 Pull Request，并说明 Skill 的用途、触发场景、风险说明和校验结果。

## 治理与发布

通过 Pull Request 和 CI 评审每一次 catalog 修改。需要稳定、可审计的 catalog 快照时，创建 Git tag 以及 GitHub 或 GitLab Release。完整的创作者、仓库管理者和终端消费者工作流，请参阅 [SKILLS_MANAGEMENT.md](SKILLS_MANAGEMENT.md)。

## 更多信息

- [Skills CLI](https://github.com/vercel-labs/skills)
- [Agent Skills 规范](https://agentskills.io/specification)
- [仓库管理指南](SKILLS_MANAGEMENT.md)

## 免责声明

这是一个用于演示 Agent Skills Catalog 管理方式的测试仓库，不提供生产支持或兼容性保证。
