"""
CloudWatch service module for AWS Diagnostic Tool.
Handles all CloudWatch-related operations using Boto3.
"""
import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime, timedelta
import random
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
        self.demo_mode = False
        
        try:
            self.client = boto3.client('cloudwatch', region_name=region_name)
            # Test credentials by making a simple call
            self.client.list_metrics(Limit=1)
        except (NoCredentialsError, ClientError):
            self.demo_mode = True
            print("⚠️  CloudWatch: Running in DEMO MODE with sample metrics data.")
    
    def get_cpu_utilization(self, instance_id: str, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Get CPU utilization metrics for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            hours: Number of hours to look back
            
        Returns:
            List of CPU utilization data points
        """
        if self.demo_mode:
            return self._get_demo_cpu_data(instance_id, hours)
            
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
        if self.demo_mode:
            return self._get_demo_network_data(instance_id, hours)
            
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
        if self.demo_mode:
            return self._get_demo_disk_data(instance_id, hours)
            
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

    def _get_demo_cpu_data(self, instance_id: str, hours: int = 1) -> List[Dict[str, Any]]:
        """Generate demo CPU utilization data."""
        data = []
        now = datetime.utcnow()
        
        # Generate different CPU patterns based on instance ID
        if 'database' in instance_id.lower() or '0987654321' in instance_id:
            base_cpu = 75.0  # High CPU for database server
        elif 'backup' in instance_id.lower() or 'abcdef' in instance_id:
            base_cpu = 0.0   # No CPU for stopped instance
        else:
            base_cpu = 45.0  # Normal CPU for web server
        
        for i in range(hours * 12):  # 5-minute intervals
            timestamp = now - timedelta(minutes=5 * i)
            
            if base_cpu == 0.0:
                cpu_value = 0.0
            else:
                # Add some realistic variation
                variation = random.uniform(-10, 15)
                cpu_value = max(0, min(100, base_cpu + variation))
            
            data.append({
                'timestamp': timestamp.isoformat(),
                'average': round(cpu_value, 2),
                'maximum': round(cpu_value + random.uniform(0, 5), 2),
                'minimum': round(max(0, cpu_value - random.uniform(0, 5)), 2)
            })
        
        return data[::-1]  # Reverse to show oldest first

    def _get_demo_network_data(self, instance_id: str, hours: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        """Generate demo network data."""
        network_in = []
        network_out = []
        now = datetime.utcnow()
        
        # Different network patterns based on instance type
        if 'database' in instance_id.lower() or '0987654321' in instance_id:
            base_in = 5000000   # 5 MB/s average
            base_out = 2000000  # 2 MB/s average
        elif 'backup' in instance_id.lower() or 'abcdef' in instance_id:
            base_in = 0
            base_out = 0
        else:
            base_in = 8000000   # 8 MB/s average for web server
            base_out = 4000000  # 4 MB/s average
        
        for i in range(hours * 12):
            timestamp = now - timedelta(minutes=5 * i)
            
            if base_in == 0:
                in_value = 0
                out_value = 0
            else:
                in_variation = random.uniform(0.5, 1.5)
                out_variation = random.uniform(0.5, 1.5)
                in_value = int(base_in * in_variation)
                out_value = int(base_out * out_variation)
            
            network_in.append({
                'timestamp': timestamp.isoformat(),
                'average': in_value,
                'maximum': int(in_value * 1.2),
                'minimum': int(in_value * 0.8)
            })
            
            network_out.append({
                'timestamp': timestamp.isoformat(),
                'average': out_value,
                'maximum': int(out_value * 1.2),
                'minimum': int(out_value * 0.8)
            })
        
        return {
            'network_in': network_in[::-1],
            'network_out': network_out[::-1]
        }

    def _get_demo_disk_data(self, instance_id: str, hours: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        """Generate demo disk data."""
        disk_read = []
        disk_write = []
        now = datetime.utcnow()
        
        # Different disk patterns based on instance type
        if 'database' in instance_id.lower() or '0987654321' in instance_id:
            base_read = 2000000   # 2 MB/s average
            base_write = 1500000  # 1.5 MB/s average
        elif 'backup' in instance_id.lower() or 'abcdef' in instance_id:
            base_read = 0
            base_write = 0
        else:
            base_read = 1000000   # 1 MB/s average
            base_write = 800000   # 0.8 MB/s average
        
        for i in range(hours * 12):
            timestamp = now - timedelta(minutes=5 * i)
            
            if base_read == 0:
                read_value = 0
                write_value = 0
            else:
                read_variation = random.uniform(0.5, 1.5)
                write_variation = random.uniform(0.5, 1.5)
                read_value = int(base_read * read_variation)
                write_value = int(base_write * write_variation)
            
            disk_read.append({
                'timestamp': timestamp.isoformat(),
                'average': read_value,
                'maximum': int(read_value * 1.3),
                'minimum': int(read_value * 0.7)
            })
            
            disk_write.append({
                'timestamp': timestamp.isoformat(),
                'average': write_value,
                'maximum': int(write_value * 1.3),
                'minimum': int(write_value * 0.7)
            })
        
        return {
            'disk_read': disk_read[::-1],
            'disk_write': disk_write[::-1]
        }
    
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