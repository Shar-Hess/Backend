from flask import Blueprint, request

import controllers

orgs = Blueprint('orgs', __name__)

@orgs.route('/org', methods=['POST'])
def add_org():
    return controllers.add_org()

@orgs.route('/orgs', methods=['GET'])
def get_all_orgs():
    return controllers.get_all_orgs(request)