from pydantic import BaseModel, Field, ConfigDict

class DataRequirement(BaseModel):
    table: str
    columns: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    dimensions: list[str] = Field(default_factory=list)
    filters: list[str] = Field(default_factory=list)


class DiscoveryResult(BaseModel):
    intent: str
    requirements: list[DataRequirement] = Field(
        default_factory=list
    )
    reasoning: str | None = None

class SQLResult(BaseModel):
    sql: str
    explanation: str | None
    tables_used: list[str]
    metrics_used: list[str]
    dimensions_used: list[str]
    model_config = ConfigDict(extra="forbid")

class SQLValidationResult(BaseModel):
    approved: bool
    sql: str
    issues: list[str] = Field(
        default_factory=list
    )

class AnalysisFinding(BaseModel):
    title: str
    description: str
    evidence: list[str] = Field(
        default_factory=list
    )

class AnalysisResult(BaseModel):
    summary: str
    findings: list[AnalysisFinding] = Field(
        default_factory=list
    )
    limitations: list[str] = Field(
        default_factory=list
    )

class VisualizationSpec(BaseModel):
    chart_type: str
    title: str
    x_column: str
    y_columns: list[str]
    description: str | None = None


class VisualizationResult(BaseModel):
    charts: list[VisualizationSpec] = Field(
        default_factory=list
    )

class ValidationResult(BaseModel):
    approved: bool
    issues: list[str] = Field(
        default_factory=list
    )
    warnings: list[str] = Field(
        default_factory=list
    )

