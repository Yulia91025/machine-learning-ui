from abc import abstractmethod
from typing import Any, Protocol

import ipywidgets as iw
from Enums.Layers import layers
from IPython.display import display


class Manager(Protocol):
    """Protocol for model managers."""

    @property
    def model(self) -> Any:
        ...

    @abstractmethod
    def add_layer(
        self,
        layer_type: Any,
        instance: Any,
        connect_to: Any,
        output_handler: Any,
        **kwargs,
    ) -> None:
        ...


class ManageLayersWidget(iw.VBox):
    """Widget to add and pop model layers."""

    layer_type_dropdown = iw.Dropdown(
        options=list(layers),
        description="Choose layer type:",
        style={"description_width": "initial"},
    )
    layer_widget_output = iw.Output()
    connect_dropdown = iw.Dropdown(
        options=("",),
        description="Connect layer to:",
        style={"description_width": "initial"},
    )
    add_layer_button = iw.Button(description="Add Layer")
    layer_status = iw.Output()

    def __init__(self, manager: Manager, **kwargs) -> None:
        """Initialize the manage layers widget window."""
        self._manager = manager
        self._current_layer = layers[self.layer_type_dropdown.value]
        self._current_layer_widget = self._current_layer.widget(manager=self._manager)

        self.layer_widget_output.append_display_data(self._current_layer_widget)

        self.layer_type_dropdown.observe(
            self._on_layer_type_dropdown_value_change, names="value"
        )
        self.add_layer_button.on_click(self._on_add_layer_button_clicked)

        super().__init__(
            children=[
                self.layer_type_dropdown,
                self.layer_widget_output,
                self.connect_dropdown,
                self.add_layer_button,
                self.layer_status,
            ],
            **kwargs,
        )

    @layer_widget_output.capture(clear_output=True, wait=True)
    def _on_layer_type_dropdown_value_change(self, change: Any) -> None:
        self._current_layer = layers[change["new"]]
        self._current_layer_widget = self._current_layer.widget(manager=self._manager)
        display(self._current_layer_widget)

    def _on_add_layer_button_clicked(self, _) -> None:
        layer_type = self.layer_type_dropdown.value

        self._manager.add_layer(
            layer_type=layer_type,
            instance=self._current_layer.instance,
            connect_to=self.connect_dropdown.value,
            output_handler=self.layer_status,
            **self._current_layer_widget.params,
        )

        self.connect_dropdown.options = ("",) + tuple(self._manager.model.layers.keys())