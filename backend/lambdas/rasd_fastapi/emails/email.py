"""RASD FastAPI Email Functionality."""


# Standard
import pathlib

# Third-Party
import jinja2

# Local
from rasd_fastapi.core import settings
from rasd_fastapi.emails import ses

# Typing
from typing import Any, Optional, Union


# Shortcuts
StrOrStrList = Union[str, list[str]]


# Jinja2 Environment
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(pathlib.Path(__file__).parent / "templates"),
    autoescape=True,
)


class Email:
    """Email Abstraction."""

    def __init__(self, template: str, subject: str) -> None:
        """Instantiates an Email."""
        # Retrieve and Store Template and Subject
        self.template = env.get_template(template)
        self.subject = subject

    def send(
        self,
        to_addresses: StrOrStrList,
        from_address: Optional[str] = None,
        cc_addresses: Optional[StrOrStrList] = None,
        bcc_addresses: Optional[StrOrStrList] = None,
        **kwargs: Any,
    ) -> None:
        """Send an email using AWS SESv2.

        Args:
            to_addresses (StrOrStrList): Email addresses to send the email to.
            from_address: (Optional[str]): Optional email address to send the
                email from. Defaults to settings.SETTINGS.FROM_EMAIL.
            cc_addresses (Optional[StrOrStrList]): Optional email addresses to
                cc the email to. Defaults to None.
            bcc_addresses (Optional[StrOrStrList]): Optional email addresses to
                bcc the email to. Defaults to None.
            **kwargs (Any): Context to render the Jinja2 Template.
        """
        # Check and replace the from address with default if required
        # The "name <email>" format is required to have a sender name in AWS SESv2
        from_address = from_address or f"{settings.SETTINGS.EMAIL_FROM_NAME} <{settings.SETTINGS.EMAIL_FROM_ADDRESS}>"

        # Listify the addresses if required
        # This allows the caller to provider a single email address (str) or
        # a list of email addresses (list[str]) without worrying about the
        # implementation or handling.
        if not isinstance(to_addresses, list):
            to_addresses = [to_addresses]
        if not isinstance(cc_addresses, list):
            cc_addresses = [cc_addresses] if cc_addresses else []
        if not isinstance(bcc_addresses, list):
            bcc_addresses = [bcc_addresses] if bcc_addresses else []

        # Render Subject and Template
        subject = self.subject.format(**kwargs)
        html_body = self.template.render(kwargs)

        # Get Client
        client = ses.ses_client()

        # Construct and Send Email
        client.send_email(
            FromEmailAddress=from_address,
            Destination={
                "ToAddresses": to_addresses,
                "CcAddresses": cc_addresses,
                "BccAddresses": bcc_addresses,
            },
            ReplyToAddresses=[from_address],
            Content={
                "Simple": {
                    "Subject": {
                        "Data": subject,
                        "Charset": "UTF-8"
                    },
                    "Body": {
                        "Html": {
                            "Data": html_body,
                            "Charset": "UTF-8"
                        },
                    },
                },
            },
        )


# Email Singletons
access_request_created = Email("dar_created.html", "RASD Acknowledgement of Data Access Request ID {request_id}")
access_request_completed = Email("dar_completed.html", "RASD Completion of Data Access Request ID {request_id}")
dataset_request_created = Email("dsr_created.html", "New Data Access Request for your organisation - Request ID {request_id}")  # noqa: E501
dataset_request_acknowledged = Email("dsr_acknowledged.html", "RASD Acknowledgement of Request ID {request_id}")
dataset_request_approved = Email("dsr_approved.html", "RASD Request ID {request_id} Approved")
dataset_request_declined = Email("dsr_declined.html", "RASD Request ID {request_id} Declined")
dataset_request_agreement = Email("dsr_agreement.html", "RASD Agreement executed for Request ID {request_id}")
dataset_request_completed = Email("dsr_completed.html", "RASD Completion of Request ID {request_id}")
registration_created = Email("registration_created.html", "RASD Registration Request Received")
registration_approved = Email("registration_approved.html", "RASD Registration Request has been approved")
registration_declined = Email("registration_declined.html", "RASD Registration Request has been declined")
registration_temporary_password = Email("registration_temporary_password.html", "RASD temporary password has been reset")  # noqa: E501
