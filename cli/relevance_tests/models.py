from typing import ClassVar, List, Optional

import pytest
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
    known_failure: bool = Field(
        description=(
            "If True, the test is expected to fail. If False, the test is "
            "expected to pass."
        ),
        default=False,
    )

    def __init__(self, **data):
        # if an id hasn't been set, use the search terms
        if "id" not in data:
            data["id"] = data["search_terms"]
        super().__init__(**data)

    @property
    def param(self):
        """Return the test case as a pytest parameter"""
        return pytest.param(
            self,
            id=self.id,
            marks=[pytest.mark.xfail] if self.known_failure else [],
        )


class PrecisionTestCase(TestCase):
    expected_ids: List[str] = Field(
        description=(
            "The IDs which should be returned first by the search. Unless "
            "strict is set to True, these results can appear in any order, "
            "as long as they make up the first results."
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
        super().__init__(**data)

    @model_validator(mode="after")
    def check_expected_ids(self):
        if len(self.expected_ids) == 0:
            raise ValueError("expected_ids must not be empty")
        if len(self.expected_ids) != len(set(self.expected_ids)):
            raise ValueError("expected_ids must be unique")
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
