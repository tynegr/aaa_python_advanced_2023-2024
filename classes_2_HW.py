import json
import keyword
from typing import Dict, Union


class ColorfulMixin:
    colors = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'purple': 35,
        'cyan': 36,
        'white': 37,
    }

    def make_color(self, color: str = 'yellow') -> str:
        """
        Возвращает строковое представление объекта с цветным форматированием.

        Параметры:
        - color (str): Цвет для форматирования. По умолчанию 'yellow'.

        Возвращает:
        str: Цветное строковое представление.
        """
        return f'\033[1;{self.colors[color]};40m{str(self)}\033[0m'


class RecursiveDict:
    def __init__(self, data: Dict[str, Union[Dict, str, int]]) -> None:
        """
        Инициализация объекта RecursiveDict.

        Параметры:
        - data (Dict): Словарь с данными для инициализации объекта.
        """
        for key, value in data.items():
            key = key + '_' if keyword.iskeyword(key) else key
            if isinstance(value, dict):
                setattr(self, key, RecursiveDict(value))
            else:
                setattr(self, key, value)

    def __getattr__(self, name: str) -> 'RecursiveDict':
        """
        Обработка доступа к неопределенным атрибутам.

        Параметры:
        - name (str): Имя атрибута.

        Возвращает:
        RecursiveDict: Пустой экземпляр RecursiveDict.
        """
        return RecursiveDict({})


class Advert(ColorfulMixin):
    def __init__(self, data: Dict[str, Union[Dict, str, int]]) -> None:
        """
        Инициализация объекта Advert.

        Параметры:
        - data (Dict): Словарь с данными для инициализации объекта.

        Исключения:
        ValueError: Если отсутствует атрибут 'title'.
        """
        if 'title' not in data:
            raise ValueError('Атрибут title обязательный')

        if 'price' in data:
            price = data['price']
            self._validate_price(price)
        else:
            price = 0

        for key, value in data.items():
            key = key + '_' if keyword.iskeyword(key) else key
            if key == 'price':
                setattr(self, 'price', price)
            elif isinstance(value, dict):
                setattr(self, key, RecursiveDict(value))
            else:
                setattr(self, key, value)

    @property
    def price(self) -> int:
        """
        Получение значения атрибута price.

        Возвращает:
        int: Значение price.
        """
        return getattr(self, '_price', 0)

    @price.setter
    def price(self, new_price: int) -> None:
        """
        Установка значения атрибута price.

        Параметры:
        - new_price (int): Новое значение price.

        Исключения:
        ValueError: Если новое значение меньше 0.
        """
        self._validate_price(new_price)
        setattr(self, '_price', new_price)

    def _validate_price(self, price: int) -> None:
        """
        Проверка, что price не меньше 0.

        Параметры:
        - price (int): Проверяемое значение price.

        Исключения:
        ValueError: Если price меньше 0.
        """
        if price < 0:
            raise ValueError('должно быть >= 0')

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Advert.

        Возвращает:
        str: Строковое представление.
        """
        attributes = []
        for key in ['price', 'title']:
            if hasattr(self, key):
                attributes.append(f'{key}: {getattr(self, key)}')
        return ' | '.join(attributes)


# создаем экземпляр класса Advert из JSON
lesson_str = """{
"title": "python",
"price": 0,
"location": {
"address": "город Москва, Лесная, 7",
"metro_stations": ["Белорусская"]
}
}"""
lesson = json.loads(lesson_str)
lesson_ad = Advert(lesson)
# обращаемся к атрибуту location.address
print(lesson_ad.location.address)

# создаем экземпляр класса Advert из JSON
dog_str = """{
"title": "Вельш-корги",
"price": 1000,
"class": "dogs"
}"""
dog = json.loads(dog_str)
dog_ad = Advert(dog)
# обращаемся к атрибуту `dog_ad.class_` вместо `dog_ad.class`
print(dog_ad.class_)

lesson_str = '{"title": "python"}'
lesson = json.loads(lesson_str)
lesson_ad = Advert(lesson)
print(lesson_ad.price)

iphone_ad = Advert({'title': 'iPhone X', 'price': 100})
print(iphone_ad)

print(dog_ad.make_color())
