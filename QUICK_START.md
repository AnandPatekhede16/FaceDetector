# 🚀 Quick Start Guide - Face Recognition System

## ❌ **Current Issue: Python Not Found**

You're seeing this error because Python is not installed or not in your system PATH.

## ✅ **Solution: Install Python**

### **Step 1: Download Python**
1. Go to: https://www.python.org/downloads/
2. Click "Download Python 3.x.x" (latest version)
3. Run the installer

### **Step 2: Install Python (IMPORTANT!)**
During installation, **MUST CHECK**:
- ✅ **"Add Python to PATH"** (This is crucial!)
- ✅ "Install for all users"
- ✅ "Add Python to environment variables"

### **Step 3: Restart Command Prompt**
After installation, **close and reopen** your command prompt.

### **Step 4: Test Python**
```bash
python --version
pip --version
```

You should see:
```
Python 3.9.7
pip 21.2.4
```

### **Step 5: Run the System**
```bash
# Install dependencies
pip install -r requirements.txt

# Test the system
python test_simple.py

# Run the system
python run_simple.py
```

## 🔧 **Alternative: Use Batch File**

Double-click `install_and_run.bat` - it will:
1. Check if Python is installed
2. Open Python download page if needed
3. Install dependencies
4. Test the system

## 🐍 **Python Installation Troubleshooting**

### **If Python Still Not Found:**

1. **Check Installation Path:**
   - Look for Python in: `C:\Python39\` or `C:\Users\YourName\AppData\Local\Programs\Python\`

2. **Manual PATH Setup:**
   - Press `Win + R`, type `sysdm.cpl`
   - Click "Environment Variables"
   - Edit "Path" variable
   - Add Python installation directory

3. **Use Full Path:**
   ```bash
   C:\Python39\python.exe test_simple.py
   ```

4. **Microsoft Store Python:**
   ```bash
   python
   # This opens Microsoft Store to install Python
   ```

## 📱 **Alternative: Anaconda**

If you prefer Anaconda:
1. Download from: https://www.anaconda.com/products/distribution
2. Install with default settings
3. Use "Anaconda Prompt" instead of regular command prompt

## ✅ **Success Indicators**

You'll know Python is working when:
- ✅ `python --version` shows Python version
- ✅ `pip --version` shows pip version
- ✅ `python test_simple.py` runs without errors

## 🎯 **Next Steps After Python Installation**

1. **Test the system:**
   ```bash
   python test_simple.py
   ```

2. **Run registration:**
   ```bash
   python simple_register.py
   ```

3. **Run recognition:**
   ```bash
   python recognize.py
   ```

## 📞 **Still Having Issues?**

If you're still having problems:
1. Make sure you **restarted** the command prompt after installing Python
2. Check that "Add Python to PATH" was checked during installation
3. Try running as administrator
4. Use the full path to Python executable

The system will work perfectly once Python is properly installed and accessible from the command line!

