"""Tag suggestion example

Tag suggestions complete an incomplete tag the same way the web UI's prompt
box does. They are free — no Anlas is consumed.
"""

from dotenv import load_dotenv

from novelai import NovelAI
from novelai.types import SuggestTagsParams

load_dotenv()


def main():
    # API key is loaded from environment variable NOVELAI_API_KEY
    with NovelAI() as client:
        # English tag completion
        for suggestion in client.image.suggest_tags(SuggestTagsParams(prompt="blue"))[
            :5
        ]:
            print(f"{suggestion.tag} (count={suggestion.count})")

        # Japanese query -> English tags to use in the prompt
        for suggestion in client.image.suggest_tags_jp(SuggestTagsParams(prompt="青"))[
            :5
        ]:
            print(f"{suggestion.jp_tag} -> {suggestion.en_tag}")


if __name__ == "__main__":
    main()
