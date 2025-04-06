import routes

def register_blueprints(app):

    app.register_blueprint(routes.exercises)
    app.register_blueprint(routes.workouts)
    app.register_blueprint(routes.user_profiles)
    app.register_blueprint(routes.exercise_types)
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.users)
