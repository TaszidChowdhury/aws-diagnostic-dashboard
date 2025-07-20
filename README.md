# AWS Diagnostic Tool

A beginner-friendly Flask web application that simulates the tasks of a technical support analyst working with AWS infrastructure. This tool provides a comprehensive dashboard for monitoring and diagnosing AWS resources.

## Features

- **EC2 Instance Management**: List and view metadata for all EC2 instances in selected AWS regions
- **Real-time Monitoring**: Fetch and display CloudWatch metrics (CPU, Network) for the last hour
- **Interactive Charts**: Visualize metrics using Plotly charts with real-time updates
- **Log Analysis**: Retrieve and display system logs from CloudWatch Logs
- **Alert System**: Automatic highlighting of instances with high CPU usage (>80%)
- **Secure Access**: Protected dashboard with Flask-Login authentication
- **Responsive UI**: Clean, modern interface built with Bootstrap

## Prerequisites

- Python 3.8 or higher
- AWS Account with appropriate permissions
- AWS credentials configured (Access Key ID and Secret Access Key)

## Installation

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
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_DEFAULT_REGION=us-east-1
   FLASK_SECRET_KEY=your_secret_key_here
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change these credentials in production!

## Project Structure

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

## IAM Policy Requirements

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
                "cloudwatch:GetMetricData",
                "cloudwatch:GetMetricStatistics",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:GetLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

## Security Best Practices

1. **Use IAM Roles**: Instead of access keys, use IAM roles when deploying on AWS
2. **Environment Variables**: Never hardcode credentials in your code
3. **HTTPS**: Always use HTTPS in production
4. **Strong Passwords**: Change default login credentials
5. **Regular Updates**: Keep dependencies updated
6. **Access Logging**: Enable CloudTrail for audit trails

## Deployment Options

### Option 1: AWS EC2
1. Launch an EC2 instance with Ubuntu/Amazon Linux
2. Install Python and dependencies
3. Use Gunicorn as WSGI server
4. Set up Nginx as reverse proxy
5. Configure environment variables

### Option 2: AWS Elastic Beanstalk
1. Package your application
2. Deploy using AWS Elastic Beanstalk console
3. Configure environment variables in EB console

### Option 3: Render (Free Tier)
1. Connect your GitHub repository
2. Set environment variables in Render dashboard
3. Deploy automatically on push

## Usage Guide

1. **Login**: Use the provided credentials to access the dashboard
2. **Select Region**: Choose your AWS region from the dropdown
3. **View Instances**: Browse all EC2 instances with their metadata
4. **Monitor Metrics**: Click on an instance to view detailed metrics
5. **Check Logs**: Access system logs for troubleshooting
6. **Alerts**: Monitor highlighted instances with high resource usage

## Troubleshooting

- **No instances shown**: Check AWS credentials and region selection
- **Metrics not loading**: Verify CloudWatch permissions
- **Login issues**: Ensure Flask secret key is set
- **Connection errors**: Check AWS region and network connectivity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review AWS documentation
- Open an issue on GitHub

## Disclaimer

This tool is for educational and diagnostic purposes. Always follow AWS best practices and security guidelines when working with production environments. 