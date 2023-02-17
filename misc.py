import json


def save_text():
    profile_ru = """
Ваш профиль

💰 Ваш баланс: {} USD
☑️ Ваше кол-во покупок: {}
🤑 Ваша сумма покупок: {}
🪪 Ваш ID: {}
"""
    parsers_ru = "Parsers WORK! 🚀"
    faq_ru = """
Добрый день, это FAQ
"""
    language_ru = "Язык в процессе"
    terms_of_use_ru = """
Правила использования

Плати
"""
    support_ru = """
Если вам нужно помощь с сервисом, то свяжитесь с саппортом: @admin
"""
    about_service_ru = """
Лучший сервис на рынке по парсингу 
Конкуренты лохи
А мы нет .
"""

    top_up_balance_ru = """
Пополнить баланс
"""

    profile_en = """
Ваш профиль

💰 Ваш баланс: {} USD
☑️ Ваше кол-во покупок: {}
🤑 Ваша сумма покупок: {}
🪪 Ваш ID: {}
"""
    parsers_en = "Parsers WORK! 🚀"
    faq_en = """
Добрый день, это FAQ
"""
    language_en = "Язык в процессе"
    terms_of_use_en = """
Правила использования

Плати
"""
    support_en = """
Если вам нужно помощь с сервисом, то свяжитесь с саппортом: @admin
"""
    about_service_en = """
Лучший сервис на рынке по парсингу
Конкуренты лохи
А мы нет .
"""

    top_up_balance_en = """
Top up balance    
"""

    data = {
        "russian": {
            "profile": profile_ru,
            "parsers": parsers_ru,
            "faq": faq_ru,
            "language": language_ru,
            "terms_of_use": terms_of_use_ru,
            "support": support_ru,
            "about_service": about_service_ru,
            "top_up_balance": top_up_balance_ru
        },
        "english": {
            "profile": profile_en,
            "parsers": parsers_en,
            "faq": faq_en,
            "language": language_en,
            "terms_of_use": terms_of_use_en,
            "support": support_en,
            "about_service": about_service_en,
            "top_up_balance": top_up_balance_en,
        }
    }
    
    with open("text.json", "w") as f:
        json.dump(data, f)
