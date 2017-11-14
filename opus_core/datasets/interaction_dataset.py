# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.misc import take_choices, do_id_mapping_dict_from_array
from opus_core.misc import DebugPrinter, get_distinct_list, unique

from opus_core.datasets.dataset import Dataset
from opus_core.variables.variable_factory import VariableFactory
from opus_core.variables.attribute_type import AttributeType
from opus_core.variables.variable import get_dependency_datasets
from opus_core.variables.functions import ln
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger
from numpy import array, repeat, ndarray, reshape
from numpy import indices, zeros, float32, asarray, arange
from numpy import logical_not, where, ones, take, resize
from opus_core.variables.variable_name import VariableName
from numpy import ma
from gc import collect

class InteractionDataset(Dataset):
    """Class serves as a holder of interaction variables."""

    def __init__(self, resources=None, dataset1=None, dataset2=None, index1=None, index2=None, dataset_name=None,
                  debug=None):
        """ Argument 'resources' is of type Resources. It is merged with arguments. It should contain:
                dataset1 - agent class
                dataset2 - class of the choice dataset
            Optional:
                index1 - 1D array, indices of dataset1
                index2 - If 2D array: row i contains indices of individuals of dataset2 that belong to
                        i-th individual of dataset1[index1].
                        If 1D array: indices of individuals of dataset2 for all individuals of dataset1[index1].
                dataset_name - subdirectory in which implementation of the interaction variables is placed (default "")
            dataset1.resources and dataset2.resources should contain key 'dataset_name' (see Dataset.get_dataset_name()).
        """
        self.resources = Resources(resources)
        self.resources.merge_if_not_None({
                "dataset1":dataset1, "dataset2":dataset2,
                "index1":index1, "index2":index2,
                "dataset_name":dataset_name, "debug":debug})
        self.attribute_boxes = {}
        self.attribute_names = []
        self.debug = self.resources.get("debug",  0)
        if not isinstance(self.debug, DebugPrinter):
            self.debug = DebugPrinter(self.debug)
        self.resources.check_obligatory_keys(["dataset1", "dataset2"])
        self.dataset1 = self.resources["dataset1"]
        self.dataset2 = self.resources["dataset2"]
        self.index1 = self.resources.get("index1", None)
        self.index2 = self.resources.get("index2", None)
        self.dataset_name = self.resources.get("dataset_name", None)
        if self.dataset_name == None:
            self.dataset_name = self.dataset1.get_dataset_name() + '_x_' + self.dataset2.get_dataset_name()
        self._primary_attribute_names=[]
        self.index1_mapping = {}
        if self.index1 is not None:
            self.index1_mapping = do_id_mapping_dict_from_array(self.index1)
        self._id_names = None # for compatibility with Dataset
        self.variable_factory = VariableFactory()
        self._aliases = {} # for compatibility with Dataset

    def _ensure_id_attribute_is_loaded(self):
        pass
    
    def get_attribute(self, name):
        """ Return an array of the (by the argument name) given attribute. """
        if not isinstance(name, VariableName):
            attr_name = VariableName(name)
        else:
            attr_name = name
        alias = attr_name.get_alias()
        dataset_name = attr_name.get_dataset_name()
        if not (alias in self.get_attribute_names()):
            if dataset_name == self.get_dataset(1).dataset_name:
                index = self.get_2d_index_of_dataset1()
                return self.get_dataset(1).get_attribute_by_index(attr_name, index)
            if dataset_name == self.get_dataset(2).dataset_name:
                index = self.get_2d_index()
                return self.get_dataset(2).get_attribute_by_index(attr_name, index)
            
            if alias in self.get_dataset(1).get_known_attribute_names():
                index = self.get_2d_index_of_dataset1()
                return self.get_dataset(1).get_attribute_by_index(attr_name, index)
            if alias in self.get_dataset(2).get_known_attribute_names():
                index = self.get_2d_index()
                return self.get_dataset(2).get_attribute_by_index(attr_name, index)
            self._raise_error(NameError, "Variable %s not found!" % alias)
        return self.attribute_boxes[alias].get_data()

    def get_attribute_of_dataset(self, name, dataset_number=1):
        """ Return values of attribute given by 'name' belonging to the given dataset, 
        possibly filtred by the corresponding indes. It is a 1d array of size 
        reduced_n or reduced_m.
        """
        index = self.get_index(dataset_number)
        if index is not None:
            return self.get_dataset(dataset_number).get_attribute_by_index(name, index)
        return self.get_dataset(dataset_number).get_attribute(name)
        
    def get_id_attribute_of_dataset(self, dataset_number=1):
        """Like 'get_attribute_of_dataset' where name is the id_name of the given dataset.
        """
        index = self.get_index(dataset_number)
        if index is not None:
            return self.get_dataset(dataset_number).get_id_attribute()[index]
        return self.get_dataset(dataset_number).get_id_attribute()

    def add_primary_attribute(self, data, name):
        """ Add values given in argument 'data' to the dataset as an attribute 'name'. 
        'data' should be an array of the same size as the dataset.
        If this attribute already exists, its values are overwritten.
        The attribute is marked as a primary attribute.
        """
        if not isinstance(data, ndarray):
            data=array(data)
        if data.shape[0] <> self.size()[0][0] or data.shape[1] <> self.size()[0][1]:
            logger.log_warning("In add_primary_attribute: Mismatch in sizes of the argument 'data' and the InteractionDataset object.")
        self.add_attribute(data, name, metadata=AttributeType.PRIMARY)
        
    def _compute_if_needed(self, name, dataset_pool, resources=None, quiet=False, version=None):
        """ Compute variable given by the argument 'name' only if this variable
        has not been computed before.
        Check first if this variable belongs to dataset1 or dataset2.
        dataset_pool holds available datasets.
        """
        if not isinstance(name, VariableName):
            variable_name = VariableName(name)
        else:
            variable_name = name
        short_name = variable_name.get_alias()
        if (short_name in self.get_attribute_names()) and (self.are_dependent_variables_up_to_date(
                            variable_name, version=version)):
            return version #nothing to be done
        dataset_name = variable_name.get_dataset_name()
        if dataset_name == self.get_dataset_name():
            new_version = self._compute_one_variable(variable_name, dataset_pool, resources)
        else:
            owner_dataset, index = self.get_owner_dataset_and_index(dataset_name)
            if owner_dataset is None:
                self._raise_error(StandardError, "Cannot find variable '%s'\nin either dataset or in the interaction set." %
                                variable_name.get_expression())
            owner_dataset.compute_variables([variable_name], dataset_pool, resources=resources, quiet=True)
            new_version = self.add_attribute(data = owner_dataset.get_attribute_by_index(variable_name, index),
                name = variable_name, metadata = AttributeType.COMPUTED)
            attribute_box = owner_dataset._get_attribute_box(variable_name)
            variable = attribute_box.get_variable_instance()
            my_attribute_box = self._get_attribute_box(variable_name)
            my_attribute_box.set_variable_instance(variable)
        return new_version

    def get_owner_dataset_and_index(self, dataset_name):
        if dataset_name == self.dataset1.get_dataset_name():
            return (self.dataset1, self.get_2d_index_of_dataset1())
        elif dataset_name == self.dataset2.get_dataset_name():
            return (self.dataset2, self.get_2d_index())
        return (None, None)

    def are_dependent_variables_up_to_date(self, variable_name, version):
        """ Return True if the version of this variable correspond to versions of all
        dependent variables, otherwise False. That is, if any of the dependent variable
        must be recomputed, the method returns False.
        """
        short_name = variable_name.get_alias()
        if short_name in self.get_primary_attribute_names():
            return self.is_version(short_name, version)

        dataset_name = variable_name.get_dataset_name()
        owner_name = variable_name.get_dataset_name()
        if owner_name == self.dataset1.get_dataset_name():
            owner_dataset = self.dataset1
        elif owner_name == self.dataset2.get_dataset_name():
            owner_dataset = self.dataset2
        else:
            owner_dataset = self

        if not(dataset_name == owner_dataset.get_dataset_name()):
                self._raise_mismatch_dataset_name_error(variable_name)
        if owner_dataset is self:
            attribute_box = owner_dataset._get_attribute_box(variable_name)
            if attribute_box is None:
                return False
            variable = attribute_box.get_variable_instance()
            res = variable.are_dependent_variables_up_to_date(version)
            return not(False in res)
        return owner_dataset.are_dependent_variables_up_to_date(variable_name, version)

    def _prepare_dataset_pool_for_variable(self, dataset_pool=None, resources=None):
        dataset_pool, compute_resources = Dataset._prepare_dataset_pool_for_variable(self, dataset_pool, resources)
        dataset1_name = "dataset1"
        dataset2_name = "dataset2"
        dataset1 = self.get_dataset(1)
        dataset2 = self.get_dataset(2)
        if dataset1 <> None:
            dataset1_name=dataset1.get_dataset_name()
        if dataset2 <> None:
            dataset2_name=dataset2.get_dataset_name()
        dataset_pool.add_datasets_if_not_included({dataset1_name: dataset1, dataset2_name: dataset2})
        return dataset_pool, compute_resources

    def get_n(self):
        """Return size of dataset 1.
        """
        return self.dataset1.size()

    def get_m(self):
        """Return size of dataset 2.
        """
        return self.dataset2.size()

    def get_reduced_n(self):
        if self.index1 is None:
            return self.get_n()
        if isinstance(self.index1, ndarray):
            return self.index1.shape[0]
        return self.get_n()

    def get_reduced_m(self):
        if self.index2 is None:
            return self.get_m()
        if isinstance(self.index2, ndarray):
            if self.index2.ndim == 1:
                return self.index2.shape[0]
            else:
                return self.index2.shape[1]
        return self.get_m()

    def size(self):
        return [(self.get_reduced_n(), self.get_reduced_m()), (self.get_n(), self.get_m())]

    def get_dataset(self, nr):
        if (nr == 1):
            return self.dataset1
        if (nr == 2):
            return self.dataset2
        return None

    def get_dataset_named(self, name):
        if name==self.dataset1.get_dataset_name():
            return self.dataset1
        if name==self.dataset2.get_dataset_name():
            return self.dataset2
        raise ValueError, "trying to get an interaction set component named %s but it does not exist" % name

    def get_index(self, nr):
        if (nr == 1):
            return self.index1
        if (nr == 2):
            return self.index2
        return None

    def attribute_sum(self, name):
        """Return the sum of values of the given attribute.
        """
        return (ma.ravel(self.get_attribute(name))).sum()

    def attribute_average(self, name):
        """Return the value of the given attribute averaged over the dataset.
        """
        return ma.average(ma.ravel(self.get_attribute(name)))

    def summary(self, names, resources=None):
        """Print a marginal summary of the attributes given in the list 'names'.
        """
        print "Summary\t\tsum\t\taverage"
        print "------------------------------------------------"
        if not isinstance(names,list):
            names = [names]
        for item in names:
            if not (item.get_alias() in self.get_attribute_names()):
                self.compute_variables([item], resources=resources)

            print item + "\t" + str(self.attribute_sum(item.alias))\
                     + "\t" + str(round(self.attribute_average(item.get_alias(),5)))

    def get_2d_dataset_attribute(self, name):
        """ Return a 2D array of the attribute given by 'name'. It is assumed
        to be an attribute of dataset2.
        The method should serve the purpose of preparing 1D arrays for computing
        intraction operations (between dataset1 and dataset2) by transfering them to the corresponding 2D array.
        The resulting array is of size n x m, where m is either the attribute length of dataset2,
        or, if index2 is a 1D array, its length, or, if index2 is a 2D array,
        the number of columns. n is size of dataset1 or of index1 if given.
        If index2 is None, all values of the given attribute are repeated n times.
        """
        dataset = self.get_dataset(2)
        index = self.get_2d_index()
        return dataset.get_attribute_by_index(name, index)

    def get_2d_index(self):
        n = self.get_reduced_n()
        m = self.get_reduced_m()
        if self.index2 is None:
            index = indices((n,m))[1]
        elif isinstance(self.index2, ndarray):
            if self.index2.ndim == 1: # one-dim array
                index = repeat(reshape(self.index2,(1,self.index2.shape[0])), n, 0)
            else:
                index = self.index2
        else:
            self._raise_error(StandardError, "'index2' has incompatible type. It should be a numpy array or None.")
        if (index.shape[0] <> n) or (index.shape[1] <> m):
            self._raise_error(StandardError, "'index2' has wrong dimensions.")
        return index

    def get_2d_index_of_dataset1(self):
        n = self.get_reduced_n()
        m = self.get_reduced_m()
        index = self.get_index(1)
        if index is None:
            index = arange(n)
        return repeat(reshape(index, (index.size,1)), m, 1)

    def create_logit_data(self, coefficients, index=None):
        """It creates a data array corresponding to specified coefficients
        (=coefficients connected to a specification) as one variable per column.
        'coefficients' is of type "SpecifiedCoefficientsFor1Submodel".
        If 'index' is not None, it is considered as index (1D array) of dataset1 determining
        which individuals should be considered.
        Return a 3D array (nobservations|len(index) x nequations x nvariables).
        """
        shape = coefficients.getshape()
        neqs, nvar = shape[0:2]
        other_dims = ()
        if len(shape) > 2:
            other_dims = shape[2:]
        nparenteqs = coefficients.parent.nequations()
        if (neqs <> self.get_reduced_m()) and (nparenteqs <> self.get_reduced_m()):
            self._raise_error(StandardError, "create_logit_data: Mismatch in number of equations and size of dataset2.")

        if index is not None:
            nobs = index.size
        else:
            nobs = self.get_reduced_n()
            index = arange(nobs)

        variables = coefficients.get_full_variable_names()
        mapping = coefficients.get_coefficient_mapping()
        # Fill the x array from data array
        data_shape = tuple([nobs,neqs,nvar] + list(other_dims))
        try:
            x = zeros(data_shape, dtype=float32)
        except:    # in case it fails due to memory allocation error
            logger.log_warning("Not enough memory. Deleting not used attributes.",
                                tags=["memory", "logit"])
            var_names = map(lambda x: x.get_alias(), variables)
            self.dataset1.unload_not_used_attributes(var_names)
            self.dataset2.unload_not_used_attributes(var_names)
            collect()
            x = zeros(data_shape, dtype=float32)
        if (len(variables) <= 0) or (nobs <= 0):
            return x
        for ivar in range(nvar): # Iterate over variables
            if variables[ivar].is_constant_or_reserved_name():
                c = where(mapping[:,ivar] < 0, 0.0, 1)
                x[:,:,ivar] = c
            else:
                data = ma.filled(self.get_attribute(variables[ivar]),0.0)[index,]
                if neqs < nparenteqs:
                    data = take(data, coefficients.get_equations_index(), axis=1)
                if x.ndim > 3:
                    data = resize(data, tuple(list(x.shape[0:2]) + list(other_dims)))
                x[:,:,ivar] = data
        return x

    def create_logit_data_from_beta_alt(self, coefficients, index=None):
        """It creates a data array corresponding to specified coefficients
        (=coefficients connected to a specification) as one coefficient per column. (Thus there can be multiple columns
        of one variable.)
        'coefficients' is of type "SpecifiedCoefficientsFor1Submodel".
        If 'index' is not None, it is considered as index (1D array) of dataset1 determining
        which individuals should be considered.
        It puts zeros on spots where the corresponding coefficient is zero. It is meant to be used for preparing data
        for estimation.
        Return a 3D array (nobservations|len(index) x nequations x ncoefficients).
        """
        shape = coefficients.getshape()
        neqs, nvar = shape[0:2]
        other_dims = ()
        if len(shape) > 2:
            other_dims = shape[2:]
        nparenteqs = coefficients.parent.nequations()
        if (neqs <> self.get_reduced_m()) and (nparenteqs <> self.get_reduced_m()):
            self._raise_error(StandardError, "create_logit_data: Mismatch in number of equations and size of dataset2.")

        mapping = coefficients.get_coefmap_alt()
        ncoef = mapping.size
        if index is not None:
            nobs = index.size
        else:
            nobs = self.get_reduced_n()
            index = arange(nobs)

        variables = coefficients.get_variable_names_from_alt()

        # Fill the x array from data array
        data_shape = tuple([nobs,neqs,ncoef] + list(other_dims))
        try:
            x = zeros(data_shape, dtype=float32)
        except:    # in case it fails due to memory allocation error
            logger.log_warning("Not enough memory. Deleting not used attributes.",
                                tags=["memory", "logit"])
            self.dataset1.unload_not_used_attributes(unique(variables))
            self.dataset2.unload_not_used_attributes(unique(variables))
            collect()
            x = zeros(data_shape, dtype=float32)

        if (len(variables) <= 0) or (nobs <= 0):
            return x

        coefvalues = coefficients.get_beta_alt()
        for ivar in range(len(variables)): # Iterate over variables
            if coefficients.is_variable_constant_or_reserved_name(variables[ivar]):
                c = where(coefvalues[:,ivar] == 0, 0.0, 1)
                x[:,:,ivar] = c
            else:
                data = ma.filled(self.get_attribute(variables[ivar]),0.0)[index,]
                if neqs < nparenteqs:
                    data = take(data, coefficients.get_equations_index(), axis=1)
                if x.ndim > 3:
                    data = reshape(data, tuple(list(x.shape[0:2]) + len(other_dims)*[1]))
                    for iodim in range(len(other_dims)):
                        data = repeat(data, other_dims[iodim], axis=2+iodim)
                x[:,:,ivar] = data
                w = where(coefvalues[:,ivar] == 0)
                if x.ndim > 3:
                    x[:,w[0], ivar, w[1:]] = 0.0
                else:
                    x[:,w,ivar] = 0.0
        return x

    def modify_logit_data_for_estimation(self, data, choice, constants_positions=array([], dtype='int32')):
        """Modify the variable columns for alternative specific constants. It is set to one
        for choices where the actual choice have been made, otherwise zeros.
        'data' is a 3D array (output of create_logit_data).
        'choice' is a 1D array containing indices of the actual choices (within the sampled choice set)
            for each agent that was included in the data array.
        'constants_positions' is an array with indices of the alternative specific constants
            within the data array.
        """
        nobs, neqs, nvar = data.shape
        if where(choice<0)[0].size > 0:
            self._raise_error(StandardError, "There are no choices for some agents. Check argument 'choice'.")
        if constants_positions.size > 0:
            for const in constants_positions:
                data[:,:,const] = 0
                data[arange(nobs), choice, const] = 1
        return data

    def get_attribute_by_choice(self, name, choices, resources=None):
        """  'name' is an attribute of dataset2, 'choices' is 1D array - choices[i] represents a choice
        (index of attribute 'name' among the values index2[i,]) for individual i of dataset1[index1].
        If name == None, indices belonging to dataset2 are returned.
        The method returns 1D array - the actual values of the choices.
        """
        if choices.size <> self.get_n():
            self._raise_error(StandardError, "get_attribute_by_choice: Argument 'choices' must be the same size as dataset1")
        resources.merge_with_defaults(self.resources)
        if name == None:
            twoDattr = self.get_2d_index()
        else:
            twoDattr = self.get_2d_dataset_attribute(name, resources)
        return take_choices(twoDattr, choices)

    def is_same_as(self, name1, name2):
        """Test equality of 2 variables. 'name1' is an attribute of dataset1, 'name2' is an attribute of 'dataset2'.
        Return a 2D array.
        """
        self.load_datasets()
        attr1 = reshape(self.get_attribute_of_dataset(name1),(self.get_reduced_n(), 1))
        return attr1 == self.get_2d_dataset_attribute(name2)

    def is_less_or_equal(self, name1, name2):
        """Test if attribute 'name1' (attr. of dataset1) is <= than attr. 'name2' (attr. 'dataset2').
        Return a 2D array.
        """
        self.load_datasets()
        attr1 = reshape(self.get_attribute_of_dataset(name1),(self.get_reduced_n(), 1))
        return attr1 <= self.get_2d_dataset_attribute(name2)

    def is_greater_or_equal(self, name1, name2):
        """est if attribute 'name1' (attr. of dataset1) is >= than attr. 'name2' (attr. 'dataset2').
        Return a 2D array.
        """
        self.load_datasets()
        attr1 = reshape(self.get_attribute_of_dataset(name1),(self.get_reduced_n(), 1))
        return attr1 >= self.get_2d_dataset_attribute(name2)

    def multiply(self, name1, name2):
        """Multiply 2 variables. 'name1' is an attribute of dataset1, 'name2' is an attribute of 'dataset2'.
        Return a 2D array.
        """
        self.load_datasets()
        attr1 = reshape(self.get_attribute_of_dataset(name1),(self.get_reduced_n(), 1))
        return attr1 * self.get_2d_dataset_attribute(name2)

    def divide(self, name1, name2):
        """ Divide variable 'name1' (attribute of dataset1) by variable 'name2' (attribute of 'dataset2').
        Return a masked 2D array.
        """
        self.load_datasets()
        attr2 = reshape(self.get_attribute_of_dataset(name2),(self.get_reduced_n(), 1))
        return self.get_2d_dataset_attribute(name1) / ma.masked_where(attr2 == 0.0, attr2.astype(float32))

    def match_agent_attribute_to_choice(self, name, dataset_pool=None):
        """ Return a tuple where the first element is a 2D array of the attribute 'name_{postfix}'. 
        It is assumed to be an attribute
        of dataset1 (possibly computed). {postfix} is created either by values of the attribute
        'name' of dataset2 (if it has any such attribute), or by the id values of dataset2.
        The second value of the resulting tuple is a list of dependent variables.
        """
        if 'name' in self.get_dataset(2).get_known_attribute_names():
            name_postfix = self.get_attribute_of_dataset('name', 2)
        else:
            name_postfix = self.get_id_attribute_of_dataset(2)
        name_postfix_alt = self.get_id_attribute_of_dataset(2)
        
        dependencies = []
        for i in range(self.get_reduced_m()):
            full_name = VariableName("%s_%s" % (name, name_postfix[i]))
            if full_name.get_dataset_name() is None:
                full_name = VariableName("%s.%s" % (self.get_dataset(1).get_dataset_name(), full_name.get_expression()))
            try:
                self.get_dataset(1).compute_variables(full_name, dataset_pool=dataset_pool)
            except:
                full_name = VariableName("%s_%s" % (name, name_postfix_alt[i]))
                if full_name.get_dataset_name() is None:
                    full_name = VariableName("%s.%s" % (self.get_dataset(1).get_dataset_name(), full_name.get_expression()))
                self.get_dataset(1).compute_variables(full_name, dataset_pool=dataset_pool)
            
            dependencies.append(full_name.get_expression())
            if i == 0:
                result = self.get_attribute(full_name)
            else:
                result[:,i] = self.get_attribute_of_dataset(full_name, 1)
        return result, dependencies
            
    def load_datasets(self):
        if self.dataset1.size() <= 0:
            self.dataset1.get_id_attribute()
        if self.dataset2.size() <= 0:
            self.dataset2.get_id_attribute()

    def get_index1_idx(self, ids):
        id = asarray(ids)
        try:
            return array(map(lambda x: self.index1_mapping[x], ids))
        except:
            return None

    def get_dependent_datasets(self, variables):
        """Return a list of dataset names that the given variables depend on."""
        result = []
        for variable in variables:
            try:
                result = result + self.get_dataset(1).get_dependent_datasets(variables=[variable], quiet=True)
            except:
                try:
                    result = result + self.get_dataset(2).get_dependent_datasets(variables=[variable], quiet=True)
                except:
                    result = result + get_dependency_datasets(variables=[variable])
        result = get_distinct_list(result)
        for i in [1,2]: # remove dependencies on datasets of this interaction, since it is implicitly given
            dataset_name = self.get_dataset(i).get_dataset_name()
            if dataset_name in result:
                result.remove(dataset_name)
        return result

    def _raise_error(self, error, msg):
        raise error("In interaction set '%s': %s'" % (self.name(), msg))

    def name(self):
        return "%s -> %s" % (self.dataset1.get_dataset_name(),
                                            self.dataset2.get_dataset_name())

    def get_mask(self, index):
        """index is an array of size reduced_n. The method returns array of 1's and 0's
        (of size reduced_n x reduced_m) where 0's are on rows determined by index.
        """
        mask = ones((self.get_reduced_n(), self.get_reduced_m()), dtype="int32")
        for i in index:
            mask[i,:] = 0
        return mask

    def interact_attribute_with_condition(self, attribute, condition, filled_value=0.0, do_logical_not=False):
        """Creates a 2D array (reduced_n x reduced_m) with values of 'attribute' on spots where values of the 'condition'
        attribute are > 0. All other spots have 'filled_value'. 'attribute' is an attribute name of
        the second dataset, condition is an attribute name of teh first dataset.
        If 'do_logical_not' is True, the condition is negated.
        """
        cond_values = self.get_attribute_of_dataset(condition)
        if do_logical_not:
            cond_values = logical_not(cond_values)
        index = where(cond_values > 0)[0]
        mask = self.get_mask(index)
        return ma.filled(ma.masked_array(self.get_2d_dataset_attribute(attribute), mask=mask), filled_value)

    def create_and_check_qualified_variable_name(self, name):
        """Convert name to a VariableName if it isn't already, and add dataset_name to
        the VariableName if it is missing.  If it already has a dataset_name, make sure
        it is the same as the name of this dataset.
        """
        if isinstance(name, VariableName):
            vname = name
        else:
            vname = VariableName(name)
        if vname.get_dataset_name() is None:
            vname.set_dataset_name(self.get_dataset_name())
        else:
            self._check_dataset_name(vname)
            
        return vname
    
    def get_flatten_dataset(self):
        """Creates a new dataset that is a 1D version of this dataset. All attributes are flattened.
        Id name is a combination of the two id attributes.
        """
        storage = StorageFactory().get_storage('dict_storage')
            
        table_name = '%s_flatten' % self.get_dataset_name()
        data = {}
        for attr in self.get_known_attribute_names():
            data[attr] = self.get_attribute(attr).ravel()
            
        ids = []
        for i in [1,2]:
            id_name = self.get_dataset(i).get_id_name()[0]
            ids.append(id_name)
            if id_name not in data.keys():
                data[id_name] = self.get_attribute(id_name).ravel()
            
        storage.write_table(
                    table_name=table_name,
                    table_data=data
                )
        dataset = Dataset(in_storage=storage, id_name=ids,
                          dataset_name=table_name, in_table_name=table_name)
        return dataset
    
    def _check_dataset_name(self, vname):
        """check that name is the name of this dataset or one of its components"""
        name = vname.get_dataset_name()
        dataset_names = set([self.get_dataset_name()] + list(self.get_dataset(i).get_dataset_name() for i in [1,2]))
        if name not in dataset_names:
            raise ValueError, "When checking dataset name of '%s': different dataset names for variable and dataset or a component: '%s' <> '%s'" % (vname.get_expression(), name, dataset_names)

    def add_mnl_bias_correction_term(self, probability, sampled_index, bias_attribute_name='__mnl_bias_correction_term'):
        """Compute and add an MNL bias correction term introduced by sampling. 
        'probability' is a probability array of the whole choice set. 
        'sampled_index' is an index of elements within the 'probability' array determining the sampled set of alternatives.
        The computed term is added to the interaction set as an additional attribute,
        using the name given in 'bias_attribute_name'.
        This method is mainly to be used by Samplers classes.
        """
        lnprob = ln(probability)
        ln1minusprob = ln(1-probability)
        bias_term = ln1minusprob.sum() - \
                    take(ln1minusprob, sampled_index).sum(axis=1).reshape((self.get_reduced_n(),1)) + \
                    take(lnprob, sampled_index).sum(axis=1).reshape((self.get_reduced_n(),1)) - \
                    take(lnprob, sampled_index)       
        self.add_attribute(bias_term, bias_attribute_name)
        
from numpy import ma
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool

class Tests(opus_unittest.OpusTestCase):

    def test_get_dataset_named(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='tests', 
            table_data={'id': array([1, 2]), 'attr1': array([1, 2]), 'attr2': array([10, 100])}
            )
        dataset_pool = DatasetPool(package_order=['opus_core'], storage=storage)
        test_x_test = dataset_pool.get_dataset('test_x_test')
        result = test_x_test.get_dataset_named('test')
        self.assertEqual(result.get_dataset_name(), 'test', msg="error in get_dataset_named")
        self.assertRaises(ValueError, test_x_test.get_dataset_named, 'squid')
        
    def test_match_agent_attribute_to_choice(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='agents', 
            table_data={'id': array([1, 2, 3, 4, 5]), 'attr_2': array([3,   2,   4,   10, 20]), 
                                                      'attr_3': array([10, 100, 1000, 500, 0]),
                                                      'attr_4': array([100, 500, 0, 20, -30])
                        }
            )
        storage.write_table(table_name='choices', 
            table_data={'id': array([1, 2, 3, 4])}
            )
        agents = Dataset(in_storage=storage, in_table_name='agents', dataset_name='agent', id_name='id')
        choices = Dataset(in_storage=storage, in_table_name='choices', dataset_name='choice', id_name='id')
        ids = InteractionDataset(dataset1=agents, dataset2=choices, index1=array([0,1,3,4]), index2=array([1,2,3])) 
        result, dep = ids.match_agent_attribute_to_choice('attr')
        should_be = array([[3, 10, 100], [2,100,500], [10,500, 20], [20, 0, -30]])
        self.assertEqual(ma.allequal(result, should_be), True)
        self.assertEqual((array(dep) == array(['agent.attr_2', 'agent.attr_3', 'agent.attr_4'])).sum() == 3, True)
        choices.add_primary_attribute(name='name', data=array(['bus', 'car', 'tran', 'walk']))
        agents.add_primary_attribute(name='attr_tran', data=array([100, 1000, 10000, 5000,10]))
        result, dep = ids.match_agent_attribute_to_choice('attr')
        should_be = array([[3, 100, 100], [2,1000,500], [10,5000, 20], [20, 10, -30]])
        self.assertEqual(ma.allequal(result, should_be), True)
        self.assertEqual((array(dep) == array(['agent.attr_2', 'agent.attr_tran', 'agent.attr_4'])).sum()==3, True)
        
if __name__=='__main__':
    opus_unittest.main()
