import pygame

import math
import time
import copy
import random

class Parcel_block_vis :
    
    def __init__(self, query_manager, filename):
        pygame.init()
        
        #color info
        self.color_dict = {"red" : (255, 0, 0), "blue" : (0,0,255), "green" : (0, 255, 0), "yellow" : (255,255,0)}

        self.height = 2000 #Set eventually by checking the size of what is being mapped (will need to adjust for different coord systems)        
        self.multiplier = self.height / (query_manager.y_max - query_manager.y_min)

        x_diff = query_manager.x_max - query_manager.x_min
        self.window = pygame.display.set_mode((int(x_diff*self.multiplier), self.height))

        #Arbitrary info
        self.filename = filename
        
    #prints blocks to a map
    def print_parcels(self, query_manager):
        
        #Print rectangle that represents training area 
        block = query_manager.current_training_block

        #Making sure the rectangle stays inside the borders
        block.x_max = min(query_manager.x_max, block.x_max) 
        block.x_min = max(query_manager.x_min, block.x_min)
        block.y_max = min(query_manager.y_max, block.y_max)
        block.y_min = max(query_manager.y_min, block.y_min)
        
        x_high_tran = int((block.x_max - query_manager.x_min)*self.multiplier)
        x_low_tran = int((block.x_min - query_manager.x_min)*self.multiplier)
        y_high_tran = int(self.height - (block.y_max - query_manager.y_min)*self.multiplier)
        y_low_tran = int(self.height - (block.y_min - query_manager.y_min)*self.multiplier)
            
        rect_info = (x_low_tran, y_high_tran, x_high_tran - x_low_tran, y_low_tran - y_high_tran)
        pygame.draw.rect(self.window, self.color_dict[block.color], rect_info, 1)

        pygame.display.flip()

        #Printing each parcel as one pixel
        count = 1
        for index in range(len(query_manager.current_rows)) :
            if query_manager.is_test_list[index] :
                row = query_manager.current_rows[index]
                x_val = float(row[query_manager.x_attribute])
                y_val = float(row[query_manager.y_attribute])

                x_tran = int((x_val - query_manager.x_min)*self.multiplier)
                y_tran = int(self.height - (y_val - query_manager.y_min)*self.multiplier)

                pygame.draw.line(self.window, self.color_dict[block.color], (x_tran, y_tran), (x_tran, y_tran))
                
                count += 1
                if count % 1000 == 0 :
                    pygame.display.flip()

        pygame.display.flip()


        #Printing the block number at the bottom right of the page
        block = query_manager.current_test_block
        x_high_tran = int((block.x_max - query_manager.x_min)*self.multiplier)
        x_low_tran = int((block.x_min - query_manager.x_min)*self.multiplier)
        y_high_tran = int(self.height - (block.y_max - query_manager.y_min)*self.multiplier)
        y_low_tran = int(self.height - (block.y_min - query_manager.y_min)*self.multiplier)

        font = pygame.font.Font(None, 36) #Make relative to size of square
        text = font.render("Block: " + str(len(query_manager.used_blocks)), True, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = int((x_low_tran + x_high_tran)/2)
        textpos.centery = int((y_low_tran + y_high_tran)/2)
        
        self.window.blit(text, textpos)
        pygame.display.update()
        

    def close_image(self, log_manager):
            
        #Saving image (MAKE WORK ON WINDOWS)
        path = log_manager.folder_address + '/' + self.filename
        pygame.image.save(self.window, path + ".jpeg")   