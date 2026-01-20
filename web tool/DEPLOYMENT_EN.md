# Twin Severe Outcome Prediction Web Diagnostic Tool - Deployment Guide

## 🚀 Quick Deployment

### Windows Users
1. Double-click `start.bat` file
2. Wait for dependency installation to complete
3. Browser access http://localhost:5000

### Linux/Mac Users
1. Run in terminal:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```
2. Browser access http://localhost:5000

## 📋 Manual Deployment Steps

### 1. Environment Requirements
- Python 3.8 or higher
- pip package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app.py
```

### 4. Access Application
Open browser and visit: http://localhost:5000

## 🔧 Configuration Instructions

### Port Configuration
Default port is 5000, to modify:
1. Edit `app.py` file
2. Modify the last line: `app.run(debug=True, host='0.0.0.0', port=5000)`
3. Change 5000 to your desired port number

### Model File
- If `best_model_gbm.pkl` file exists, system will automatically load it
- Otherwise, create model with default parameters

## 🌐 Network Access

### LAN Access
Application is bound to `0.0.0.0` by default, other devices on LAN can access via:
- `http://[Your IP Address]:5000`

### External Network Access (requires configuration)
1. Ensure firewall allows port 5000
2. Configure router port forwarding
3. Access using public IP

## 📱 Mobile Support

Application uses responsive design, supporting:
- Mobile browsers
- Tablet browsers
- Desktop browsers

## 🔒 Security Considerations

1. **Data Privacy**: All data processed locally, not uploaded to external servers
2. **Network Security**: Recommended for use in intranet environment
3. **Access Control**: Can configure access permissions and user authentication

## 🐛 Troubleshooting

### Common Issues

**Q: Port 5000 is occupied**
A: Modify port number in `app.py`, or close programs occupying that port

**Q: Dependency installation failed**
A: Try using domestic mirror:
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

**Q: Model loading failed**
A: Check if `best_model_gbm.pkl` file exists, or use default model

**Q: Page cannot access**
A: Check firewall settings, ensure port 5000 is open

### Log Viewing
Application displays detailed logs in console during runtime, including:
- Model loading status
- Prediction request processing
- Error messages

## 📊 Performance Optimization

### Server Configuration
- **CPU**: 2 cores or more
- **Memory**: 4GB or more
- **Storage**: 1GB available space

### Concurrent Processing
Default configuration supports multiple users accessing simultaneously, for handling large concurrency:
1. Use WSGI servers like Gunicorn
2. Configure load balancing
3. Use caching systems like Redis

## 🔄 Update and Maintenance

### Model Updates
1. Replace `best_model_gbm.pkl` file
2. Restart application
3. Verify prediction results

### Feature Updates
1. Backup current version
2. Update code files
3. Restart application
4. Test new features

## 📞 Technical Support

If encountering technical issues, please provide:
1. Operating system version
2. Python version
3. Error logs
4. Problem description

---

**Note**: This tool is for research and clinical reference only. Please ensure compliance with relevant medical regulations.
