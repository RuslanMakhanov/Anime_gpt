from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton)


def test_back():
    """
    Функция для тестовой кнопки назад
    """
    back_button_test = [[KeyboardButton(text="Назад")]]
    t_b = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=back_button_test)
    return t_b


def menu_generator(button_list, back_b=False):
    back_button = KeyboardButton(text="Назад")
    buttons = [[KeyboardButton(text=button)] for button in button_list]
    if back_b is not False:
        buttons.append([back_button])
    menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return menu


main_menu_list = ["Настройки", "Дебаг Функции", "Игры"]

main_menu_actions = {
    main_menu_list[0]: ("settings", "Меню настроек:", test_back()),
    main_menu_list[1]: ("debug", "Дебаг меню:", test_back()),
    main_menu_list[2]: ("games", "Игры:", test_back()),
}

main_menu_1 = menu_generator(main_menu_list)
