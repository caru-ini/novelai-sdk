"""User account example

This example demonstrates how to fetch the subscription state, the actual
Anlas balance, and the Opus usage limit of your account.
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

        # Opus usage limit: the allowance that free V5 generations draw from.
        # The web UI shows it as "N% of Opus Generations remaining".
        # client.user.get_opus_usage() returns the same object on its own.
        usage = sub.usage
        if usage is not None:
            print(f"Opus generations remaining: {usage.percent}%")
            if usage.purchased_percent > 0:
                print(f"  extra usage: +{usage.purchased_percent}%")
            if usage.is_negative:
                print("  used up: V5 generations cost Anlas until it refills")

        # Shortcut when only the balance is needed
        print(f"Balance via get_anlas(): {client.user.get_anlas()}")


if __name__ == "__main__":
    main()
