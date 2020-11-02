# Copyright (C) 2020 Cancer Care Associates

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pymedphys._imports import pandas as pd
from pymedphys._imports import streamlit as st

import pymedphys
from pymedphys._gui.streamlit.mudensity import (
    _config,
    _deliveries,
    _exceptions,
    _utilities,
)
from pymedphys._utilities import patient as utl_patient


@st.cache
def read_trf(filepath):
    return pymedphys.read_trf(filepath)


def trf_input_method(patient_id="", key_namespace="", **_):
    indexed_trf_directory = get_indexed_trf_directory()

    patient_id = st.text_input(
        "Patient ID", patient_id, key=f"{key_namespace}_patient_id"
    )
    patient_id

    filepaths = list(indexed_trf_directory.glob(f"*/{patient_id}_*/*/*/*/*.trf"))

    raw_timestamps = ["_".join(path.parent.name.split("_")[0:2]) for path in filepaths]
    timestamps = list(
        pd.to_datetime(raw_timestamps, format="%Y-%m-%d_%H%M%S").astype(str)
    )

    timestamp_filepath_map = dict(zip(timestamps, filepaths))

    timestamps = sorted(timestamps, reverse=True)

    if len(timestamps) == 0:
        if patient_id != "":
            st.write(
                st_exceptions.NoRecordsFound(
                    f"No TRF log file found for patient ID {patient_id}"
                )
            )
        return {"patient_id": patient_id}

    if len(timestamps) == 1:
        default_timestamp = timestamps[0]
    else:
        default_timestamp = []

    selected_trf_deliveries = st.multiselect(
        "Select TRF delivery timestamp(s)",
        timestamps,
        default=default_timestamp,
        key=f"{key_namespace}_trf_deliveries",
    )

    if not selected_trf_deliveries:
        return {}

    """
    #### TRF filepath(s)
    """

    selected_filepaths = [
        timestamp_filepath_map[timestamp] for timestamp in selected_trf_deliveries
    ]
    [str(path.resolve()) for path in selected_filepaths]

    """
    #### Log file header(s)
    """

    headers = []
    tables = []
    for path in selected_filepaths:
        header, table = read_trf(path)
        headers.append(header)
        tables.append(table)

    headers = pd.concat(headers)
    headers.reset_index(inplace=True)
    headers.drop("index", axis=1, inplace=True)

    headers

    """
    #### Corresponding Mosaiq SQL Details
    """

    mosaiq_details = get_logfile_mosaiq_info(headers)
    mosaiq_details = mosaiq_details.drop("beam_completed", axis=1)

    mosaiq_details

    patient_names = set()
    for _, row in mosaiq_details.iterrows():
        row
        patient_name = utl_patient.convert_patient_name_from_split(
            row["last_name"], row["first_name"]
        )
        patient_names.add(patient_name)

    patient_name = filter_patient_names(patient_names)

    deliveries = cached_deliveries_loading(tables, delivery_from_trf)

    individual_identifiers = [
        f"{path.parent.parent.parent.parent.name} {path.parent.name}"
        for path in selected_filepaths
    ]

    identifier = f"TRF ({individual_identifiers[0]})"

    return {
        "site": None,
        "patient_id": patient_id,
        "patient_name": patient_name,
        "data_paths": selected_filepaths,
        "identifier": identifier,
        "deliveries": deliveries,
    }
