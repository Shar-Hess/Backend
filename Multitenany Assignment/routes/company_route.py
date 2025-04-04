from flask import Blueprint
from controllers import company_controller

company = Blueprint('company', __name__)

@company.route('/company', methods=["POST"])
def company_add():
    return company_controller.company_add()

@company.route('/companies', methods=["GET"])
def companies_get_all():
    return company_controller.companies_get_all()

@company.route('/company/<company_id>', methods=["GET"])
def company_get_by_id(company_id):
    return company_controller.company_get_by_id(company_id)

@company.route('/company/<company_id>', methods=['PUT'])
def company_update_by_id(company_id):
    return company_controller.company_update_by_id(company_id)