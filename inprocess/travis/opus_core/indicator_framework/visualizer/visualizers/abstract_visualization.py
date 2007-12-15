

class Visualization(object):
    def get_file_extension(self):
        '''Returns the file extension of the outputted indicator 
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('abstract_image_type.get_file_extension needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)

    def get_visualization_shorthand(self):
        '''Returns the shorthand for this output type
        
           Abstract method that needs to be overridden in child classes.
        '''
        message = ('abstract_image_type.get_visualization_shorthand needs '
                   'to be overridden by child class.')
        raise NotImplementedError(message)
            
    def get_additional_metadata(self):
        '''returns additional attributes
        
           Child method should override this method if there are any 
           additional attributes that it has. Return a list of
           (attr_name,value) tuples.
        '''
        return []