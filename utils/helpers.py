"""
Helper utility functions for the AWS Diagnostic Tool.
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def format_datetime(dt: datetime) -> str:
    """Format datetime object to human-readable string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def format_bytes(bytes_value: int) -> str:
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def get_instance_state_color(state: str) -> str:
    """Get Bootstrap color class for instance state."""
    state_colors = {
        'running': 'success',
        'stopped': 'danger',
        'pending': 'warning',
        'terminated': 'secondary',
        'stopping': 'warning',
        'starting': 'info'
    }
    return state_colors.get(state.lower(), 'secondary')


def validate_aws_credentials() -> Dict[str, Any]:
    """
    Validate AWS credentials and return status.
    
    Returns:
        Dict containing validation status and error message if any
    """
    try:
        # Try to create a simple AWS client to test credentials
        sts = boto3.client('sts')
        sts.get_caller_identity()
        return {'valid': True, 'error': None}
    except NoCredentialsError:
        return {'valid': False, 'error': 'AWS credentials not found'}
    except ClientError as e:
        return {'valid': False, 'error': f'AWS credentials error: {str(e)}'}
    except Exception as e:
        return {'valid': False, 'error': f'Unexpected error: {str(e)}'}


def get_aws_regions() -> List[Dict[str, str]]:
    """
    Get list of available AWS regions.
    
    Returns:
        List of dictionaries with region information
    """
    try:
        ec2 = boto3.client('ec2')
        regions = ec2.describe_regions()
        return [
            {
                'name': region['RegionName'],
                'endpoint': region['Endpoint'],
                'display_name': region['RegionName'].replace('-', ' ').title()
            }
            for region in regions['Regions']
        ]
    except Exception:
        # Fallback to common regions if API call fails
        return [
            {'name': 'us-east-1', 'endpoint': 'ec2.us-east-1.amazonaws.com', 'display_name': 'US East (N. Virginia)'},
            {'name': 'us-west-2', 'endpoint': 'ec2.us-west-2.amazonaws.com', 'display_name': 'US West (Oregon)'},
            {'name': 'eu-west-1', 'endpoint': 'ec2.eu-west-1.amazonaws.com', 'display_name': 'Europe (Ireland)'},
            {'name': 'ap-southeast-1', 'endpoint': 'ec2.ap-southeast-1.amazonaws.com', 'display_name': 'Asia Pacific (Singapore)'}
        ]


def parse_instance_tags(tags: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Parse EC2 instance tags into a dictionary.
    
    Args:
        tags: List of tag dictionaries from AWS API
        
    Returns:
        Dictionary of tag key-value pairs
    """
    if not tags:
        return {}
    
    return {tag['Key']: tag['Value'] for tag in tags}


def get_instance_name(tags: List[Dict[str, str]]) -> str:
    """
    Extract instance name from tags.
    
    Args:
        tags: List of tag dictionaries from AWS API
        
    Returns:
        Instance name or 'Unnamed Instance'
    """
    tag_dict = parse_instance_tags(tags)
    return tag_dict.get('Name', 'Unnamed Instance')


def format_metric_data(metric_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format CloudWatch metric data for charting.
    
    Args:
        metric_data: Raw metric data from CloudWatch
        
    Returns:
        Formatted data for Plotly charts
    """
    formatted_data = []
    
    for metric in metric_data:
        if 'Datapoints' in metric and metric['Datapoints']:
            # Sort datapoints by timestamp
            datapoints = sorted(metric['Datapoints'], key=lambda x: x['Timestamp'])
            
            # Extract timestamps and values
            timestamps = [dp['Timestamp'].isoformat() for dp in datapoints]
            values = [dp['Average'] if 'Average' in dp else dp['Value'] for dp in datapoints]
            
            formatted_data.append({
                'metric_name': metric['Label'],
                'timestamps': timestamps,
                'values': values,
                'unit': metric.get('Unit', 'None')
            })
    
    return formatted_data


def calculate_alert_status(cpu_utilization: float, threshold: float = 80.0) -> Dict[str, Any]:
    """
    Calculate alert status based on CPU utilization.
    
    Args:
        cpu_utilization: Current CPU utilization percentage
        threshold: Alert threshold percentage
        
    Returns:
        Dictionary with alert status and severity
    """
    if cpu_utilization >= threshold:
        return {
            'alert': True,
            'severity': 'high' if cpu_utilization >= 90 else 'medium',
            'message': f'High CPU usage: {cpu_utilization:.1f}%'
        }
    elif cpu_utilization >= threshold * 0.7:  # 70% of threshold
        return {
            'alert': True,
            'severity': 'low',
            'message': f'Elevated CPU usage: {cpu_utilization:.1f}%'
        }
    else:
        return {
            'alert': False,
            'severity': 'none',
            'message': f'Normal CPU usage: {cpu_utilization:.1f}%'
        }


def sanitize_log_content(content: str, max_length: int = 1000) -> str:
    """
    Sanitize log content for safe display.
    
    Args:
        content: Raw log content
        max_length: Maximum length to display
        
    Returns:
        Sanitized log content
    """
    if not content:
        return "No log content available"
    
    # Truncate if too long
    if len(content) > max_length:
        content = content[:max_length] + "... (truncated)"
    
    # Basic HTML escaping (Flask's Markup will handle this, but good practice)
    content = content.replace('<', '&lt;').replace('>', '&gt;')
    
    return content


def get_time_range(hours: int = 1) -> tuple:
    """
    Get start and end time for metric queries.
    
    Args:
        hours: Number of hours to look back
        
    Returns:
        Tuple of (start_time, end_time) as datetime objects
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)
    return start_time, end_time 