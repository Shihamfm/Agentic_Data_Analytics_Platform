import pandas as pd
import plotly.express as px

from analytics_agents.models.results import (
    VisualizationSpec,
)


class VisualizationRenderer:

    def render(
        self,
        dataframe: pd.DataFrame,
        spec: VisualizationSpec,
    ):

        self._validate_columns(
            dataframe,
            spec,
        )

        if spec.chart_type == "line":

            return px.line(
                dataframe,
                x=spec.x_column,
                y=spec.y_columns,
                title=spec.title,
            )

        if spec.chart_type == "bar":

            return px.bar(
                dataframe,
                x=spec.x_column,
                y=spec.y_columns,
                title=spec.title,
                orientation=(
                    "h"
                    if spec.orientation == "horizontal"
                    else "v"
                ),
            )

        if spec.chart_type == "scatter":

            if len(spec.y_columns) != 1:
                raise ValueError(
                    "Scatter plots require exactly "
                    "one y column."
                )

            return px.scatter(
                dataframe,
                x=spec.x_column,
                y=spec.y_columns[0],
                title=spec.title,
            )

        if spec.chart_type == "histogram":

            if len(spec.y_columns) != 1:
                raise ValueError(
                    "Histograms require exactly "
                    "one column."
                )

            return px.histogram(
                dataframe,
                x=spec.y_columns[0],
                title=spec.title,
            )

        if spec.chart_type == "area":

            return px.area(
                dataframe,
                x=spec.x_column,
                y=spec.y_columns,
                title=spec.title,
            )

        raise ValueError(
            f"Unsupported chart type: "
            f"{spec.chart_type}"
        )

    @staticmethod
    def _validate_columns(
        dataframe: pd.DataFrame,
        spec: VisualizationSpec,
    ) -> None:

        required_columns = {
            spec.x_column,
            *spec.y_columns,
        }

        missing_columns = (
            required_columns
            - set(dataframe.columns)
        )

        if missing_columns:
            raise ValueError(
                "Visualization references "
                f"missing columns: "
                f"{sorted(missing_columns)}"
            )