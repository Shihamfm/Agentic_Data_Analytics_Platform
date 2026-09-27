from analytics_agents.config.settings import settings


def test_settings_load():

    assert settings.app_name == "Agentic Data Analytics"