class Color:
    """
    A class representing a color with RGB values.

    Attributes:
    - red (int): The red component of the color (0 to 255).
    - green (int): The green component of the color (0 to 255).
    - blue (int): The blue component of the color (0 to 255).

    Methods:
    - __init__: Initializes a Color object with given RGB values.
    - __repr__: Returns a string representation
    of the color in ANSI escape code format.
    - __eq__: Checks if two Color objects are equal.
    - __add__: Adds two Color objects.
    - __hash__: Returns the hash value of the Color object.
    - __mul__: Multiplies the color by a scalar value between 0 and 1.
    - __rmul__: Allows multiplication in reverse order.

    """

    def __init__(self, red: int, green: int, blue: int) -> None:
        """
        Initializes a Color object with given RGB values.

        Args:
        - red (int): The red component of the color (0 to 255).
        - green (int): The green component of the color (0 to 255).
        - blue (int): The blue component of the color (0 to 255).

        Returns:
        None
        """
        self._red = self._check(red)
        self._green = self._check(green)
        self._blue = self._check(blue)

    @property
    def red(self) -> int:
        """
        Getter for the red component of the color.

        Returns:
        int: The red component.
        """
        return self._red

    @red.setter
    def red(self, value: int) -> None:
        """
        Setter for the red component of the color.

        Args:
        - value (int): The new value for the red component.

        Returns:
        None
        """
        self._red = self._check(value)

    @property
    def green(self) -> int:
        """
        Getter for the green component of the color.

        Returns:
        int: The green component.
        """
        return self._green

    @green.setter
    def green(self, value: int) -> None:
        """
        Setter for the green component of the color.

        Args:
        - value (int): The new value for the green component.

        Returns:
        None
        """
        self._green = self._check(value)

    @property
    def blue(self) -> int:
        """
        Getter for the blue component of the color.

        Returns:
        int: The blue component.
        """
        return self._blue

    @blue.setter
    def blue(self, value: int) -> None:
        """
        Setter for the blue component of the color.

        Args:
        - value (int): The new value for the blue component.

        Returns:
        None
        """
        self._blue = self._check(value)

    def _check(self, value: int) -> int:
        """
        Private method to check if the value is within
        the valid range (0 to 255).

        Args:
        - value (int): The value to be checked.

        Returns:
        int: The checked and converted value.
        """
        if not (0 <= value <= 255):
            value = 0
        return int(value)

    def __repr__(self) -> str:
        """
        Returns a string representation of the
        color in ANSI escape code format.

        Returns:
        str: The string representation of the color.
        """
        end = '\033[0'
        start = '\033[1;38;2'
        mod = 'm'
        return f'{start};' \
               f'{self._red};{self._green};{self._blue}{mod}●{end}{mod}'

    def __eq__(self, other) -> bool:
        """
        Checks if two Color objects are equal.

        Args:
        - other (Color): The other Color object.

        Returns:
        bool: True if equal, False otherwise.
        """
        return self.red == other.red \
            and self.green == other.green \
            and self.blue == other.blue

    def __add__(self, other) -> 'Color':
        """
        Adds two Color objects.

        Args:
        - other (Color): The other Color object.

        Returns:
        Color: The resulting Color object.
        """
        if not isinstance(other, Color):
            raise ValueError()
        else:
            return Color(self.red + other.red,
                         self.green + other.green, self.blue + other.blue)

    def __hash__(self) -> int:
        """
        Returns the hash value of the Color object.

        Returns:
        int: The hash value.
        """
        return hash((self.red, self.green, self.blue))

    def __mul__(self, other):
        """
        Multiplies the color by a scalar value between 0 and 1.

        Args:
        - other (float): The scalar value.

        Returns:
        Color: The resulting Color object.
        """
        c = other
        if c < 0 or c > 1:
            raise ValueError()
        cl = -256 * (1 - c)
        f = 259 * (cl + 255) / (255 * (259 - cl))
        new_red = f * (self.red - 128) + 128
        new_green = f * (self.green - 128) + 128
        new_blue = f * (self.blue - 128) + 128
        return Color(new_red, new_green, new_blue)

    def __rmul__(self, other):
        """
        Allows multiplication in reverse order.

        Args:
        - other (float): The scalar value.

        Returns:
        Color: The resulting Color object.
        """
        c = other
        if c < 0 or c > 1:
            raise ValueError()
        cl = -256 * (1 - c)
        f = 259 * (cl + 255) / (255 * (259 - cl))
        new_red = f * (self.red - 128) + 128
        new_green = f * (self.green - 128) + 128
        new_blue = f * (self.blue - 128) + 128
        return Color(new_red, new_green, new_blue)


#1
END = '\033[0'
START = '\033[1;38;2'
MOD = 'm'
red_level = 100
green_level = 149
blue_level = 237
print("1-ое:", f'{START};{red_level};{green_level};'
               f'{blue_level}{MOD}●{END}{MOD}')


#2
Red = Color(255, 0, 0)
Green = Color(0, 255, 0)
print("2-ое:", Red == Green)
print("2-ое:", Red == Color(255, 0, 0))


#3
Red = Color(255, 0, 0)
Green = Color(0, 255, 0)
print("3-ое:", Red + Green)


#4
orange1 = Color(255, 165, 0)
Red = Color(255, 0, 0)
Green = Color(0, 255, 0)
orange2 = Color(255, 165, 0)
color_list = [orange1, Red, Green, orange2]
print("4-ое:", set(color_list))


#5
Red = Color(255, 0, 0)
print("5-ое:", 0.5 * Red)
