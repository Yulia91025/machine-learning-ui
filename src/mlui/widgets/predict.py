import streamlit as st

import mlui.classes.data as data
import mlui.classes.errors as errors
import mlui.classes.model as model


def make_predictions_ui(data: data.Data, model: model.UploadedModel) -> None:
    """Generate the UI for making the model predictions.

    Parameters
    ----------
    data : Data
        Data object.
    model : Model
        Model object.
    """
    st.header("Make Predictions")

    batch_size = st.number_input(
        "Batch size:", min_value=1, max_value=1024, value=32, step=1
    )
    make_predictions_btn = st.button("Make Predictions")

    if make_predictions_btn:
        with st.status("Predictions"):
            try:
                df = data.dataframe
                predictions = model.predict(df, int(batch_size))
                outputs = model.outputs

                for position, output in enumerate(outputs):
                    st.subheader(output)
                    st.dataframe(predictions[position])

                st.toast("Predictions are completed!", icon="✅")
            except errors.ModelError as error:
                st.toast(error, icon="❌")
