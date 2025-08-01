#!/bin/bash

echo "🎨 AI漫画转换器 - 自动安装脚本"
echo "================================"

# 检查Python版本
echo "🔍 检查Python版本..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ 找到Python: $python_version"
else
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查pip
echo "🔍 检查pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ 找到pip3"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo "✅ 找到pip"
    PIP_CMD="pip"
else
    echo "❌ 未找到pip，请先安装pip"
    exit 1
fi

# 创建虚拟环境 (可选)
read -p "🤔 是否创建虚拟环境? (推荐) [y/N]: " create_venv
if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    
    # 激活虚拟环境
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    echo "✅ 虚拟环境已激活"
fi

# 升级pip
echo "⬆️ 升级pip..."
$PIP_CMD install --upgrade pip

# 安装依赖
echo "📚 安装依赖包..."
$PIP_CMD install -r requirements.txt

# 创建必要目录
echo "📁 创建必要目录..."
mkdir -p uploads outputs static models_cache

# 复制环境变量文件
if [[ ! -f .env ]]; then
    echo "⚙️ 创建环境变量文件..."
    cp .env.example .env
    echo "✅ 请编辑 .env 文件配置相关参数"
fi

# 检查CUDA支持
echo "🔍 检查GPU支持..."
python3 -c "import torch; print('✅ CUDA可用' if torch.cuda.is_available() else '⚠️ 仅CPU模式')"

echo ""
echo "🎉 安装完成！"
echo ""
echo "🚀 启动应用:"
echo "   python3 app.py"
echo ""
echo "🌐 访问地址:"
echo "   http://localhost:5000"
echo ""
echo "📖 更多信息请查看 README.md"