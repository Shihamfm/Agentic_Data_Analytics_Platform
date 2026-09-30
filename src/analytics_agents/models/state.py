from typing import Any

from pydantic import BaseModel, Field

from analytics_agents.models.results import (
    DiscoveryResult,
    SQLResult,
    SQLValidationResult,
    AnalysisResult,
    VisualizationResult,
    ValidationResult,
)

class ExecutionMetadata(BaseModel):
    run_id: str | None = None
    started_at: str | None = None
    completed_at: str | None = None

    total_execution_time_seconds: float | None = None

    agent_execution_times: dict[str, float] = Field(
        default_factory=dict
    )

    errors: list[str] = Field(
        default_factory=list
    )


class AnalyticsState(BaseModel):

    user_query: str
    discovery: DiscoveryResult | None = None
    sql_result: SQLResult | None = None
    sql_validation: SQLValidationResult | None = None
    query_result: Any | None = None
    analysis: AnalysisResult | None = None
    visualization: VisualizationResult | None = None
    validation: ValidationResult | None = None
    final_response: str | None = None
    
    metadata: ExecutionMetadata = Field(
        default_factory=ExecutionMetadata
    )