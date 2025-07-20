# Deployment Guide

This guide provides step-by-step instructions for deploying the AWS Diagnostic Tool on various platforms.

## Prerequisites

- Python 3.8 or higher
- AWS Account with appropriate permissions
- Git (for version control)

## Local Development Setup

### 1. Clone and Setup

```bash
git clone <repository-url>
cd aws-diagnostic-dashboard
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp env_example.txt .env
# Edit .env with your AWS credentials and settings
```

### 3. Run Application

```bash
python app.py
```

Access the application at `http://localhost:5000`

## AWS EC2 Deployment

### 1. Launch EC2 Instance

- Use Amazon Linux 2 or Ubuntu 20.04 LTS
- Instance type: t3.micro (free tier) or larger
- Security Group: Allow HTTP (80), HTTPS (443), and SSH (22)

### 2. Connect and Setup

```bash
# Connect to your instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Update system
sudo yum update -y  # Amazon Linux
# or
sudo apt update && sudo apt upgrade -y  # Ubuntu

# Install Python and dependencies
sudo yum install python3 python3-pip git -y  # Amazon Linux
# or
sudo apt install python3 python3-pip git -y  # Ubuntu
```

### 3. Deploy Application

```bash
# Clone repository
git clone <repository-url>
cd aws-diagnostic-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env_example.txt .env
# Edit .env with your settings
```

### 4. Configure IAM Role (Recommended)

Instead of using access keys, create an IAM role:

1. Go to IAM Console
2. Create a new role for EC2
3. Attach the policy from `iam_policy_example.json`
4. Attach the role to your EC2 instance

### 5. Setup Systemd Service

Create `/etc/systemd/system/aws-diagnostic.service`:

```ini
[Unit]
Description=AWS Diagnostic Tool
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/aws-diagnostic-dashboard
Environment=PATH=/home/ec2-user/aws-diagnostic-dashboard/venv/bin
ExecStart=/home/ec2-user/aws-diagnostic-dashboard/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
Restart=always

[Install]
WantedBy=multi-user.target
```

### 6. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable aws-diagnostic
sudo systemctl start aws-diagnostic
sudo systemctl status aws-diagnostic
```

### 7. Setup Nginx (Optional)

Install and configure Nginx as a reverse proxy:

```bash
sudo yum install nginx -y  # Amazon Linux
# or
sudo apt install nginx -y  # Ubuntu

# Configure Nginx
sudo nano /etc/nginx/sites-available/aws-diagnostic
```

Add configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and start Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/aws-diagnostic /etc/nginx/sites-enabled/
sudo systemctl enable nginx
sudo systemctl start nginx
```

## AWS Elastic Beanstalk Deployment

### 1. Prepare Application

Create `application.py` in the root directory:

```python
from app import create_app

application = create_app()
```

### 2. Create Requirements File

Ensure `requirements.txt` includes:

```
Flask==2.3.3
Flask-Login==0.6.3
boto3==1.34.0
python-dotenv==1.0.0
plotly==5.17.0
pandas==2.1.4
gunicorn==21.2.0
```

### 3. Deploy via EB CLI

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
eb init aws-diagnostic-tool --platform python-3.8

# Create environment
eb create aws-diagnostic-prod

# Set environment variables
eb setenv AWS_ACCESS_KEY_ID=your_key AWS_SECRET_ACCESS_KEY=your_secret

# Deploy
eb deploy
```

## Render Deployment

### 1. Connect Repository

1. Go to [Render](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service

### 2. Configure Service

- **Name**: aws-diagnostic-tool
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:create_app()`

### 3. Set Environment Variables

Add these in Render dashboard:

```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
FLASK_SECRET_KEY=your_secret_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
```

### 4. Deploy

Click "Create Web Service" and Render will automatically deploy your application.

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
```

### 2. Build and Run

```bash
docker build -t aws-diagnostic-tool .
docker run -p 5000:5000 -e AWS_ACCESS_KEY_ID=your_key -e AWS_SECRET_ACCESS_KEY=your_secret aws-diagnostic-tool
```

## Security Considerations

### 1. Environment Variables

- Never commit `.env` files to version control
- Use secure secret management services
- Rotate credentials regularly

### 2. IAM Permissions

- Use least privilege principle
- Use IAM roles instead of access keys when possible
- Regularly audit permissions

### 3. Network Security

- Use HTTPS in production
- Configure security groups properly
- Consider using AWS WAF for additional protection

### 4. Application Security

- Change default admin credentials
- Use strong passwords
- Enable logging and monitoring
- Keep dependencies updated

## Monitoring and Logging

### 1. Application Logs

```bash
# View application logs
sudo journalctl -u aws-diagnostic -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. CloudWatch Monitoring

- Set up CloudWatch alarms for CPU, memory, and disk usage
- Monitor application metrics
- Set up log aggregation

### 3. Health Checks

The application provides a health check endpoint at `/health` that can be used by load balancers and monitoring systems.

## Troubleshooting

### Common Issues

1. **AWS Credentials Error**
   - Verify credentials are correct
   - Check IAM permissions
   - Ensure region is correct

2. **Port Already in Use**
   - Check if another service is using port 5000
   - Change port in configuration
   - Kill conflicting processes

3. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python version compatibility
   - Verify virtual environment is activated

4. **Permission Denied**
   - Check file permissions
   - Ensure proper user permissions
   - Verify IAM role permissions

### Getting Help

- Check application logs for error messages
- Verify AWS credentials and permissions
- Test connectivity to AWS services
- Review security group configurations

## Performance Optimization

### 1. Gunicorn Configuration

For production, use multiple workers:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### 2. Caching

Consider implementing Redis caching for frequently accessed data.

### 3. Database

For larger deployments, consider using a database for user management and session storage.

### 4. CDN

Use CloudFront or similar CDN for static assets in production. 