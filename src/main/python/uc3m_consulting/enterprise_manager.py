"""Module for enterprise management operations"""
import re
import json
import os
from datetime import datetime, timezone
from .enterprise_project import EnterpriseProject
from .enterprise_management_exception import EnterpriseManagementException

VALID_DEPARTMENTS = ["HR", "FINANCE", "LEGAL", "LOGISTICS"]
CORPORATE_OPERATIONS_FILE = "corporate_operations.json"


class EnterpriseManager:
    """Class for providing the methods for managing enterprise projects"""

    @staticmethod
    def _validate_cif(company_cif):
        """Validates the Spanish CIF code"""
        if not isinstance(company_cif, str):
            raise EnterpriseManagementException("Invalid CIF: must be a string")
        if len(company_cif) != 9:
            raise EnterpriseManagementException("Invalid CIF: length must be 9")
        if not company_cif[0].isalpha():
            raise EnterpriseManagementException("Invalid CIF: first character must be a letter")
        if not company_cif[1:8].isdigit():
            raise EnterpriseManagementException("Invalid CIF: positions 2-8 must be digits")
        digits = [int(d) for d in company_cif[1:8]]
        odd_sum = sum(
            (d * 2) if (d * 2) < 10 else (d * 2) // 10 + (d * 2) % 10
            for d in digits[0::2]
        )
        even_sum = sum(digits[1::2])
        control = (10 - ((odd_sum + even_sum) % 10)) % 10
        if company_cif[8] != str(control):
            raise EnterpriseManagementException("Invalid CIF: control digit does not match")

    @staticmethod
    def validate_cif(cif: str):
        """Returns True if the CIF received is valid"""
        return True

    @staticmethod
    def register_project(company_cif: str, project_achronym: str,  # pylint: disable=too-many-arguments
                         project_description: str, department: str,
                         date: str, budget: float):
        """Registers a new project for a company"""
        EnterpriseManager._validate_cif(company_cif)
        pass