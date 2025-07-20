#!/usr/bin/env python3
"""
Simple test script to verify the AWS Diagnostic Tool can start properly.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from flask import Flask
        print("✅ Flask imported successfully")
        
        from boto3 import client
        print("✅ Boto3 imported successfully")
        
        from config import config
        print("✅ Config imported successfully")
        
        # Test service imports
        from services.ec2_service import EC2Service
        print("✅ EC2Service imported successfully")
        
        from services.cloudwatch_service import CloudWatchService
        print("✅ CloudWatchService imported successfully")
        
        # Test route imports
        from routes.auth import auth_bp
        print("✅ Auth blueprint imported successfully")
        
        from routes.dashboard import dashboard_bp
        print("✅ Dashboard blueprint imported successfully")
        
        from routes.api import api_bp
        print("✅ API blueprint imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_services():
    """Test if services can be instantiated."""
    try:
        print("\nTesting services...")
        
        # Test EC2 service
        ec2_service = EC2Service('us-east-1')
        print("✅ EC2Service instantiated successfully")
        
        # Test CloudWatch service
        cw_service = CloudWatchService('us-east-1')
        print("✅ CloudWatchService instantiated successfully")
        
        print("🎉 All services working!")
        return True
        
    except Exception as e:
        print(f"❌ Service error: {e}")
        return False

def test_app_creation():
    """Test if Flask app can be created."""
    try:
        print("\nTesting app creation...")
        
        from app import create_app
        app = create_app('development')
        print("✅ Flask app created successfully")
        
        print("🎉 App creation successful!")
        return True
        
    except Exception as e:
        print(f"❌ App creation error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("AWS Diagnostic Tool - Test Script")
    print("=" * 50)
    
    # Run tests
    imports_ok = test_imports()
    services_ok = test_services()
    app_ok = test_app_creation()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Services: {'✅ PASS' if services_ok else '❌ FAIL'}")
    print(f"App Creation: {'✅ PASS' if app_ok else '❌ FAIL'}")
    print("=" * 50)
    
    if all([imports_ok, services_ok, app_ok]):
        print("\n🎉 All tests passed! The application should work correctly.")
        print("\nTo start the application:")
        print("1. source venv/bin/activate")
        print("2. python app.py")
        print("3. Open http://localhost:5000 in your browser")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 