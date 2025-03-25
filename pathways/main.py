"""Generate different pathways of the book, as determined by profiles.yml."""

from argparse import ArgumentParser
from pathlib import Path
from shutil import which
from subprocess import run

from yaml import safe_dump, safe_load

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

    if clargs.build:
        jupyter_book_executable = which("jupyter-book")
        if not jupyter_book_executable:
            msg = (
                "Unable to find jupyter-book executable."
                " This is required to build the book."
            )
            raise FileNotFoundError(msg)

        run(  # noqa:S603
            [jupyter_book_executable, "build", clargs.book_path],
            check=True,
        )


def get_config_and_profiles(book_path):
    """Get config and pathways from myst.yml and profiles.yml respectively."""

    with open(book_path / "myst.yml", encoding="utf-8") as f:
        config = safe_load(f)

    with open(book_path / "profiles.yml", encoding="utf-8") as f:
        profiles = safe_load(f)

    return config, profiles


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
    config, profiles = get_config_and_profiles(book_path)
    toc = config.get("project").get("toc")

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
    ammend_toc(book_path, config)

    print("Finished adding pathways.")  # noqa: T201


def ammend_toc(book_path, config):
    toc = config.get("project").get("toc")
    toc.insert(
        1,
        {
            "title": "Pathways",
            "children": [
                {"pattern": "pathways/*.md"},
            ],
        },
    )

    with open(book_path / "myst.yml", "w") as f:
        safe_dump(config, f)


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

            elif key == "children":
                sub_components = mask_parts(value, whitelist)
                if sub_components:
                    new_component[key] = sub_components

        if new_component:
            # Add other entries, like "title": "my title"
            for key, value in component.items():
                if key not in ("file", "children"):
                    new_component[key] = value

            new_components.append(new_component)

    return new_components


def generate_toc(toc, profile):
    """Generate a new ToC for each profile."""
    return mask_parts(toc, profile["files"])
