page_header_style = {
    "coords": (0.5, 0.01),
    "anchor": "center",
    "font": ("Arial", 9),
}

page_title_style = {
    "pady": 10,
    "font": ("Arial", 35),
}

page_description_style = {
    "pady": 25,
    "font": ("Arial", 12),
}

page_description_separator_style = {
    "text": "_" * 70,
    "pady": 0,
    "font": ("Arial", 10),
}

page_question_style = {
    "pady": 25,
    "font": ("Arial", 15),
}

page_instructions_style = {
    "pady": 3,
    "font": ("Arial", 13),
}

_button_style = {
    "width": 2,
    "border": 0,
    "cursor": "hand2",
    "font": ("Arial", 50),
}

records_button_style = {
    **_button_style,
    "text": "📝",
    "fg": "ivory4",
    "activeforeground": "Gray20",
}

records_button_text_style = {
    "anchor": "center",
    "fg": "black",
    "font": ("Arial", 14),
}

about_button_style = {
    **_button_style,
    "text": "❀",
    "fg": "springGreen4",
    "activeforeground": "violetred4",
}

about_button_text_style = {
    "anchor": "center",
    "fg": "black",
    "font": ("Arial", 14),
}

exit_button_style = {
    **_button_style,
    "relief": "sunken",
    "fg": "Red3",
    "activeforeground": "black",
}

exit_button_text_style = {
    "text": "⥱",
    "anchor": "center",
    "font": ("Arial", 25),
}
