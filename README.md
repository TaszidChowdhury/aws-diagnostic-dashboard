# AWS Diagnostic Tool

A beginner-friendly Flask web application that simulates the tasks of a technical support analyst working with AWS infrastructure. This tool provides a comprehensive dashboard for monitoring and diagnosing AWS resources.

## 🚀 Quick Start Guide

### **Option 1: Demo Mode (No AWS Account Required)**
Perfect for testing and learning without real AWS credentials!

```bash
# 1. Clone and setup
git clone <repository-url>
cd aws-diagnostic-dashboard

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
python app.py

# 5. Access the application
# Open http://localhost:5000 in your browser
# Login: admin / admin123
```

**Demo Mode Features:**
- ✅ Sample EC2 instances with realistic data
- ✅ Interactive performance metrics and charts
- ✅ Alert system with high CPU indicators
- ✅ Console output and system logs
- ✅ All dashboard features fully functional

### **Option 2: Real AWS Data**
Connect to your actual AWS account for production use.

## Features

- **EC2 Instance Management**: List and view metadata for all EC2 instances in selected AWS regions
- **Real-time Monitoring**: Fetch and display CloudWatch metrics (CPU, Network, Disk) for the last hour
- **Interactive Charts**: Visualize metrics using Plotly charts with real-time updates
- **Log Analysis**: Retrieve and display system logs from CloudWatch Logs
- **Alert System**: Automatic highlighting of instances with high CPU usage (>80%)
- **Secure Access**: Protected dashboard with Flask-Login authentication
- **Responsive UI**: Clean, modern interface built with Bootstrap
- **Demo Mode**: Full functionality with sample data (no AWS credentials required)

## 📋 Prerequisites

- Python 3.8 or higher
- AWS Account with appropriate permissions (for real data)
- AWS credentials configured (Access Key ID and Secret Access Key) - optional for demo mode

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd aws-diagnostic-dashboard
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   # AWS Configuration (optional for demo mode)
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_DEFAULT_REGION=us-east-1

   # Flask Configuration
   FLASK_SECRET_KEY=your-secret-key-change-in-production
   FLASK_DEBUG=True
   FLASK_CONFIG=development

   # Application Configuration
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin123

   # Server Configuration
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## 🔐 Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change these credentials in production!

## 🎯 How to Use the Application

### **Step 1: Login**
1. Open `http://localhost:5000` in your browser
2. Enter credentials: `admin` / `admin123`
3. Click "Login"

### **Step 2: Explore the Dashboard**
Once logged in, you'll see:

#### **📊 Summary Cards (Top)**
- **Total Instances**: Count of all EC2 instances
- **Running Instances**: Currently active instances
- **Stopped Instances**: Terminated or stopped instances
- **Active Alerts**: Instances with high resource usage

#### **🌍 Region Selector (Top-Right)**
- Dropdown to choose AWS region
- Default: `us-east-1`
- Changes refresh the dashboard with region-specific data

#### **📋 Instances Table**
- List of all EC2 instances with key information
- **Filter Buttons**: All, Running, Stopped
- **Action Icons** for each instance:
  - 👁️ **Eye Icon**: View detailed instance information
  - 📊 **Chart Icon**: View performance metrics (CPU, network, disk)
  - ℹ️ **Info Icon**: Quick status check

### **Step 3: View Instance Details**
Click the **👁️ eye icon** next to any instance to see:

- **Basic Information**: Instance ID, type, state, launch time
- **Network Details**: Public/private IPs, VPC, subnet
- **Security Groups**: Associated security configurations
- **Block Devices**: EBS volumes and configurations
- **Performance Metrics**: Interactive charts
- **Console Output**: System logs and console output

### **Step 4: Check Performance Metrics**
Click the **📊 chart icon** to see:

- **CPU Utilization**: Line chart over the last hour
- **Network Traffic**: In/out traffic patterns
- **Disk I/O**: Read/write operations
- **Interactive Features**: Hover for details, zoom capabilities

### **Step 5: Monitor Alerts**
The dashboard automatically highlights:
- **🔴 Red**: High CPU usage (>80%)
- **🟡 Yellow**: Medium CPU usage (>70%)
- **🟢 Green**: Normal usage

### **Step 6: Navigate the Interface**

#### **Sidebar Navigation:**
- **🏠 Dashboard**: Main overview
- **📊 Instances**: Detailed instance list
- **🚨 Alerts**: Active alerts and notifications
- **📈 Metrics**: Performance overview
- **📝 Logs**: System and application logs
- **👤 Profile**: User settings

#### **Top Navigation:**
- **Region Selector**: Change AWS region
- **User Menu**: Profile, settings, logout

## 🎮 Demo Mode Features

When running without AWS credentials, you'll see:

### **Sample Instances:**
1. **Web Server 1** (Running, 45% CPU)
   - Instance ID: `i-1234567890abcdef0`
   - Type: `t3.micro`
   - Public IP: `52.23.45.67`

2. **Database Server** (Running, 85% CPU - High Alert!)
   - Instance ID: `i-0987654321fedcba0`
   - Type: `t3.small`
   - Public IP: `52.23.45.68`

3. **Backup Server** (Stopped, 0% CPU)
   - Instance ID: `i-abcdef1234567890`
   - Type: `t3.micro`
   - Status: Stopped

### **Interactive Features:**
- ✅ **Realistic Data**: Sample instances with realistic names, IPs, configurations
- ✅ **Dynamic Metrics**: CPU, network, disk data that changes over time
- ✅ **Alert Conditions**: High CPU usage triggers visual alerts
- ✅ **Console Logs**: Sample system boot and operation logs
- ✅ **Security Groups**: Sample security group configurations
- ✅ **Block Devices**: Sample EBS volume information

## 🔄 Connecting Real AWS Data

When you're ready to see actual AWS instances:

### **Step 1: Get AWS Credentials**
1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Click your username → "Security credentials"
3. Under "Access keys" → "Create access key"
4. Copy the Access Key ID and Secret Access Key

### **Step 2: Update Configuration**
```bash
# Edit the .env file
nano .env
```

### **Step 3: Replace Placeholder Values**
```env
AWS_ACCESS_KEY_ID=AKIA...your_actual_access_key
AWS_SECRET_ACCESS_KEY=your_actual_secret_key
AWS_DEFAULT_REGION=us-east-1  # or your preferred region
```

### **Step 4: Restart Application**
```bash
# Stop current process (Ctrl+C)
python app.py
```

## 🛠️ Troubleshooting

### **Common Issues and Solutions:**

#### **1. Port Already in Use**
```bash
# Check what's using the port
lsof -i :5000

# Kill processes using the port
pkill -f "python.*app.py"

# Or use a different port
FLASK_PORT=5001 python app.py
```

#### **2. AWS Credentials Error**
```
AWS credentials error: An error occurred (InvalidClientTokenId)
```
**Solution**: 
- Check your `.env` file has correct credentials
- Verify your AWS access keys are valid
- Ensure the region is correct
- Or use demo mode (no credentials required)

#### **3. No Instances Shown**
**Solution**:
- Verify you have EC2 instances in the selected region
- Check your IAM permissions include EC2 read access
- Try switching to a different region
- In demo mode, instances should always appear

#### **4. Error Loading Metrics**
**Solution**:
- Ensure CloudWatch monitoring is enabled on instances
- Check IAM permissions include CloudWatch access
- Verify instances are running (stopped instances won't have metrics)
- Demo mode provides sample metrics automatically

#### **5. Login Failed**
**Solution**:
- Use default credentials: `admin` / `admin123`
- Check the `.env` file has correct `ADMIN_USERNAME` and `ADMIN_PASSWORD`
- Ensure Flask secret key is set

#### **6. Application Won't Start**
```bash
# Check for syntax errors
python -m py_compile app.py

# Test imports
python -c "import app; print('App imported successfully')"

# Check dependencies
pip list | grep -E "(flask|boto3)"
```

### **Getting Help**

1. **Check the logs**: Look at the terminal output for error messages
2. **Verify setup**: Ensure virtual environment is activated
3. **Test connectivity**: Try accessing the health endpoint
4. **Review permissions**: Ensure your IAM user has required permissions
5. **Use demo mode**: Test with sample data first

## 📱 Mobile Usage

The interface is fully responsive:
- Works on phones and tablets
- Touch-friendly buttons
- Swipe navigation
- Optimized charts for mobile

## 🔒 Security Best Practices

### **For Production Use:**

1. **Change Default Credentials**:
   ```env
   ADMIN_USERNAME=your_secure_username
   ADMIN_PASSWORD=your_strong_password
   ```

2. **Use IAM Roles** (instead of access keys):
   - Create an IAM role with the policy from `iam_policy_example.json`
   - Attach the role to your EC2 instance
   - Remove access keys from `.env`

3. **Enable HTTPS**:
   - Use a reverse proxy (Nginx) with SSL certificates
   - Configure Flask for HTTPS in production

4. **Regular Updates**:
   - Keep dependencies updated
   - Monitor for security patches
   - Rotate credentials regularly

## 🚀 Deployment Options

### **Local Development**
```bash
python app.py
# Access at http://localhost:5000
```

### **AWS EC2**
1. Launch EC2 instance with Ubuntu/Amazon Linux
2. Install Python and dependencies
3. Use Gunicorn as WSGI server
4. Set up Nginx as reverse proxy
5. Configure environment variables

### **AWS Elastic Beanstalk**
1. Package your application
2. Deploy using AWS Elastic Beanstalk console
3. Configure environment variables in EB console

### **Render (Free Tier)**
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy automatically on push

### **Docker**
```bash
# Build and run with Docker
docker build -t aws-diagnostic-tool .
docker run -p 5000:5000 aws-diagnostic-tool
```

## 📊 API Endpoints

The application provides RESTful APIs for programmatic access:

```bash
# Get all instances
curl http://localhost:5000/api/instances

# Get metrics for specific instance
curl http://localhost:5000/api/metrics/i-1234567890abcdef0

# Get alerts
curl http://localhost:5000/api/alerts

# Health check
curl http://localhost:5000/health
```

## 🎯 Common Use Cases

### **Scenario 1: Check for Performance Issues**
1. Login to dashboard
2. Look for red/yellow CPU indicators
3. Click on problematic instances
4. View detailed metrics and logs
5. Check console output for errors

### **Scenario 2: Monitor Instance Health**
1. Select your AWS region
2. Review the summary cards
3. Check instance states (running/stopped)
4. Examine system and instance status
5. View recent console output

### **Scenario 3: Investigate Network Issues**
1. Click on a running instance
2. Navigate to the metrics section
3. Check network in/out charts
4. Look for unusual traffic patterns
5. Review security group configurations

## 📁 Project Structure

```
aws-diagnostic-dashboard/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
├── templates/           # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── instance_detail.html
├── routes/             # Flask route modules
│   ├── __init__.py
│   ├── auth.py
│   ├── dashboard.py
│   └── api.py
├── services/           # AWS service modules
│   ├── __init__.py
│   ├── ec2_service.py
│   ├── cloudwatch_service.py
│   └── logs_service.py
└── utils/             # Utility functions
    ├── __init__.py
    └── helpers.py
```

## 🔐 IAM Policy Requirements

Create an IAM user with the following policy for read-only access:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceStatus",
                "ec2:GetConsoleOutput",
                "cloudwatch:GetMetricData",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:GetLogEvents",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review AWS documentation
- Open an issue on GitHub
- Use demo mode to test features without AWS credentials

## ⚠️ Disclaimer

This tool is for educational and diagnostic purposes. Always follow AWS best practices and security guidelines when working with production environments. The demo mode provides a safe way to learn and test the interface without affecting real AWS resources.

---

**🎉 Ready to get started?** 

1. **For immediate testing**: Use demo mode (no AWS account required)
2. **For production use**: Add your AWS credentials and follow security best practices
3. **For learning**: Explore all features with the sample data first

The AWS Diagnostic Tool is designed to be both educational and practical, providing a comprehensive interface for AWS infrastructure monitoring and troubleshooting! 