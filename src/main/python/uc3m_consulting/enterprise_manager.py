"""Module """
from .enterprise_project import EnterpriseProject
class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    @staticmethod
    def register_project(company_cif: str, project_achronym: str,
                         project_description: str, department: str,
                         date: str, budget: float):
        """Registers a new project for a company"""
        enterprise_project = EnterpriseProject(
            company_cif, project_achronym, project_description,
            department, date, budget)
        return enterprise_project.project_id