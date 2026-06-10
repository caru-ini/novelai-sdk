"""User account type definitions for NovelAI API.

These models mirror the response of ``GET /user/subscription``, which reports
the account tier, perks, and remaining Anlas (NovelAI's "training steps").
Field aliases match the camelCase JSON returned by the API, while the Python
attributes use snake_case.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

_OPUS_TIER: int = 3

_TIER_NAMES: dict[int, str] = {0: "Paper", 1: "Tablet", 2: "Scroll", 3: "Opus"}


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
    "Subscription",
    "SubscriptionPerks",
    "TrainingStepsLeft",
    "UnlimitedImageGenerationLimit",
]
