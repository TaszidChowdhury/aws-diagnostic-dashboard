"""
API routes for AWS Diagnostic Tool.
Handles AJAX requests and data endpoints for dynamic content.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from services.ec2_service import EC2Service
from services.cloudwatch_service import CloudWatchService
from services.logs_service import LogsService
from utils.helpers import calculate_alert_status
import json

# Create blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/api/metrics/<instance_id>')
@login_required
def get_metrics(instance_id):
    """
    Get CloudWatch metrics for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        hours = int(request.args.get('hours', 1))
        
        cloudwatch_service = CloudWatchService(region)
        metrics = cloudwatch_service.get_all_metrics(instance_id, hours)
        
        return jsonify({
            'success': True,
            'metrics': metrics
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/metrics/<instance_id>/cpu')
@login_required
def get_cpu_metrics(instance_id):
    """
    Get CPU utilization metrics for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        hours = int(request.args.get('hours', 1))
        
        cloudwatch_service = CloudWatchService(region)
        cpu_data = cloudwatch_service.get_cpu_utilization(instance_id, hours)
        
        return jsonify({
            'success': True,
            'cpu_data': cpu_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/metrics/<instance_id>/network')
@login_required
def get_network_metrics(instance_id):
    """
    Get network metrics for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        hours = int(request.args.get('hours', 1))
        
        cloudwatch_service = CloudWatchService(region)
        network_data = cloudwatch_service.get_network_metrics(instance_id, hours)
        
        return jsonify({
            'success': True,
            'network_data': network_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/metrics/<instance_id>/disk')
@login_required
def get_disk_metrics(instance_id):
    """
    Get disk metrics for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        hours = int(request.args.get('hours', 1))
        
        cloudwatch_service = CloudWatchService(region)
        disk_data = cloudwatch_service.get_disk_metrics(instance_id, hours)
        
        return jsonify({
            'success': True,
            'disk_data': disk_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/logs/<instance_id>')
@login_required
def get_instance_logs(instance_id):
    """
    Get logs for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        hours = int(request.args.get('hours', 1))
        
        logs_service = LogsService(region)
        logs_data = logs_service.get_instance_logs(instance_id, hours)
        
        return jsonify({
            'success': True,
            'logs': logs_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/logs/groups')
@login_required
def get_log_groups():
    """
    Get available CloudWatch log groups.
    """
    try:
        region = request.args.get('region', 'us-east-1')
        
        logs_service = LogsService(region)
        log_groups = logs_service.get_log_groups()
        
        return jsonify({
            'success': True,
            'log_groups': log_groups
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/logs/groups/<log_group_name>/streams')
@login_required
def get_log_streams(log_group_name):
    """
    Get log streams for a specific log group.
    
    Args:
        log_group_name: Name of the log group
    """
    try:
        region = request.args.get('region', 'us-east-1')
        
        logs_service = LogsService(region)
        log_streams = logs_service.get_log_streams(log_group_name)
        
        return jsonify({
            'success': True,
            'log_streams': log_streams
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/logs/search')
@login_required
def search_logs():
    """
    Search logs using filter patterns.
    """
    try:
        region = request.args.get('region', 'us-east-1')
        log_group_name = request.args.get('log_group')
        filter_pattern = request.args.get('filter_pattern', '')
        hours = int(request.args.get('hours', 1))
        
        if not log_group_name:
            return jsonify({
                'success': False,
                'error': 'Log group name is required'
            }), 400
        
        logs_service = LogsService(region)
        events = logs_service.search_logs(log_group_name, filter_pattern, hours)
        
        return jsonify({
            'success': True,
            'events': events
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/instance/<instance_id>/status')
@login_required
def get_instance_status(instance_id):
    """
    Get detailed status for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        
        ec2_service = EC2Service(region)
        status = ec2_service.get_instance_status(instance_id)
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/instance/<instance_id>/console')
@login_required
def get_console_output(instance_id):
    """
    Get console output for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        
        ec2_service = EC2Service(region)
        console_output = ec2_service.get_instance_console_output(instance_id)
        
        return jsonify({
            'success': True,
            'console_output': console_output
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/alarms/<instance_id>')
@login_required
def get_instance_alarms(instance_id):
    """
    Get CloudWatch alarms for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        
        cloudwatch_service = CloudWatchService(region)
        alarms = cloudwatch_service.get_metric_alarms(instance_id)
        
        return jsonify({
            'success': True,
            'alarms': alarms
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/regions')
@login_required
def get_regions():
    """
    Get available AWS regions.
    """
    try:
        from utils.helpers import get_aws_regions
        
        regions = get_aws_regions()
        
        return jsonify({
            'success': True,
            'regions': regions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/instances/filter')
@login_required
def filter_instances():
    """
    Filter instances by various criteria.
    """
    try:
        region = request.args.get('region', 'us-east-1')
        state = request.args.get('state', '')
        instance_type = request.args.get('instance_type', '')
        name_pattern = request.args.get('name_pattern', '')
        
        ec2_service = EC2Service(region)
        instances = ec2_service.get_all_instances()
        
        # Apply filters
        if state:
            instances = [i for i in instances if i['state'].lower() == state.lower()]
        
        if instance_type:
            instances = [i for i in instances if instance_type.lower() in i['instance_type'].lower()]
        
        if name_pattern:
            instances = [i for i in instances if name_pattern.lower() in i['name'].lower()]
        
        return jsonify({
            'success': True,
            'instances': instances,
            'count': len(instances)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/metrics/available/<instance_id>')
@login_required
def get_available_metrics(instance_id):
    """
    Get available metrics for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        region = request.args.get('region', 'us-east-1')
        
        cloudwatch_service = CloudWatchService(region)
        metrics = cloudwatch_service.get_available_metrics(instance_id)
        
        return jsonify({
            'success': True,
            'metrics': metrics
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/api/metrics/<instance_id>/custom/<metric_name>')
@login_required
def get_custom_metric(instance_id, metric_name):
    """
    Get a custom metric for a specific instance.
    
    Args:
        instance_id: The EC2 instance ID
        metric_name: Name of the metric to fetch
    """
    try:
        region = request.args.get('region', 'us-east-1')
        hours = int(request.args.get('hours', 1))
        
        cloudwatch_service = CloudWatchService(region)
        metric_data = cloudwatch_service.get_custom_metric(instance_id, metric_name, hours)
        
        return jsonify({
            'success': True,
            'metric_data': metric_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 