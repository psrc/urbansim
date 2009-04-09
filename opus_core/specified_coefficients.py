# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.misc import ematch, do_id_mapping_dict_from_array, unique_values, create_combination_indices
from opus_core.variables.variable_name import VariableName
from opus_core.logger import logger
from numpy import asarray, repeat, reshape, zeros, float32, int16, ones, where, array
from numpy import sometrue, take, compress, arange, resize, newaxis
import sys

class SpecifiedCoefficients(object):
    """
    A class for variable coefficients connected to the specification.
    Class attributes:
        n - number of variables
        neqs - number of equations
        nsubmodels - number of submodels
        coefficient_names - names of coefficients (string array)
        variable_names - names of variables (string array)
        beta - 3D array of coefficients (neqs x n x nsubmodels).
                beta[i,j,k] corresponds to the coefficient value for i-th equation,
                j-th variable and k-th submodel. The order of the variables correspond to the order of
                variable names in the array 'variable_names'.
        beta_se - standard errors of the coefficients. Array of the same shape as beta.
        coefmap - 3D array of the same shape as beta. It maps coefficient values to their names: A coefficient value
                    beta[i,j,k] corresponds to the name self.coefficient_names[coefmap[i,j,k]]. Value -2 means that
                    the coefficient is not used for this combination of i,j,k.
        submodels_mapping - mapping for submodels
        other_measures - a dictionary where key is the name of a measure, values are its values.
        beta_alt - 3D array of coefficients (neqs x ncoef x nsubmodels).
                beta_alt[i,j,k] corresponds to the coefficient value for i-th equation,
                j-th coefficient and k-th submodel. The order of the coefficients correspond to the order of
                coefficient names in the array 'coefficient_names'. It is used for estimation.
        beta_se_alt - standard errors of the coefficients. Array of the same shape as beta_alt.
        coefmap_alt - 2D array.  It maps coefficient names to variable names: for each submodel j
                coefficient_names[i,j] correspond to variable_names[coefmap_alt[i,j].
        other_measures_alt - like other_measures but the dictionary values are in the same form as beta_alt.
    """
    # name of variable that is considered as a constant
    constant_string = 'constant'
    reserved_name_prefix = '__' # variable names with this prefix are not considered as variables,
                                 # but some additional parameters

    def __init__(self):
        self.specification = None
        self.coefficients = None
        self.beta = None
        self.beta_se = None
        self.coefmap = None
        self.n=0
        self.neqs=0
        self.nsubmodels=0
        self.variable_names=None
        self.coefficient_names=None
        self.submodels_mapping = {}
        self.other_measures = {}
        self.other_measures_alt = {}
        self.beta_alt = None
        self.beta_se_alt = None
        self.coefmap_alt = None
        self.other_dimensions_values = {}
        self.other_dimensions_mapping = {}
        self._equation_index_mapping = {}

    def create(self, coefficients, specification, const=1.0, neqs=1, equation_ids=None):
        """
        Arguments:
            coefficients - an object of class Coefficients
            specification - an object of class EquationSpecification
            const - 2D array of constants
            neqs - number of equations. It has to be provided in nonalternative specific computations, otherwise it is ignored.
        """
        self.specification = specification
        self.coefficients = self.truncate_coefficients(coefficients)
        self.create_coefficient_arrays(neqs, equation_ids)
        self.create_beta_alt()
        self.check_consistency()
        return self

    def create_coefficient_arrays (self, neqs, equation_ids=None):
        self.variable_names = array(map(lambda x: ModelVariableName(x,
                                         self.constant_string, self.reserved_name_prefix),
                                   self.specification.get_distinct_long_variable_names()))
        submodels = self.coefficients.get_submodels()
        if equation_ids is not None:
            self.neqs = int(max(self.specification.get_nequations(),len(equation_ids), neqs))   
            unique_eqs = equation_ids
            for ieq in range(unique_eqs.size):
                self._equation_index_mapping[unique_eqs[ieq]] = ieq
        else:
            self.neqs = int(max(self.specification.get_nequations(), neqs))
        self.nsubmodels = int(self.specification.get_nsubmodels())
        names = self.coefficients.get_names()
        if names.size > 0:
            self.coefficient_names = names
        else:
            self.coefficient_names = array([], dtype='int32')
        # Constants not solved yet
#        constants = get_constants(self.specification)
#        self.coefficient_names = get_names_without_constants(names,constants)
        self.n = self.get_variable_names().size
        if self.n > 0:
            self.initialize_coefficient_arrays()

            submodels_array = self.specification.get_distinct_submodels()
            if (submodels_array.size <=0) or ((self.get_nsubmodels() == 1) and (submodels_array[0] < 0)):
                submodels_array = array([-2]) #set sub_model_id = -2 if have no or 1 submodel
            self.submodels_mapping = do_id_mapping_dict_from_array(submodels_array)
            for dimname in self.other_dimensions_values.keys():
                self.other_dimensions_mapping[dimname] = do_id_mapping_dict_from_array(self.other_dimensions_values[dimname])
            self.match_variable_with_coefficient_names(self.specification.get_coefficient_names(),
                    self.specification.get_variable_names())
            self.fill_values()

    def create_beta_alt(self):
        """Transform beta and beta_se into beta_alt and beta_se_alt."""
        ncoef = self.get_coefficient_names().size
        nsub = self.get_nsubmodels()
        neqs = self.nequations()
        shape = tuple([neqs, ncoef, nsub] + list(self.get_other_ndim()))
        self.beta_alt = zeros(shape, dtype=float32)
        self.beta_se_alt = zeros(shape, dtype=float32)
        self.coefmap_alt = resize(array([-2], dtype="int32"), (ncoef, nsub))
        index = create_combination_indices(tuple([neqs, self.size(), nsub] + list(self.get_other_ndim())))
        for i in range(index.shape[0]):
            tindex = tuple(index[i].tolist())
            if self.coefmap[tindex] >= 0:
                self.beta_alt[tuple([tindex[0], self.coefmap[tindex]] + list(tindex[2:]))] = self.beta[tindex]
                self.beta_se_alt[tuple([tindex[0], self.coefmap[tindex]] + list(tindex[2:]))] = self.beta_se[tindex]
                self.coefmap_alt[self.coefmap[tindex], tindex[2]] = tindex[1]

    def fill_beta_from_beta_alt(self,submodels=None):
        if submodels==None:
            submodels = arange(self.get_nsubmodels())
        for name in self.other_measures_alt.keys():
            if not name in self.other_measures.keys():
                self.initialize_arrays_of_other_measures([name])
        index = create_combination_indices(tuple([self.nequations(), self.size()] + list(self.get_other_ndim())))
        for k in submodels:
            for l in range(index.shape[0]):
                if index[l].size > 2:
                    tidx = tuple(index[l][0:2].tolist() + [k] + index[l][2:].tolist())
                    tidx_alt = tuple([index[l][0], self.coefmap[tidx], k] + index[l][2:].tolist())
                else:
                    tidx = tuple(index[l][0:2].tolist() + [k])
                    tidx_alt = tuple([index[l][0], self.coefmap[tidx], k])
                if self.coefmap[tidx] >= 0:
                    self.beta[tidx] = self.beta_alt[tidx_alt]
                    self.beta_se[tidx] = self.beta_se_alt[tidx_alt]
                    for m in self.other_measures_alt.keys():
                        self.other_measures[m][tidx] = self.other_measures_alt[m][tidx_alt]
                else:
                    self.beta[tidx] = 0.0
                    self.beta_se[tidx] = 0.0
                    for m in self.other_measures_alt.keys():
                        self.other_measures[m][tidx] = 0.0

    def get_beta_alt(self):
        return self.beta_alt

    def get_coefmap_alt(self):
        return self.coefmap_alt

    def truncate_coefficients(self, coefficients):
        """Leave only that part of coefficients that corresponds to specification."""
        specnames = self.specification.get_distinct_coefficient_names()
        if specnames.size <= 0:
            return coefficients.copy_and_truncate(array([], dtype='int32'))
        coefnames = coefficients.get_names()
        index_list=[]

        for icoef in range(specnames.size):
            matches = ematch(coefnames, specnames[icoef])
            l = len(matches)
            if l > 0:
                for i in range(l):
                    index_list.append(matches[i])
        # don't remove reserved names, i.e. starting with '__'
        #idx = where(map(lambda x: x.startswith('__'), coefnames))[0]
        #[index_list.append(i) for i in idx if i not in index_list]
        return coefficients.copy_and_truncate(array(index_list, dtype=int16))

    def initialize_coefficient_1d_arrays(self):
        self.beta = zeros((1,self.n,1), dtype=float32)
        self.beta_se = zeros((1,self.n,1), dtype=float32)
        self.coefmap = resize(array([-2], dtype=int16), (1,self.n,1))
        for key in self.coefficients.other_measures.keys():
            self.other_measures[key] = zeros((1,self.n,1), dtype=float32)

    def initialize_coefficient_arrays(self):
        self.initialize_coefficient_1d_arrays()
        self.repeat_along_dimension(self.neqs, 0)
        self.repeat_along_dimension(self.get_nsubmodels(), 2)
        other_dimension_names = self.specification.get_other_dim_field_names()
        for dimname in other_dimension_names:
            self.add_dimensions()
            self.other_dimensions_values[dimname] = self.specification.get_distinct_values_of_other_field(dimname)
            self.repeat_along_dimension(self.other_dimensions_values[dimname].size)

    def repeat_along_dimension(self, n, dim=None):
        if dim is None:
            dim = self.beta.ndim-1 # if dim is missing, it is repeated along the last dimension
        self.beta = repeat(self.beta, n, dim)
        self.beta_se = repeat(self.beta_se, n, dim)
        self.coefmap = repeat(self.coefmap, n, dim)
        for key in self.coefficients.other_measures.keys():
            self.other_measures[key] = repeat(self.other_measures[key], n, dim)
        
    def add_dimensions(self):
        self.beta = self.beta[...,newaxis]
        self.beta_se = self.beta_se[...,newaxis]
        self.coefmap = self.coefmap[...,newaxis]
        for key in self.coefficients.other_measures.keys():
            self.other_measures[key] = self.other_measures[key][...,newaxis]

    def initialize_arrays_of_other_measures(self, keys):
        for key in keys:
            self.other_measures[key] = zeros((1,self.n,1), dtype=float32)
            self.other_measures[key] = self._initialize_other_measures(self.other_measures[key])

    def initialize_alt_arrays_of_other_measures(self, keys):
        for key in keys:
            self.other_measures_alt[key] = zeros((1,self.get_coefficient_names().size,1), dtype=float32)
            self.other_measures_alt[key] = self._initialize_other_measures(self.other_measures_alt[key])
            
    def _initialize_other_measures(self, measure):
        measure = repeat(measure, self.neqs, 0)
        measure = repeat(measure, self.get_nsubmodels(), 2)
        for dimname in self.other_dimensions_values.keys():
            measure = measure[...,newaxis]
            measure = repeat(measure, self.other_dimensions_values[dimname].size,  measure.ndim-1)
        return measure

    def summary(self):
        logger.log_status("Specified Coefficients:")
        logger.log_status("size: %dx%dx%d" % (self.nequations(), self.size(), self.get_nsubmodels()))
        logger.log_status("beta:")
        logger.log_status(str(self.get_coefficient_values()))
        logger.log_status("standard error (beta):")
        logger.log_status(self.get_standard_errors())
        for key in self.other_measures.keys():
            logger.log_status(key)
            logger.log_status(self.other_measures[key])
        logger.log_status("coefficient names: %s" % self.get_coefficient_names())
        logger.log_status("variables:")
        logger.log_status(self.get_variable_names())
        logger.log_status("variables mapping")
        logger.log_status(self.get_coefficient_mapping())

    def compare_and_try_raise_coeflengthexception(self, value, compvalue, name):
        if value != compvalue:
            try:
                raise CoefLengthException(name)
            except CoefLengthException, msg:
                logger.log_status(msg)
                sys.exit(1)

    def check_3d_array(self, value, name):
        self.compare_and_try_raise_coeflengthexception(value.shape[0],self.neqs,name)
        self.compare_and_try_raise_coeflengthexception(value.shape[1],self.n,name)
        self.compare_and_try_raise_coeflengthexception(value.shape[2],self.nsubmodels,name)

    def check_consistency(self):
        if self.size() > 0:
            self.compare_and_try_raise_coeflengthexception(len(self.get_variable_names()),self.size(),"names")
            self.check_3d_array(self.get_coefficient_values(),"beta")
            self.check_3d_array(self.get_standard_errors(),"beta_se")
            for key in self.other_measures.keys():
                self.check_3d_array(self.get_standard_errors(),key)
            self.check_3d_array(self.get_coefficient_mapping(),"coefmap")

    def match_variable_with_coefficient_names(self, coefnames, varnames):
        """The i-th element of the string array 'coefnames' is matched to the i-th element of the string array 'varnames'.
        """
        ndisteqs = self.nequations()

        for ivar in range(self.n):
            matches = ematch(varnames, self.variable_names[ivar].get_alias())
            l = matches.size
            if (l > (ndisteqs*self.nsubmodels*max(1,sum(self.get_other_ndim())))) or (l == 0):
                raise StandardError, "Method match_variable_with_coefficient_names: something wrong with variable names."
            for i in range(l): #iterate over matches of variables
                v_matches = ematch(self.coefficient_names, coefnames[matches[i]])
                if v_matches.size == 0:
                    raise StandardError, "Method match_variable_with_coefficient_names: Mismatch in coefficient and variable names."
                for j in range(v_matches.size): #iterate over matches in coefficient class
                    if (self.nsubmodels==1) or (self.specification.get_submodels()[matches[i]] ==
                            self.coefficients.get_submodels()[v_matches[j]]):
                        eqidx = 0
                        submidx = 0
                        if self.nsubmodels > 1:
                            submidx = self.submodels_mapping[self.specification.get_submodels()[matches[i]]]
                        if len(self.specification.get_equations()) > 1:
                            if len(self._equation_index_mapping.keys()) > 0:
                                eqidx = self._equation_index_mapping[self.specification.get_equations()[matches[i]]]
                            else:
                                eqidx = int(self.specification.get_equations()[matches[i]]-1)
                        else:
                            eqidx = range(self.coefmap.shape[0])
                        coefmap_index = [eqidx,ivar,submidx]
                        for dimname in self.other_dimensions_values.keys():
                            idx = self.other_dimensions_mapping[dimname][self.specification.get_other_field(dimname)[matches[i]]]
                            coefmap_index.append(idx)
                        self.coefmap[tuple(coefmap_index)] = v_matches[j]


    def fill_values(self):
        values = self.coefficients.get_values()
        se =  self.coefficients.get_standard_errors()
        others = {}
        for key in self.other_measures.keys():
            others[key] = self.coefficients.get_measure(key)
        shape = self.getshape()
        # create combinations of all indices
        index = create_combination_indices(shape)
            
        for i in range(index.shape[0]):
            tindex = tuple(index[i].tolist())
            if self.coefmap[tindex] < 0:
                self.beta[tindex] = 0.0
                self.beta_se[tindex] = 0.0
                for key in self.other_measures.keys():
                    self.other_measures[key][tindex] = 0.0
            else:
                self.beta[tindex] = values[self.coefmap[tindex]]
                self.beta_se[tindex] = se[self.coefmap[tindex]]
                for key in self.other_measures.keys():
                    self.other_measures[key][tindex] = others[key][self.coefmap[tindex]]

    def getshape(self):
        return tuple([self.nequations(), self.size(), self.get_nsubmodels()] + list(self.get_other_ndim()))

    def get_variable_names(self):
        if self.variable_names.size <= 0:
            return []
        return array(map(lambda x: x.get_alias(), self.variable_names))

    def get_full_variable_names(self):
        return self.variable_names

    def get_variables_without_constants(self):
        is_con = array(map(lambda x: x.is_constant, self.variable_names))
        return self.variable_names[is_con==False]

    def get_variables_without_constants_and_reserved_names(self):
        is_con = array(map(lambda x: x.is_constant_or_reserved_name(), self.variable_names))
        return self.variable_names[is_con==False]

    def get_variable_names_without_constants(self):
        vars = self.get_variables_without_constants()
        return array(map(lambda x: x.get_alias(), vars))

    def get_full_variable_names_without_constants(self):
        vars = self.get_variables_without_constants()
        return array(map(lambda x: x.get_expression(), vars))

    def get_full_variable_names_without_constants_and_reserved_names(self):
        vars = self.get_variables_without_constants_and_reserved_names()
        return array(map(lambda x: x.get_expression(), vars))

    def get_coefficient_values(self):
        return self.beta

    def get_standard_errors(self):
        return self.beta_se

    def get_coefficient_mapping(self):
        return self.coefmap

    def get_measure(self, name):
        return self.other_measures[name]

    def size(self):
        return self.n

    def nequations(self):
        return self.neqs

    def get_nsubmodels(self):
        return self.nsubmodels
    
    def get_other_ndim(self):
        if self.beta.ndim <= 3:
            return ()
        return self.beta.shape[3:]

    def get_coefficient_names(self):
        return self.coefficient_names

    def get_submodel_index(self, submodel):
        if self.size() <= 0:
            return None
        return self.submodels_mapping[submodel]

    def get_submodels(self):
        return self.submodels_mapping.keys()

    def get_constants_positions(self):
        """Return an index of variables that are constants."""
        i=0
        result=[]
        for var in self.get_variable_names():
            if var == self.constant_string:
                result.append(i)
            i+=1
        return array(result, dtype="int32")

    def add_calibration_constants(self, constants_array):
        const_index = self.get_constants_positions()[0]
        coef_names = self.coefficient_names.tolist()
        ncoef = self.coefficient_names.size
        submodels = self.get_submodels()
        coefnames_changed = False
        for i in range(self.get_nsubmodels()):
            self.beta[:,const_index,i] = self.beta[:,const_index,i] + constants_array[i,:]
            nonzeros_idx = where(self.beta[:,const_index,i] != 0)[0]
            for j in nonzeros_idx:
                if self.coefmap[j,const_index,i] < 0: # doesn't have coefficient name
                    coefname = "calibration_constant_"+ str(int(submodels[i])) + "_"  +str(j+1)
                    coef_names.append(coefname)
                    ncoef = ncoef+1
                    self.coefmap[j,const_index,i] = ncoef-1
                    self.specification.add_item("constant", coefname, int(submodels[i]), j+1)
                    coefnames_changed = True
        if coefnames_changed:
            self.coefficient_names = array(coef_names)

    def get_variable_names_from_alt(self, submodel):
        mapping = self.get_coefmap_alt()[:,submodel]
        idx = where(mapping >=0)[0]
        names = mapping.size*['']
        for i in range(mapping[idx].size):
            names[idx[i]] = self.variable_names[mapping[idx[i]]].get_alias()
        return names
    
class SpecifiedCoefficientsFor1Submodel(SpecifiedCoefficients):
    """Class for dealing with coefficients as 2D arrays, i.e. coefficients for a specific submodel.
    """
    def __init__(self, parent, submodel):
        """Argument 'submodel' determines for which submodel the coefficients
        should be extracted.
        """
        self.parent = parent
        self.submodel_idx = parent.get_submodel_index(submodel)
        used = []
        coef_used = []
        for i in range(self.parent.size()):
            if (sometrue(self.parent.beta[:,i,self.submodel_idx].ravel()<>0.0)) and \
                sometrue(self.parent.coefmap[:,i,self.submodel_idx].ravel()>=0):
                used.append(i)
                coef_used = coef_used + where(self.parent.coefmap_alt[:,self.submodel_idx] == i)[0].tolist()
        eqs_used = []
        for i in range(self.parent.nequations()):
        #    if (sometrue(self.parent.beta[i,:,self.submodel_idx].ravel()<>0.0)) and \
        #        sometrue(self.parent.coefmap[i,:,self.submodel_idx].ravel()>=0):
            eqs_used.append(i)
        self.used_variables_idx = array(used) #index of variables that are used by this submodel
        self.used_coef_idx = array(coef_used)
        self.used_equations_idx = array(eqs_used)
        self.other_measures = {}
        self.other_info = {}
        
    def get_equations_index(self):
        return self.used_equations_idx

    def get_variable_names(self):
        return array(self.parent.get_variable_names())[self.used_variables_idx].tolist()

    def get_coefficient_values(self):
        beta = self.parent.beta[:,:,self.submodel_idx]
        beta = take(beta, self.used_variables_idx, axis=1)
        return take(beta, self.used_equations_idx, axis=0)

    def get_standard_errors(self):
        beta_se = self.parent.beta_se[:,:,self.submodel_idx]
        beta_se = take(beta_se, self.used_variables_idx, axis=1)
        return take(beta_se, self.used_equations_idx, axis=0)

    def get_coefficient_mapping(self):
        coefmap = self.parent.coefmap[:,:,self.submodel_idx]
        coefmap = take(coefmap, self.used_variables_idx, axis=1)
        return take(coefmap, self.used_equations_idx, axis=0)

    def size(self):
        return self.used_variables_idx.size

    def nequations(self):
        return self.used_equations_idx.size

    def get_nsubmodels(self):
        return 1

    def getshape(self):
        return tuple([self.nequations(), self.size()] + list(self.parent.get_other_ndim()))

    def get_distinct_coefficient_names(self):
        flatmap = self.get_coefficient_mapping().ravel()
        flatmap = flatmap[where(flatmap>=0)]
        coef_idx = unique_values(flatmap)
        return self.parent.get_coefficient_names()[coef_idx]

    def get_distinct_coefficient_values(self):
        values = self.get_coefficient_values()
        return self._get_distinct_values(values)

    def get_distinct_standard_errors(self):
        values = self.get_standard_errors()
        return self._get_distinct_values(values)

    def get_distinct_measure(self, name):
        values = self.get_measure(name)
        return self._get_distinct_values(values)

    def _get_distinct_values(self, values):
        coefmap = self.get_coefficient_mapping()
        coefmapflat = coefmap.ravel()
        coefmapflat = coefmapflat[where(coefmapflat>=0)]
        coef_idx = unique_values(coefmapflat)
        result = map(lambda x: values[coefmap==x][0], coef_idx)
        return array(result)

    def get_measure(self, name):
        values = self.parent.other_measures[name][:,:,self.submodel_idx]
        values = take(values, self.used_variables_idx, axis=1)
        return take(values, self.used_equations_idx, axis=0)

    def get_coefficient_names(self):
        names_idx = self.get_coefficient_mapping()
        return asarray(self.parent.get_coefficient_names())[names_idx]

    def get_coefficient_names_without_constant(self):
        names = self.get_coefficient_names()
        pos = self.get_constants_positions()
        if pos.size > 0:
            shrink=ones(names.shape[1], dtype="int8")
            shrink[pos]=0
            return names.compress(shrink, axis=1)
        return names

    def set_coefficient_values(self, values):
        self._set_values(self.parent.beta, self.used_variables_idx, values)

    def set_beta_alt(self, values):
        self._set_values(self.parent.beta_alt, self.used_coef_idx, values)

    def set_beta_se_alt(self, values):
        self._set_values(self.parent.beta_se_alt, self.used_coef_idx, values)

    def set_measure_from_alt(self, name, values):
        if not name in self.parent.other_measures_alt.keys():
            self.parent.initialize_alt_arrays_of_other_measures([name])
        self._set_values(self.parent.other_measures_alt[name], self.used_coef_idx, values)

    def fill_beta_from_beta_alt(self):
        self.parent.fill_beta_from_beta_alt(submodels=[self.submodel_idx])

    def set_standard_errors(self, values):
        for i in range(self.used_variables_idx.size):
            for j in range(self.used_equations_idx.size):
                self.parent.beta_se[:, self.used_variables_idx[i], self.submodel_idx] = values[i]

    def set_measure(self, name, values):
        if not name in self.parent.other_measures.keys():
            self.parent.initialize_arrays_of_other_measures([name])
        self._set_values(self.parent.other_measures[name], self.used_variables_idx, values)

    def _set_values(self, to_array, used_idx, values):
        for i in range(used_idx.size):
            for j in range(self.used_equations_idx.size):
                to_array[self.used_equations_idx[j], used_idx[i], self.submodel_idx] = values[i]

    def set_other_info(self, name, value):
        self.other_info[name] = value

    def get_beta_alt(self):
        beta = self.parent.get_beta_alt()[:,:,self.submodel_idx]
        beta = take(beta, self.used_coef_idx, axis=1)
        return take(beta, self.used_equations_idx, axis=0)

    def get_coefmap_alt(self):
        values = self.parent.get_coefmap_alt()[:,self.submodel_idx]
        return values[self.used_coef_idx]

    def get_coefficient_names_from_alt(self):
        return self.parent.get_coefficient_names()[self.used_coef_idx]

    def get_variable_names_from_alt(self):
        names = self.parent.get_variable_names_from_alt(submodel=self.submodel_idx)
        return asarray(names)[self.used_coef_idx].tolist()

    def get_full_variable_names(self):
        return self.parent.get_full_variable_names()[self.used_variables_idx]

    def is_variable_constant_or_reserved_name(self, variable_name):
        return ModelVariableName(variable_name,
                                 self.constant_string, self.reserved_name_prefix).is_constant_or_reserved_name()

class ModelVariableName(VariableName):
    def __init__(self, name, constant_string="constant", reserved_name_prefix='__'):
        VariableName.__init__(self, name)
        self.is_constant = self.is_variable_constant(constant_string)
        self.is_reserved_name = self.is_variable_reserved_name(reserved_name_prefix)

    def is_variable_constant(self, constant_string="constant"):
        return self.get_alias() == constant_string

    def is_variable_reserved_name(self, reserved_name_prefix='__'):
        return self.get_alias()[0:2] == reserved_name_prefix

    def is_constant_or_reserved_name(self):
        return (self.is_constant or self.is_reserved_name)

#Functions

def get_constants(specification):
    variable_names = asarray(specification.get_variable_names())
    matches = ematch(variable_names, constant_string)
#    matches = matches[where(specification.equations[matches] < 1)]
    coefnames = get_distinct_names(specification.get_coefficient_names()[matches])
#    if len(coefnames) > 1:
#        raise CoefConstantsLengthException
    return coefnames

def get_names_without_constants(names,constants):
    lc=len(constants)
    if lc > 0:
        namelist = names.tolist()
        for i in range(lc):
            if constants[i] in namelist:
                namelist.remove(constants[i])
        return asarray(namelist)
    else:
        return names

def update_constants(const, neqs):
    const = asarray(const)
    if const.ndim <= 0: #single value
        const = reshape(const, (1,))
        const = repeat(const, neqs, 0)
    if const.shape[0] <> neqs:
        raise StandardError, "Mismatch in 'const' shape and the number of equations."
    return const

class CoefLengthException(Exception):
    def __init__(self, name):
        self.args = "Something is wrong with the size of the specified coefficient object " + name + "!"