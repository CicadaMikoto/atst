import datetime
from flask import url_for

from tests.factories import (
    UserFactory,
    PortfolioFactory,
    PortfolioRoleFactory,
    InvitationFactory,
    TaskOrderFactory,
)
from atst.domain.portfolios import Portfolios
from atst.models.portfolio_role import Status as PortfolioRoleStatus
from atst.models.invitation import Status as InvitationStatus
from atst.domain.users import Users


def test_existing_member_accepts_valid_invite(client, user_session):
    portfolio = PortfolioFactory.create()
    user = UserFactory.create()
    ws_role = PortfolioRoleFactory.create(
        portfolio=portfolio, user=user, status=PortfolioRoleStatus.PENDING
    )
    invite = InvitationFactory.create(user_id=user.id, portfolio_role=ws_role)

    # the user does not have access to the portfolio before accepting the invite
    assert len(Portfolios.for_user(user)) == 0

    user_session(user)
    response = client.get(url_for("portfolios.accept_invitation", token=invite.token))

    # user is redirected to the portfolio view
    assert response.status_code == 302
    assert (
        url_for("portfolios.show_portfolio", portfolio_id=invite.portfolio.id)
        in response.headers["Location"]
    )
    # the one-time use invite is no longer usable
    assert invite.is_accepted
    # the user has access to the portfolio
    assert len(Portfolios.for_user(user)) == 1


def test_new_member_accepts_valid_invite(monkeypatch, client, user_session):
    portfolio = PortfolioFactory.create()
    user_info = UserFactory.dictionary()

    user_session(portfolio.owner)
    client.post(
        url_for("portfolios.create_member", portfolio_id=portfolio.id),
        data={"portfolio_role": "developer", **user_info},
    )

    user = Users.get_by_dod_id(user_info["dod_id"])
    token = user.invitations[0].token

    monkeypatch.setattr(
        "atst.domain.auth.should_redirect_to_user_profile", lambda *args: False
    )
    user_session(user)
    response = client.get(url_for("portfolios.accept_invitation", token=token))

    # user is redirected to the portfolio view
    assert response.status_code == 302
    assert (
        url_for("portfolios.show_portfolio", portfolio_id=portfolio.id)
        in response.headers["Location"]
    )
    # the user has access to the portfolio
    assert len(Portfolios.for_user(user)) == 1


def test_member_accepts_invalid_invite(client, user_session):
    portfolio = PortfolioFactory.create()
    user = UserFactory.create()
    ws_role = PortfolioRoleFactory.create(
        user=user, portfolio=portfolio, status=PortfolioRoleStatus.PENDING
    )
    invite = InvitationFactory.create(
        user_id=user.id,
        portfolio_role=ws_role,
        status=InvitationStatus.REJECTED_WRONG_USER,
    )
    user_session(user)
    response = client.get(url_for("portfolios.accept_invitation", token=invite.token))

    assert response.status_code == 404


def test_user_who_has_not_accepted_portfolio_invite_cannot_view(client, user_session):
    user = UserFactory.create()
    portfolio = PortfolioFactory.create()

    # create user in portfolio with invitation
    user_session(portfolio.owner)
    response = client.post(
        url_for("portfolios.create_member", portfolio_id=portfolio.id),
        data={"portfolio_role": "developer", **user.to_dictionary()},
    )

    # user tries to view portfolio before accepting invitation
    user_session(user)
    response = client.get("/portfolios/{}/applications".format(portfolio.id))
    assert response.status_code == 404


def test_user_accepts_invite_with_wrong_dod_id(client, user_session):
    portfolio = PortfolioFactory.create()
    user = UserFactory.create()
    different_user = UserFactory.create()
    ws_role = PortfolioRoleFactory.create(
        user=user, portfolio=portfolio, status=PortfolioRoleStatus.PENDING
    )
    invite = InvitationFactory.create(user_id=user.id, portfolio_role=ws_role)
    user_session(different_user)
    response = client.get(url_for("portfolios.accept_invitation", token=invite.token))

    assert response.status_code == 404


def test_user_accepts_expired_invite(client, user_session):
    portfolio = PortfolioFactory.create()
    user = UserFactory.create()
    ws_role = PortfolioRoleFactory.create(
        user=user, portfolio=portfolio, status=PortfolioRoleStatus.PENDING
    )
    invite = InvitationFactory.create(
        user_id=user.id,
        portfolio_role=ws_role,
        status=InvitationStatus.REJECTED_EXPIRED,
        expiration_time=datetime.datetime.now() - datetime.timedelta(seconds=1),
    )
    user_session(user)
    response = client.get(url_for("portfolios.accept_invitation", token=invite.token))

    assert response.status_code == 404


def test_revoke_invitation(client, user_session):
    portfolio = PortfolioFactory.create()
    user = UserFactory.create()
    ws_role = PortfolioRoleFactory.create(
        user=user, portfolio=portfolio, status=PortfolioRoleStatus.PENDING
    )
    invite = InvitationFactory.create(
        user_id=user.id,
        portfolio_role=ws_role,
        status=InvitationStatus.REJECTED_EXPIRED,
        expiration_time=datetime.datetime.now() - datetime.timedelta(seconds=1),
    )
    user_session(portfolio.owner)
    response = client.post(
        url_for(
            "portfolios.revoke_invitation",
            portfolio_id=portfolio.id,
            token=invite.token,
        )
    )

    assert response.status_code == 302
    assert invite.is_revoked


def test_resend_invitation_sends_email(client, user_session, queue):
    user = UserFactory.create()
    portfolio = PortfolioFactory.create()
    ws_role = PortfolioRoleFactory.create(
        user=user, portfolio=portfolio, status=PortfolioRoleStatus.PENDING
    )
    invite = InvitationFactory.create(
        user_id=user.id, portfolio_role=ws_role, status=InvitationStatus.PENDING
    )
    user_session(portfolio.owner)
    client.post(
        url_for(
            "portfolios.resend_invitation",
            portfolio_id=portfolio.id,
            token=invite.token,
        )
    )

    assert len(queue.get_queue()) == 1


def test_existing_member_invite_resent_to_email_submitted_in_form(
    client, user_session, queue
):
    portfolio = PortfolioFactory.create()
    user = UserFactory.create()
    ws_role = PortfolioRoleFactory.create(
        user=user, portfolio=portfolio, status=PortfolioRoleStatus.PENDING
    )
    invite = InvitationFactory.create(
        user_id=user.id,
        portfolio_role=ws_role,
        status=InvitationStatus.PENDING,
        email="example@example.com",
    )
    user_session(portfolio.owner)
    client.post(
        url_for(
            "portfolios.resend_invitation",
            portfolio_id=portfolio.id,
            token=invite.token,
        )
    )

    send_mail_job = queue.get_queue().jobs[0]
    assert user.email != "example@example.com"
    assert send_mail_job.func.__func__.__name__ == "_send_mail"
    assert send_mail_job.args[0] == ["example@example.com"]


def test_contracting_officer_accepts_invite(monkeypatch, client, user_session):
    portfolio = PortfolioFactory.create()
    task_order = TaskOrderFactory.create(portfolio=portfolio)
    user_info = UserFactory.dictionary()

    # create contracting officer
    user_session(portfolio.owner)
    client.post(
        url_for("task_orders.new", screen=3, task_order_id=task_order.id),
        data={
            "portfolio_role": "contracting_officer",
            "ko_first_name": user_info["first_name"],
            "ko_last_name": user_info["last_name"],
            "ko_email": user_info["email"],
            "ko_phone_number": user_info["phone_number"],
            "ko_dod_id": user_info["dod_id"],
            "cor_phone_number": user_info["phone_number"],
            "so_phone_number": user_info["phone_number"],
            "so_dod_id": task_order.so_dod_id,
            "cor_dod_id": task_order.cor_dod_id,
            "ko_invite": True,
        },
    )

    # contracting officer accepts invitation
    user = Users.get_by_dod_id(user_info["dod_id"])
    token = user.invitations[0].token
    monkeypatch.setattr(
        "atst.domain.auth.should_redirect_to_user_profile", lambda *args: False
    )
    user_session(user)
    response = client.get(url_for("portfolios.accept_invitation", token=token))

    # user is redirected to the task order review page
    assert response.status_code == 302
    to_review_url = url_for(
        "portfolios.view_task_order",
        portfolio_id=task_order.portfolio_id,
        task_order_id=task_order.id,
        _external=True,
    )
    assert response.headers["Location"] == to_review_url