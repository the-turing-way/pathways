"""Create Cards for the Welcome page."""

HEADING_TITLE = "## Different Pathways"


def insert_into_md(path_welcome_md, heading_title, panel_string):
    """Take the markdown file, add the panels, and save the markdown file."""

    md_text = get_text_from_md(path_welcome_md)
    new_md_text = insert_text_after_string(md_text, heading_title, panel_string)
    overwrite_md(new_md_text, path_welcome_md)


def get_text_from_md(path_welcome_md):
    """Get the text from the markdown file."""
    with open(path_welcome_md, encoding="utf-8") as md:
        md_text = md.read()
    return md_text


def insert_text_after_string(md_text, heading_title, panel_string):
    """Look for a heading and insert string after that heading."""
    md_text = md_text.replace(heading_title, heading_title + "\n" + panel_string)
    return md_text


def overwrite_md(new_md_text, path_welcome_md):
    """Overwrite the markdown file with new added panel text."""
    with open(path_welcome_md, "w", encoding="utf-8") as txt:
        txt.write(new_md_text)


def create_bullet_string(file_list):
    """From the list of files for a single toc, create a bullet point string."""
    toc_string = ""
    max_bullets = 3

    for f in file_list[:max_bullets]:
        toc_string += f"- [](./{f})\n"

    if len(file_list) > max_bullets:
        toc_string += "\nAnd more…\n"

    return toc_string


def create_card(profile_name, file_list, landing_name):
    """Create a single card."""
    card_start = f":::{{card}} {profile_name}"
    link = f":link: pathways/{landing_name}"
    card_end = ":::"

    return "\n".join(
        [
            card_start,
            link,
            create_bullet_string(file_list),
            card_end,
        ]
    )


def create_panel(list_cards):
    """Create the full panel, with all cards."""

    panel_start = "::::{grid} 1 1 2 2\n"
    panel_end = "\n::::\n"

    panel_string = panel_start
    panel_string += "\n".join(list_cards)
    panel_string += panel_end
    return panel_string
