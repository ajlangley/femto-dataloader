# How to use this data loader
## Instantiate a data loader object

The data loader will download the FEMTO-ST dataset into your working directory if it is not already. Supply a `data_dir` argument to the `FEMTODataset` constructor or use the default, `femto-st`.

`femto_st = FEMTODataset(data_dir='femto-st')`

## How to access experimental measurements

The dataset is split into training, validation, and testing portions, represented by `FEMTOPartition` objects. To access train, validation, and test samples use `femto_st.train`, `femto_st.val`, or `femto_st.test`, respectively.

You can index each `FEMTOPartition` in two ways: You can use a numbered index, or a bearing name ('1_1', '1_2', '1_3', etc.).  Refer to `femto-details.pdf` for more information about the bearing experiment nomenclature. Indexing a `FEMTOPartition` return a 'RTFExperiment' representing one run-to-failure bearing experiment.

The data loader currently support accessing accelerometer readings only. For example, to access the horizontal and vertical accelerometer readings of the i-th training example, use `femto_st.train[i].h_acc`, and `femto_st.train[i].v_acc`. `h_acc` and `v_acc` are numpy arrays of shape (N, 2560).

## Additional features

In addition to accelerometer readings, each `RTFExperiment` stores information about the experimental conditions. To retrieve the RPM, experimental bearing load, and the total duration of the experiment use `exp.rpm`, `exp.bearing_load`, and `exp.total_useful_life`, respectively.
