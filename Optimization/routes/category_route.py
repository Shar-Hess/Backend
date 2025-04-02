from flask import Blueprint
from controllers import category_controller

category = Blueprint('category', __name__)

@category.route('/category', methods=["POST"])
def category_add():
    return category_controller.category_add()

@category.route('/categories', methods=["GET"])
def categories_get_all():
    return category_controller.categories_get_all()

@category.route('/category/<category_id>', methods=["GET"])
def category_get_by_id(category_id):
    return category_controller.category_get_by_id(category_id)

@category.route('/category/<category_id>', methods=["PUT"])
def category_update_by_id(category_id):
    return category_controller.category_update_by_id(category_id)

@category.route('/category/delete/<category_id>', methods=["DELETE"])
def category_delete_by_id(category_id):
    return category_controller.category_delete_by_id(category_id)