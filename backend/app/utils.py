import logging
from typing import Dict, Any

import emails
from emails.template import JinjaTemplate

from app.config import get_settings
from app.core.security.utils import create_access_token

settings = get_settings()


def send_email(send_to: str = "", subject: str = "", html: str = "", template_vars: Dict[str, Any] = {}) -> None:
    message = emails.Message(
        subject=JinjaTemplate(subject),
        html=JinjaTemplate(html),
        mail_from=(settings.emails_from_name, settings.emails_from_email),
    )
    smtp_options = {"host": settings.smtp_host, "port": settings.smtp_port}
    if settings.smtp_tls:
        smtp_options["tls"] = True
    if settings.smtp_user:
        smtp_options["user"] = settings.smtp_user
    if settings.smtp_password:
        smtp_options["password"] = settings.smtp_password
    response = message.send(to=send_to, render=template_vars, smtp=smtp_options)
    logging.info(f"send email result: {response.status_code}, sent to: {send_to}, subject: {subject}")


def new_user_email(email: str, username: str, full_name: str) -> None:
    with open("app/email_templates/new_user.html") as f:
        html = f.read()
    token = create_access_token(
        data={"sub": username, "type": "new_user"},
        expiry=settings.new_user_token_expiry,
        key=settings.auth_secret_key,
        algorithm=settings.token_algorithm,
    )
    send_email(
        send_to=email,
        subject=f"User account confirmation: {username}",
        html=html,
        template_vars={
            "confirm_link": f"http://{settings.server_host}/api/users/confirm?token={token.decode('utf-8')}",
            "user": full_name.split(" ")[0],
        },
    )
