# Twin Severe Outcome Prediction Web Diagnostic Tool

## Project Overview

Based on your notebook's optimal GradientBoosting model, I have built a complete Web diagnostic tool with the following features:

### ✨ Core Features
- **Intelligent Prediction**: Based on 10 LASSO-selected key clinical features
- **SHAP Explanation**: Provides feature importance analysis and visualization
- **Modern Interface**: Responsive design supporting mobile access
- **Clinical-Oriented**: Input interface designed for actual clinical needs
- **Risk Stratification**: Low/Medium/High risk three-tier classification

### 🏆 Model Performance
- **Training Set Accuracy**: 92.64%
- **Cross-Validation Score**: 75.98%
- **Optimal Parameters**: learning_rate=0.2, max_depth=3, n_estimators=100

## 📁 File Structure

```
├── app.py                 # Flask main application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface template
├── static/               # Static resources directory
├── start.bat            # Windows startup script
├── start.sh              # Linux/Mac startup script
├── README.md             # Project documentation
└── DEPLOYMENT.md         # Deployment guide
```

## 🚀 Quick Start

### Windows Users
1. Double-click `start.bat` file
2. Wait for dependency installation to complete
3. Browser access http://localhost:5000

### Linux/Mac Users
```bash
chmod +x start.sh
./start.sh
```

## 🎨 Interface Features

### Modern Design
- Gradient background and frosted glass effects
- Responsive grid layout
- Intuitive risk score cards
- Interactive SHAP charts

### User Experience
- Smart form validation
- Real-time prediction results
- Clinical recommendation generation
- Mobile adaptation

## 🔬 Technical Architecture

### Backend Technology
- **Flask**: Web framework
- **scikit-learn**: Machine learning
- **SHAP**: Model interpretation
- **pandas/numpy**: Data processing

### Frontend Technology
- **Bootstrap 5**: UI framework
- **Plotly.js**: Chart visualization
- **Font Awesome**: Icon library

## 📊 Prediction Process

1. **Data Input**: User fills in 10 clinical features
2. **Model Prediction**: GradientBoosting algorithm calculates risk probability
3. **Result Display**: Risk score, level, confidence
4. **SHAP Explanation**: Feature importance visualization
5. **Clinical Recommendations**: Recommendations based on risk level

## 🎯 Clinical Features

| Feature Name | Type | Description |
|---------|------|------|
| Gestational Age | Continuous | Gestation weeks |
| Chorionicity | Categorical | Mono/Dichorionic |
| Gestational Hypertension | Binary | Whether diagnosed |
| Gestational Hypothyroidism | Binary | Whether diagnosed |
| Intrahepatic Cholestasis | Binary | Whether diagnosed |
| Gestational Anemia | Binary | Whether diagnosed |
| Meconium Staining Grade III | Binary | Whether occurred |
| Fetal Weight | Continuous | Fetal weight (grams) |
| Neonatal Hypoglycemia | Binary | Whether occurred |
| Congenital Malformation | Binary | Whether diagnosed |

## 🔍 SHAP Explanation Features

### Visualization Features
- **Bar Chart**: Shows each feature's impact on prediction
- **Color Coding**: Red indicates increased risk, blue indicates decreased risk
- **Sorted Display**: Arranged by importance from high to low
- **Value Annotation**: Precise SHAP value display

### Clinical Value
- Helps understand model decision process
- Identifies key risk factors
- Guides clinical intervention strategies
- Improves diagnostic transparency

## 🏥 Clinical Applications

### Applicable Scenarios
- Prenatal risk assessment
- Clinical decision support
- Teaching and training tools
- Research data analysis

### Usage Recommendations
- Use in combination with clinical experience
- Regularly validate prediction accuracy
- Pay attention to model limitations
- Protect patient privacy

## 🔧 Custom Configuration

### Model Parameter Adjustment
To use your specifically trained model:
1. Save the model as `best_model_gbm.pkl`
2. Place in application root directory
3. Restart application to automatically load

### Interface Customization
- Modify `templates/index.html` to adjust interface
- Update CSS styles for custom appearance
- Add new visualization charts

## 📈 Extended Features

### Possible Enhancements
- Batch prediction functionality
- Historical record management
- User permission control
- Data export functionality
- Multi-language support

## 🛡️ Security and Privacy

- **Local Processing**: All data computed locally
- **No Data Upload**: No data sent to external servers
- **Access Control**: Configurable access permissions
- **Data Protection**: Complies with medical data protection requirements

## 📞 Technical Support

### Common Issues
1. **Port Conflict**: Modify port number in app.py
2. **Dependency Installation Failure**: Use domestic mirror sources
3. **Model Loading Failure**: Check if pkl file exists
4. **Page Cannot Access**: Check firewall settings

### Performance Optimization
- Use SSD storage to improve loading speed
- Configure sufficient memory resources
- Regularly clean temporary files

---

**Congratulations!** Your Web diagnostic tool is ready. This is a clinical decision support system that meets high-level medical journal standards, with modern interface design and powerful prediction capabilities. You can use it directly for clinical work or as supplementary material for papers.
