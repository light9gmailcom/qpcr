# qpcr
### A python package to analyse qPCR data and perform various actions such as Delta-Delta CT analysis in single-use or high-throughput

This project represents a python package that includes a number of functions useful for the analysis of qPCR data generated generated by Qiagen RotorGene® 
and is taylored to work with the Excel Spreadhseet exported from this device (or, more precisely, a csv copy of the same). User friendliness and quick and easy workflows were of primary concern while developing this package. Also, the exported results are formatted to be readily imported into professional graphing software :chart:. This package was mostly taylored to work directly with GraphPad Prism but has been tested to also work well with other graphing software. I initially developed the package for data from my Bachelor Thesis and have expanded functionality hence.

## An Example: __qPCR Analysis__ can be so quick 'n easy :-)
```python
import qpcr.Analysis as qA
hnrnpl_nmd = "Example Data/HNRNPL_nmd.csv"
hnrnpl_prot = "Example Data/HNRNPL_prot.csv"
s28 = "Example Data/28S.csv"

groups = ["wt-", "wt+", "ko-", "ko+"]
result = qA.delta_deltaCt([s28, hnrnpl_nmd, hnrnpl_prot], 
                        replicates=6, normaliser="28S",
                        anchor="first", group_names=groups)

qA.preview_results(result)
```


![Figure_1](https://user-images.githubusercontent.com/89252165/130232298-256e2d1e-db07-429b-97c3-38bdaebc826d.png)
> Do these figures not look like what you want? No problem, they're just instant previews, you will automatically be generating csv files with your results that you can import into Graphpad Prism or whatever your favourite graphing software happens to be ;-)

## Input Data
Qiagen RotorGene® generates raw CT data in a two column format. The first column shows the run-/replicate name, while the second shows the actual CT value. This package is designed to work with csv files with this kind of data formatting. The package is designed to work with multiple separate data-files, so that different qPCR runs may be stored in their separate data sheets and yet easily combined during analysis. This package is also designed to work directly with the raw CT values so there is no need to pre-compute the average of each group of replicates!

| Sample  | CT   |
| ------- | ---- |
| geneX_1 | 10.6 |
| geneX_2 | 10.9 |
| geneX_3 | 10.2 |
| geneY_1 | 5.8  |
| ...     | …    |

## Data Analysis
This package processes data from input files and stores and processes them in dictionaries (not dataframes). 
To perform analysis a set of functions are defined within the `qpcr` module which can be easily combined into a workflow. Alternatively, this package also includes a sub-module `qpcr.Analysis` which is designed to provide a quick solution to simple analyses using predefined workflows. These are:

### Predefined Analyses using `qpcr.Analysis`
##### single Delta CT analysis: `qpcr.Analysis.single_deltaCt`
`qpcr.Analysis.single_deltaCt` is designed to work with one single input data file where the first group of replicates represents the normaliser. 
`qpcr.Analysis.single_deltaCt` expects the following parameters to work with: 
| Parameter        | Explination                                                  | Example                                                      |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| data_file        | the source file                                              | "mydata.csv"                                                 |
| replicates       | the number of replicates in each group of replicates. Either n (int) or tuple | 3 (each group has 3 replicates) or (3, 3, 2) (two groups each with three replicates, and one with only 2) |
| mode             | either "replicate" (default) or "stats". determines if results shall be maintained with all replicate values or if Avg+StDev shall be directly computed | replicate" (default) or "stats"                              |
| group_names      | List of strings (default None) to provide a name to each group of replicates. If None are provided Group1, Group2,… will automatically be assigned | ["GeneX", "GeneY"]                                           |
| anchor           | "first", "grouped" (default), or float. determines if the first Delta CT shall be taken against either: ("first") the very first entry of the input data file, ("grouped", default) the first entry in each group of replicates respectively, or (any float) any specific given value | "first" or "grouped" (default) or any float (e.g. 5.56)      |
| dCt_exp          | True (default) / False allows to choose wether to compute $$Ct_1-Ct_0$$ (False) instead of $$2^{(Ct_1-Ct_0)}$$ (True, default) | True (default) / False                                       |
| export           | True (default) or False. determines wether or not a csv file shall directly be written from the results | True/False                                                   |
| transpose        | transpose columns and rows during export, True (default) or False | True/False                                                   |
| exportname_addon | Any string (optional) to add to the name of the exported csv file (if export=True is set) | "My_analysis"                                                |



##### Delta-Delta CT analysis: `qpcr.Analysis.delta_deltaCt`
`qpcr.Analysis.delta_deltaCt` is designed to work with one input file for the data from the normaliser and a list of input files for each of the target genes to be analysed. 
`qpcr.Analysis.delta_deltaCt` shares many parameters with `qpcr.Analysis.single_deltaCt` but requires a few additional ones. All parameters of `qpcr.Analysis.delta_deltaCt` are: 
| Parameter  | Explination                                                  | Example                                                      |
| ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| data_files | the source files                                             | ["geneX.csv", "geneY.csv"]                                   |
| replicates | the number of replicates in each group of replicates. Either n (int) or tuple | 3 (each group has 3 replicates) or (3, 3, 2) (two groups each with three replicates, and one with only 2) |
| mode       | either "replicate" (default) or "stats". determines if results shall be maintained with all replicate values or if Avg+StDev shall be directly computed | replicate" (default) or "stats"                              |
| normaliser | a source file for the normaliser                             | "Norm.csv"                                                   |
| run_names  | List of strings (default "auto"). A name for each of the files within data_files. By default it will pick the filename | ["geneX", "geneY"] or "auto" (default)                       |
| group_names      | List of strings (default None) to provide a name to each group of replicates. If None are provided Group1, Group2,… will automatically be assigned | ["wildtype", "geneZ_knockout"]                                           |
| anchor           | "first", "grouped" (default), or float. determines if the first Delta CT shall be taken against either: ("first") the very first entry of the input data file, ("grouped", default) the first entry in each group of replicates respectively, or (any float) any specific given value | "first" or "grouped" (default) or any float (e.g. 5.56)      |
| dCt_exp          | True (default) / False allows to choose wether to compute $$Ct_1-Ct_0$$ (False) instead of $$2^{(Ct_1-Ct_0)}$$ (True, default) | True (default) / False                                       |
| export           | True (default) or False. determines wether or not a csv file shall directly be written from the results | True/False                                                   |
| transpose        | transpose columns and rows during export, True (default) or False | True/False                                                   |
| exportname_addon | Any string (optional) to add to the name of the exported csv file (if export=True is set) | "My_analysis"                                                |


##### Preview: `qpcr.Analysis.preview_results`
`qpcr.Analysis.preview_results` takes in the results dictionary of either `qpcr.Analysis.single_deltaCt` or `qpcr.Analysis.delta_deltaCt` and generates a crude bar chart of the results for each analysed target gene.
![Figure_1](https://user-images.githubusercontent.com/89252165/130232298-256e2d1e-db07-429b-97c3-38bdaebc826d.png)

##### Normalise two conditions: `qpcr.Analysis.normalise_pairs`
`qpcr.Analysis.normalise_pairs` allows to normalise entire sets of sample dictionaries against a corresponding set of normalisers. This is especially useful when for instance separate RNA isoforms were analysed separately with different primer pairs and are now supposed to be normalised against each other. `qpcr.Analysis.normalise_pairs` takes in a _dictionary of targets_ and a _dictionary of normalisers_ (!). It will then iteratively normalise each target with its corresponding normaliser (hence, both dictionaries must contain the right order of targets and normalisers). Optionally, it is possible to assign `pair_names` to give specific titles to each normalisation. It also takes in arguments `export`(True/False) to save the result directly to a csv file (True is default), if export=True is set, an `export_location` must be given to save the file. It is also possible to transpose the results data using `transpose=True`. 

### Manual Analysis using `qpcr` functions directly
For more control of the process or more elaborate analyses the functions of `qpcr` must be used manually. Here all the functions are explained (sometimes repetitive of the above arguments). Available functions are:

##### Open input files: `qpcr.open_csv_file`
`qpcr.open_csv_file` takes in a filepath to the input file and returns a dictionary of the data. Optionally, the data may be returned as a list of lines using the parameter `export="list"` but this is not suitable for further analysis using the `qpcr` package!

##### Organise data in groups of replicates: `qpcr.group_samples`
`qpcr.group_samples` takes in a data dictionary (from `qpcr.open_csv_file`) as well as a `replicates` argument which may either be an `int` (if all groups have the same number of replicates) or a `list`, in which case each group of replicates must be given its own number of replicates. 

##### Rename Groups: `qpcr.rename_groups`
By default groups of replicates are assigned Group1,Group2,... automatically. To change this to meaningful group names `qpcr.rename_groups` takes in a grouped dictionary and a list of strings containing the new name of each group of replicates. It is important that any dictionaries that shall be used for the same analysis have _the same_ group names! 

##### Delta-CT: `qpcr.Delta_Ct`
`qpcr.Delta_Ct` takes in one grouped dictionary (one that has been processed using `qpcr.group_samples`) and an `anchor` argument which may be: `"grouped"` (or None, this is the default) in which case the first entry of each group is taken as reference, `"first"` in which case the very first line of the dataset is taken as reference for all groups, or `any float` in which case a specific reference may be given which will be used for the entire dataset. Optionally, it is possible to choose wether or not to compute the Delta-CT exponentially as 2^(Delta-Ct) (default) or not using the argument `exp = False`.

##### Delta-Delta-CT: `qpcr.normalise`
`qpcr.normalise` is used to take the second Delta-CT in Delta-Delta CT analysis to normalise against a normaliser. It takes in one pre-processed dictionary for the `normaliser`argument and one pre-processed dictionary for the `sample`argument. For this to work it is necessary to that both normaliser and sample have _the same_ group names!
Optionally a line containing "Legend" : "DDCT" may be added to the resulting dictionary using the argument `no_head=False`. 

##### Combining Normalisers: `qpcr.preprocess_normalisers` and `qpcr.combine_normalisers`
Sometimes it is desirable to use not one single normaliser but instead a combined (= averaged) version of multiple normalisers (e.g. Actin + 28S rRNA). This package also provides 
In this case the normalisers must first be preprocessed using `qpcr.preprocess_normalisers` which takes in a list of input files, as well as parameters `replicates`, `run_names`
(to define the names, default is None and uses the filenames), `group_names` (which must be the same as those used in the target datasets!), and `anchor`. Once the normalisers are preprocessed they can be combined using `qpcr.combine_normalisers` which will take in the list of preprocessed normalisers that is returned by `qpcr.preprocess_normalisers`.

##### Summarising Results: `qpcr.get_stats`
After Delta-CT or Delta-Delta CT results were generated they still contain all the individual grouped replicates. To collapse each group into a Mean+StDev format you may use `qpcr.get_stats` which takes in a results dictionary. Using the optional parameter `export` you may specify which statistics you which to export. Available are: `"avg"`, `"stdv"`, and `"med"` which can be combined in a list. Default is `["avg", "stdv"]`. 

##### Saving Results: `qpcr.export_to_csv`
`qpcr.export_to_csv` takes in a results dictionary and a filename and stores the results into a new csv file. Optionally you can transpose columns and rows using the argument `transpose=True`. 

##### Saving Raw CTs: `qpcr.export_raw_data`
In case you wish to also get a processed representation of your raw CT values you may use `qpcr.export_raw_data` which takes in an input file, as well as parameters `replicates`, `group_names`, as well as an optional `export_location` in case you wish to specify a directory to save the file in (by default the same folder is used where the input file is located). 

##### Loading Results: `qpcr.load_results`
This function opens pre-computed results csv files. 
It supports two modes: `"individual"` (default) where filename specifies the file to be opened. It returns a dictionary containing the grouped computed values (replciates, or avg, stdev) or `"pairs"`which allows users to load an entire set of samples and normalisers that were previously computed to then be used by `qpcr.Analysis.normalise_pairs`. It returns two separate dictionaries each containing the set of sample files it was given by kwargs parameters `samples` and `normalisers`. Optionally, names may be additionally assigned to samples and normalisers using `sample_names` and `norm_names` To facilitate working with replicate assays (i.e. same qPCR assay normalised against different normalisers separately), samples / normalisers support only partial naming and need no full filepath to function. Like this multiple analysis result with e.g. "HNRNPL NMD" in their name will all be loaded. 

## Ouput Data
This package offers great versatility with regard to output formatting.
##### Default Format: individual replicate values for each assay
| GeneX | GeneY | GeneZ |
| ----- | ----- | ----- |
| 4.56  | 10.23 | 7.56  |
| 4.98  | 11.1  | 7.32  |
| ...   | ...   | ...   |
##### Statistics Format: each assay is represented by Mean and StDev
| Legend | Avg   | StDev |
| ------ | ----- | ----- |
| GeneX  | 4.78  | 0.32  |
| GeneY  | 10.65 | 0.54  |
| ...    | ...   | ...   |
##### Both of these can be transposed as well using `transpose=True` in  `qpcr.export_to_csv`
