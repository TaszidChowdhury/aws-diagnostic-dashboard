"""
EC2 service module for AWS Diagnostic Tool.
Handles all EC2-related operations using Boto3.
"""
import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime
from utils.helpers import format_datetime, parse_instance_tags, get_instance_name


class EC2Service:
    """Service class for EC2 operations."""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize EC2 service with specified region.
        
        Args:
            region_name: AWS region name
        """
        self.region_name = region_name
        self.client = boto3.client('ec2', region_name=region_name)
        self.resource = boto3.resource('ec2', region_name=region_name)
    
    def get_all_instances(self) -> List[Dict[str, Any]]:
        """
        Get all EC2 instances in the region.
        
        Returns:
            List of instance dictionaries with metadata
        """
        try:
            response = self.client.describe_instances()
            instances = []
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_data = self._format_instance_data(instance)
                    instances.append(instance_data)
            
            return instances
            
        except NoCredentialsError:
            raise Exception("AWS credentials not found. Please configure your credentials.")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UnauthorizedOperation':
                raise Exception("Insufficient permissions to describe EC2 instances.")
            else:
                raise Exception(f"AWS API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_instance_by_id(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific EC2 instance by ID.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            Instance dictionary or None if not found
        """
        try:
            response = self.client.describe_instances(
                InstanceIds=[instance_id]
            )
            
            if response['Reservations']:
                instance = response['Reservations'][0]['Instances'][0]
                return self._format_instance_data(instance)
            
            return None
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidInstanceID.NotFound':
                return None
            else:
                raise Exception(f"AWS API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_instance_status(self, instance_id: str) -> Dict[str, Any]:
        """
        Get detailed status information for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            Dictionary with status information
        """
        try:
            response = self.client.describe_instance_status(
                InstanceIds=[instance_id],
                IncludeAllInstances=True
            )
            
            if response['InstanceStatuses']:
                status = response['InstanceStatuses'][0]
                return {
                    'instance_id': status['InstanceId'],
                    'state': status['InstanceState']['Name'],
                    'system_status': status['SystemStatus']['Status'],
                    'instance_status': status['InstanceStatus']['Status'],
                    'system_status_details': status['SystemStatus'].get('Details', []),
                    'instance_status_details': status['InstanceStatus'].get('Details', [])
                }
            
            return {}
            
        except ClientError as e:
            raise Exception(f"AWS API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_instance_console_output(self, instance_id: str) -> str:
        """
        Get console output for an instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            Console output as string
        """
        try:
            response = self.client.get_console_output(
                InstanceId=instance_id
            )
            
            return response.get('Output', 'No console output available')
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidInstanceID.NotFound':
                return "Instance not found"
            else:
                return f"Error retrieving console output: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def _format_instance_data(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format raw instance data from AWS API.
        
        Args:
            instance: Raw instance data from AWS API
            
        Returns:
            Formatted instance data
        """
        # Extract basic information
        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']
        launch_time = instance['LaunchTime']
        
        # Extract network information
        public_ip = instance.get('PublicIpAddress', 'N/A')
        private_ip = instance.get('PrivateIpAddress', 'N/A')
        
        # Extract tags
        tags = instance.get('Tags', [])
        instance_name = get_instance_name(tags)
        tag_dict = parse_instance_tags(tags)
        
        # Extract security groups
        security_groups = [
            {
                'group_id': sg['GroupId'],
                'group_name': sg['GroupName']
            }
            for sg in instance.get('SecurityGroups', [])
        ]
        
        # Extract block device mappings
        block_devices = []
        for device in instance.get('BlockDeviceMappings', []):
            block_devices.append({
                'device_name': device['DeviceName'],
                'volume_id': device['Ebs']['VolumeId'] if 'Ebs' in device else 'N/A',
                'delete_on_termination': device['Ebs'].get('DeleteOnTermination', False) if 'Ebs' in device else False
            })
        
        return {
            'instance_id': instance_id,
            'name': instance_name,
            'instance_type': instance_type,
            'state': state,
            'launch_time': format_datetime(launch_time),
            'launch_time_raw': launch_time,
            'public_ip': public_ip,
            'private_ip': private_ip,
            'vpc_id': instance.get('VpcId', 'N/A'),
            'subnet_id': instance.get('SubnetId', 'N/A'),
            'availability_zone': instance.get('Placement', {}).get('AvailabilityZone', 'N/A'),
            'platform': instance.get('Platform', 'linux'),
            'architecture': instance.get('Architecture', 'N/A'),
            'tags': tag_dict,
            'security_groups': security_groups,
            'block_devices': block_devices,
            'monitoring': instance.get('Monitoring', {}).get('State', 'disabled'),
            'iam_instance_profile': instance.get('IamInstanceProfile', {}).get('Arn', 'N/A') if instance.get('IamInstanceProfile') else 'N/A'
        }
    
    def get_instances_by_state(self, state: str) -> List[Dict[str, Any]]:
        """
        Get instances filtered by state.
        
        Args:
            state: Instance state to filter by
            
        Returns:
            List of instances in the specified state
        """
        all_instances = self.get_all_instances()
        return [instance for instance in all_instances if instance['state'].lower() == state.lower()]
    
    def get_running_instances(self) -> List[Dict[str, Any]]:
        """Get all running instances."""
        return self.get_instances_by_state('running')
    
    def get_stopped_instances(self) -> List[Dict[str, Any]]:
        """Get all stopped instances."""
        return self.get_instances_by_state('stopped')
    
    def get_instance_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics for all instances.
        
        Returns:
            Dictionary with instance statistics
        """
        instances = self.get_all_instances()
        
        total_instances = len(instances)
        running_instances = len([i for i in instances if i['state'] == 'running'])
        stopped_instances = len([i for i in instances if i['state'] == 'stopped'])
        pending_instances = len([i for i in instances if i['state'] == 'pending'])
        terminated_instances = len([i for i in instances if i['state'] == 'terminated'])
        
        # Count by instance type
        instance_types = {}
        for instance in instances:
            instance_type = instance['instance_type']
            instance_types[instance_type] = instance_types.get(instance_type, 0) + 1
        
        return {
            'total': total_instances,
            'running': running_instances,
            'stopped': stopped_instances,
            'pending': pending_instances,
            'terminated': terminated_instances,
            'by_type': instance_types
        } 