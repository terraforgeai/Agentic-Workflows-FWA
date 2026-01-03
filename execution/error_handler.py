#!/usr/bin/env python3
"""
Error Handler - Standardized Error Handling for FWA Odoo Operations

Purpose: Provide consistent error handling, logging, and recovery suggestions
Input: Exceptions from execution scripts
Output: Standardized error responses with actionable recommendations

Related Directive: N/A (Core infrastructure)
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum


class ErrorCategory(Enum):
    """Categories of errors for better handling."""
    AUTHENTICATION = "authentication"
    CONNECTION = "connection"
    VALIDATION = "validation"
    NOT_FOUND = "not_found"
    PERMISSION = "permission"
    RATE_LIMIT = "rate_limit"
    DATA_INTEGRITY = "data_integrity"
    UNKNOWN = "unknown"


# Error patterns and their categories
ERROR_PATTERNS = {
    "authenticate": ErrorCategory.AUTHENTICATION,
    "access denied": ErrorCategory.PERMISSION,
    "permission": ErrorCategory.PERMISSION,
    "not found": ErrorCategory.NOT_FOUND,
    "does not exist": ErrorCategory.NOT_FOUND,
    "invalid": ErrorCategory.VALIDATION,
    "required": ErrorCategory.VALIDATION,
    "missing": ErrorCategory.VALIDATION,
    "connection": ErrorCategory.CONNECTION,
    "timeout": ErrorCategory.CONNECTION,
    "rate limit": ErrorCategory.RATE_LIMIT,
    "too many requests": ErrorCategory.RATE_LIMIT,
    "constraint": ErrorCategory.DATA_INTEGRITY,
    "duplicate": ErrorCategory.DATA_INTEGRITY,
    "unique": ErrorCategory.DATA_INTEGRITY,
}

# Recovery suggestions by category
RECOVERY_SUGGESTIONS = {
    ErrorCategory.AUTHENTICATION: [
        "Check credentials in .env file (ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD/ODOO_API_KEY)",
        "Verify API key is still valid (Odoo may expire tokens)",
        "Confirm user account is active in Odoo",
        "Run 'python execution/odoo_connect.py --test' to verify connection"
    ],
    ErrorCategory.CONNECTION: [
        "Check internet connection",
        "Verify ODOO_URL is correct in .env file",
        "Check if Odoo server is accessible (try opening URL in browser)",
        "Wait a moment and retry - may be temporary network issue"
    ],
    ErrorCategory.VALIDATION: [
        "Check field_mappings.py for correct field definitions",
        "Verify all required fields are provided",
        "Check field types match Odoo expectations",
        "Look up field requirements in related directive"
    ],
    ErrorCategory.NOT_FOUND: [
        "Verify the record exists in Odoo (check manually in UI)",
        "Use internal IDs instead of names if possible",
        "Check for typos in record names or references",
        "Ensure prerequisite records are created first"
    ],
    ErrorCategory.PERMISSION: [
        "Check user's access rights in Odoo Settings > Users",
        "Verify user has appropriate group membership",
        "Some operations require admin privileges",
        "Contact Odoo administrator to grant access"
    ],
    ErrorCategory.RATE_LIMIT: [
        "Add delays between bulk operations (1-2 seconds per 100 records)",
        "Break large operations into smaller batches",
        "Wait a few minutes before retrying",
        "Consider running during off-peak hours"
    ],
    ErrorCategory.DATA_INTEGRITY: [
        "Check for duplicate records in Odoo",
        "Verify unique constraints (e.g., product codes, partner refs)",
        "Ensure foreign key references are valid",
        "Check for circular dependencies"
    ],
    ErrorCategory.UNKNOWN: [
        "Check the full error message and stack trace",
        "Review Odoo server logs if accessible",
        "Search Odoo documentation for the error",
        "Ask for clarification about the operation"
    ],
}


def categorize_error(error: Exception) -> ErrorCategory:
    """
    Categorize an error based on its message.

    Args:
        error: The exception to categorize

    Returns:
        ErrorCategory enum value
    """
    error_str = str(error).lower()

    for pattern, category in ERROR_PATTERNS.items():
        if pattern in error_str:
            return category

    return ErrorCategory.UNKNOWN


def handle_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Handle an error and return a standardized response.

    Args:
        error: The exception that occurred
        context: Optional context about the operation (model, method, params, etc.)

    Returns:
        Dictionary with error details and recovery suggestions
    """
    category = categorize_error(error)
    suggestions = RECOVERY_SUGGESTIONS.get(category, RECOVERY_SUGGESTIONS[ErrorCategory.UNKNOWN])

    error_response = {
        'status': 'error',
        'error_type': category.value,
        'message': str(error),
        'suggestions': suggestions,
        'timestamp': datetime.now().isoformat(),
    }

    if context:
        error_response['context'] = context

    # Log the error
    logger = logging.getLogger(__name__)
    logger.error(f"[{category.value.upper()}] {error}")
    if context:
        logger.error(f"Context: {json.dumps(context, default=str)}")

    return error_response


def log_operation(status: str, data: Any, operation: Optional[str] = None) -> None:
    """
    Log an operation to the audit log.

    Args:
        status: 'SUCCESS' or 'ERROR'
        data: Operation result or error data
        operation: Optional operation name
    """
    # Get log path from environment or use default
    log_path = os.getenv('LOG_PATH', '.tmp/audit_logs/')

    # Ensure log directory exists
    project_root = Path(__file__).parent.parent
    log_dir = project_root / log_path
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create log entry
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'status': status,
        'operation': operation,
        'data': data if isinstance(data, dict) else str(data)
    }

    # Write to daily log file
    date_str = datetime.now().strftime('%Y%m%d')
    log_file = log_dir / f'audit_{date_str}.jsonl'

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, default=str) + '\n')

    # Also write to human-readable log
    operations_log = log_dir / f'operations_{date_str}.log'
    with open(operations_log, 'a', encoding='utf-8') as f:
        status_icon = '' if status == 'SUCCESS' else ''
        f.write(f"{log_entry['timestamp']} {status_icon} [{status}]")
        if operation:
            f.write(f" {operation}")
        f.write(f": {json.dumps(data, default=str)[:200]}\n")


class OperationLogger:
    """Context manager for logging operations."""

    def __init__(self, operation_name: str, context: Optional[Dict[str, Any]] = None):
        self.operation_name = operation_name
        self.context = context or {}
        self.start_time = None
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting operation: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()

        if exc_type is None:
            self.logger.info(f"Completed operation: {self.operation_name} ({duration:.2f}s)")
            log_operation('SUCCESS', {
                'operation': self.operation_name,
                'duration_seconds': duration,
                **self.context
            }, self.operation_name)
        else:
            error_data = handle_error(exc_val, self.context)
            error_data['duration_seconds'] = duration
            log_operation('ERROR', error_data, self.operation_name)

        # Don't suppress the exception
        return False


def format_error_for_user(error_response: Dict[str, Any]) -> str:
    """
    Format an error response for display to the user.

    Args:
        error_response: Error response from handle_error()

    Returns:
        Human-readable error message
    """
    lines = [
        f" Error: {error_response.get('message', 'Unknown error')}",
        f"   Type: {error_response.get('error_type', 'unknown').replace('_', ' ').title()}",
        "",
        " Suggestions:"
    ]

    for suggestion in error_response.get('suggestions', []):
        lines.append(f"   - {suggestion}")

    return '\n'.join(lines)


if __name__ == '__main__':
    # Test error handling
    print("Testing error handler...")
    print("-" * 40)

    # Test different error types
    test_errors = [
        Exception("Unable to authenticate user"),
        Exception("Record product.product(123,) does not exist"),
        Exception("Field 'partner_id' is required but missing"),
        Exception("Connection timeout"),
        Exception("Too many requests, rate limit exceeded"),
        Exception("Some random unknown error"),
    ]

    for error in test_errors:
        response = handle_error(error, {'test': True})
        print(f"\nError: {error}")
        print(f"Category: {response['error_type']}")
        print(f"First suggestion: {response['suggestions'][0]}")

    print("\n" + "-" * 40)
    print("Error handler test complete!")
