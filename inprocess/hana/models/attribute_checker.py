from opus_core.models.model import Model
from opus_core.logger import logger
class CheckAttributeModel(Model):
    model_name = 'Check Attribute Model'
    def run(self, dataset, attribute):
        logger.log_status("Stats for attribute %s:" % attribute, 
                            '\n\tmin\t:', dataset[attribute].min(), 
                            '\n\taverage\t:', dataset[attribute].mean(), 
                            '\n\tmax\t:', dataset[attribute].max())
