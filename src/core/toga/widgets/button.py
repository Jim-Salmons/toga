from toga.handlers import wrapped_handler

from .base import Widget


class Button(Widget):
    """A clickable button widget.

    Args:
        label (str): Text to be shown on the button.
        id (str): An identifier for this widget.
        key_equivalent (str): An optional shortcut key to 'press' the button.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        on_press (:obj:`callable`): Function to execute when pressed.
        enabled (bool): Whether or not interaction with the button is possible,
            defaults to `True`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not
            needed)
    """

    def __init__(
            self, label, key_equivalent='', id=None, style=None, on_press=None,
            enabled=True, factory=None
    ):
        super().__init__(id=id, style=style, enabled=enabled, factory=factory)

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        # Set all the properties
        self.label = label
        self.key_equivalent = key_equivalent
        self.on_press = on_press
        self.enabled = enabled

    @property
    def label(self):
        """
        Returns:
            The button label as a ``str``
        """
        return self._label

    @label.setter
    def label(self, value):
        if value is None:
            self._label = ''
        else:
            self._label = str(value)
        self._impl.set_label(value)
        self._impl.rehint()

    @property
    def key_equivalent(self):
        """	Setting the key_equivalent creates a shortcut key for the button.
                On macOS, if set to '\r' the button will be activated when the 
                user presses the return key and will set the Button as the
                default for its window or dialog as indicated by the Button's
                background color highlight. Not yet tested on other platforms.

        Returns:
            The button key_equivalent as a ``str``.
        """
        return self._key_equivalent

    @key_equivalent.setter
    def key_equivalent(self, value):
        if value is None:
            self._key_equivalent = ''
        else:
            self._key_equivalent = str(value)
        self._impl.set_key_equivalent(value)

    @property
    def on_press(self):
        """The handler to invoke when the button is pressed.

        Returns:
            The function ``callable`` that is called on button press.
        """
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        """Set the handler to invoke when the button is pressed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the button is pressed.
        """
        self._on_press = wrapped_handler(self, handler)
        self._impl.set_on_press(self._on_press)
