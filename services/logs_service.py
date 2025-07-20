"""
CloudWatch Logs service module for AWS Diagnostic Tool.
Handles all CloudWatch Logs-related operations using Boto3.
"""
import boto3
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime, timedelta
from utils.helpers import sanitize_log_content


class LogsService:
    """Service class for CloudWatch Logs operations."""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize CloudWatch Logs service with specified region.
        
        Args:
            region_name: AWS region name
        """
        self.region_name = region_name
        self.client = boto3.client('logs', region_name=region_name)
    
    def get_log_groups(self) -> List[Dict[str, Any]]:
        """
        Get all CloudWatch log groups.
        
        Returns:
            List of log group information
        """
        try:
            response = self.client.describe_log_groups()
            
            log_groups = []
            for group in response['logGroups']:
                log_group_info = {
                    'log_group_name': group['logGroupName'],
                    'creation_time': group.get('creationTime'),
                    'stored_bytes': group.get('storedBytes', 0),
                    'metric_filter_count': group.get('metricFilterCount', 0),
                    'arn': group.get('arn'),
                    'retention_in_days': group.get('retentionInDays')
                }
                log_groups.append(log_group_info)
            
            return log_groups
            
        except ClientError as e:
            raise Exception(f"Error fetching log groups: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_log_streams(self, log_group_name: str) -> List[Dict[str, Any]]:
        """
        Get log streams for a specific log group.
        
        Args:
            log_group_name: Name of the log group
            
        Returns:
            List of log stream information
        """
        try:
            response = self.client.describe_log_streams(
                logGroupName=log_group_name,
                orderBy='LastEventTime',
                descending=True,
                maxItems=50
            )
            
            log_streams = []
            for stream in response['logStreams']:
                stream_info = {
                    'log_stream_name': stream['logStreamName'],
                    'creation_time': stream.get('creationTime'),
                    'first_event_time': stream.get('firstEventTime'),
                    'last_event_time': stream.get('lastEventTime'),
                    'stored_bytes': stream.get('storedBytes', 0),
                    'arn': stream.get('arn')
                }
                log_streams.append(stream_info)
            
            return log_streams
            
        except ClientError as e:
            raise Exception(f"Error fetching log streams: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_log_events(self, log_group_name: str, log_stream_name: str, 
                      start_time: Optional[int] = None, end_time: Optional[int] = None,
                      limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get log events from a specific log stream.
        
        Args:
            log_group_name: Name of the log group
            log_stream_name: Name of the log stream
            start_time: Start time in milliseconds since epoch
            end_time: End time in milliseconds since epoch
            limit: Maximum number of events to retrieve
            
        Returns:
            List of log events
        """
        try:
            kwargs = {
                'logGroupName': log_group_name,
                'logStreamName': log_stream_name,
                'limit': limit
            }
            
            if start_time:
                kwargs['startTime'] = start_time
            if end_time:
                kwargs['endTime'] = end_time
            
            response = self.client.get_log_events(**kwargs)
            
            events = []
            for event in response['events']:
                event_info = {
                    'timestamp': event['timestamp'],
                    'message': sanitize_log_content(event['message']),
                    'ingestion_time': event.get('ingestionTime')
                }
                events.append(event_info)
            
            return events
            
        except ClientError as e:
            raise Exception(f"Error fetching log events: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_recent_logs(self, log_group_name: str, hours: int = 1, 
                       limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent log events from a log group.
        
        Args:
            log_group_name: Name of the log group
            hours: Number of hours to look back
            limit: Maximum number of events to retrieve
            
        Returns:
            List of recent log events
        """
        try:
            # Calculate time range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            # Convert to milliseconds
            start_ms = int(start_time.timestamp() * 1000)
            end_ms = int(end_time.timestamp() * 1000)
            
            # Get log streams
            streams = self.get_log_streams(log_group_name)
            
            all_events = []
            for stream in streams[:5]:  # Limit to 5 most recent streams
                try:
                    events = self.get_log_events(
                        log_group_name, 
                        stream['log_stream_name'],
                        start_time=start_ms,
                        end_time=end_ms,
                        limit=limit // 5  # Distribute limit across streams
                    )
                    all_events.extend(events)
                except Exception:
                    # Skip streams that can't be accessed
                    continue
            
            # Sort by timestamp and limit
            all_events.sort(key=lambda x: x['timestamp'], reverse=True)
            return all_events[:limit]
            
        except Exception as e:
            raise Exception(f"Error fetching recent logs: {str(e)}")
    
    def search_logs(self, log_group_name: str, filter_pattern: str, 
                   hours: int = 1) -> List[Dict[str, Any]]:
        """
        Search logs using a filter pattern.
        
        Args:
            log_group_name: Name of the log group
            filter_pattern: CloudWatch Logs filter pattern
            hours: Number of hours to look back
            
        Returns:
            List of matching log events
        """
        try:
            # Calculate time range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            # Convert to milliseconds
            start_ms = int(start_time.timestamp() * 1000)
            end_ms = int(end_time.timestamp() * 1000)
            
            response = self.client.filter_log_events(
                logGroupName=log_group_name,
                startTime=start_ms,
                endTime=end_ms,
                filterPattern=filter_pattern,
                maxItems=100
            )
            
            events = []
            for event in response['events']:
                event_info = {
                    'timestamp': event['timestamp'],
                    'message': sanitize_log_content(event['message']),
                    'log_stream_name': event['logStreamName'],
                    'ingestion_time': event.get('ingestionTime')
                }
                events.append(event_info)
            
            return events
            
        except ClientError as e:
            raise Exception(f"Error searching logs: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_instance_logs(self, instance_id: str, hours: int = 1) -> Dict[str, Any]:
        """
        Get logs related to a specific EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            hours: Number of hours to look back
            
        Returns:
            Dictionary with various log sources for the instance
        """
        try:
            logs_data = {
                'instance_id': instance_id,
                'timestamp': datetime.utcnow().isoformat(),
                'duration_hours': hours,
                'console_output': None,
                'system_logs': [],
                'application_logs': [],
                'error_logs': []
            }
            
            # Try to find log groups that might contain instance logs
            log_groups = self.get_log_groups()
            
            # Common log group patterns for EC2 instances
            instance_patterns = [
                f"/aws/ec2/{instance_id}",
                f"ec2-{instance_id}",
                f"instance-{instance_id}",
                f"/aws/ec2/instances/{instance_id}"
            ]
            
            for pattern in instance_patterns:
                for group in log_groups:
                    if pattern in group['log_group_name']:
                        try:
                            recent_logs = self.get_recent_logs(
                                group['log_group_name'], 
                                hours, 
                                limit=50
                            )
                            logs_data['system_logs'].extend(recent_logs)
                        except Exception:
                            continue
            
            # Search for error logs
            for group in log_groups:
                if 'error' in group['log_group_name'].lower() or 'err' in group['log_group_name'].lower():
                    try:
                        error_logs = self.search_logs(
                            group['log_group_name'],
                            f'"{instance_id}"',
                            hours
                        )
                        logs_data['error_logs'].extend(error_logs)
                    except Exception:
                        continue
            
            return logs_data
            
        except Exception as e:
            raise Exception(f"Error fetching instance logs: {str(e)}")
    
    def get_application_logs(self, application_name: str, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Get application-specific logs.
        
        Args:
            application_name: Name of the application
            hours: Number of hours to look back
            
        Returns:
            List of application log events
        """
        try:
            log_groups = self.get_log_groups()
            
            app_logs = []
            for group in log_groups:
                if application_name.lower() in group['log_group_name'].lower():
                    try:
                        logs = self.get_recent_logs(
                            group['log_group_name'],
                            hours,
                            limit=100
                        )
                        app_logs.extend(logs)
                    except Exception:
                        continue
            
            return app_logs
            
        except Exception as e:
            raise Exception(f"Error fetching application logs: {str(e)}")
    
    def get_log_group_metrics(self, log_group_name: str) -> Dict[str, Any]:
        """
        Get metrics for a specific log group.
        
        Args:
            log_group_name: Name of the log group
            
        Returns:
            Dictionary with log group metrics
        """
        try:
            response = self.client.describe_log_groups(
                logGroupNamePrefix=log_group_name
            )
            
            if response['logGroups']:
                group = response['logGroups'][0]
                return {
                    'log_group_name': group['logGroupName'],
                    'stored_bytes': group.get('storedBytes', 0),
                    'metric_filter_count': group.get('metricFilterCount', 0),
                    'retention_in_days': group.get('retentionInDays'),
                    'creation_time': group.get('creationTime')
                }
            
            return {}
            
        except ClientError as e:
            raise Exception(f"Error fetching log group metrics: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}") 