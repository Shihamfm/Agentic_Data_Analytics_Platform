from analytics_agents.models.state import AnalyticsState


def test_initial_state():

    state = AnalyticsState(
        user_query="Why did revenue decrease in August?"
    )

    assert (
        state.user_query
        == "Why did revenue decrease in August?"
    )

    assert state.discovery is None
    assert state.sql_result is None
    assert state.analysis is None
    assert state.final_response is None