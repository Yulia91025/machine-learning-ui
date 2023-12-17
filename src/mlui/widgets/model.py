import streamlit as st
import streamlit_extras.capture as capture

import mlui.classes.data as data
import mlui.classes.model as model


def model_info_ui(model: model.Model) -> None:
    """Generate the UI for displaying model information.

    Parameters
    ----------
    model : Model
        Model object.
    """
    st.header("Model Info")

    task = st.session_state.get("task")
    built = model.built
    input_configured = model.input_configured
    output_configured = model.output_configured
    compiled = model.compiled

    if not built:
        st.info("The model is not uploaded/created.", icon="💡")
        return

    if input_configured:
        st.success("The model's input layers are configured.", icon="✅")
    else:
        st.info("The model's input layers are not configured.", icon="💡")

    if task != "Predict" and output_configured:
        st.success("The model's output layers are configured.", icon="✅")
    elif task != "Predict" and not output_configured:
        st.info("The model's output layers are not configured.", icon="💡")

    if compiled:
        st.success("The model is compiled.", icon="✅")
    else:
        st.info("The model is not compiled.", icon="💡")


def summary_ui(model: model.Model) -> None:
    """Generate the UI for displaying the model's summary.

    Parameters
    ----------
    model : Model
        Model object.
    """
    st.header("Summary")

    with st.expander("Summary"):
        with capture.stdout(st.empty().code):
            model.summary


def graph_ui(model: model.Model) -> None:
    """Generate the UI for downloading the model's graph.

    Parameters
    ----------
    model : Model
        Model object.
    """
    st.header("Graph")

    graph = model.graph

    st.download_button("Download Graph", graph, "model_graph.pdf")


def download_model_ui(model: model.Model) -> None:
    """Generate the UI for downloading the model.

    Parameters
    ----------
    model : Model
        Model object.
    """
    st.header("Download Model")

    model_as_bytes = model.as_bytes

    st.download_button("Download Model", model_as_bytes, "model.h5")


def reset_model_ui(data: data.Data, model: model.Model) -> None:
    """Generate the UI for resetting the model.

    Parameters
    ----------
    data : Data
        Data object.
    model : Model
        Model object.
    """
    st.header("Reset Model")

    reset_model_btn = st.button("Reset Model")

    if reset_model_btn:
        model.reset_state()
        data.update_state()
        st.rerun()
