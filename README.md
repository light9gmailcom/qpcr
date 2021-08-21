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

### For a detailed introduction, check out the wiki page!

## Now available as a web-app that facilitates quick and versatile (and high-throughput) qPCR data analysis without any coding: <a href = "https://share.streamlit.io/noahhenrikkleinschmidt/qpcr-analyser/main/main.py"> qPCR Analysis Tool </a>
