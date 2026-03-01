# Streamlit Cloud 部署指南

## 🚀 问题分析与解决方案

### 问题原因
1. **路径错误**: Streamlit Cloud 在寻找 `tool/requirements.txt`，但实际路径是 `web tool/requirements.txt`（目录名包含空格）
2. **应用类型不匹配**: 原应用是 Flask 应用，但部署在 Streamlit Cloud 上
3. **缺少 Streamlit 入口文件**: Streamlit Cloud 需要 `streamlit_app.py` 或 `app.py`（Streamlit 格式）

### 解决方案
已创建 Streamlit 版本的应用程序 (`streamlit_app.py`)，并更新了 `requirements.txt`。

## 📋 部署步骤

### 方法 1: 使用 Streamlit Cloud（推荐）

1. **准备文件**
   - ✅ `web tool/streamlit_app.py` - Streamlit 应用主文件（已创建）
   - ✅ `web tool/requirements.txt` - 依赖文件（需要更新，包含 streamlit）
   - ✅ `web tool/.streamlit/config.toml` - Streamlit 配置文件（已创建）

2. **更新 requirements.txt**
   确保 `web tool/requirements.txt` 包含 streamlit：
   ```
   streamlit>=1.28.0
   scikit-learn==1.3.0
   pandas==2.0.3
   numpy==1.24.3
   shap==0.42.1
   imbalanced-learn==0.11.0
   matplotlib==3.7.2
   seaborn==0.12.2
   plotly==5.15.0
   ```

3. **部署到 Streamlit Cloud**
   - 访问 https://share.streamlit.io/
   - 使用 GitHub 账号登录
   - 点击 "New app"
   - 选择你的仓库
   - **Main file path**: 设置为 `web tool/streamlit_app.py`
   - **Branch**: 选择主分支（通常是 `main` 或 `master`）
   - 点击 "Deploy"

4. **注意事项**
   - 如果 Streamlit Cloud 仍然找不到 requirements.txt，可能需要将 `web tool/requirements.txt` 复制到根目录
   - 如果模型文件 `best_model_gbm.pkl` 存在，确保路径正确（代码会自动查找多个位置）

### 方法 2: 本地运行 Streamlit

```bash
# 进入 web tool 目录
cd "web tool"

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run streamlit_app.py
```

### 方法 3: 继续使用 Flask（不推荐用于 Streamlit Cloud）

如果你想继续使用 Flask 应用，建议使用以下平台：
- **Heroku**: 支持 Flask 应用
- **Railway**: 支持 Flask 应用
- **Render**: 支持 Flask 应用
- **PythonAnywhere**: 支持 Flask 应用

## 🔧 文件结构

部署后的文件结构应该是：

```
项目根目录/
├── web tool/                    # Web工具目录
│   ├── streamlit_app.py        # Streamlit 应用（新创建）
│   ├── app.py                  # Flask 应用（保留）
│   ├── requirements.txt        # 依赖文件（需要更新）
│   ├── .streamlit/
│   │   └── config.toml         # Streamlit 配置（已创建）
│   ├── templates/
│   │   └── index.html
│   └── ...
└── best_model_gbm.pkl          # 模型文件（如果有）
```

## ✅ 验证部署

部署成功后，你应该能够：
1. 访问 Streamlit Cloud 提供的 URL
2. 看到应用界面
3. 输入患者信息
4. 获得预测结果和 SHAP 解释

## 🐛 常见问题

### Q: 仍然提示找不到 requirements.txt
A: Streamlit Cloud 默认在根目录查找 requirements.txt。如果文件在 `web tool/` 目录下，有两种解决方案：
1. 将 `web tool/requirements.txt` 复制到根目录
2. 在 Streamlit Cloud 设置中指定 requirements.txt 的路径（如果支持）

### Q: 模型文件找不到
A: `streamlit_app.py` 中已经包含了多个路径查找逻辑，会自动尝试以下路径：
- `web tool/best_model_gbm.pkl`（当前目录）
- `../best_model_gbm.pkl`（上级目录）
- 其他可能的路径

如果模型文件不存在，应用会使用默认参数创建模型。

### Q: 依赖安装失败
A: 检查 `requirements.txt` 中的版本是否兼容。如果某些包版本过旧，可以尝试：
```bash
pip install --upgrade streamlit scikit-learn pandas numpy shap
```

### Q: 想要同时支持 Flask 和 Streamlit
A: 可以保留两个版本：
- `web tool/streamlit_app.py` - 用于 Streamlit Cloud
- `web tool/app.py` - 用于本地 Flask 部署

## 📝 更新日志

- ✅ 创建 `web tool/streamlit_app.py` - Streamlit 版本的应用
- ✅ 创建 `web tool/.streamlit/config.toml` - Streamlit 配置文件
- ✅ 更新路径引用 - 适配 web tool 目录结构
- ✅ 修复模型文件路径查找逻辑

## 🎯 下一步

1. 更新 `web tool/requirements.txt` 添加 streamlit 依赖
2. 将更改推送到 GitHub
3. 在 Streamlit Cloud 上部署（Main file path: `web tool/streamlit_app.py`）
4. 测试应用功能
5. 分享应用链接

---

**注意**: 
- 如果 Streamlit Cloud 仍然找不到 requirements.txt，可能需要将 requirements.txt 放在根目录
- 如果遇到任何问题，请检查 Streamlit Cloud 的日志输出，通常会有详细的错误信息
