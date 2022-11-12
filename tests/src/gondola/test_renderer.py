import pytest

from src.gondola.models import AdventCalendarContributionRequestMail


class Test_EmailRenderer:
    @pytest.fixture
    def email_renderer(self, renderer):
        return renderer.email

    def test_advent_calendar_contribution_request(
        self,
        email_renderer,
        base_email,
        multiple_lines_text,
    ):
        mock_title = "This is title of advent calender"
        mock_abstract = multiple_lines_text("abstract")
        mock_expected_content = multiple_lines_text("expected_content")

        actual = email_renderer.advent_calendar_contribution_request(
            AdventCalendarContributionRequestMail(
                mail=base_email,
                title=mock_title,
                abstract=mock_abstract,
                expected_content=mock_expected_content,
            )
        )

        assert base_email.receiver.display_name in actual
        assert base_email.sender.display_name in actual
        for cc_receiver in base_email.cc_receivers:
            assert cc_receiver.display_name in actual
        assert mock_title in actual
        assert mock_abstract in actual
