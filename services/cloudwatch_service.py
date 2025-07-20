"""
CloudWatch service module for AWS Diagnostic Tool.
Handles all CloudWatch-related operations using Boto3.
"""
import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime, timedelta
from utils.helpers import format_metric_data, get_time_range


class CloudWatchService:
    """Service class for CloudWatch operations."""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize CloudWatch service with specified region.
        
        Args:
            region_name: AWS region name
        """
        self.region_name = region_name
        self.client = boto3.client('cloudwatch', region_name=region_name)
    
    def get_cpu_utilization(self, instance_id: str, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Get CPU utilization metrics for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            hours: Number of hours to look back
            
        Returns:
            List of CPU utilization data points
        """
        try:
            start_time, end_time = get_time_range(hours)
            
            response = self.client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,  # 5-minute intervals
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            
            return self._format_cpu_data(response['Datapoints'])
            
        except ClientError as e:
            raise Exception(f"Error fetching CPU metrics: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_network_metrics(self, instance_id: str, hours: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get network metrics (NetworkIn, NetworkOut) for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            hours: Number of hours to look back
            
        Returns:
            Dictionary with NetworkIn and NetworkOut data
        """
        try:
            start_time, end_time = get_time_range(hours)
            
            # Get NetworkIn metrics
            network_in_response = self.client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='NetworkIn',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            
            # Get NetworkOut metrics
            network_out_response = self.client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='NetworkOut',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            
            return {
                'network_in': self._format_network_data(network_in_response['Datapoints']),
                'network_out': self._format_network_data(network_out_response['Datapoints'])
            }
            
        except ClientError as e:
            raise Exception(f"Error fetching network metrics: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_disk_metrics(self, instance_id: str, hours: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get disk metrics for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            hours: Number of hours to look back
            
        Returns:
            Dictionary with disk read/write data
        """
        try:
            start_time, end_time = get_time_range(hours)
            
            # Get DiskReadBytes metrics
            disk_read_response = self.client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='DiskReadBytes',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            
            # Get DiskWriteBytes metrics
            disk_write_response = self.client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='DiskWriteBytes',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            
            return {
                'disk_read': self._format_disk_data(disk_read_response['Datapoints']),
                'disk_write': self._format_disk_data(disk_write_response['Datapoints'])
            }
            
        except ClientError as e:
            raise Exception(f"Error fetching disk metrics: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_all_metrics(self, instance_id: str, hours: int = 1) -> Dict[str, Any]:
        """
        Get all available metrics for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            hours: Number of hours to look back
            
        Returns:
            Dictionary with all metrics data
        """
        try:
            cpu_data = self.get_cpu_utilization(instance_id, hours)
            network_data = self.get_network_metrics(instance_id, hours)
            disk_data = self.get_disk_metrics(instance_id, hours)
            
            return {
                'cpu': cpu_data,
                'network': network_data,
                'disk': disk_data,
                'timestamp': datetime.utcnow().isoformat(),
                'instance_id': instance_id,
                'duration_hours': hours
            }
            
        except Exception as e:
            raise Exception(f"Error fetching all metrics: {str(e)}")
    
    def get_metric_alarms(self, instance_id: str) -> List[Dict[str, Any]]:
        """
        Get CloudWatch alarms associated with an instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            List of alarm information
        """
        try:
            response = self.client.describe_alarms(
                AlarmNamePrefix=f"*{instance_id}*"
            )
            
            alarms = []
            for alarm in response['MetricAlarms']:
                alarm_info = {
                    'alarm_name': alarm['AlarmName'],
                    'alarm_arn': alarm['AlarmArn'],
                    'state': alarm['StateValue'],
                    'state_reason': alarm.get('StateReason', 'N/A'),
                    'metric_name': alarm['MetricName'],
                    'namespace': alarm['Namespace'],
                    'threshold': alarm['Threshold'],
                    'comparison_operator': alarm['ComparisonOperator'],
                    'evaluation_periods': alarm['EvaluationPeriods'],
                    'period': alarm['Period']
                }
                alarms.append(alarm_info)
            
            return alarms
            
        except ClientError as e:
            # If no alarms found, return empty list
            if 'NoSuchEntity' in str(e):
                return []
            raise Exception(f"Error fetching alarms: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def _format_cpu_data(self, datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format CPU utilization datapoints.
        
        Args:
            datapoints: Raw datapoints from CloudWatch
            
        Returns:
            Formatted CPU data
        """
        formatted_data = []
        
        for dp in sorted(datapoints, key=lambda x: x['Timestamp']):
            formatted_data.append({
                'timestamp': dp['Timestamp'].isoformat(),
                'average': dp.get('Average', 0),
                'maximum': dp.get('Maximum', 0),
                'minimum': dp.get('Minimum', 0),
                'unit': dp.get('Unit', 'Percent')
            })
        
        return formatted_data
    
    def _format_network_data(self, datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format network metrics datapoints.
        
        Args:
            datapoints: Raw datapoints from CloudWatch
            
        Returns:
            Formatted network data
        """
        formatted_data = []
        
        for dp in sorted(datapoints, key=lambda x: x['Timestamp']):
            formatted_data.append({
                'timestamp': dp['Timestamp'].isoformat(),
                'average': dp.get('Average', 0),
                'maximum': dp.get('Maximum', 0),
                'minimum': dp.get('Minimum', 0),
                'unit': dp.get('Unit', 'Bytes')
            })
        
        return formatted_data
    
    def _format_disk_data(self, datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format disk metrics datapoints.
        
        Args:
            datapoints: Raw datapoints from CloudWatch
            
        Returns:
            Formatted disk data
        """
        formatted_data = []
        
        for dp in sorted(datapoints, key=lambda x: x['Timestamp']):
            formatted_data.append({
                'timestamp': dp['Timestamp'].isoformat(),
                'average': dp.get('Average', 0),
                'maximum': dp.get('Maximum', 0),
                'minimum': dp.get('Minimum', 0),
                'unit': dp.get('Unit', 'Bytes')
            })
        
        return formatted_data
    
    def get_available_metrics(self, instance_id: str) -> List[str]:
        """
        Get list of available metrics for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            List of available metric names
        """
        try:
            response = self.client.list_metrics(
                Namespace='AWS/EC2',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ]
            )
            
            return [metric['MetricName'] for metric in response['Metrics']]
            
        except ClientError as e:
            raise Exception(f"Error fetching available metrics: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_custom_metric(self, instance_id: str, metric_name: str, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Get a custom metric for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            metric_name: Name of the metric to fetch
            hours: Number of hours to look back
            
        Returns:
            List of metric datapoints
        """
        try:
            start_time, end_time = get_time_range(hours)
            
            response = self.client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName=metric_name,
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            
            return self._format_cpu_data(response['Datapoints'])  # Reuse CPU format
            
        except ClientError as e:
            raise Exception(f"Error fetching custom metric {metric_name}: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}") 