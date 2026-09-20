# model-to-ar

把任意 3D 模型（`.glb` / `.gltf` / `.stl` / `.3mf`）变成「扫码即可在手机 AR 里查看」的体验。

基于 Google `<model-viewer>` **一键 AR**（Android Scene Viewer / iOS AR Quick Look），终端用户无需安装 App：
扫码打开网页 → 点「在 AR 中查看」→ 模型落入现实空间。

- 本地用 `scripts/launch_ar.py` 起服务并生成局域网二维码，快速测试（无需任何托管）
- 用 `scripts/deploy_pages.py` 推到 **GitHub Pages**，得到公网 HTTPS 二维码，永久分享

本仓库同时是一个 **CodeBuddy Skill**，完整用法见 [`SKILL.md`](./SKILL.md)。

## 快速开始

```bat
pip install segno
python scripts/launch_ar.py "D:/path/to/model.glb" --usdz "model.usdz" --port 8000
rem 手机连同一 Wi-Fi，打开打印的 http://<IP>:8000/ ，或扫描 site/qr.png
```

## 公网发布（GitHub Pages）

```bat
python scripts/deploy_pages.py "add historical king model"
rem 仓库 Settings → Pages → Branch: main, Folder: /site
rem 二维码地址即 https://<user>.github.io/model-to-ar/
```

## 目录

| 路径 | 说明 |
|------|------|
| `SKILL.md` | Skill 主流程与使用说明 |
| `assets/ar-template.html` | `<model-viewer>` AR 网页模板 |
| `scripts/` | `launch_ar.py` / `deploy_pages.py` / `qr_generate.py` |
| `references/` | model-viewer 属性、模型转换、托管方式详解 |
| `site/` | 由脚本生成的可部署 AR 页面（Pages 源） |

> iOS AR 需要额外的 `.usdz` 文件；Android 仅需 `.glb`。详见 `references/convert.md`。
