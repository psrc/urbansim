# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from numpy import sort, where, array, logical_or, ones

class JobDataset(UrbansimDataset):
    """Set of jobs."""

    id_name_default = "job_id"
    in_table_name_default = "jobs"
    out_table_name_default = "jobs"
    dataset_name = "job"

    def get_home_based_jobs(self, index):
        home_based = self.get_attribute_by_index("is_home_based_job", index)
        return index[home_based > 0]

    def get_non_home_based_jobs(self, index):
        home_based = self.get_attribute_by_index("is_home_based_job", index)
        return index[home_based == 0]

    def is_in_sector(self, sectors, index):
        return array(map(lambda x: x in sectors, self.get_attribute_by_index("sector_id", index)))

    def get_home_based_jobs_of_sectors(self, sectors, index):
        home_based = self.get_home_based_jobs(index)
        in_sectors = self.is_in_sector(sectors, home_based)
        return home_based[in_sectors > 0]

    def get_non_home_based_jobs_of_sectors(self, sectors, index):
        non_home_based = self.get_non_home_based_jobs(index)
        in_sectors = self.is_in_sector(sectors, non_home_based)
        return non_home_based[in_sectors > 0]

    def get_non_home_based_commercial_jobs_of_sectors(self, sectors, index):
        """Variable 'is_commercial' must be computed before calling this method.
        Returns indices of jobs that are non-home based commercial of the given sectors.
        """
        non_home_based_in_sectors = self.get_non_home_based_jobs_of_sectors(sectors, index)
        is_commercial = self.get_attribute_by_index("is_commercial", non_home_based_in_sectors)
        return non_home_based_in_sectors[is_commercial.astype("bool8")]

    def get_non_home_based_commercial_jobs(self, index):
        """Variable 'is_commercial' must be computed before calling this method.
        Returns indices of jobs that are non-home based commercial.
        """
        non_home_based = self.get_non_home_based_jobs(index)
        is_commercial = self.get_attribute_by_index("is_commercial", non_home_based)
        return non_home_based[is_commercial.astype("bool8")]

    def get_non_home_based_industrial_jobs_of_sectors(self, sectors, index):
        """Variable 'is_industrial' must be computed before calling this method.
        Returns indices of jobs that are non-home based industrial of the given sectors.
        """
        non_home_based_in_sectors = self.get_non_home_based_jobs_of_sectors(sectors, index)
        is_industrial = self.get_attribute_by_index("is_industrial", non_home_based_in_sectors)
        return non_home_based_in_sectors[is_industrial.astype("bool8")]

    def get_non_home_based_industrial_jobs(self, index):
        """Variable 'is_industrial' must be computed before calling this method.
        Returns indices of jobs that are non-home based industrial.
        """
        non_home_based = self.get_non_home_based_jobs(index)
        is_industrial = self.get_attribute_by_index("is_industrial", non_home_based)
        return non_home_based[is_industrial.astype("bool8")]

    def get_non_home_based_jobs_of_elc_sectors(self, index, resources=None):
        self.compute_variables([
            "urbansim.job.is_in_elc_sector_group"], resources=resources)
        index2 = self.get_non_home_based_jobs(index)
        is_in_elc = self.get_attribute_by_index("is_in_elc_sector_group", index2)
        return index2[is_in_elc > 0]

    def get_non_home_based_jobs_of_scalable_sectors(self, index, resources=None):
        self.compute_variables([
            "urbansim.job.is_in_scalable_sector_group",
            "urbansim.job.is_governmental"], resources=resources)
        index2=self.get_non_home_based_jobs(index)
        is_in = self.get_attribute_by_index("is_in_scalable_sector_group", index2)
        is_gov = self.get_attribute_by_index("is_governmental", index2)
        return index2[logical_or(is_in,is_gov)]

    def get_jobs_of_scalable_sectors(self, index, resources=None):
        self.compute_variables([
            "urbansim.job.is_in_scalable_sector_group"],
                resources=resources)
        is_in = self.get_attribute_by_index("is_in_scalable_sector_group", index)
        return index[is_in > 0]

    def get_home_based_jobs_of_elc_sectors(self, index, resources=None):
        self.compute_variables([
            "urbansim.job.is_in_elc_sector_group"], resources=resources)
        index2 = self.get_home_based_jobs(index)
        is_in_elc = self.get_attribute_by_index("is_in_elc_sector_group", index2)
        return index2[is_in_elc > 0]

    def divide_into_hb_nhb_scalable(self, index, sectors_hb, sectors_nhbcom, sectors_nhbind, resources=None):
        """ Divide jobs given by index into jobs for the ELCM HB, ELCM NHB Commercial, ELCM NHB Industrial
        and the Scaling model. The indices of these jobs are returned in a dictionary.
        """
        result={}
        self.compute_variables(["urbansim.job.is_commercial",
                                "urbansim.job.is_industrial"], resources=resources)
        non_scaling_jobs = -1*ones((self.size(),))
        non_scaling_jobs[index] = 0
        if sectors_hb is not None:
            if sectors_hb.size <= 0: # no sector distinction
                hb = self.get_home_based_jobs(index)
            else:
                hb = self.get_home_based_jobs_of_sectors(sectors_hb, index)
            non_scaling_jobs[hb] = 1
        else:
            hb = None
        if sectors_nhbcom is not None:
            if sectors_nhbcom.size <= 0:
                nhbcom = self.get_non_home_based_commercial_jobs(index)
            else:
                nhbcom = self.get_non_home_based_commercial_jobs_of_sectors(sectors_nhbcom, index)
            non_scaling_jobs[nhbcom] = 1
        else:
            nhbcom = None
        if sectors_nhbind is not None:
            if sectors_nhbind.size <= 0:
                nhbind = self.get_non_home_based_industrial_jobs(index)
            else:
                nhbind = self.get_non_home_based_industrial_jobs_of_sectors(sectors_nhbind, index)
            non_scaling_jobs[nhbind] = 1
        else:
            nhbind = None

        result["home_based"] = hb
        result["commercial"] = nhbcom
        result["industrial"] = nhbind
        result["scalable"] = where(non_scaling_jobs == 0)[0]
        return result