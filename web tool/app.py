#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双胞胎严重结局预测Web诊断工具
基于GradientBoostingClassifier的最佳模型
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
import shap
import plotly.graph_objects as go
import plotly.utils
import json

app = Flask(__name__)

# 全局变量
model = None
scaler = None
feature_names = None
feature_descriptions = None

def load_model():
    """加载训练好的模型"""
    global model, scaler, feature_names, feature_descriptions
    
    # LASSO筛选的特征
    feature_names = [
        'Gestational Age', 'Chorionicity', 'GestationalHypertension', 
        'GestationalHypothyroidism', 'IntrahepaticCholestasis', 
        'GestationalAnemia', 'MeconiumStainingIII', 'FetalWeight', 
        'NeonatalHypoglycemia', 'CongenitalMalformation'
    ]
    
    # Feature descriptions in English
    feature_descriptions = {
        'Gestational Age': 'Gestational Age (weeks)',
        'Chorionicity': 'Chorionicity (0=Monochorionic, 1=Dichorionic)',
        'GestationalHypertension': 'Gestational Hypertension (0=No, 1=Yes)',
        'GestationalHypothyroidism': 'Gestational Hypothyroidism (0=No, 1=Yes)',
        'IntrahepaticCholestasis': 'Intrahepatic Cholestasis (0=No, 1=Yes)',
        'GestationalAnemia': 'Gestational Anemia (0=No, 1=Yes)',
        'MeconiumStainingIII': 'Meconium Staining Grade III (0=No, 1=Yes)',
        'FetalWeight': 'Fetal Weight (grams)',
        'NeonatalHypoglycemia': 'Neonatal Hypoglycemia (0=No, 1=Yes)',
        'CongenitalMalformation': 'Congenital Malformation (0=No, 1=Yes)'
    }
    
    # 检查是否有保存的模型文件
    if os.path.exists('best_model_gbm.pkl'):
        try:
            model = pickle.load(open('best_model_gbm.pkl', 'rb'))
            print("✅ Successfully loaded saved model")
        except:
            print("❌ Failed to load model, creating model with default parameters")
            create_default_model()
    else:
        print("⚠️ Saved model file not found, creating model with default parameters")
        create_default_model()

def create_default_model():
    """创建默认的GB模型（基于notebook中的最优参数）"""
    global model
    
    # 基于notebook中的最优参数
    gbm_params = {
        'learning_rate': 0.2,
        'max_depth': 3,
        'min_samples_leaf': 2,
        'min_samples_split': 10,
        'n_estimators': 100,
        'random_state': 42
    }
    
    # 创建Pipeline
    smote = SMOTE(random_state=42)
    gbm = GradientBoostingClassifier(**gbm_params)
    
    model = Pipeline([
        ('smote', smote),
        ('gbm', gbm)
    ])
    
    print("✅ Created GB model with default parameters")

def predict_risk(input_data):
    """预测严重结局风险"""
    try:
        # 转换为DataFrame
        df = pd.DataFrame([input_data], columns=feature_names)
        
        # 预测概率
        proba = model.predict_proba(df)[0]
        risk_score = proba[1]  # 严重结局的概率
        
        # 预测类别
        prediction = model.predict(df)[0]
        
        return {
            'risk_score': float(risk_score),
            'prediction': int(prediction),
            'risk_level': get_risk_level(risk_score),
            'confidence': get_confidence(proba)
        }
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

def get_risk_level(risk_score):
    """Determine risk level based on risk score"""
    if risk_score < 0.3:
        return "Low Risk"
    elif risk_score < 0.7:
        return "Medium Risk"
    else:
        return "High Risk"

def get_confidence(proba):
    """Calculate prediction confidence"""
    max_proba = max(proba)
    if max_proba > 0.8:
        return "High"
    elif max_proba > 0.6:
        return "Medium"
    else:
        return "Low"

def generate_shap_explanation(input_data):
    """生成SHAP解释"""
    try:
        # 提取实际的GB模型
        if hasattr(model, 'named_steps'):
            actual_model = model.named_steps['gbm']
        else:
            actual_model = model
        
        # 创建SHAP解释器
        explainer = shap.TreeExplainer(actual_model)
        
        # 转换为DataFrame
        df = pd.DataFrame([input_data], columns=feature_names)
        
        # 计算SHAP值
        shap_values = explainer.shap_values(df)
        
        # 如果是二分类，取正类的SHAP值
        if len(shap_values) == 2:
            shap_values = shap_values[1]
        
        # 创建SHAP条形图数据
        shap_data = []
        for i, (feature, value) in enumerate(zip(feature_names, shap_values[0])):
            shap_data.append({
                'feature': feature_descriptions[feature],
                'shap_value': float(value),
                'feature_value': float(input_data[i]),
                'importance': abs(float(value))
            })
        
        # 按重要性排序
        shap_data.sort(key=lambda x: x['importance'], reverse=True)
        
        return shap_data
    except Exception as e:
        print(f"SHAP explanation error: {e}")
        return None

@app.route('/')
def index():
    """主页"""
    return render_template('index.html', 
                         features=feature_names, 
                         descriptions=feature_descriptions)

@app.route('/predict', methods=['POST'])
def predict():
    """预测接口"""
    try:
        # 获取输入数据
        input_data = []
        for feature in feature_names:
            value = request.form.get(feature)
            if value is None or value == '':
                return jsonify({'error': f'Please fill in {feature_descriptions[feature]}'})
            
            try:
                input_data.append(float(value))
            except ValueError:
                return jsonify({'error': f'{feature_descriptions[feature]} must be a number'})
        
        # 预测
        result = predict_risk(input_data)
        if result is None:
            return jsonify({'error': 'Prediction failed'})
        
        # 生成SHAP解释
        shap_data = generate_shap_explanation(input_data)
        
        return jsonify({
            'success': True,
            'prediction': result,
            'shap_explanation': shap_data
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'})

@app.route('/api/model_info')
def model_info():
    """获取模型信息"""
    return jsonify({
        'model_type': 'GradientBoostingClassifier',
        'features': feature_names,
        'feature_descriptions': feature_descriptions,
        'model_parameters': {
            'learning_rate': 0.2,
            'max_depth': 3,
            'min_samples_leaf': 2,
            'min_samples_split': 10,
            'n_estimators': 100
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Twin Severe Outcome Prediction Web Diagnostic Tool...")
    load_model()
    print("✅ Model loading completed")
    print("🌐 Visit http://localhost:5000 to use the diagnostic tool")
    app.run(debug=True, host='0.0.0.0', port=5000)


