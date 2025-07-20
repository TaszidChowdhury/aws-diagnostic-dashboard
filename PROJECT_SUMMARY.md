# AWS Diagnostic Tool - Project Summary

## Overview

The AWS Diagnostic Tool is a comprehensive Flask web application designed to simulate the tasks of a technical support analyst working with AWS infrastructure. This beginner-friendly application provides a modern, responsive dashboard for monitoring and diagnosing AWS resources.

## 🚀 Key Features

### Core Functionality
- **EC2 Instance Management**: List and view metadata for all EC2 instances across AWS regions
- **Real-time Monitoring**: Fetch and display CloudWatch metrics (CPU, Network, Disk) for the last hour
- **Interactive Charts**: Visualize metrics using Plotly.js with real-time updates
- **Log Analysis**: Retrieve and display system logs from CloudWatch Logs
- **Alert System**: Automatic highlighting of instances with high CPU usage (>80%)
- **Secure Access**: Protected dashboard with Flask-Login authentication
- **Responsive UI**: Clean, modern interface built with Bootstrap 5

### Technical Features
- **Multi-region Support**: Switch between AWS regions seamlessly
- **API Endpoints**: RESTful API for AJAX requests and data fetching
- **Error Handling**: Comprehensive error handling and user-friendly messages
- **Health Checks**: Built-in health check endpoints for monitoring
- **Modular Architecture**: Clean separation of concerns with blueprints and services

## 🏗️ Architecture

### Project Structure
```
aws-diagnostic-dashboard/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── env_example.txt       # Environment variables template
├── iam_policy_example.json # IAM policy for AWS permissions
├── README.md             # Comprehensive documentation
├── DEPLOYMENT.md         # Deployment instructions
├── PROJECT_SUMMARY.md    # Project overview
├── .gitignore           # Git ignore rules
├── static/              # Static files (CSS, JS)
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── login.html       # Login page
│   ├── dashboard.html   # Main dashboard
│   ├── instance_detail.html # Instance details page
│   ├── profile.html     # User profile page
│   └── errors/          # Error pages (404, 500)
├── routes/              # Flask route modules
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   └── api.py           # API endpoints
├── services/            # AWS service modules
│   ├── ec2_service.py   # EC2 operations
│   ├── cloudwatch_service.py # CloudWatch metrics
│   └── logs_service.py  # CloudWatch Logs
└── utils/               # Utility functions
    └── helpers.py       # Helper functions
```

### Technology Stack
- **Backend**: Flask 2.3.3, Python 3.8+
- **Frontend**: Bootstrap 5, jQuery, Plotly.js
- **AWS SDK**: Boto3 for AWS service integration
- **Authentication**: Flask-Login
- **Deployment**: Gunicorn (production), Flask development server (development)

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- AWS Account with appropriate permissions
- AWS credentials (Access Key ID and Secret Access Key)

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd aws-diagnostic-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env_example.txt .env
# Edit .env with your AWS credentials

# Run application
python app.py
```

### Default Login Credentials
- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change these credentials in production!

## 🔐 Security Features

### Authentication
- Flask-Login integration for session management
- Protected routes with `@login_required` decorator
- Secure password handling
- Session-based authentication

### AWS Security
- Environment variable configuration for credentials
- IAM policy with least privilege principle
- Read-only access to EC2 and CloudWatch services
- Support for IAM roles (recommended for production)

### Application Security
- CSRF protection
- Secure headers
- Input sanitization
- Error handling without information disclosure

## 📊 Dashboard Features

### Instance Overview
- **Summary Cards**: Total, running, stopped instances, and alerts
- **Instance Table**: Detailed view with filtering options
- **State Indicators**: Color-coded instance states
- **Quick Actions**: View details, metrics, and logs

### Metrics Visualization
- **CPU Utilization**: Real-time CPU usage charts
- **Network Traffic**: Network in/out metrics
- **Disk I/O**: Disk read/write operations
- **Interactive Charts**: Plotly.js powered visualizations

### Alert System
- **CPU Thresholds**: Configurable alert levels (default: 80%)
- **Severity Levels**: High, medium, low alert categories
- **Visual Indicators**: Color-coded alerts in the dashboard
- **Real-time Updates**: Auto-refresh functionality

## 🌐 API Endpoints

### Authentication
- `POST /login` - User authentication
- `GET /logout` - User logout
- `GET /profile` - User profile

### Dashboard
- `GET /` - Main dashboard
- `GET /dashboard` - Dashboard overview
- `GET /instance/<id>` - Instance details
- `GET /health` - Health check

### API Endpoints
- `GET /api/instances` - List instances
- `GET /api/metrics/<id>` - Instance metrics
- `GET /api/logs/<id>` - Instance logs
- `GET /api/alerts` - Active alerts
- `GET /api/summary` - Instance summary

## 🚀 Deployment Options

### Local Development
- Flask development server
- Debug mode enabled
- Hot reloading

### Production Deployment
1. **AWS EC2**: Traditional server deployment
2. **AWS Elastic Beanstalk**: Managed platform
3. **Render**: Free tier hosting
4. **Docker**: Containerized deployment

### Environment Configuration
- Development, production, and testing configurations
- Environment-specific settings
- Secure credential management

## 📈 Monitoring & Logging

### Application Monitoring
- Health check endpoints
- Performance metrics
- Error tracking
- User activity logging

### AWS Integration
- CloudWatch metrics collection
- Log aggregation
- Alarm configuration
- Resource monitoring

## 🛠️ Development Features

### Code Quality
- Modular architecture with blueprints
- Comprehensive error handling
- Type hints and documentation
- Clean code practices

### Testing
- Unit test structure ready
- Integration test endpoints
- Health check validation
- Error scenario testing

### Documentation
- Comprehensive README
- Deployment guide
- API documentation
- Code comments

## 🔄 Future Enhancements

### Planned Features
- **Database Integration**: User management and session storage
- **Advanced Filtering**: More sophisticated instance filtering
- **Custom Metrics**: Support for custom CloudWatch metrics
- **Notification System**: Email/SMS alerts
- **Multi-user Support**: Role-based access control
- **Export Functionality**: Data export in various formats

### Scalability Improvements
- **Caching**: Redis integration for performance
- **Load Balancing**: Multiple worker processes
- **CDN Integration**: Static asset optimization
- **Microservices**: Service decomposition

## 📝 Usage Examples

### Technical Support Workflow
1. **Login** to the dashboard
2. **Select Region** where issues are reported
3. **Review Alerts** for high CPU usage instances
4. **Examine Metrics** for performance issues
5. **Check Logs** for error messages
6. **Generate Reports** for stakeholders

### Common Scenarios
- **High CPU Usage**: Identify and investigate performance issues
- **Instance Failures**: Check status and console output
- **Network Issues**: Monitor network traffic patterns
- **Security Audits**: Review security groups and configurations

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Include docstrings for functions
- Write meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Troubleshooting
- Check AWS credentials and permissions
- Verify network connectivity
- Review application logs
- Consult deployment documentation

### Getting Help
- Review the README and documentation
- Check the troubleshooting section
- Open an issue on GitHub
- Contact the development team

## 🎯 Conclusion

The AWS Diagnostic Tool provides a comprehensive, beginner-friendly solution for AWS infrastructure monitoring and diagnostics. With its modern UI, robust backend, and extensive feature set, it serves as an excellent foundation for technical support workflows and AWS resource management.

The application demonstrates best practices in Flask development, AWS integration, and web application security, making it suitable for both learning and production use. 