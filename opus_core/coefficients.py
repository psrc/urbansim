# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.misc import create_string_list, get_distinct_names, flatten_list
from opus_core.misc import ematch, unique_values
from opus_core.store.storage import Storage
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from opus_core.specified_coefficients import SpecifiedCoefficients, SpecifiedCoefficientsFor1Submodel
from opus_core.simulation_state import SimulationState
from opus_core.logger import logger
from opus_core.variables.attribute_type import AttributeType
from numpy import int32, array, zeros, float32, arange, nan, resize, newaxis
from numpy import apply_along_axis, ndarray, concatenate
from numpy.random import normal, uniform
import sys
import os
import string

class Coefficients(object):
    """
    A class for variable coefficients and their parametric distributions. A Coefficients object can be created by passing coefficient values directly to the constructor. Alternatively, the method 'load' can be used to read the values from storage. In that case 'storage' has to be passed as argument either to the constructor or the 'load' method.
    """
    #defaults for column names on the storage, can be rewritten by resources
    field_submodel_id = 'sub_model_id'
    field_coefficient_name = 'coefficient_name'
    field_estimate = 'estimate'
    field_standard_error = 'standard_error'
    other_fields =['t_statistic', 'p_value']

    def __init__(self, names=array([]), values=array([]), standard_errors=array([]), submodels=array([]),
                    in_storage=None, out_storage=None, other_measures=None, other_info=None):
        """
            names - array of coefficient names.
            values - array of coefficient values. If not empty, it has to be of the same length as names.
            standard_errors - array of standard errors. If not empty, it has to be of the same length as names.
            submodels - array of submodels. If not empty, it has to be of the same length as names.
            in_storage, out_storage - objects of class Storage.
            other_measures - a dictionary for other coefficient measures, such as t-values. Keys are the names
                            of the measures, values are arrays of the same length as names.
            other_info - holder for other information about the coefficients, such as goodness of fit values.
            A coefficient i has name names[i], value values[i], optionally stand. error standard_errors[i], and
            is used in sub model submodels[i].
        """
        self.set_values(values)
        self.set_standard_errors(standard_errors)
        self.set_names(names)
        self.set_submodels(submodels)
        self.in_storage = in_storage
        self.out_storage = out_storage
        if other_measures == None:
            self.other_measures = {}
        else:
            self.other_measures = other_measures
        if other_info == None:
            self.other_info = {}
        else:
            self.other_info = other_info
        self.create_coefficient_attributes()
        self.check_consistency()

    def load(self, resources=None, in_storage=None, in_table_name=None):
        """
        """ # TODO: insert docstring
        local_resources = Resources(resources)
        local_resources.merge_with_defaults({
            "field_submodel_id":self.field_submodel_id,
            "field_coefficient_name":self.field_coefficient_name,
            "field_estimate":self.field_estimate,
            "field_standard_error":self.field_standard_error,
            "other_fields":self.other_fields})
        if in_storage <> None:
            self.in_storage = in_storage
        if not isinstance(self.in_storage, Storage):
            logger.log_warning("in_storage has to be of type Storage. No coefficients loaded.")
        else:
            data = self.in_storage.load_table(table_name=in_table_name)
            submodels = data[local_resources["field_submodel_id"]]
            self.names = data[local_resources["field_coefficient_name"]]
            self.values = data[local_resources["field_estimate"]]
            self.standard_errors = data[local_resources["field_standard_error"]]
            for measure in local_resources["other_fields"]:
                if measure in data.keys():
                    self.other_measures[measure] = data[measure]
            if submodels.max() >= 0:
                self.submodels=submodels
            self.check_consistency()

    def write(self, resources=None, out_storage=None, out_table_name=None):
        """
        """ # TODO: insert docstring
        local_resources = Resources(resources)
        local_resources.merge_with_defaults({
            "field_submodel_id":self.field_submodel_id,
            "field_coefficient_name":self.field_coefficient_name,
            "field_estimate":self.field_estimate,
            "field_standard_error":self.field_standard_error,
            "other_fields":self.other_fields,
            "out_table_name":out_table_name})
        if out_storage <> None:
            self.out_storage = out_storage
        if not isinstance(self.out_storage, Storage):
            logger.log_warning("out_storage has to be of type Storage. No coefficients written.")
            return

        submodels = self.get_submodels()
        if submodels.size <= 0 :
            submodels = resize(array([-2], dtype=int32), self.size())
        values = {local_resources["field_submodel_id"]: submodels,
               local_resources["field_coefficient_name"]:  self.get_names(),
               local_resources["field_estimate"]:  self.get_values(),
               local_resources["field_standard_error"]:  self.get_standard_errors()}
        for measure in self.other_measures.keys():
            values[measure] = self.other_measures[measure]
        types = {local_resources["field_submodel_id"]: 'integer',
               local_resources["field_coefficient_name"]:  'text',
               local_resources["field_estimate"]:  'double',
               local_resources["field_standard_error"]:  'double'}
        attrtypes = {local_resources["field_submodel_id"]: AttributeType.PRIMARY,
               local_resources["field_coefficient_name"]:  AttributeType.PRIMARY,
               local_resources["field_estimate"]:  AttributeType.PRIMARY,
               local_resources["field_standard_error"]: AttributeType.PRIMARY}
        for measure in self.other_measures.keys():
            types[measure]= 'double'
            attrtypes[measure] = AttributeType.PRIMARY
        local_resources.merge({"values":values, 'valuetypes': types, "drop_table_flag":1,
                               "attrtype":attrtypes})
        
        self.out_storage.write_table(table_name=local_resources['out_table_name'],
            table_data = local_resources['values'])       

    def create_coefficient_attributes (self):
        self.create_default_coefficient_names()
        self.create_default_se()

    def create_default_coefficient_names(self):
        if self.names.size == 0:
            self.names = array(create_string_list('coef',self.values.size))

    def create_default_se(self):
        if self.standard_errors.size == 0:
            self.standard_errors = zeros(self.values.size)

    def summary(self):
        logger.log_status("Coefficient object:")
        logger.log_status("size:", self.size())
        logger.log_status("names:", self.get_names())
        logger.log_status("values:")
        logger.log_status(self.get_values())
        logger.log_status("standard errors:")
        logger.log_status(self.get_standard_errors())
        for key in self.other_measures.keys():
            logger.log_status(key+":")
            logger.log_status(self.other_measures[key])
        if self.submodels.size > 0:
            logger.log_status("submodels:", self.get_submodels())

    def size(self):
        return self.names.size

    def get_values(self):
        return self.values

    def get_values_of_one_coefficient(self, name):
        """Get values of a coefficient given by 'name'."""
        idx = ematch(self.get_names(), name)
        return array(self.get_values())[idx]

    def get_standard_errors(self):
        return self.standard_errors

    def get_measure(self, name):
        return self.other_measures[name]

    def get_names(self):
        return self.names

    def get_distinct_names(self):
        return get_distinct_names(self.get_names())

    def get_submodels(self):
        return self.submodels

    def get_nsubmodels(self):
        if self.get_submodels().size > 0:
            return self.get_submodels().max()
        return 1

    def set_values(self, values):
        self.values = values
        if not isinstance(self.values, ndarray):
            self.values = array(self.values)

    def set_standard_errors(self, values):
        self.standard_errors = values
        if not isinstance(self.standard_errors, ndarray):
            self.standard_errors = array(self.standard_errors)

    def set_names(self, names):
        self.names = names
        if not isinstance(self.names, ndarray):
            self.names = array(self.names)

    def set_measure(self, name, values):
        self.other_measures[name] = values
        if not isinstance(self.other_measures[name], ndarray):
            self.other_measures[name] = array(self.other_measures[name])

    def set_submodels(self, values):
        self.submodels = values
        if not isinstance(self.submodels, ndarray):
            self.submodels = array(self.submodels)

    def compare_and_try_raise_coeflengthexception(self, value, compvalue, name):
        if value != compvalue:
            try:
                raise CoefLengthException(name)
            except CoefLengthException, msg:
                logger.log_status(msg)
                sys.exit(1)


    def check_consistency(self):
        if self.values.size > 0:
            self.compare_and_try_raise_coeflengthexception(self.size(), self.values.size,"values")
        if self.standard_errors.size > 0:
            self.compare_and_try_raise_coeflengthexception(self.size(),self.standard_errors.size,"standard_errors")
        if self.submodels.size > 0:
            self.compare_and_try_raise_coeflengthexception(self.size(),self.submodels.size,"submodels")
        for key in self.other_measures.keys():
            self.compare_and_try_raise_coeflengthexception(self.size(),len(self.get_measure(key)),key)


    def copy_and_truncate(self, index):
        if index.size <= 0:
            return Coefficients()
        new = Coefficients(names=self.names[index])
        if self.values.size > 0:
            new.values = self.values[index]
        if self.standard_errors.size > 0:
            new.standard_errors = self.standard_errors[index]
        if self.submodels.size > 0:
            new.submodels = self.submodels[index]
        new.other_measures = {}
        for key in self.other_measures.keys():
            new.other_measures[key] = self.get_measure(key)[index]
        return new

    def fill_coefficients(self, new_coefficients):
        """Fill class attributes with the appropriate values.
        'new_coefficients' is a dictionary with keys equal to submodels and values are
        instances of class SpecifiedCoefficientsFor1Submodel.
        """
        if (not isinstance(new_coefficients, SpecifiedCoefficientsFor1Submodel)) \
            and isinstance(new_coefficients, SpecifiedCoefficients):
            new_coef = {}
            for submodel in new_coefficients.get_submodels():
                new_coef[submodel] = SpecifiedCoefficientsFor1Submodel(
                                            new_coefficients, submodel)
        else:
            new_coef = new_coefficients
        coefnames = map(lambda x: new_coef[x].get_distinct_coefficient_names().tolist(), new_coef.keys())
        submodels = map(lambda x: len(x), coefnames)
        submodels = map(lambda x,y: x*[y], submodels, new_coef.keys())
        coefvalues = map(lambda x: new_coef[x].get_distinct_coefficient_values().tolist(), new_coef.keys())
        se = map(lambda x: new_coef[x].get_distinct_standard_errors().tolist(), new_coef.keys())
        coefnames = flatten_list(coefnames) #flattens nested list
        coefvalues = flatten_list(coefvalues)
        se = flatten_list(se)
        submodels = flatten_list(submodels)
        self.set_names(coefnames)
        self.set_values(coefvalues)
        self.set_standard_errors(se)
        self.set_submodels(submodels)

        for measure in new_coef[new_coef.keys()[0]].parent.other_measures.keys():
            values = map(lambda x: new_coef[x].get_distinct_measure(measure).tolist(), new_coef.keys())
            self.set_measure(measure, flatten_list(values))

        for submodel in self.get_submodels():
            self.other_info[submodel] = new_coef[submodel].other_info


    def add_item(self, name, value, standard_error=0.0, submodel=None, other_measures=None):
        self.names = concatenate((self.names, array([name])))
        self.values = concatenate((self.values, array([value])))
        self.standard_errors = concatenate((self.standard_errors, array([standard_error])))
        if submodel is not None:
            self.submodels = concatenate((self.submodels, array([submodel])))
        elif self.get_submodels().size > 0:
            self.submodels = concatenate((self.submodels, array([-2])))
        if other_measures is not None:
            for field in other_measures.keys():
                self.other_measures[field] = concatenate((self.other_measures[field], array([other_measures[field]],
                                                                               dtype=self.other_measures[field].dtype)))
                
                
    def make_tex_table(self, table_name, path='.', header_submodel='Submodel',
                       header_coef_name='Coefficient Name',
                       header_value='Estimate', header_se='Standard Error', other_headers={},
                       label=None, caption=None):
        """Create a TeX file with two tables: coefficient table and a table with additional
        information about the coefficients.
        'table_name' is the file name without '.tex'. 'path' specifies directory for the file.
        The 'header_*" arguments specify what header to use. 'other_headers' is a dictionary with
        key equals other measure (returned by the estimation procedure), e.g. t_statistic, ll_ratio_index,
        and value equals the corresponding header to be used.
        """
        tex_file_path = '%s.tex' % table_name
        if path is not None:
            tex_file_path = os.path.join(path, tex_file_path)
        tex_file = open(tex_file_path, 'w')

        # Coefficients table
        header=""
        ncol = 0
        if self.get_nsubmodels() > 1:
            header = header + header_submodel + ' & '
            ncol = ncol+1
        header = header + header_coef_name + ' & ' + header_value + ' & ' + header_se
        ncol = ncol + 3
        for measure in self.other_measures:
            ncol = ncol + 1
            if measure in other_headers.keys():
                hmeasure = other_headers[measure]
            else:
                hmeasure = measure
            header = header + ' & ' + hmeasure
        header = header + r'\\ \hline '
        tex_file.write('\\begin{center}\n')
        tex_file.write(r"\begin{longtable}{")
        s = ncol*'r'
        tex_file.write(s+"}  \n")
        tex_file.write(string.replace(header, "_", "\_"))
        tex_file.write("\n")
        if caption is not None:
            tex_file.write('\\caption{%s}\n' % caption)
        if label is not None:
            tex_file.write('\\label{%s}\n' % label)
        if caption is not None:
            tex_file.write('\\\\\n')
        for row in range(self.size()):
            if self.get_nsubmodels() > 1:
                tex_file.write("%s & " % str(self.get_submodels()[row]))

            coeff_name = self.get_names()[row]
            tex_file.write("%s " % string.replace(coeff_name, "_", "\_"))

            values = zeros(2+len(self.other_measures.keys()), dtype=float32)
            values[0] = self.get_values()[row]
            values[1] = self.get_standard_errors()[row]
            i=2
            for measure in self.other_measures:
                values[i] = self.other_measures[measure][row]
                i=i+1

            for value in values:
                # if the number is 0, big enough to not need sci notation, or a number like .001,
                # then just write out in x.xxxx format
                split_value = string.split("%s"%value,".")
                if  (0 == value) or (abs(value) >= .1) or (len(split_value)>1 and len(split_value[1]) < 5):
                    tex_file.write("& $ %.4f $" % value)
                # otherwise, write out in sci notation
                else:
                    tex_file.write("& $ %.4e $" % value)
            tex_file.write('\\\\ \n')
        tex_file.write(r'\hline \\')
        tex_file.write(r"\end{longtable}")
        tex_file.write('\\end{center}\n')
        tex_file.write('\n')
        if self.other_info.keys():
            # Table with additional info
            ncol = max(1,self.get_nsubmodels())+1
            tex_file.write('\n')
            tex_file.write('~\\\\ \n')
            tex_file.write(r"\begin{longtable}{")
            s = ncol*'r'
            tex_file.write(s+"}  \n")
            if self.get_nsubmodels() > 1:
                header = "Info "
                for i in range(self.get_nsubmodels()):
                    header=header+" & " + str(i)
                header = header + r'\\ \hline'
                tex_file.write(header)
                tex_file.write('\n')
            for info in self.other_info[self.other_info.keys()[0]].keys():
                if info in other_headers.keys():
                    info_header = other_headers[info]
                else:
                    info_header = info
                info_header = string.replace(info_header, "_", "\_")
                tex_file.write(info_header)
                for submodel in unique_values(self.get_submodels()):
                    value = self.other_info[submodel][info]
                    if  (0 == value) or (abs(value) >= .1) or len(string.split("%s"%value,".")[1]) < 5:
                        tex_file.write("& $ %.4f $" % value)
                    else:
                        tex_file.write("& $ %.4e $" % value)
                tex_file.write(r"\\")
                tex_file.write('\n')
            tex_file.write(r"\end{longtable}")
            tex_file.write('\n')

    def sample_values(self, distribution=None, distribution_dictionary=None, **kwargs):
        """
        Return a copy of self, where values are sampled from given distribution(s).
        If 'distribution' is 'normal', all coefficients are sampled from normal distribution
        (see docstring for sample_values_from_normal_distribution).
        If 'distribution' is 'uniform', all coefficients are sampled from uniform distribution
        (see docstring for sample_values_from_uniform_distribution).
        In both cases, kwargs are passed to the appropriate method.
        If 'distribution' is None, argument 'distribution_dictionary' must be given.
        This dictionary contains arguments for sampling different coefficients using different distributions.
        Keys of this dictionary are coefficient names, values are again dictionaries. These must have a 
        key 'distribution' which is either 'normal' or 'uniform'. An optional entry 'parameters' contains 
        a dictionary with keyword arguments passed to either sample_one_value_from_normal_distribution (multiplicator) or 
        sample_one_value_from_uniform_distribution (a, b, center_around_value). See example in test_sample_coefficients_mixed_distr.
        """
        if distribution == 'normal':
            return self.sample_values_from_normal_distribution(**kwargs)
        elif distribution == 'uniform':
            return self.sample_values_from_uniform_distribution(**kwargs)
        elif distribution is None: 
            if not isinstance(distribution_dictionary, dict):
                raise TypeError, "Either argument 'distribution' or argument 'distribution_dictionary' must be not None."
            # Every coefficient can have different distribution
            new_coef = self.copy_and_truncate(arange(self.size()))
            for name, args in distribution_dictionary.iteritems():
                idx = ematch(self.get_names(), name)
                if idx.size <= 0:
                    logger.log_warning('Coefficient %s not found. Sampling for this coefficient ignored.' % name)
                    continue
                if 'distribution' not in args.keys():
                    logger.log_warning("The sampling dictionary for coefficient %s must contain the entry 'distribution'. Sampling for this coefficient ignored." % name)
                    continue
                pars = {}
                if 'parameters' in args:
                    pars = args['parameters']
                if args['distribution'] == 'normal':
                    new_coef.values[idx] = self.sample_one_value_from_normal_distribution(idx, **pars)
                elif args['distribution'] == 'uniform':
                    new_coef.values[idx] = self.sample_one_value_from_uniform_distribution(idx, **pars)
                else:
                    logger.log_warning("Sampling from %s distribution not implemented. Sampling for %s ignored.", (args['distribution'], name))
            return new_coef
        raise ValueError("Sampling from %s distribution not implemented." % distribution)
        
    def sample_values_from_uniform_distribution(self, a=0.5, b=0.5, center_around_value=True):
        """Return a copy of self, where values are sampled from uniform distribution.
        If 'center_around_value' is True, the distribution is U(x-a,x+b) where x are values 
        of the coefficients. Otherwise, the distribution is U(a,b).
        """
        values = self.get_values()
        
        def draw_rn (x, n):
            return uniform(x-a, x+b, size=n)
        
        if center_around_value:
            sampled_values = apply_along_axis(draw_rn, 1, values[:,newaxis], 1).reshape((values.size,)).astype(values.dtype)
        else:                        
            sampled_values = uniform(a, b, size= values.size).astype(values.dtype)

        new_coef = self.copy_and_truncate(arange(self.size()))
        new_coef.set_values(sampled_values)
        return new_coef
    
    def sample_one_value_from_uniform_distribution(self, index, a=0.5, b=0.5, center_around_value=True):
        x = self.get_values()[index]
        if center_around_value:
            return uniform(x-a, x+b, size=1)[0]
        else:
            return uniform(a, b, size=1)[0]
        
    def sample_values_from_normal_distribution(self, multiplicator=1):
        """Return a copy of self, where values are sampled from normal distribution
           with means equal to values of self and standard deviation equal to
           standard error of self multiplied by 'multiplicator'.
        """
        values = self.get_values()
        se = self.get_standard_errors()

        def draw_rn (mean_var, n):
            if mean_var[1] == 0:
                return resize(array([mean_var[0]]), n)
            return normal(mean_var[0], mean_var[1], size=n)
        sampled_values = apply_along_axis(draw_rn, 0,
                                          (values, multiplicator*se), 1).reshape((values.size,)).astype(values.dtype)
        new_coef = self.copy_and_truncate(arange(self.size()))
        new_coef.set_values(sampled_values)
        return new_coef

    def sample_one_value_from_normal_distribution(self, index, multiplicator=1):
        x = self.get_values()[index]
        se = self.get_standard_errors()[index]
        if se == 0:
            return x
        return normal(x, multiplicator*se, size=1)[0]
    
    def is_invalid(self):
        for to_check in [
                self.other_info[-2]['Adjusted R-Squared'],
                self.other_info[-2]['R-Squared'],
                self.other_measures['t_statistic'][0],
                self.other_measures['t_statistic'][1],
                self.standard_errors[0],
                self.standard_errors[1],
                self.values[0],
                self.values[1],
                ]:
            if str(to_check) == str(nan):
                break
        else:
            return False

        return True

    def flush_coefficients(self, table_name, storage=None):
        if storage is None:
            simstate = SimulationState()
            storage = StorageFactory().get_storage('flt_storage', subdir='store',
                storage_location=simstate.get_current_cache_directory())
        self.write(out_storage=storage, out_table_name=table_name)

class CoefLengthException(Exception):
    def __init__(self, name):
        self.args = "Something is wrong with the size of the coefficient object " + name + "!"

#Functions
def create_coefficient_from_specification(specification, constant=1.0):
    names = specification.get_coefficient_names()
    values = resize(array([constant]), names.size,)
    return Coefficients(names=names, values=values, submodels=specification.get_submodels())

from opus_core.tests import opus_unittest
from numpy import ma
class CoefficientsTests(opus_unittest.OpusTestCase):
    def test_make_tex_table(self):
        coef = Coefficients(names=array(["coef1", "coef2"]), values = array([0.5, 0.00001]),
                             standard_errors=array([0.02, 0.0000001]),
                             other_measures={"t_stat":array([2.5, 4.99999])})
        from tempfile import mktemp
        tmp_file_prefix = mktemp()
        try:
            coef.make_tex_table(tmp_file_prefix)
        finally:
            os.remove('%s.tex' % tmp_file_prefix)

    def test_sample_normal_coefficients(self):
        """Coefficients are sampled from N(x, sd=2*se), where x is the coefficient value and se is coefficient standard error."""
        coef_values = array([0.5, -0.00001], dtype="float32")
        se = array([0.02, 0.0000001])
        multiplicator = 2
        coef = Coefficients(names=array(["coef1", "coef2"]), values = coef_values,
                             standard_errors = se,
                             other_measures={"t_stat":array([2.5, 4.99999])})


        new_coef = coef.sample_values(distribution='normal', multiplicator=multiplicator)
        values = new_coef.get_values()
        should_be = coef_values
        std = multiplicator*se

        for i in range(values.size):
            self.assertEqual(ma.allclose(new_coef.get_values()[i], should_be[i], atol=3*std[i]), True)
        # check data type
        self.assert_(values.dtype.name == "float32", msg = "Error in coefficients data type.")
        
    def test_sample_uniform_coefficients(self):
        """Coefficients are sampled from U(x-0.5, x+0.5), where x is the coefficient value."""
        
        from opus_core.third_party.pstat import chisqprob
        coef_values = array([0.5, -0.00001], dtype="float32")
        coef = Coefficients(names=array(["coef1", "coef2"]), values = coef_values)

        # for each coefficient run a one-sided Chi^2 test
        expected_values = coef_values
        TS = zeros(coef_values.size)
        df = 9
        significance_level = 0.05
        for j in range(df+1):
            new_coef = coef.sample_values(distribution='uniform')
            values = new_coef.get_values()
            TS += ((values - expected_values)**2)/expected_values
            
        for i in range(values.size):
            prob = chisqprob(TS[i], df)
            if (prob < significance_level/2.0):
                self.fail(msg="prob=%f is not in [%f,%f]" % (prob, significance_level/2.0, 1-significance_level/2.0))
 
        # check data type
        self.assert_(values.dtype.name == "float32", msg = "Error in coefficients data type.")

    def test_sample_uniform_0_1_coefficients(self):
        """ All coefficients are sampled from U(5,10). """
        
        from opus_core.third_party.pstat import chisqprob
        coef_values = array([0,0], dtype="float32")
        coef = Coefficients(names=array(["coef1", "coef2"]), values = coef_values)

        # for each coefficient run a one-sided Chi^2 test
        expected_values = array([7.5, 7.5])
        TS = zeros(coef_values.size)
        df = 9
        significance_level = 0.05
        for j in range(df+1):
            new_coef = coef.sample_values(distribution='uniform', center_around_value=False, a=5, b=10)
            values = new_coef.get_values()
            TS += ((values - expected_values)**2)/expected_values
            
        for i in range(values.size):
            prob = chisqprob(TS[i], df)
            if (prob < significance_level/2.0):
                self.fail(msg="prob=%f is not in [%f,%f]" % (prob, significance_level/2.0, 1-significance_level/2.0))
                
    def test_sample_coefficients_mixed_distr(self):
        """ 2 coefficients are sampled from different distributions, one stays the same. """
        
        from opus_core.third_party.pstat import chisqprob
        coef_values = array([1, 0.5, 0.2], dtype="float32")
        se = array([0, 0.02, 0.001], dtype="float32")
        coef = Coefficients(names=array(["coef_uniform", "coef_const", "coef_normal"]), values = coef_values,
                            standard_errors = se)
        sampling_dict = {"coef_uniform": {"distribution": "uniform",
                                          "parameters": {"a": 1, "b": 1}
                                          },
                        "coef_normal": {"distribution": "normal",
                                        "parameters": {"multiplicator": 10}
                                          }
                        }
        # for coefficient 1 and 3 run a one-sided Chi^2 test
        expected_values = coef_values
        TSU = 0
        TSN = 0
        df = 9
        significance_level = 0.05
        for j in range(df+1):
            new_coef = coef.sample_values(distribution_dictionary=sampling_dict)
            values = new_coef.get_values()
            TSU += ((values[0] - expected_values[0])**2)/expected_values[0]
            TSN += ((values[2] - expected_values[2])/(se[2]*10))**2
            self.assertEqual(ma.allclose(new_coef.get_values()[1], expected_values[1]), True)
            
        prob = chisqprob(TSU, df)
        if (prob < significance_level/2.0):
            self.fail(msg="prob=%f is not in [%f,%f]" % (prob, significance_level/2.0, 1-significance_level/2.0))
        prob = chisqprob(TSN, df)
        if (prob < significance_level/2.0):
            self.fail(msg="prob=%f is not in [%f,%f]" % (prob, significance_level/2.0, 1-significance_level/2.0))
                
if __name__=="__main__":
    opus_unittest.main()