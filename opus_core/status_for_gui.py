# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array, concatenate

class StatusForGui:
    def __init__(self, model):
        self.status_file_for_gui = None
        self.model = model
        
    def initialize_pieces(self, number_of_pieces, pieces_description=None):
        self.total_number_of_pieces = number_of_pieces
        self.current_piece = 0
        self.pieces_description = pieces_description
        if self.pieces_description is None:
            self.pieces_description = array(self.total_number_of_pieces*[''])
            
    def update_pieces_using_submodels(self, submodels, leave_pieces=0):
        if self.status_file_for_gui is not None:
            npieces = len(submodels)
            self.total_number_of_pieces = npieces+leave_pieces
            self.current_piece = 0
            self.pieces_description = concatenate((self.pieces_description[0:leave_pieces], 
                                                            array(map(lambda x: 'submodel: %s' % x, submodels))))
            self.write_status_for_gui()
                    
    def _increment_current_piece(self):
        if self.status_file_for_gui is not None:
            self.current_piece += 1
            self.write_status_for_gui()
        
    def get_total_number_of_pieces(self):
        return self.total_number_of_pieces
    
    def get_current_piece(self):
        return self.current_piece
    
    def get_current_piece_description(self):
        return self.pieces_description[self.get_current_piece()]
    
    def _get_total_pieces_from_model(self):
        return self.model._get_status_total_pieces()
    
    def _get_current_piece_from_model(self):
        return self.model._get_status_current_piece()
        
    def _get_piece_description_from_model(self):
        return self.model._get_status_piece_description()
    
    def set_model_system_parameters(self, current_year=0, total_number_of_models=1, number_of_current_model=1, status_file_for_gui=None):
        self.status_file_for_gui = status_file_for_gui
        if self.status_file_for_gui is not None:
            self.status_current_year = current_year
            self.status_total_number_of_models = total_number_of_models
            self.status_number_of_current_model = number_of_current_model  
            
    def write_status_for_gui(self):
        # Write a status file for each model run.
        # The GUI uses this to update a progress bar.  The file is ascii, with
        # the following format (1 item per line):
        #   current year
        #   total number of models
        #   number of current model that is about to run (starting with 0)
        #   name of current model
        #   total number of pieces of current model (could be 1)
        #   number of current piece
        #   description of current piece (empty string if no description)
        if self.status_file_for_gui is not None:
            status = '%d\n%d\n%d\n%s\n%d\n%d\n%s\n' % (self.status_current_year, self.status_total_number_of_models, 
                                                       self.status_number_of_current_model, self.model.name(), 
                                                       self._get_total_pieces_from_model(), self._get_current_piece_from_model(), 
                                                       self._get_piece_description_from_model())
            f = open(self.status_file_for_gui, 'w')
            f.write(status)
            f.close()