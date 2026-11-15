"""User account type definitions for NovelAI API.

These models mirror the response of ``GET /user/subscription``, which reports
the account tier, perks, remaining Anlas (NovelAI's "training steps"), and the
Opus usage limit. Field aliases match the camelCase JSON returned by the API,
while the Python attributes use snake_case.
"""

from __future__ import annotations

from math import floor
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

_OPUS_TIER: int = 3

_TIER_NAMES: dict[int, str] = {0: "Paper", 1: "Tablet", 2: "Scroll", 3: "Opus"}

# Figures the web UI uses to present the Opus usage limit.
_USAGE_FULL_PERCENT: int = 100
_USAGE_IMAGES_PER_PERCENT: float = 17.3
_SECONDS_PER_DAY: int = 86_400


def _round_half_up(value: float) -> int:
    """Round like JavaScript's ``Math.round``, which the web UI uses.

    Python's ``round()`` rounds ties to even, so 5% would read as 86 images
    where the web UI shows 87.
    """
    return floor(value + 0.5)


class TrainingStepsLeft(BaseModel):
    """Remaining Anlas (module training steps), split by source."""

    fixed_training_steps_left: int = Field(
        alias="fixedTrainingStepsLeft",
        description="Anlas granted by the subscription, reset every month",
    )
    purchased_training_steps: int = Field(
        alias="purchasedTrainingSteps",
        description="Anlas bought separately, which do not expire",
    )

    model_config = ConfigDict(populate_by_name=True)

    @property
    def total(self) -> int:
        """Total Anlas available (subscription + purchased)."""
        return self.fixed_training_steps_left + self.purchased_training_steps


class UnlimitedImageGenerationLimit(BaseModel):
    """Free image-generation allowance for one resolution bracket."""

    resolution: int = Field(
        description="Maximum pixel count (width * height) the allowance covers"
    )
    max_prompts: int = Field(
        alias="maxPrompts",
        description="Number of images per generation that are free",
    )

    model_config = ConfigDict(populate_by_name=True)


class SubscriptionPerks(BaseModel):
    """Feature limits granted by the current subscription tier."""

    max_priority_actions: int = Field(default=0, alias="maxPriorityActions")
    start_priority: int = Field(default=0, alias="startPriority")
    context_tokens: int = Field(default=0, alias="contextTokens")
    unlimited_max_priority: bool = Field(default=False, alias="unlimitedMaxPriority")
    module_training_steps: int = Field(default=0, alias="moduleTrainingSteps")
    voice_generation: bool = Field(default=False, alias="voiceGeneration")
    image_generation: bool = Field(default=False, alias="imageGeneration")
    unlimited_image_generation: bool = Field(
        default=False,
        alias="unlimitedImageGeneration",
        description="Whether free image generation (the Opus perk) is granted",
    )
    unlimited_image_generation_limits: list[UnlimitedImageGenerationLimit] = Field(
        default_factory=list[UnlimitedImageGenerationLimit],
        alias="unlimitedImageGenerationLimits",
    )

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class OpusUsage(BaseModel):
    """Opus usage limit, the ``usage`` object of ``GET /user/subscription``.

    On Opus, free NovelAI Diffusion V5 generations draw from an allowance that
    refills by itself over time. The web UI shows it as "N% of Opus Generations
    remaining"; once it is used up, those generations cost Anlas until it
    refills.

    NovelAI does not document this object. The derived properties follow what
    the web UI computes from it.
    """

    percent: int | float = Field(
        description="Allowance left, as a percentage of a full allowance"
    )
    purchased_percent: int | float = Field(
        default=0,
        alias="purchasedPercent",
        description="Extra usage added by Opus Usage Boosts, in percent",
    )
    is_negative: bool = Field(
        default=False,
        alias="isNegative",
        description="Whether the allowance is used up, so V5 generations cost Anlas",
    )
    time_until_next_percent: int | float = Field(
        default=0,
        alias="timeUntilNextPercent",
        description="Seconds the allowance takes to refill by one percent",
    )

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    @property
    def remaining_percent(self) -> float:
        """Percentage left as the web UI shows it (``0`` once used up)."""
        return 0 if self.is_negative else max(0, self.percent)

    @property
    def refill_percent_per_day(self) -> float:
        """Percent regained per day, to one decimal place.

        ``0`` while the allowance is full, because it stops refilling at 100%,
        and when the API reports no refill rate.
        """
        if (
            self.time_until_next_percent <= 0
            or self.remaining_percent >= _USAGE_FULL_PERCENT
        ):
            return 0
        return _round_half_up(_SECONDS_PER_DAY / self.time_until_next_percent * 10) / 10

    @property
    def estimated_images(self) -> int:
        """Rough number of images left, purchased extra usage included.

        The web UI's estimate: about 17.3 images per percent.
        """
        return _round_half_up(
            _USAGE_IMAGES_PER_PERCENT
            * (self.remaining_percent + max(0, self.purchased_percent))
        )


class Subscription(BaseModel):
    """Account subscription state from ``GET /user/subscription``."""

    tier: int = Field(
        description="Subscription tier (0=Paper, 1=Tablet, 2=Scroll, 3=Opus)"
    )
    active: bool = Field(description="Whether the subscription is currently active")
    expires_at: int = Field(
        alias="expiresAt",
        description="Subscription expiry as a Unix timestamp (seconds)",
    )
    perks: SubscriptionPerks
    training_steps_left: TrainingStepsLeft = Field(alias="trainingStepsLeft")
    account_type: int | None = Field(default=None, alias="accountType")
    is_grace_period: bool = Field(default=False, alias="isGracePeriod")
    payment_processor_data: dict[str, Any] | None = Field(
        default=None, alias="paymentProcessorData"
    )
    usage: OpusUsage | None = Field(
        default=None,
        description="Opus usage limit, or None when the API reports none. "
        "Only meaningful on an active Opus subscription",
    )

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    @property
    def anlas(self) -> int:
        """Current total Anlas balance (subscription + purchased)."""
        return self.training_steps_left.total

    @property
    def tier_name(self) -> str:
        """Subscription tier name (e.g. ``"Opus"``)."""
        return _TIER_NAMES.get(self.tier, f"Unknown ({self.tier})")

    @property
    def is_opus(self) -> bool:
        """Whether the account is on the Opus tier.

        Pairs with ``calculate_anlas(is_opus=...)`` to apply the free
        image-generation discount. ``perks.unlimited_image_generation``
        reports the same perk independently of the tier number.
        """
        return self.tier == _OPUS_TIER


__all__ = [
    "OpusUsage",
    "Subscription",
    "SubscriptionPerks",
    "TrainingStepsLeft",
    "UnlimitedImageGenerationLimit",
]
