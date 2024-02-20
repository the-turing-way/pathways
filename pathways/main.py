"""Generate different pathways of the book, as determined by profiles.yml."""

from argparse import ArgumentParser
from pathlib import Path
from shutil import which
from subprocess import run

from yaml import safe_load

from pathways import landing_page
from pathways.badge import generate_badge, insert_badges
from pathways.card import HEADING_TITLE, create_card, create_panel, insert_into_md


def main():
    """Parse arguments and call sub-commands as appropriate."""

    # Get the arguments passed in by the user
    parser = ArgumentParser(description="Build a Jupyter Book.")

    parser.add_argument(
        "book_path", type=Path, help="the path to the root of your Jupyter Book"
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Run jupyterbook build",
    )

    clargs = parser.parse_args()

    pathways(clargs.book_path)

    jupyter_book_executable = which("jupyter-book")
    if clargs.build:
        run(
            [jupyter_book_executable, "build", clargs.book_path],  # noqa:S603
            check=True,
        )


def get_toc_and_profiles(book_path):
    """Get the contents of _toc.yml and profiles.yml."""

    with open(book_path / "_toc.yml", encoding="utf-8") as f:
        toc = safe_load(f)

    with open(book_path / "profiles.yml", encoding="utf-8") as f:
        profiles = safe_load(f)

    return toc, profiles


def generate_card(profile: dict, landing_name):
    return create_card(profile["name"], profile["files"], landing_name=landing_name)


def generate_landing_page(profile, toc, landing_name, description):
    a_landing_page = landing_page.LandingPage(
        persona=profile, landing_name=landing_name, description=description
    )
    a_landing_page.gather_curated_links(toc)
    return a_landing_page


def insert_cards(welcome_path, cards):
    insert_into_md(welcome_path, HEADING_TITLE, create_panel(cards))


def insert_landing_pages(landing_pages):
    for lp in landing_pages:
        lp.write_content()


def generate_landing_name(profile_name):
    landing_name = profile_name.replace(" ", "-")
    landing_name = landing_name.lower()
    return landing_name


def pathways(book_path):
    """Add extra pathways to the book."""
    landing_page.LandingPage.book_path = book_path
    toc, profiles = get_toc_and_profiles(book_path)

    landing_pages = []
    badges = []
    cards = []

    for profile in profiles:
        landing_name = generate_landing_name(profile["name"])
        # Input profile is profile name + file list
        cards.append(generate_card(profile, landing_name))
        badges.append(generate_badge(profile["name"], profile["colour"], landing_name))
        landing_pages.append(
            generate_landing_page(
                profile["name"],
                generate_toc(toc, profile),
                landing_name,
                profile["description"],
            )
        )

    insert_cards(book_path / "index.md", cards)
    insert_landing_pages(landing_pages)
    insert_badges(book_path, badges, profiles)

    print("Finished adding pathways.")  # noqa: T201


def mask_parts(components, whitelist):
    """Makes a new components list, containing only whitelisted files.

    Args:
        components: An iterable of parts, chapters or sections.
        whitelist: An iterable of files to keep.

    Returns:
        A new list of parts, chapters or sections that omits files that aren't
        whitelisted and components that are now empty.
    """

    # Don't modify components as they may be needed by other profiles
    new_components = []

    # We could have a list of parts, chapters or sections
    for component in components:
        new_component = {}

        for key, value in component.items():
            if key == "file":
                if value in whitelist:
                    new_component["file"] = value

            elif key in ("parts", "chapters", "sections"):
                sub_components = mask_parts(value, whitelist)
                if sub_components:
                    new_component[key] = sub_components

        if new_component:
            # Add other entries, like "title": "my title"
            for key, value in component.items():
                if key not in ("file", "parts", "chapters", "sections"):
                    new_component[key] = value

            new_components.append(new_component)

    return new_components


def mask_toc(toc, whitelist):
    """Makes a new ToC, containing only whitelisted files.

    Args:
        toc: A Table of Contents dictionary.
        whitelist: An iterable of files to keep.

    Returns:
        A new Table of Contents that omits files that aren't whitelisted and
        components that are now empty.
    """
    masked_toc = mask_parts([toc], whitelist)
    return masked_toc[0]


def generate_toc(toc, profile):
    """Generate a new ToC for each profile."""
    return mask_toc(toc, profile["files"])
