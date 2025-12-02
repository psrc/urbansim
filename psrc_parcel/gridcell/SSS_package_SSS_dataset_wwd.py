from opus_core.variables.variable import Variable

class SSS_package_SSS_dataset_SSS_wwd(Variable):
    """Sum of a variable (given by the third SSS, defined in a package given by the first SSS,
    for a dataset given by the second SSS) 
        over gridcells located within walking distance. If the variable is a primary attribute,
        the package is not used (but must be given).
        E.g. psrc_parcel.gridcell.urbansim_parcel_package_household_dataset_population_wwd
        computes variable population urbansim_parcel.gridcell.population and sums it over gridcells within walking distance,
        while using household.grid_id.
    """
        
    def __init__(self, package, dataset, name):
        self.var_package = package
        self.var_name = name
        self.var_dataset = dataset
        Variable.__init__(self)
        
    def dependencies(self):
        return ["gridcell.grid_id",
                "urbansim_parcel.%s.grid_id" % self.var_dataset, 
                '_%s_wwd = %s.gridcell.sum_%s_within_walking_distance' % (self.var_name, self.var_package, self.var_name)
                ]

    def compute(self, dataset_pool):
        return self.get_dataset()["_%s_wwd" % self.var_name]

