# Add root project dir to the python path
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import ctypes
import sqlalchemy
from sqlalchemy import or_, event as sqlalchemy_event

from atst.database import db
from atst.app import make_config, make_app

from atst.models.audit_event import AuditEvent
from atst.models.environment import Environment
from atst.models.environment_role import EnvironmentRole
from atst.models.project import Project
from atst.models.request import Request
from atst.models.request_revision import RequestRevision
from atst.models.request_status_event import RequestStatus, RequestStatusEvent
from atst.models.role import Role
from atst.models.user import User
from atst.models.workspace_role import WorkspaceRole
from atst.models.workspace import Workspace
from atst.models.mixins import AuditableMixin

from atst.domain.environments import Environments
from atst.domain.exceptions import NotFoundError
from atst.domain.reports import MONTHLY_SPEND_AARDVARK, MONTHLY_SPEND_BELUGA
from atst.domain.requests import Requests
from atst.domain.users import Users
from atst.domain.workspaces import Workspaces
from tests.factories import RequestFactory, TaskOrderFactory


dod_ids = [
    "1234567890",
    "2345678901",
    "3456789012",
    "4567890123",
    "5678901234",
    "6789012345",
    "2342342342", # Andy
    "3453453453", # Sally
    "4564564564", # Betty
    "6786786786",
]


def create_demo_workspace(name, data):
    try:
        workspace_owner = Users.get_by_dod_id("678678678") # Other
        auditor = Users.get_by_dod_id("3453453453") # Sally
    except NotFoundError:
        print("Could not find demo users; will not create demo workspace {}".format(name))
        return

    request = RequestFactory.build(creator=workspace_owner)
    request.task_order = TaskOrderFactory.build()
    request = Requests.update(
        request.id, {"financial_verification": RequestFactory.mock_financial_data()}
    )
    approved_request = Requests.set_status(request, RequestStatus.APPROVED)

    workspace = Requests.approve_and_create_workspace(request)
    Workspaces.update(workspace, { "name": name })

    for name in data:
        project = Project(workspace=workspace, name=name, description='')
        env_names = [env for env in data[name]]
        envs = Environments.create_many(project, env_names)
        db.session.add(project)
        db.session.commit()


def remove_sample_data(all_users=False):
    query = db.session.query(User)
    if not all_users:
        query = query.filter(User.dod_id.in_(dod_ids))
    users = query.all()

    delete_listeners = [
        k
        for k in sqlalchemy_event.registry._key_to_collection
        if k[1] == "after_delete"
    ]
    for listener in delete_listeners:
        [class_id, identifier, _] = listener
        model = ctypes.cast(class_id, ctypes.py_object).value
        sqlalchemy_event.remove(model, identifier, AuditableMixin.audit_delete)

    for user in users:
        requests = (
            db.session.query(Request)
            .filter(Request.id.in_([r.id for r in user.owned_requests]))
            .all()
        )
        request_audit = (
            db.session.query(AuditEvent)
            .filter(AuditEvent.request_id.in_([r.id for r in requests]))
            .all()
        )
        request_audit = (
            db.session.query(AuditEvent)
            .filter(AuditEvent.request_id.in_([r.id for r in requests]))
            .all()
        )
        events = [ev for r in requests for ev in r.status_events]
        revisions = [rev for r in requests for rev in r.revisions]
        workspaces = [r.workspace for r in requests if r.workspace]
        ws_audit = (
            db.session.query(AuditEvent)
            .filter(AuditEvent.workspace_id.in_([w.id for w in workspaces]))
            .all()
        )
        workspace_roles = [role for workspace in workspaces for role in workspace.roles]
        projects = [p for workspace in workspaces for p in workspace.projects]
        environments = (
            db.session.query(Environment)
            .filter(Environment.project_id.in_([p.id for p in projects]))
            .all()
        )
        roles = [role for env in environments for role in env.roles]

        for set_of_things in [
            roles,
            environments,
            projects,
            workspace_roles,
            ws_audit,
            events,
            revisions,
            request_audit,
        ]:
            for thing in set_of_things:
                db.session.delete(thing)

        db.session.commit()

        query = "DELETE FROM workspaces WHERE workspaces.id = ANY(:ids);"
        db.session.connection().execute(
            sqlalchemy.text(query), ids=[w.id for w in workspaces]
        )

        query = "DELETE FROM requests WHERE requests.id = ANY(:ids);"
        db.session.connection().execute(
            sqlalchemy.text(query), ids=[r.id for r in requests]
        )

        db.session.commit()


if __name__ == "__main__":
    config = make_config()
    app = make_app(config)
    with app.app_context():
        remove_sample_data()
        create_demo_workspace('Aardvark', MONTHLY_SPEND_AARDVARK)
        create_demo_workspace('Beluga', MONTHLY_SPEND_BELUGA)