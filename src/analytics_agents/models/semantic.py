from pydantic import BaseModel, Field

class SemanticMetric(BaseModel):
    name: str
    expression: str
    description: str
    data_type: str = "numeric"


class SemanticDimension(BaseModel):
    name: str
    column: str
    description: str
    data_type: str = "string"


class SemanticTable(BaseModel):
    name: str
    description: str
    columns: list[str] = Field(default_factory=list)


class SemanticCatalog(BaseModel):
    tables: list[SemanticTable] = Field(
        default_factory=list
    )

    metrics: list[SemanticMetric] = Field(
        default_factory=list
    )

    dimensions: list[SemanticDimension] = Field(
        default_factory=list
    )