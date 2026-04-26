from flask import Flask
from flask_restful import Api
from data import db_session, users_resource, jobs_resource

app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init("db/blogs.db")
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:jobs_id>')
    app.run(debug=True)


if __name__ == '__main__':
    main()