from flask import Blueprint
from controllers import warranty_controller

warranty = Blueprint('warranty', __name__)


@warranty.route('/warranty', methods=["POST"])
def warranty_add():
    return warranty_controller.warranty_add()


@warranty.route('/warranty/<warranty_id>', methods=["GET"])
def warranty_get_by_id(warranty_id):
    return warranty_controller.warranty_get_by_id(warranty_id)


@warranty.route('/warranty/<warranty_id>', methods=["PUT"])
def warranty_update_by_id(warranty_id):
    return warranty_controller.warranty_update_by_id(warranty_id)


@warranty.route('/warranty/delete/<warranty_id>', methods=["DELETE"])
def warranty_delete_by_id(warranty_id):
    return warranty_controller.warranty_delete_by_id(warranty_id)
