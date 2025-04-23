from assets import load_fonts

# fonts
fonts = load_fonts()

font_26 = fonts["font_26"]
font_30 = fonts["font_30"]
font_40 = fonts["font_40"]
font_50 = fonts["font_50"]

def load_menu_static_titles():
    """Loads all menu static title needed by the game."""
    title_main_menu_text = font_50.render("MENU", True, (255, 255, 255))
    title_main_menu_rect = title_main_menu_text.get_rect(center=(640, 150))

    title_params_menu_text = font_40.render("PARAMS", True, (255, 255, 255))
    title_params_menu_rect = title_params_menu_text.get_rect(center=(640, 150))

    title_controls_menu_text = font_30.render("CONTROLS", True, (255, 255, 255))
    title_controls_menu_rect = title_controls_menu_text.get_rect(center=(640, 150))

    title_music_menu_text = font_40.render("MUSIC", True, (255, 255, 255))
    title_music_menu_rect = title_music_menu_text.get_rect(center=(640, 150))

    title_pause_menu_text = font_40.render("PAUSE", True, (255, 255, 255))
    title_pause_menu_rect = title_pause_menu_text.get_rect(center=(640, 150))

    title_game_over_menu_text = font_30.render("GAME OVER", True, (255, 255, 255))
    title_game_over_menu_rect = title_game_over_menu_text.get_rect(center=(640, 150))

    number_version_main_menu_text = font_26.render("v.2", True, (0, 0, 0))
    number_version_main_menu_rect = number_version_main_menu_text.get_rect(center=(640, 630))

    jump_title_controls_menu_text = font_26.render("Jump", True, (116, 160, 80))  # green
    jump_title_controls_menu_rect = jump_title_controls_menu_text.get_rect(center=(640, 290))

    jump_keys_controls_menu_text = font_26.render("up & space", True, (0, 0, 0))
    jump_keys_controls_menu_rect = jump_keys_controls_menu_text.get_rect(center=(640, 330))

    pause_title_controls_menu_text = font_26.render("Pause", True, (116, 160, 80))  # green
    pause_title_controls_menu_rect = pause_title_controls_menu_text.get_rect(center=(640, 410))

    pause_keys_controls_menu_text = font_26.render("escape", True, (0, 0, 0))
    pause_keys_controls_menu_rect = pause_keys_controls_menu_text.get_rect(center=(640, 450))

    return {
        "title_main_menu_text": title_main_menu_text,
        "title_main_menu_rect": title_main_menu_rect,
        "title_params_menu_text": title_params_menu_text,
        "title_params_menu_rect": title_params_menu_rect,
        "title_controls_menu_text": title_controls_menu_text,
        "title_controls_menu_rect": title_controls_menu_rect,
        "title_music_menu_text": title_music_menu_text,
        "title_music_menu_rect": title_music_menu_rect,
        "title_pause_menu_text": title_pause_menu_text,
        "title_pause_menu_rect": title_pause_menu_rect,
        "title_game_over_menu_text": title_game_over_menu_text,
        "title_game_over_menu_rect": title_game_over_menu_rect,
        "number_version_main_menu_text": number_version_main_menu_text,
        "number_version_main_menu_rect": number_version_main_menu_rect,
        "jump_title_controls_menu_text": jump_title_controls_menu_text,
        "jump_title_controls_menu_rect": jump_title_controls_menu_rect,
        "jump_keys_controls_menu_text": jump_keys_controls_menu_text,
        "jump_keys_controls_menu_rect": jump_keys_controls_menu_rect,
        "pause_title_controls_menu_text": pause_title_controls_menu_text,
        "pause_title_controls_menu_rect": pause_title_controls_menu_rect,
        "pause_keys_controls_menu_text": pause_keys_controls_menu_text,
        "pause_keys_controls_menu_rect": pause_keys_controls_menu_rect,
    }



def update_menu_music_texts(music_on):
    """Load and Update the style (color) of the ON / OFF text in the music params menu of the game."""
    # MUSIC ON / OFF TEXT FOR MUSIC PARAMS MENU + COLOUR MANAGEMENT
    music_on_text = font_26.render("ON", True, (116, 160, 80) if music_on else (0, 0, 0))
    music_off_text = font_26.render("OFF", True, (116, 160, 80) if not music_on else (0, 0, 0))

    music_on_rect = music_on_text.get_rect(center=(570, 430))
    music_off_rect = music_off_text.get_rect(center=(710, 430))

    return music_on_text, music_on_rect, music_off_text, music_off_rect