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
    def _validate_acronym(project_achronym):
        """Validates the project acronym"""
        if not isinstance(project_achronym, str):
            raise EnterpriseManagementException("Invalid acronym: must be a string")
        if len(project_achronym) < 5 or len(project_achronym) > 10:
            raise EnterpriseManagementException("Invalid acronym: length must be between 5 and 10")
        if not re.match(r'^[A-Z0-9]+$', project_achronym):
            raise EnterpriseManagementException("Invalid acronym: only A-Z and 0-9 allowed")

    @staticmethod
    def _validate_description(project_description):
        """Validates the project description"""
        if not isinstance(project_description, str):
            raise EnterpriseManagementException("Invalid description: must be a string")
        if len(project_description) < 10 or len(project_description) > 30:
            raise EnterpriseManagementException("Invalid description: length must be between 10 and 30")

    @staticmethod
    def _validate_department(department):
        """Validates the department value"""
        if not isinstance(department, str):
            raise EnterpriseManagementException("Invalid department: must be a string")
        if department not in VALID_DEPARTMENTS:
            raise EnterpriseManagementException("Invalid department: must be HR, FINANCE, LEGAL or LOGISTICS")

    @staticmethod
    def register_project(company_cif: str, project_achronym: str,  # pylint: disable=too-many-arguments
                         project_description: str, department: str,
                         date: str, budget: float):
        """Registers a new project for a company"""
        EnterpriseManager._validate_cif(company_cif)
        EnterpriseManager._validate_acronym(project_achronym)
        EnterpriseManager._validate_description(project_description)
        EnterpriseManager._validate_department(department)
        pass