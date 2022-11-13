import pytest

from src.gondola.models import AdventCalendarContributionRequestMail


class Test_MailRenderer:
    @pytest.fixture
    def mail_renderer(self, renderer):
        return renderer.mail

    def test_advent_calendar_contribution_request(
        self,
        mail_renderer,
        base_mail,
        multiple_lines_text,
    ):
        mock_expected_content = multiple_lines_text("expected_content")

        actual = mail_renderer.advent_calendar_contribution_request(
            AdventCalendarContributionRequestMail(
                mail=base_mail,
                expected_content=mock_expected_content,
            )
        )

        assert base_mail.receiver.display_name in actual
        assert base_mail.sender.display_name in actual
        for cc_receiver in base_mail.cc_receivers:
            assert cc_receiver.display_name in actual
