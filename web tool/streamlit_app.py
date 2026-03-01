#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双胞胎严重结局预测Web诊断工具 - Streamlit版本
基于GradientBoostingClassifier的最佳模型
"""

import streamlit as st
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
import matplotlib.pyplot as plt

# 页面配置
st.set_page_config(
    page_title="双胞胎严重结局预测工具",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 全局变量
@st.cache_resource
def load_model():
    """加载训练好的模型"""
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
    
    # 检查是否有保存的模型文件（更新路径，因为现在在 web tool 目录下）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    model_paths = [
        os.path.join(current_dir, 'best_model_gbm.pkl'),  # web tool/best_model_gbm.pkl
        os.path.join(parent_dir, 'best_model_gbm.pkl'),   # 根目录/best_model_gbm.pkl
        'best_model_gbm.pkl',  # 当前目录
        '../best_model_gbm.pkl'  # 上级目录
    ]
    
    model = None
    for path in model_paths:
        if os.path.exists(path):
            try:
                model = pickle.load(open(path, 'rb'))
                st.success(f"✅ 成功加载模型: {path}")
                break
            except Exception as e:
                st.warning(f"⚠️ 加载模型失败 {path}: {e}")
    
    if model is None:
        st.info("⚠️ 未找到保存的模型文件，使用默认参数创建模型")
        model = create_default_model()
    
    return model, feature_names, feature_descriptions

def create_default_model():
    """创建默认的GB模型（基于notebook中的最优参数）"""
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
    
    return model

def predict_risk(model, input_data, feature_names):
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
        st.error(f"预测错误: {e}")
        return None

def get_risk_level(risk_score):
    """根据风险评分确定风险等级"""
    if risk_score < 0.3:
        return "低风险"
    elif risk_score < 0.7:
        return "中等风险"
    else:
        return "高风险"

def get_confidence(proba):
    """计算预测置信度"""
    max_proba = max(proba)
    if max_proba > 0.8:
        return "高"
    elif max_proba > 0.6:
        return "中等"
    else:
        return "低"

def generate_shap_explanation(model, input_data, feature_names):
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
        
        # 创建SHAP数据
        shap_data = []
        for i, (feature, value) in enumerate(zip(feature_names, shap_values[0])):
            shap_data.append({
                'feature': feature,
                'shap_value': float(value),
                'feature_value': float(input_data[i]),
                'importance': abs(float(value))
            })
        
        # 按重要性排序
        shap_data.sort(key=lambda x: x['importance'], reverse=True)
        
        return shap_data
    except Exception as e:
        st.error(f"SHAP解释错误: {e}")
        return None

# 主应用
def main():
    # 标题
    st.title("🏥 双胞胎严重结局预测Web诊断工具")
    st.markdown("---")
    st.markdown("基于GradientBoostingClassifier的最佳模型进行预测")
    
    # 加载模型
    model, feature_names, feature_descriptions = load_model()
    
    # 侧边栏
    with st.sidebar:
        st.header("📋 模型信息")
        st.info("""
        **模型类型**: GradientBoostingClassifier
        
        **特征数量**: 10个LASSO筛选的特征
        
        **准确率**: 训练集92.64%
        
        **交叉验证**: 75.98%
        """)
        
        st.markdown("---")
        st.header("📊 特征说明")
        for feature, desc in feature_descriptions.items():
            st.text(f"• {desc}")
    
    # 主界面
    st.header("📝 输入患者信息")
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    input_data = {}
    
    with col1:
        st.subheader("基本信息")
        input_data['Gestational Age'] = st.number_input(
            "Gestational Age (weeks)",
            min_value=20.0,
            max_value=45.0,
            value=37.0,
            step=0.1,
            help="妊娠周数"
        )
        
        input_data['Chorionicity'] = st.selectbox(
            "Chorionicity",
            options=[0, 1],
            format_func=lambda x: "Monochorionic" if x == 0 else "Dichorionic",
            help="绒毛膜性 (0=单绒毛膜, 1=双绒毛膜)"
        )
        
        input_data['FetalWeight'] = st.number_input(
            "Fetal Weight (grams)",
            min_value=500.0,
            max_value=5000.0,
            value=2500.0,
            step=50.0,
            help="胎儿体重（克）"
        )
        
        input_data['GestationalHypertension'] = st.selectbox(
            "Gestational Hypertension",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="妊娠期高血压 (0=否, 1=是)"
        )
        
        input_data['GestationalHypothyroidism'] = st.selectbox(
            "Gestational Hypothyroidism",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="妊娠期甲状腺功能减退 (0=否, 1=是)"
        )
    
    with col2:
        st.subheader("并发症信息")
        input_data['IntrahepaticCholestasis'] = st.selectbox(
            "Intrahepatic Cholestasis",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="肝内胆汁淤积 (0=否, 1=是)"
        )
        
        input_data['GestationalAnemia'] = st.selectbox(
            "Gestational Anemia",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="妊娠期贫血 (0=否, 1=是)"
        )
        
        input_data['MeconiumStainingIII'] = st.selectbox(
            "Meconium Staining Grade III",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="胎粪污染III度 (0=否, 1=是)"
        )
        
        input_data['NeonatalHypoglycemia'] = st.selectbox(
            "Neonatal Hypoglycemia",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="新生儿低血糖 (0=否, 1=是)"
        )
        
        input_data['CongenitalMalformation'] = st.selectbox(
            "Congenital Malformation",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            help="先天性畸形 (0=否, 1=是)"
        )
    
    # 预测按钮
    st.markdown("---")
    if st.button("🔮 开始预测", type="primary", use_container_width=True):
        # 准备输入数据
        input_array = [input_data[feature] for feature in feature_names]
        
        # 预测
        with st.spinner("正在预测..."):
            result = predict_risk(model, input_array, feature_names)
            
            if result:
                # 显示结果
                st.success("✅ 预测完成！")
                
                # 结果展示
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("风险评分", f"{result['risk_score']:.2%}")
                
                with col2:
                    risk_color = {
                        "低风险": "🟢",
                        "中等风险": "🟡",
                        "高风险": "🔴"
                    }
                    st.metric("风险等级", f"{risk_color.get(result['risk_level'], '')} {result['risk_level']}")
                
                with col3:
                    st.metric("预测结果", "严重结局" if result['prediction'] == 1 else "正常")
                
                with col4:
                    st.metric("置信度", result['confidence'])
                
                # 风险评分可视化
                st.markdown("---")
                st.subheader("📊 风险评分可视化")
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=result['risk_score'] * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "风险评分 (%)"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # SHAP解释
                st.markdown("---")
                st.subheader("🔍 SHAP特征重要性分析")
                
                shap_data = generate_shap_explanation(model, input_array, feature_names)
                
                if shap_data:
                    # 创建SHAP条形图
                    shap_df = pd.DataFrame(shap_data)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=shap_df['importance'],
                        y=shap_df['feature'],
                        orientation='h',
                        marker=dict(
                            color=shap_df['shap_value'],
                            colorscale='RdBu',
                            showscale=True,
                            colorbar=dict(title="SHAP值")
                        ),
                        text=[f"{v:.4f}" for v in shap_df['shap_value']],
                        textposition='outside'
                    ))
                    
                    fig.update_layout(
                        title="特征重要性分析 (SHAP值)",
                        xaxis_title="重要性 (绝对值)",
                        yaxis_title="特征",
                        height=500,
                        yaxis={'categoryorder': 'total ascending'}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # SHAP值表格
                    st.subheader("📋 详细SHAP值")
                    display_df = pd.DataFrame([
                        {
                            '特征': feature_descriptions[item['feature']],
                            '特征值': item['feature_value'],
                            'SHAP值': f"{item['shap_value']:.4f}",
                            '重要性': f"{item['importance']:.4f}"
                        }
                        for item in shap_data
                    ])
                    st.dataframe(display_df, use_container_width=True)
                
                # 临床建议
                st.markdown("---")
                st.subheader("💡 临床建议")
                
                if result['risk_level'] == "高风险":
                    st.error("""
                    **高风险患者建议**:
                    - 密切监测胎儿状况
                    - 考虑提前分娩
                    - 加强产前检查频率
                    - 准备新生儿重症监护资源
                    """)
                elif result['risk_level'] == "中等风险":
                    st.warning("""
                    **中等风险患者建议**:
                    - 定期产前检查
                    - 监测相关并发症指标
                    - 保持与医疗团队的沟通
                    """)
                else:
                    st.success("""
                    **低风险患者建议**:
                    - 常规产前检查
                    - 保持良好的生活习惯
                    - 定期随访
                    """)

if __name__ == "__main__":
    main()
