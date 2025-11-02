"""Sampler constants"""

from __future__ import annotations

from typing import Literal

Sampler = Literal[
    "k_euler",
    "k_euler_ancestral",
    "k_dpm_2",
    "k_dpm_2_ancestral",
    "k_dpmpp_2m",
    "k_dpmpp_2s_ancestral",
    "k_dpmpp_sde",
    "ddim",
]

K_EULER: Sampler = "k_euler"
K_EULER_ANCESTRAL: Sampler = "k_euler_ancestral"
K_DPM_2: Sampler = "k_dpm_2"
K_DPM_2_ANCESTRAL: Sampler = "k_dpm_2_ancestral"
K_DPM_FAST: Sampler = "k_dpmpp_2m"
K_DPM_ADAPTIVE: Sampler = "k_dpmpp_2s_ancestral"
K_DPM_SDE: Sampler = "k_dpmpp_sde"
DDIM: Sampler = "ddim"
