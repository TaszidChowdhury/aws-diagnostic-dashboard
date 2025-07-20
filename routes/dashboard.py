"""
Dashboard routes for AWS Diagnostic Tool.
Handles main dashboard views and instance overview.
"""
from flask import Blueprint, render_template, request, jsonify, flash, current_app, redirect, url_for
from flask_login import login_required, current_user
from services.ec2_service import EC2Service
from services.cloudwatch_service import CloudWatchService
from utils.helpers import validate_aws_credentials, get_aws_regions, calculate_alert_status
import json
from datetime import datetime

# Create blueprint
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    """
    Main dashboard page showing EC2 instances overview.
    """
    try:
        # Get selected region from query parameters or session
        selected_region = request.args.get('region') or request.cookies.get('selected_region', 'us-east-1')
        
        # Validate AWS credentials
        creds_status = validate_aws_credentials()
        if not creds_status['valid']:
            flash(f"AWS credentials error: {creds_status['error']}", 'error')
            return render_template('dashboard.html', 
                                 instances=[], 
                                 summary={}, 
                                 regions=[],
                                 selected_region=selected_region,
                                 creds_error=True)
        
        # Get available regions
        regions = get_aws_regions()
        
        # Initialize services
        ec2_service = EC2Service(selected_region)
        
        # Get instances and summary
        instances = ec2_service.get_all_instances()
        summary = ec2_service.get_instance_summary()
        
        # Calculate alerts for running instances
        cloudwatch_service = CloudWatchService(selected_region)
        for instance in instances:
            if instance['state'] == 'running':
                try:
                    # Get latest CPU utilization
                    cpu_data = cloudwatch_service.get_cpu_utilization(instance['instance_id'], hours=1)
                    if cpu_data:
                        latest_cpu = cpu_data[-1]['average'] if cpu_data else 0
                        alert_status = calculate_alert_status(latest_cpu)
                        instance['alert_status'] = alert_status
                        instance['current_cpu'] = latest_cpu
                    else:
                        instance['alert_status'] = {'alert': False, 'severity': 'none', 'message': 'No CPU data available'}
                        instance['current_cpu'] = 0
                except Exception:
                    instance['alert_status'] = {'alert': False, 'severity': 'none', 'message': 'Error fetching CPU data'}
                    instance['current_cpu'] = 0
            else:
                instance['alert_status'] = {'alert': False, 'severity': 'none', 'message': 'Instance not running'}
                instance['current_cpu'] = 0
        
        return render_template('dashboard.html',
                             instances=instances,
                             summary=summary,
                             regions=regions,
                             selected_region=selected_region,
                             creds_error=False)
                             
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", 'error')
        return render_template('dashboard.html',
                             instances=[],
                             summary={},
                             regions=[],
                             selected_region='us-east-1',
                             creds_error=True)

@dashboard_bp.route('/instance/<instance_id>')
@login_required
def instance_detail(instance_id):
    """
    Detailed view for a specific EC2 instance.
    
    Args:
        instance_id: The EC2 instance ID
    """
    try:
        selected_region = request.args.get('region') or request.cookies.get('selected_region', 'us-east-1')
        
        # Initialize services
        ec2_service = EC2Service(selected_region)
        cloudwatch_service = CloudWatchService(selected_region)
        
        # Get instance details
        instance = ec2_service.get_instance_by_id(instance_id)
        if not instance:
            flash(f"Instance {instance_id} not found.", 'error')
            return redirect(url_for('dashboard.index'))
        
        # Get instance status
        status = ec2_service.get_instance_status(instance_id)
        
        # Get metrics if instance is running
        metrics = None
        if instance['state'] == 'running':
            try:
                metrics = cloudwatch_service.get_all_metrics(instance_id, hours=1)
            except Exception as e:
                flash(f"Error fetching metrics: {str(e)}", 'warning')
        
        # Get console output
        console_output = None
        if instance['state'] == 'running':
            try:
                console_output = ec2_service.get_instance_console_output(instance_id)
            except Exception as e:
                flash(f"Error fetching console output: {str(e)}", 'warning')
        
        return render_template('instance_detail.html',
                             instance=instance,
                             status=status,
                             metrics=metrics,
                             console_output=console_output,
                             selected_region=selected_region)
                             
    except Exception as e:
        flash(f"Error loading instance details: {str(e)}", 'error')
        return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/api/instances')
@login_required
def api_instances():
    """
    API endpoint to get instances data for AJAX requests.
    """
    try:
        selected_region = request.args.get('region', 'us-east-1')
        state_filter = request.args.get('state', '')
        
        ec2_service = EC2Service(selected_region)
        instances = ec2_service.get_all_instances()
        
        # Apply state filter if provided
        if state_filter:
            instances = [i for i in instances if i['state'].lower() == state_filter.lower()]
        
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

@dashboard_bp.route('/api/summary')
@login_required
def api_summary():
    """
    API endpoint to get instance summary statistics.
    """
    try:
        selected_region = request.args.get('region', 'us-east-1')
        
        ec2_service = EC2Service(selected_region)
        summary = ec2_service.get_instance_summary()
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/api/alerts')
@login_required
def api_alerts():
    """
    API endpoint to get instances with alerts.
    """
    try:
        selected_region = request.args.get('region', 'us-east-1')
        
        ec2_service = EC2Service(selected_region)
        cloudwatch_service = CloudWatchService(selected_region)
        
        instances = ec2_service.get_running_instances()
        alerts = []
        
        for instance in instances:
            try:
                cpu_data = cloudwatch_service.get_cpu_utilization(instance['instance_id'], hours=1)
                if cpu_data:
                    latest_cpu = cpu_data[-1]['average'] if cpu_data else 0
                    alert_status = calculate_alert_status(latest_cpu)
                    if alert_status['alert']:
                        alerts.append({
                            'instance_id': instance['instance_id'],
                            'name': instance['name'],
                            'cpu_utilization': latest_cpu,
                            'alert_status': alert_status
                        })
            except Exception:
                continue
        
        return jsonify({
            'success': True,
            'alerts': alerts,
            'count': len(alerts)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/health')
@login_required
def health_check():
    """
    Health check endpoint for the application.
    """
    try:
        # Check AWS credentials
        creds_status = validate_aws_credentials()
        
        # Check if we can access EC2
        ec2_status = {'status': 'unknown', 'error': None}
        if creds_status['valid']:
            try:
                ec2_service = EC2Service()
                ec2_service.get_instance_summary()
                ec2_status = {'status': 'healthy', 'error': None}
            except Exception as e:
                ec2_status = {'status': 'unhealthy', 'error': str(e)}
        
        return jsonify({
            'application': 'healthy',
            'aws_credentials': creds_status,
            'ec2_service': ec2_status,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'application': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500 