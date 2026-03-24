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
        EnterpriseManager._validate_date(date)
        EnterpriseManager._validate_budget(budget)
        pass

    @staticmethod
    def _validate_date(date):
        """Validates the project start date"""
        if not isinstance(date, str):
            raise EnterpriseManagementException("Invalid date: must be a string")
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date):
            raise EnterpriseManagementException("Invalid date: format must be DD/MM/YYYY")
        parts = date.split('/')
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
        if day < 1 or day > 31:
            raise EnterpriseManagementException("Invalid date: DD must be between 01 and 31")
        if month < 1 or month > 12:
            raise EnterpriseManagementException("Invalid date: MM must be between 01 and 12")
        if year < 2025 or year > 2027:
            raise EnterpriseManagementException("Invalid date: year must be between 2025 and 2027")
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y")
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date: not a valid calendar date") from ex
        today = datetime.now(timezone.utc).replace(tzinfo=None, hour=0, minute=0, second=0, microsecond=0)
        if date_obj < today:
            raise EnterpriseManagementException("Invalid date: must be equal to or after request date")

    @staticmethod
    def _validate_budget(budget):
        """Validates the project budget"""
        if not isinstance(budget, float):
            raise EnterpriseManagementException("Invalid budget: must be a float")
        if round(budget, 2) != budget:
            raise EnterpriseManagementException("Invalid budget: must have exactly 2 decimal places")
        if budget < 50000.00 or budget > 1000000.00:
            raise EnterpriseManagementException("Invalid budget: must be between 50000.00 and 1000000.00")
