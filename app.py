from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import base64
import io
import json
from PIL import Image
import cv2
import numpy as np
import easyocr
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from transformers import BlipProcessor, BlipForConditionalGeneration
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# 配置
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 初始化AI模型
print("正在加载AI模型...")
reader = easyocr.Reader(['ch_sim', 'en'])  # 中英文OCR

# 图像理解模型
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Stable Diffusion模型 (用于风格转换)
device = "cuda" if torch.cuda.is_available() else "cpu"
try:
    sd_pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)
    print(f"Stable Diffusion模型已加载到 {device}")
except Exception as e:
    print(f"Stable Diffusion模型加载失败: {e}")
    sd_pipe = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_path):
    """从图片中提取文字"""
    try:
        results = reader.readtext(image_path)
        texts = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:  # 只保留置信度高的文字
                texts.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
        return texts
    except Exception as e:
        print(f"OCR错误: {e}")
        return []

def understand_image_content(image_path):
    """理解图片内容"""
    try:
        image = Image.open(image_path).convert('RGB')
        inputs = blip_processor(image, return_tensors="pt")
        out = blip_model.generate(**inputs, max_length=100)
        description = blip_processor.decode(out[0], skip_special_tokens=True)
        return description
    except Exception as e:
        print(f"图像理解错误: {e}")
        return "无法理解图像内容"

def convert_style(image_path, style_prompt, strength=0.7):
    """转换图片风格"""
    if sd_pipe is None:
        return None
    
    try:
        # 加载原图
        image = Image.open(image_path).convert('RGB')
        
        # 调整图片大小以适应模型
        image = image.resize((512, 512))
        
        # 生成新风格的图片
        prompt = f"{style_prompt}, high quality, detailed"
        negative_prompt = "low quality, blurry, distorted"
        
        result = sd_pipe(
            prompt=prompt,
            image=image,
            strength=strength,
            guidance_scale=7.5,
            negative_prompt=negative_prompt
        ).images[0]
        
        # 保存结果
        output_filename = f"styled_{uuid.uuid4().hex}.jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        result.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"风格转换错误: {e}")
        return None

@app.route('/')
def index():
    """主页 - 提供静态HTML文件"""
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """提供静态文件服务"""
    return send_from_directory('static', filename)

@app.route('/api/styles', methods=['GET'])
def get_styles():
    """获取可用的画风选项"""
    styles = {
        'anime': {
            'name': '动漫风格',
            'prompt': 'anime style, manga, cel shading, vibrant colors',
            'description': '日式动漫风格，色彩鲜艳'
        },
        'watercolor': {
            'name': '水彩画风',
            'prompt': 'watercolor painting, soft colors, artistic',
            'description': '水彩画效果，柔和色调'
        },
        'sketch': {
            'name': '素描风格',
            'prompt': 'pencil sketch, black and white, detailed lines',
            'description': '铅笔素描效果'
        },
        'cartoon': {
            'name': '卡通风格',
            'prompt': 'cartoon style, colorful, simplified shapes',
            'description': '卡通化效果，简化造型'
        },
        'realistic': {
            'name': '写实风格',
            'prompt': 'photorealistic, detailed, high resolution',
            'description': '照片级写实效果'
        },
        'cyberpunk': {
            'name': '赛博朋克',
            'prompt': 'cyberpunk style, neon colors, futuristic',
            'description': '未来科幻风格，霓虹色彩'
        }
    }
    return jsonify(styles)

@app.route('/api/upload', methods=['POST'])
def upload_and_process():
    """上传并处理漫画图片"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        files = request.files.getlist('files')
        style = request.form.get('style', 'anime')
        strength = float(request.form.get('strength', 0.7))
        
        if not files or files[0].filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # 保存上传的文件
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                # 提取文字
                texts = extract_text_from_image(filepath)
                
                # 理解图片内容
                description = understand_image_content(filepath)
                
                # 获取风格设置
                styles_data = get_styles().get_json()
                style_config = styles_data.get(style, styles_data['anime'])
                
                # 转换风格
                styled_path = convert_style(filepath, style_config['prompt'], strength)
                
                result = {
                    'original_filename': file.filename,
                    'processed_filename': filename,
                    'texts': texts,
                    'description': description,
                    'style': style_config,
                    'styled_image': os.path.basename(styled_path) if styled_path else None
                }
                
                results.append(result)
        
        return jsonify({
            'success': True,
            'results': results,
            'message': f'成功处理 {len(results)} 张图片'
        })
        
    except Exception as e:
        return jsonify({'error': f'处理失败: {str(e)}'}), 500

@app.route('/outputs/<filename>')
def get_output_file(filename):
    """获取生成的图片文件"""
    try:
        return send_file(os.path.join(OUTPUT_FOLDER, filename))
    except Exception as e:
        return jsonify({'error': f'文件不存在: {str(e)}'}), 404

@app.route('/uploads/<filename>')
def get_upload_file(filename):
    """获取上传的图片文件"""
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, filename))
    except Exception as e:
        return jsonify({'error': f'文件不存在: {str(e)}'}), 404

if __name__ == '__main__':
    print("AI漫画转换器启动中...")
    print("正在加载模型，请稍候...")
    app.run(debug=True, host='0.0.0.0', port=5000)