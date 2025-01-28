from flask import Blueprint, jsonify, request

from controllers import company_controller

company = Blueprint('company', __name__)

@company.route('/company', methods=["POST"])
def create_company():
    new_company = company_controller.create_company(data)

    return jsonify(new_company), 201