# Bubble · 小狐狸情绪泡泡机

一个轻量、温柔的情绪互动网页。写下一句话，它会变成缓慢上浮的泡泡；戳破泡泡后，可以获得本地预设或大模型生成的回应，并选择使用语音播放。

## 功能

- 3D 质感泡泡与碰撞动画
- 自定义心情、颜色、头像与狐狸图片
- OpenAI / Google Gemini 智能回复
- MiniMax TTS 语音回复
- 本地历史记录与备注
- 自定义背景音乐
- 响应式桌面与移动端界面

## 使用

这是一个纯前端项目，不需要构建步骤。

```bash
python -m http.server 8000
```

浏览器打开 `http://localhost:8000`。也可以直接部署到 GitHub Pages、Vercel 或任意静态网站托管服务。

> API Key 会写入浏览器 LocalStorage。不要在公共或不可信设备上保存真实密钥，也不要把密钥直接提交到仓库。

## 页面

- `index.html`：情绪泡泡主界面
- `settings.html`：模型、语音、个人资料与主题设置

## 技术

HTML、Tailwind CSS CDN、Font Awesome、原生 JavaScript 与 LocalStorage。
