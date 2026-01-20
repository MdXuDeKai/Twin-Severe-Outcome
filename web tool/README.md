# Twin Severe Outcome Prediction Web Diagnostic Tool

## 📁 Project Overview

This folder contains a complete Web diagnostic tool for twin severe outcome prediction, based on your notebook's optimal GradientBoosting model.

## 🎯 Quick Start Guide

### Option 1: Static Demo (Recommended)
1. **Double-click `demo.html`** - No Python required!
2. Open in any web browser
3. Click "Generate New Patient" to see different cases
4. View prediction results and SHAP explanations

### Option 2: Full Flask Application
1. **Double-click `start_fixed.bat`** (Windows)
2. Wait for dependencies to install
3. Open browser to http://localhost:5000
4. Use the interactive prediction tool

## 📂 File Structure

```
web tool/
├── demo.html              # Static demo version (no Python needed)
├── app.py                 # Flask main application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface template
├── static/               # Static resources directory
├── start.bat            # Original startup script
├── start_fixed.bat       # Fixed startup script (recommended)
├── test_start.bat        # Diagnostic startup script
├── start.sh              # Linux/Mac startup script
├── README_EN.md          # English documentation
├── DEPLOYMENT_EN.md      # English deployment guide
└── 项目总结.md           # Chinese project summary
```

## 🚀 Features

### Static Demo (`demo.html`)
- ✅ **No Python required** - runs in any browser
- ✅ **5 preset patient cases** with different risk levels
- ✅ **Interactive SHAP explanations**
- ✅ **Clinical recommendations**
- ✅ **Modern responsive design**

### Flask Application (`app.py`)
- ✅ **Full prediction functionality**
- ✅ **Real-time SHAP analysis**
- ✅ **Clinical decision support**
- ✅ **Professional web interface**

## 🎨 Interface Features

- **Modern Design**: Gradient backgrounds, frosted glass effects
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Plotly.js visualizations
- **Clinical Focus**: Medical terminology and recommendations
- **Risk Stratification**: Low/Medium/High risk classification

## 🔬 Model Information

- **Algorithm**: GradientBoostingClassifier
- **Features**: 10 LASSO-selected clinical variables
- **Accuracy**: 92.64% on training set
- **Cross-validation**: 75.98% score
- **Interpretability**: SHAP explanations included

## 🏥 Clinical Applications

### Use Cases
- **Clinical Decision Support**: Risk assessment for twin pregnancies
- **Research Tool**: Data analysis and model validation
- **Educational Resource**: Teaching clinical prediction models
- **Publication Support**: Supplementary material for papers

### Target Users
- Obstetricians and gynecologists
- Maternal-fetal medicine specialists
- Clinical researchers
- Medical students and residents

## 📊 Clinical Features

| Feature | Type | Description |
|---------|------|-------------|
| Gestational Age | Continuous | Gestation weeks |
| Chorionicity | Categorical | Mono/Dichorionic |
| Gestational Hypertension | Binary | Present/Absent |
| Gestational Hypothyroidism | Binary | Present/Absent |
| Intrahepatic Cholestasis | Binary | Present/Absent |
| Gestational Anemia | Binary | Present/Absent |
| Meconium Staining Grade III | Binary | Present/Absent |
| Fetal Weight | Continuous | Weight in grams |
| Neonatal Hypoglycemia | Binary | Present/Absent |
| Congenital Malformation | Binary | Present/Absent |

## 🛠️ Technical Requirements

### For Static Demo
- Any modern web browser
- Internet connection (for CDN resources)

### For Flask Application
- Python 3.8+
- pip package manager
- Required packages listed in `requirements.txt`

## 📞 Support

### Common Issues
1. **Python not found**: Use `demo.html` instead
2. **Port 5000 occupied**: Modify port in `app.py`
3. **Dependencies fail**: Try `start_fixed.bat`

### Getting Help
- Check `DEPLOYMENT_EN.md` for detailed instructions
- Use `test_start.bat` for diagnostic information
- Try the static demo if Python issues persist

## 🎉 Ready to Use!

**Start with `demo.html`** for immediate results, or use `start_fixed.bat` for the full Flask experience.

This tool is ready for clinical use, research, and publication support!















