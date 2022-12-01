from enum import Enum


class Watch(str, Enum):
    FILE = "_on_file_uploaded"
    MODEL = "_on_model_instantiated"
    LAYER_ADDED = "_on_layer_added"
    OUTPUTS_SET = "_on_outputs_set"
    OPTIMIZER_SELECTED = "_on_optimizer_selected"
    LOSSES_SELECTED = "_on_losses_selected"