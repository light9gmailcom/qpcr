"""
This submodule defines a number of filters that can be used to 
remove faulty replicates from `qpcr.Assay`s before before passing them to an `qpcr.Analyser`.

## Available Filters
--------
### RangeFilter 
Filters out all raw Ct values that do not comply to a user-specified range (default is `+/-1` around replicate group median)
The user has the option of specifying another anchor and limits for the inclusion range.

### IQRFilter
Filters out any outliers by `n x IQR`, where `n` is a scaling factor (default `n = 1.5`) around the replicate group median (anchor).
"""

from re import L
import qpcr
import pandas as pd
import numpy as np
import qpcr._auxiliary.warnings as aw
import qpcr.defaults as defaults
import qpcr._auxiliary as aux
import os 
import qpcr.Plotters as Plotters
import logging

class Filter(aux._ID):
    """
    The super filtering class that takes in a `qpcr.Assay` object and updates its dataframe to a filtered version.
    """
    def __init__(self):
        super().__init__()
        self._Assay = None
        self._report_loc = None
        self._id = type(self).__name__
        
        # by default we ignore groups with NaN anchors
        # like this we avoid Errors and don't filter out 
        # any unicate groups like the diluent sample...
        self._ignore_nan = True

        # by default we set outliers to NaN and 
        # don't drop them anymore
        self._drop_outliers = False

        self._boxplot_mode = defaults.plotmode
        self._BoxPlotter = Plotters.FilterSummary( mode = self._boxplot_mode )

        self._filter_stats = pd.DataFrame({
                                            "assay" : [], "group" : [], 
                                            "anchor" : [], "upper" : [], "lower" : []
                                        })
    
    def plot_params(self, **params):
        """
        Allows to pre-specify plotting parameters of the FilterSummary Figure.
        This can also be passed directly while calling `Filter.plot`.

        Parameters
        ----------
        **kwargs
            Any accepted additional keyword arguments. 
        """
        self._BoxPlotter.params(**params)
            

    def get_stats(self):
        """
        Returns 
        -------
        stats : pd.DataFrame
            The filtering statistics dataframe (a summary of filtering parameters used)
        """
        return self._filter_stats

    def ignore_nan(self, bool):
        """
        Set a policy for how to deal with groups that have a `NaN` anchor.
        If set to `True` such groups will be ignored and filtering will proceed.
        If set to `False` the Filter will raise an Error!
        """
        self._ignore_nan = bool

    def drop_outliers(self, bool):
        """
        If True, will completely remove outlier Ct values from the dataset.
        If False, will set outliers to NaN
        """
        self._drop_outliers = bool

    def plotmode(self, mode ):
        """
        Set graph mode if a summary Boxplot shall be made

        Parameters
        ----------
        mode : str
            Can be either "interactive" (plotly) or "static" (matplotlib), or None to disable plotting.
        """
        if mode is None: mode = defaults.plotmode
        self._boxplot_mode = mode
        self._BoxPlotter = Plotters.FilterSummary(mode = self._boxplot_mode)
        self._BoxPlotter.params(title = "Filter Summary")

    def plot(self, **kwargs):
        """
        Generates a boxplot summary plot. 

        Note
        ----
        This is designed to be done AFTER all samples have passed the filter.

        Parameters
        ----------
        **kwargs
            Any keyword arguments that should be passed to the plotting method.
        """
        plotter = self._BoxPlotter
        fig = plotter.plot(**kwargs)
        if self._report_loc is not None and self._boxplot_mode is not None: 
            filename = f"{self.id()}_summary"
            suffix = plotter.suffix()
            plotter.save(os.path.join(self._report_loc, f"{filename}.{suffix}"))
        return fig

    def __qplot__( self, **kwargs ):
        return self.plot

    def link(self, Assay:qpcr.Assay):
        """
        Links a `qpcr.Assay` to be filtered
        
        Parameters
        ----------
            Assay : `qpcr.Assay`
                A `qpcr.Assay` object to be filtered.
        """
        self._Assay = Assay

    def pipe(self, Assay:qpcr.Assay, **kwargs):
        """
        A shortcut for link+filter.
        This is the suggested usage for Filters.
        
        Parameters
        ----------
        Assay : `qpcr.Assay`
            A `qpcr.Assay` object to be filtered.
        **kwargs
            Any keyword arguments that should be passed to the plotting method.
        
        Returns
        -------
        Assay : `qpcr.Assay`
            A `qpcr.Assay` object containing only entries that passed the filter.

        """
        if isinstance( Assay, list ):
            return [ self.pipe( assay ) for assay in Assay ]
        else:
            self.link(Assay)
            self.filter(**kwargs)
            return self._Assay    

    def filter(self, **kwargs):
        """
        Applies the filter 
        
        Parameters
        ----------
        **kwargs
            Any keyword arguments that should be passed to the filtering method.
        
        Returns
        -------
        Assay : `qpcr.Assay`
            An updated `qpcr.Assay` object containing only entries that passed the filter.
        """
        if self._Assay is not None:
            self._filter(**kwargs)
            return self._Assay
        else: 
            e = aw.FilterError( "no_assay" )
            logging.critical( e )
            raise e 

    def report(self, directory = None):
        """
        Sets up a location to store a report of any replicates that were filtered out.

        Parameters
        ----------
        directory : str
            A directory where to store report text-files and summary boxplots.

        Returns
        -------
        location : str
            If no new directory is provided, it returns the current report location.
        """
        if directory is not None:
            self._report_loc = directory

            # if the directory does not yet exist, we make it
            if not os.path.exists(self._report_loc):
                os.mkdir(self._report_loc)

        else: 
            return self._report_loc

    def reset(self):
        """
        Resets the excluded indices
        """
        self._faulty_indices = []

    def set_lim(self, lim = None, upper = None, lower = None):
        """
        Sets the range limits for the inclusion range.
        Limits can be either specified symmetrically using `lim` or asymmetrically, using `upper` and `lower`.
        
        Parameters
        ----------
        lim : float
            Sets symmetric upper and lower bounds. 
            Default settings are `lim = 1` setting both `upper` and `lower` to `1`.
        upper : float
            Sets the upper inclusion-range boundary.
        lower : float
            Sets the lower inclusion-range boundary.
        """
        if lim is not None: self._upper, self._lower = lim, lim
        if upper is not None: self._upper = upper
        if lower is not None: self._lower = lower


    def _filter(self, **kwargs):
        """
        The actual filtering function that each FilterObject will define.
        """
        print("The actual filtering function that each FilterObject will define")
        # do stuff
        return self._Assay

    def _write_report(self, faulty_indices, details={}):
        """
        Generates a filtering report file
        """
        filename = "filter_" + self._Assay.id() + ".txt"
        filename = os.path.join(self._report_loc, filename)

        report_string = f"""
Filtering Report

Filter: 
{self._id}
Assay: 
{self._Assay.id()}
Found faulty Replicates: 
{len(faulty_indices)}
Found Indices: 
{faulty_indices}
Details: 
{details}
        """
        report_string = report_string.strip()
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write(report_string.replace("Filtering Report", ""))
        else:
            with open(filename, "w") as f:
                f.write(report_string)

    def _filter_out(self, faulty_indices):
        """
        Removes any faulty replicates based on their indices
        """
        # exclude faulty entries
        if len(faulty_indices) > 0:
            self._Assay.ignore(faulty_indices, drop = self._drop_outliers)
    
    def _save_stats(self, assay, group, anchor, upper, lower):
        """
        Saves filtering stats for a given group to self._filter_stats
        """
        new_stats = pd.DataFrame({
                                    "assay" : [assay], "group" : [group], 
                                    "anchor" : [anchor], "upper" : [upper], "lower" : [lower]
                                })
        self._filter_stats = self._filter_stats.append(new_stats, ignore_index=True)

class RangeFilter(Filter):
    """
    Filters out any replicate that lie outside a user-specified range.
    Default are `+/- 1` around the replicate-group median. 
    """
    def __init__(self):
        super().__init__()
        self._upper = 1
        self._lower = 1
        self._anchor = None

    
    def set_anchor(self, anchor):
        """
        Set the range anchor (center of inclusion range)

        Parameters
        ----------
        anchor 
            Supported types for `anchor` are: a numeric value (`int or float`),
            an `iterable` of same length as groups in the dataframe, 
            a `dict` where keys must be numeric group identifiers (starting from 0) and values are numeric values to be used as anchor (`int or float`),
            or a `function` that works with a pandas dataframe as stored by `qpcr.Assay` objects, 
            which must return a single numeric value for the anchor (it will be applied to replicate-grouped subsets of the total dataframe).
        """
        self._anchor = anchor

    def _filter(self, **kwargs):
        """
        Filters out any replicates that are out of range and updates the Assay's dataframe.
        """

        plotter = self._BoxPlotter

        plotter.add_before( self._Assay )

        df = self._Assay.get()
        groups = self._Assay.groups()

        faulty_indices = []
        for group in groups:
            tmp = df.query(f"group == {group}")

            # get anchor and check if its nan
            anchor = self._get_anchor(kwargs, group, tmp)
            if self._ignore_nan and anchor != anchor: 
                continue 

            # generate inclusion range boundries
            upper, lower = self._set_bounds(anchor)

            # get faulty indices
            Ct = defaults.raw_col_names[1]
            faulty_replicates = tmp.query(f"{Ct} < {lower} or {Ct} > {upper}")
            faulty_indices.extend(list(faulty_replicates.index))

            self._save_stats(self._Assay.id(), group, anchor, upper, lower)
        
        # remove faulty indices
        self._filter_out(faulty_indices)

        plotter.add_after( self._Assay )


        if self._report_loc is not None: 
            self._write_report(faulty_indices, details = {
                                                            "anchor" : "group median" if self._anchor is None else self._anchor,
                                                            "upper_bound" : str(self._upper),
                                                            "lower_bound" : str(self._lower), 
                                                        }
                                                    )

        return self._Assay

    
    def _set_bounds(self, anchor):
        """
        Set upper and lower boundaries of inclusion_range
        """
        upper, lower = anchor + self._upper, anchor - self._lower
        return upper,lower

    def _get_anchor(self, kwargs, group, tmp):
        """
        Set anchor for inclusion range
        """
        Ct = defaults.raw_col_names[1]
        if self._anchor is None:
            anchor = np.median(tmp[Ct])
        elif type(self._anchor) == type(print):
            anchor = self._anchor(tmp, **kwargs)
        elif isinstance(self._anchor, (list, tuple, dict)):
            anchor = self._anchor[group]
        elif isinstance(self._anchor, (int, float)):
            anchor = self._anchor
        return anchor

class IQRFilter(Filter):
    """
    Filters out outliers based on the classical n x IQR (with n = 1.5 by default) approach.
    """
    def __init__(self):
        super().__init__()
        self._upper = 1.5
        self._lower = 1.5

    def _filter(self, **kwargs):
        """
        Gets IQR for each group and finds outliers based on self._upper / lower
        """

        plotter = self._BoxPlotter

        plotter.add_before( self._Assay )
    
        df = self._Assay.get()
        groups = self._Assay.groups()
        Ct = defaults.raw_col_names[1]
        
        faulty_indices = []
        for group in groups:
            tmp = df.query(f"group == {group}")

            # get anchor
            anchor = np.nanmedian(tmp[Ct])
            # ignore Nan if so specified
            if self._ignore_nan and anchor != anchor: 
                continue

            # generate inclusion range boundries
            first, third = np.nanquantile(tmp[Ct], 0.26), np.nanquantile(tmp[Ct], 0.76)
            upper, lower = self._set_bounds(anchor, first, third)
            
            # get faulty replicates
            faulty_replicates = tmp.query(f"{Ct} < {lower} or {Ct} > {upper}")
            faulty_indices.extend(list(faulty_replicates.index))

            self._save_stats(self._Assay.id(), group, anchor, upper, lower)        
        
        self._filter_out(faulty_indices)

        plotter.add_after( self._Assay )


        if self._report_loc is not None: 
            self._write_report(faulty_indices, details = {
                                                            "upper_max" : str(self._upper),
                                                            "lower_max" : str(self._lower), 
                                                        }
                                                    )

        return self._Assay
    
    def _set_bounds(self, anchor, first, third):
        """
        Set upper and lower boundaries of inclusion_range
        """
        iqr = third - first
        upper, lower = anchor + iqr * self._upper, anchor - iqr * self._lower
        return upper,lower




def filter( assay, mode: str = "range", lim: (float or tuple) = None, anchor = None, ignore_nan : bool = True, drop_outliers : bool = False ):
    """
    Filter a single or multiple `qpcr.Assay` objects using default `Filter` setups.

    Parameters
    ----------
    assay : qpcr.Assay or list
        A single `qpcr.Assay` object or a list thereof.
    
    mode : str
        Either `"range"` to call a `RangeFilter` that uses a static range to filter values, or `"iqr"` to call a `IQRFilter` that uses the Interquantile Range
        to filter values. 
    
    lim : float or tuple
        The filtering limits for the inclusion range. Any values outside of these will be filtered out. For the `RangeFilter` these are absolute values around the `anchor` (+/- 1 by default)
        while for the `IQRFilter` these are scalars (+- 1.5 by default) for the IQR. If a single `float` is supplied the limits are interpreted symmetrically, while a `tuple` is read as first lower bound, then upper bound.
    
    anchor : 
            Only used for `RangeFilters`. Supported types for `anchor` are: a numeric value (`int or float`),
            an `iterable` of same length as groups in the dataframe, 
            a `dict` where keys must be numeric group identifiers (starting from 0) and values are numeric values to be used as anchor (`int or float`),
            or a `function` that works with a pandas dataframe as stored by `qpcr.Assay` objects, 
            which must return a single numeric value for the anchor (it will be applied to replicate-grouped subsets of the total dataframe).
    
    ignore_nan : bool
        Ignore NaN values when computing inclusion ranges. If set to `False` a single NaN value will render the entire replicate group unfilterable!
    
    drop_outliers : bool
        If `True` entries are actually dropped from the dataframe. By default any entries that do not match the inclusion range are set to NaN.


    Parameters
    ----------
    assay : qpcr.Assay or list
        The same as input but with filtered dataframes.
    """
    f = RangeFilter() if mode == "range" else IQRFilter

    if lim is not None:
        if isinstance(lim, (tuple, list, np.ndarray)): 
            f.set_lim( upper = lim[0], lower = lim[1] )
        else: 
            f.set_lim( lim = lim )
    if mode == "range" and anchor is not None:
        f.set_anchor( anchor = anchor )

    f.ignore_nan( ignore_nan )
    f.drop_outliers( drop_outliers ) 

    return f.pipe( assay )


if __name__ == "__main__":
    
    normalisers = ["./Examples/Example Data/28S.csv", "./Examples/Example Data/actin.csv"]
    assays = ["./Examples/Example Data/HNRNPL_nmd.csv", "./Examples/Example Data/HNRNPL_prot.csv"]

    groupnames = ["wt-", "wt+", "ko-", "ko+"]

    reader = qpcr.DataReader()
    assays = [ reader.read(i, replicates = 6) for i in assays ]
    normalisers = [ reader.read(i, replicates = 6) for i in normalisers ]

    filter = RangeFilter()
    # filter.plotmode("static")
    assays = [ filter.pipe(i) for i in assays ]
    normalisers = [ filter.pipe(i) for i in normalisers ]

    analyser = qpcr.Analyser()
    assays = [ analyser.pipe(i) for i in assays ]
    normalisers = [ analyser.pipe(i) for i in normalisers ]

    normaliser = qpcr.Normaliser()
    normaliser.link(assays, normalisers)
    normaliser.normalise()

    fig = filter.plot(show = False)

    print( type( fig ))

    # prev = Plotters.PreviewResults("interactive")
    # prev.link( normaliser.get() )
    # prev.plot()
