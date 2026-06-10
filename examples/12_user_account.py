"""User account example

This example demonstrates how to fetch the subscription state and the actual
Anlas balance of your account.
"""

from dotenv import load_dotenv

from novelai import NovelAI

load_dotenv()


def main():
    # API key is loaded from environment variable NOVELAI_API_KEY
    with NovelAI() as client:
        sub = client.user.get_subscription()

        print(f"Tier: {sub.tier_name} (tier {sub.tier})")
        print(f"Active: {sub.active}")
        print(f"Expires at: {sub.expires_at} (Unix seconds)")
        print(f"Anlas balance: {sub.anlas}")
        steps_left = sub.training_steps_left
        print(f"  from subscription: {steps_left.fixed_training_steps_left}")
        print(f"  purchased: {steps_left.purchased_training_steps}")
        print(f"Free image generation: {sub.perks.unlimited_image_generation}")

        # Shortcut when only the balance is needed
        print(f"Balance via get_anlas(): {client.user.get_anlas()}")


if __name__ == "__main__":
    main()
