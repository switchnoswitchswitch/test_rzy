# AI漫画转换器

一个基于人工智能的漫画风格转换应用，能够读取漫画内容并按照指定画风进行转换。

## 🌟 主要功能

- **📖 智能内容理解**: 使用OCR技术识别漫画中的文字内容
- **🎨 多种画风转换**: 支持动漫、水彩、素描、卡通、写实、赛博朋克等多种风格
- **🖼️ 批量处理**: 支持同时上传和处理多张图片
- **⚡ 实时预览**: 即时查看原图和转换后的效果对比
- **🎛️ 可调参数**: 支持调节转换强度，精确控制效果

## 🛠️ 技术栈

- **后端**: Python Flask + AI模型集成
- **前端**: HTML5 + CSS3 + JavaScript (原生)
- **AI模型**: 
  - EasyOCR (文字识别)
  - BLIP (图像理解)
  - Stable Diffusion (风格转换)

## 📋 系统要求

- Python 3.8+
- 4GB+ RAM (推荐8GB+)
- CUDA支持的显卡 (可选，用于加速)

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd ai-comic-converter
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量 (可选)
```bash
cp .env.example .env
# 编辑 .env 文件，添加相关API密钥
```

### 4. 启动应用
```bash
python app.py
```

### 5. 访问应用
打开浏览器访问: `http://localhost:5000`

## 📖 使用指南

### 上传图片
1. 点击上传区域或拖拽图片文件
2. 支持 JPG, PNG, GIF 格式
3. 单个文件大小限制: 10MB
4. 支持批量上传多张图片

### 选择画风
应用提供6种预设画风：
- **动漫风格**: 日式动漫风格，色彩鲜艳
- **水彩画风**: 水彩画效果，柔和色调
- **素描风格**: 铅笔素描效果
- **卡通风格**: 卡通化效果，简化造型
- **写实风格**: 照片级写实效果
- **赛博朋克**: 未来科幻风格，霓虹色彩

### 调节参数
- **转换强度**: 0.1-1.0，数值越高转换效果越明显
- 推荐值: 0.7 (平衡原图特征和新风格)

### 查看结果
- 原图和转换后图片对比展示
- 显示识别的文字内容和置信度
- 展示AI对图片内容的理解描述

## 🎯 API接口

### GET /api/styles
获取可用的画风列表
```json
{
  "anime": {
    "name": "动漫风格",
    "prompt": "anime style, manga, cel shading, vibrant colors",
    "description": "日式动漫风格，色彩鲜艳"
  }
}
```

### POST /api/upload
上传并处理图片
- **参数**: 
  - `files`: 图片文件 (multipart/form-data)
  - `style`: 画风类型 (string)
  - `strength`: 转换强度 (float, 0.1-1.0)

## 🔧 高级配置

### 环境变量
- `OPENAI_API_KEY`: OpenAI API密钥 (可选)
- `HUGGINGFACE_TOKEN`: Hugging Face访问令牌 (可选)
- `MAX_FILE_SIZE`: 文件上传大小限制 (MB)
- `MODEL_CACHE_DIR`: 模型缓存目录

### 模型优化
- 首次运行会自动下载所需模型
- 模型文件较大，请确保网络连接稳定
- 有CUDA显卡时会自动启用GPU加速

## 🚨 注意事项

1. **首次启动**: 需要下载AI模型，可能需要较长时间
2. **内存需求**: 建议至少4GB可用内存
3. **网络要求**: 需要稳定的网络连接下载模型
4. **文件格式**: 仅支持常见图片格式 (JPG, PNG, GIF)
5. **处理时间**: 风格转换需要一定时间，请耐心等待

## 🐛 常见问题

### Q: 模型加载失败怎么办？
A: 检查网络连接，确保能访问Hugging Face。可以设置镜像源或使用VPN。

### Q: 转换效果不理想？
A: 尝试调整转换强度参数，或选择不同的画风。某些图片可能需要特定的参数组合。

### Q: 支持哪些语言的文字识别？
A: 目前支持中文和英文文字识别，可以在代码中添加更多语言支持。

### Q: 可以添加自定义画风吗？
A: 可以在 `app.py` 的 `get_styles()` 函数中添加新的画风配置。

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - 文字识别
- [Stable Diffusion](https://github.com/huggingface/diffusers) - 图像生成
- [BLIP](https://github.com/salesforce/BLIP) - 图像理解
- [Flask](https://flask.palletsprojects.com/) - Web框架
