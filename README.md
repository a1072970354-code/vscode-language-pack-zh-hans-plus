# Chinese (Simplified) Plus — VS Code 简体中文增强语言包

非官方社区构建。在微软官方 `ms-ceintl.vscode-language-pack-zh-hans` **1.131** 的基础上，补齐 **VS Code 1.132 – 1.146** 新增界面的简体中文译文。

官方语言包自 2026-09 起停留在 1.131，而 VS Code 已经到 1.146；新增的 **Sessions（会话）**、**Agent Host（智能体主机）**、**Copilot 聊天面板**、**Automations**、**Canvases**、**Hooks** 等界面一直没有中文，全部回退显示英文。本包把这些缺口补上。

## 覆盖率

| 项目 | 数值 |
|---|---|
| 应用条目（`out/nls.messages.json`） | 32,108 |
| 本包含中文条目 | 31,554 |
| 覆盖率 | **98.27%** |
| 剩余未译 | 181 条，均为品牌名 / 缩写 / 单位 |

剩余 181 条是**故意保留英文**的，例如 `Copilot`、`MCP`、`CRLF`、`LF`、`Alt`、`URL`、`ChatGPT`、`Claude`、`Codex`、`{0} GB`。强行翻译反而会造成术语混乱。

## 下载

**[v1.146.0 VSIX](https://github.com/a1072970354-code/vscode-language-pack-zh-hans-plus/releases/download/v1.146.0/vscode-language-pack-zh-hans-plus-1.146.0.vsix)**（960 KB）

一行命令装完并切到中文：

```bash
curl -L -o /tmp/zh.vsix https://github.com/a1072970354-code/vscode-language-pack-zh-hans-plus/releases/download/v1.146.0/vscode-language-pack-zh-hans-plus-1.146.0.vsix && code --install-extension /tmp/zh.vsix --force
```

装完 `Cmd+Shift+P` → `Configure Display Language` → `中文(简体)`，然后**完全退出** VS Code 再打开。

## 安装

### 方式一：VSIX（推荐）

```bash
code --install-extension vscode-language-pack-zh-hans-plus-1.146.0.vsix
```

然后 `Cmd+Shift+P` → `Configure Display Language` → `中文(简体)`，**完整退出并重开** VS Code（不是窗口 reload）。

### 方式二：手动覆盖

不需要装新扩展，直接把 `extras/zh_146.json` 合并进已装的官方语言包：

```bash
python3 tools/apply_patch.py --apply --clear-cache
```

脚本会自动备份原文件、合并增量、清掉 `clp` 译文缓存，然后请你重启 VS Code。

## 这个包和官方包的关系

- 目录结构、`package.json` 的 `contributes.localizations`、95 个 `translations/*.i18n.json` 全部沿用官方包的格式，**只是把 `main.i18n.json` 换成了补全版**
- `package.json` 里 `publisher` 改为 `zh-hans-plus`、`name` 改为 `vscode-language-pack-zh-hans-plus`，避免和官方包 ID 冲突（同 ID 会互相覆盖）
- 官方原文与既有译文版权归 Microsoft，按 MIT 授权（见 `LICENSE.md`）；本仓库新增的 2,802 条译文同样以 MIT 发布

## 仓库结构

```
package.json                 # 扩展清单（publisher=zh-hans-plus, version=1.146.0）
translations/                # 95 个 i18n 文件，main.i18n.json 已补全
extras/zh_146.json           # 仅本仓库新增的 2,802 条增量译文（便于 review / 复用）
tools/apply_patch.py         # 体检 + 合并 + 清缓存脚本
LICENSE / LICENSE.md         # MIT（含 Microsoft 原始版权声明）
ThirdPartyNotices.txt        # 官方第三方声明，随包保留
```

`extras/zh_146.json` 只包含新增部分，格式 `{"<模块路径>::<键名>": "<中文>"}`，方便你审阅每一条译文，也方便下一版官方包发布后做 diff。

## 重新生成译文（VS Code 再升级时）

```bash
# 1. 体检：看新版应用还缺多少条
python3 tools/apply_patch.py

# 2. 从应用自带的键表生成待译清单
#    /Applications/Visual Studio Code.app/Contents/Resources/app/out/nls.keys.json
#    /Applications/Visual Studio Code.app/Contents/Resources/app/out/nls.messages.json

# 3. 翻译后写入 extras/zh_XXX.json，再 --apply
```

## 已知问题

- 语言包版本号写成 `1.146.0`，但 `engines.vscode` 也是 `^1.146.0`；在更低版本 VS Code 上会被拒绝安装（这是有意的，低版本用官方 1.131 就够）
- 与官方语言包**不能同时启用**：两者 `languageId` 都是 `zh-cn`，同时开会互相覆盖。装了本包请禁用官方包
- 微软若在未来发布 1.147+ 官方包，本包会落后，需要重新跑一遍生成流程

## 许可

MIT。原始 VS Code 本地化文件版权归 Microsoft Corporation；本仓库新增译文版权归贡献者，同样以 MIT 授权。
