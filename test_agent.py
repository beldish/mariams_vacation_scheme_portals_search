#!/usr/bin/env python3
"""
Test script for Vacation Scheme Search Agent

This script tests the basic functionality without actually sending emails
or making API calls (unless configured).
"""

import sys
import os


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import configparser
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from datetime import datetime
        import schedule
        import pytz
        from serpapi import GoogleSearch
        print("✓ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_config_example():
    """Test that the example config file exists and is valid."""
    print("\nTesting example configuration...")
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini.example')
        
        # Check required sections
        required_sections = ['serpapi', 'email', 'search']
        for section in required_sections:
            if not config.has_section(section):
                print(f"✗ Missing section: {section}")
                return False
        
        print("✓ Example configuration file is valid")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False


def test_search_agent_structure():
    """Test that the search agent module has expected structure."""
    print("\nTesting search agent structure...")
    try:
        from search_agent import VacationSchemeSearchAgent
        
        # Check that the class has expected methods
        expected_methods = ['search_vacation_schemes', 'format_results', 'send_email', 'run']
        for method in expected_methods:
            if not hasattr(VacationSchemeSearchAgent, method):
                print(f"✗ Missing method: {method}")
                return False
        
        print("✓ Search agent has expected structure")
        return True
    except Exception as e:
        print(f"✗ Search agent error: {e}")
        return False


def test_scheduler_structure():
    """Test that the scheduler module can be imported."""
    print("\nTesting scheduler structure...")
    try:
        import scheduler
        print("✓ Scheduler module can be imported")
        return True
    except Exception as e:
        print(f"✗ Scheduler error: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Vacation Scheme Search Agent - Test Suite")
    print("="*60)
    
    tests = [
        test_imports,
        test_config_example,
        test_search_agent_structure,
        test_scheduler_structure
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    print("Test Results")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
