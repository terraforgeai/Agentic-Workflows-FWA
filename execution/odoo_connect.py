#!/usr/bin/env python3
"""
Odoo Connection Manager - Foundational Connection Script

Purpose: Manage connection and authentication to Odoo Online (fwapparel)
Input: Environment variables from .env file
Output: Authenticated Odoo RPC connection

This is the FOUNDATIONAL script - all other execution scripts depend on this.

Related Directive: N/A (Core infrastructure)
"""

import os
import sys
import xmlrpc.client
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OdooConnectionError(Exception):
    """Custom exception for Odoo connection errors."""
    pass


class OdooConnection:
    """
    Manages connection to Odoo via XML-RPC API.

    Usage:
        odoo = OdooConnection()
        # Search for records
        partner_ids = odoo.search('res.partner', [('is_company', '=', True)])
        # Read records
        partners = odoo.read('res.partner', partner_ids, ['name', 'email'])
        # Create records
        new_id = odoo.create('res.partner', {'name': 'New Partner'})
        # Update records
        odoo.write('res.partner', [new_id], {'phone': '123-456-7890'})
    """

    def __init__(self, env_path: Optional[str] = None):
        """
        Initialize Odoo connection from environment variables.

        Args:
            env_path: Optional path to .env file. Defaults to project root.
        """
        # Load environment variables
        if env_path:
            load_dotenv(env_path)
        else:
            # Try to find .env in project root
            project_root = Path(__file__).parent.parent
            env_file = project_root / '.env'
            if env_file.exists():
                load_dotenv(env_file)
            else:
                logger.warning(f".env file not found at {env_file}")

        # Get connection parameters
        self.url = os.getenv('ODOO_URL')
        self.db = os.getenv('ODOO_DB')
        self.username = os.getenv('ODOO_USERNAME')
        self.password = os.getenv('ODOO_PASSWORD')
        self.api_key = os.getenv('ODOO_API_KEY')

        # Validate required parameters
        self._validate_config()

        # Initialize connection attributes
        self.uid: Optional[int] = None
        self.common: Optional[xmlrpc.client.ServerProxy] = None
        self.models: Optional[xmlrpc.client.ServerProxy] = None

        # Connect on initialization
        self._connect()

    def _validate_config(self) -> None:
        """Validate that all required configuration is present."""
        missing = []
        if not self.url:
            missing.append('ODOO_URL')
        if not self.db:
            missing.append('ODOO_DB')
        if not self.username:
            missing.append('ODOO_USERNAME')
        if not self.password and not self.api_key:
            missing.append('ODOO_PASSWORD or ODOO_API_KEY')

        if missing:
            raise OdooConnectionError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Please check your .env file."
            )

    def _connect(self) -> None:
        """Establish connection to Odoo and authenticate."""
        try:
            # Create XML-RPC proxies
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

            # Authenticate - use API key if available, otherwise password
            auth_credential = self.api_key if self.api_key else self.password

            self.uid = self.common.authenticate(
                self.db,
                self.username,
                auth_credential,
                {}
            )

            if not self.uid:
                raise OdooConnectionError(
                    f"Authentication failed for user '{self.username}' on database '{self.db}'. "
                    f"Please verify your credentials in .env file."
                )

            logger.info(f"Connected to Odoo: {self.url} (db: {self.db}, uid: {self.uid})")

        except xmlrpc.client.Fault as e:
            raise OdooConnectionError(f"Odoo XML-RPC Fault: {e.faultString}")
        except Exception as e:
            raise OdooConnectionError(f"Failed to connect to Odoo: {str(e)}")

    def _get_auth(self) -> str:
        """Get authentication credential (API key or password)."""
        return self.api_key if self.api_key else self.password

    def search(self, model: str, domain: List, offset: int = 0,
               limit: Optional[int] = None, order: Optional[str] = None) -> List[int]:
        """
        Search for record IDs matching the domain.

        Args:
            model: Odoo model name (e.g., 'res.partner', 'sale.order')
            domain: Search domain (e.g., [('is_company', '=', True)])
            offset: Number of records to skip
            limit: Maximum number of records to return
            order: Sort order (e.g., 'name asc, id desc')

        Returns:
            List of matching record IDs
        """
        kwargs = {'offset': offset}
        if limit:
            kwargs['limit'] = limit
        if order:
            kwargs['order'] = order

        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, 'search', [domain], kwargs
        )

    def search_count(self, model: str, domain: List) -> int:
        """
        Count records matching the domain.

        Args:
            model: Odoo model name
            domain: Search domain

        Returns:
            Number of matching records
        """
        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, 'search_count', [domain]
        )

    def read(self, model: str, ids: List[int],
             fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Read field values from records.

        Args:
            model: Odoo model name
            ids: List of record IDs to read
            fields: List of field names to read (None = all fields)

        Returns:
            List of dictionaries with record data
        """
        kwargs = {}
        if fields:
            kwargs['fields'] = fields

        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, 'read', [ids], kwargs
        )

    def search_read(self, model: str, domain: List,
                    fields: Optional[List[str]] = None,
                    offset: int = 0, limit: Optional[int] = None,
                    order: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search and read in one call (more efficient).

        Args:
            model: Odoo model name
            domain: Search domain
            fields: Fields to read
            offset: Number of records to skip
            limit: Maximum records to return
            order: Sort order

        Returns:
            List of matching records with field values
        """
        kwargs = {'offset': offset}
        if fields:
            kwargs['fields'] = fields
        if limit:
            kwargs['limit'] = limit
        if order:
            kwargs['order'] = order

        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, 'search_read', [domain], kwargs
        )

    def create(self, model: str, values: Dict[str, Any]) -> int:
        """
        Create a new record.

        Args:
            model: Odoo model name
            values: Dictionary of field values

        Returns:
            ID of the created record
        """
        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, 'create', [values]
        )

    def write(self, model: str, ids: List[int], values: Dict[str, Any]) -> bool:
        """
        Update existing records.

        Args:
            model: Odoo model name
            ids: List of record IDs to update
            values: Dictionary of field values to update

        Returns:
            True if successful
        """
        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, 'write', [ids, values]
        )

    def unlink(self, model: str, ids: List[int]) -> bool:
        """
        Delete records.

        Args:
            model: Odoo model name
            ids: List of record IDs to delete

        Returns:
            True if successful
        """
        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, 'unlink', [ids]
        )

    def execute(self, model: str, method: str, *args, **kwargs) -> Any:
        """
        Execute any method on an Odoo model.

        Args:
            model: Odoo model name
            method: Method name to call
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Method result
        """
        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, method, list(args), kwargs
        )

    def get_fields(self, model: str, attributes: Optional[List[str]] = None) -> Dict:
        """
        Get field definitions for a model.

        Args:
            model: Odoo model name
            attributes: Field attributes to return (e.g., ['type', 'string', 'required'])

        Returns:
            Dictionary of field definitions
        """
        kwargs = {}
        if attributes:
            kwargs['attributes'] = attributes

        return self.models.execute_kw(
            self.db, self.uid, self._get_auth(),
            model, 'fields_get', [], kwargs
        )

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection and return server info.

        Returns:
            Dictionary with connection status and server info
        """
        try:
            version = self.common.version()
            user_info = self.read('res.users', [self.uid], ['name', 'login', 'company_id'])

            return {
                'status': 'success',
                'message': f'Connected to Odoo {self.db}',
                'server_version': version.get('server_version'),
                'user_id': self.uid,
                'user_name': user_info[0]['name'] if user_info else 'Unknown',
                'user_login': user_info[0]['login'] if user_info else 'Unknown',
                'company': user_info[0]['company_id'][1] if user_info and user_info[0].get('company_id') else 'Unknown'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }


def test_connection():
    """CLI test function."""
    print("Testing Odoo connection...")
    print("-" * 40)

    try:
        odoo = OdooConnection()
        result = odoo.test_connection()

        if result['status'] == 'success':
            print(f"Connected to Odoo [{result.get('server_version', 'unknown')}]")
            print(f"  Database: {odoo.db}")
            print(f"  User: {result.get('user_name')} ({result.get('user_login')})")
            print(f"  Company: {result.get('company')}")
            print(f"  User ID: {result.get('user_id')}")
            print("-" * 40)
            print("Connection test PASSED")
            return True
        else:
            print(f"Connection test FAILED: {result.get('message')}")
            return False

    except OdooConnectionError as e:
        print(f"Connection test FAILED: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Odoo Connection Manager')
    parser.add_argument('--test', action='store_true', help='Test connection to Odoo')

    args = parser.parse_args()

    if args.test:
        success = test_connection()
        sys.exit(0 if success else 1)
    else:
        # Default: run test
        test_connection()
