from typing import List, Optional, ClassVar

from pydantic import BaseModel, Field, model_validator


class TestCase(BaseModel):
    id: Optional[str] = Field(
        description="A unique identifier for the test case"
    )
    search_terms: str = Field(
        description="The terms which will be searched for."
    )
    description: Optional[str] = Field(
        description=(
            "An optional description of the test case. Can be used to explain "
            "what the test intention is, any assumptions made, links to "
            "discussions which motivated the test, etc."
        ),
        default=None,
    )

    def __init__(self, **data):
        # if an id hasn't been set, use the search terms
        if "id" not in data:
            data["id"] = data["search_terms"]
        super().__init__(**data)


class PrecisionTestCase(TestCase):
    expected_ids: List[str] = Field(
        description=(
            "The IDs which should be returned first by the search. Unless "
            "strict is set to True, these results can appear in any order, "
            "as long as they make up the first results."
        )
    )
    threshold_position: Optional[int] = Field(
        description=(
            "The last possible position for the expected ID in the search "
            "results. If None, the expected IDs must be the first results. If "
            "specified, the expected IDs must appear at or before this "
            "position, otherwise the test should fail. If the expected ID is "
            "between the first and this position, the test should raise a "
            "warning."
        )
    )
    strict: bool = Field(
        description=(
            "If True, the expected IDs must be the first results, in the "
            "order specified. If False, the expected IDs can appear in any "
            "order, as long as they are the first results."
        ),
        default=False,
    )

    def __init__(self, **data):
        # if the threshold position hasn't been specified, it should be
        # the same as the number of expected IDs
        if "threshold_position" not in data:
            data["threshold_position"] = len(data["expected_ids"])
        super().__init__(**data)

    @model_validator(mode="after")
    def check_expected_ids(self):
        if len(self.expected_ids) == 0:
            raise ValueError("expected_ids must not be empty")
        if len(self.expected_ids) != len(set(self.expected_ids)):
            raise ValueError("expected_ids must be unique")
        return self

    @model_validator(mode="after")
    def check_threshold_position(self):
        """Check that the threshold position is valid"""
        if self.threshold_position is not None:
            if self.threshold_position < 0:
                raise ValueError(
                    "threshold_position must be greater than or equal to 0"
                )
            if self.threshold_position < len(self.expected_ids):
                raise ValueError(
                    "threshold_position must be greater than the number of "
                    "expected IDs"
                )
        return self


class RecallTestCase(TestCase):
    expected_ids: List[str] = Field(
        description=(
            "The IDs which should be returned by the search. Unless "
            "strict is set to True, these results can appear in any order."
        )
    )

    threshold_position: Optional[int] = Field(
        description=(
            "The last possible position for the expected ID in the search "
            "results",
        ),
        default=10_000,
    )

    @model_validator(mode="after")
    def check_expected_ids(self):
        if len(self.expected_ids) == 0:
            raise ValueError("expected_ids must not be empty")
        if len(self.expected_ids) != len(set(self.expected_ids)):
            raise ValueError("expected_ids must be unique")
        return self


class OrderTestCase(TestCase):
    before_ids: list[str] = Field(
        ...,
        description=(
            "The IDs which are expected to be returned by the search before "
            "the IDs in the 'after_ids' field."
        ),
    )
    after_ids: list[str] = Field(
        ...,
        description=(
            "The IDs which are expected to be returned by the search after the "
            "IDs in the 'before_ids' field."
        ),
    )

    threshold_position: ClassVar[int] = 10_000

    @model_validator(mode="after")
    def check_expected_ids(self):
        if len(self.before_ids) != len(set(self.before_ids)):
            raise ValueError("before_ids must be unique")
        if len(self.after_ids) != len(set(self.after_ids)):
            raise ValueError("after_ids must be unique")
        if len(set(self.before_ids).intersection(set(self.after_ids))) > 0:
            raise ValueError(
                "before_ids and after_ids must not contain the same IDs"
            )
        if len(self.before_ids) == 0:
            raise ValueError("before_ids must not be empty")
        if len(self.after_ids) == 0:
            raise ValueError("after_ids must not be empty")
        return self
