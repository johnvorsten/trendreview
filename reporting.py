# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 14:13:55 2021

Create reports based on failed rules
When passed a FDDException, log the exception message, and create a graph
containing the exceptions data

@author: jvorsten
"""

# Python imports
from typing import MutableMapping
import os
import glob
import re

# Third party imports
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.dates import AutoDateLocator

# Local imports
from FDDExceptions import FDDException

# Declarations


#%%

class FDDImageGeneration:
    base_imgname = "figure"
    img_format = "png"
    
    def __init__(self, save_directory: str):
        
        if not os.path.isdir(save_directory):
            msg="Passed path is not a directory: {}".format(save_directory)
            raise ValueError(msg)
        self.save_directory = save_directory
        
        self.image_number = self.get_highest_img_number(self.save_directory)
        
        return None
    
    @classmethod
    def generate_image(cls, exception: FDDException, 
                       chart_properties: MutableMapping[str,str]):
        """
        inputs
        -------
        chart_properties: (dict) of mappings for matplotlib style configuration
        options. See https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html"""
        # Annotate data
        data = exception.data
        independent_label = data['primary_axis_label']
        dependent_labels = data['dependent_axis_labels']
        x_data = data[independent_label]
        
        # Create the image
        fig, ax = plt.subplots(1,1)
        # Set axes x and y label
        ax.set_xlabel(independent_label)
        ylabel = str()
        for label in dependent_labels:
            ylabel += ", " + label
        ax.set_ylabel(ylabel)
        # Set data
        for dependent_label in dependent_labels:
            ys = data[dependent_label]
            lines = ax.plot(x_data, ys, 
                            label=dependent_label, **chart_properties)
        
        ax.legend()
        
        # Format dates on X axis
        locator = AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        fig.autofmt_xdate()
        
        return fig
    
    def save_image(self, fig: Figure):
        
        filename = (self.save_directory + os.sep + self.base_imgname + 
                    str(self.image_number) + "." + self.img_format)
        fig.savefig(filename, dpi='figure', format=self.img_format,
                    bbox_inches='tight')
        self.image_number += 1
        
        return None
    
    @classmethod
    def get_highest_img_number(cls, save_directory: str) -> int:
        fig_number = 1
        names = glob.glob(
            (os.path.normpath(save_directory) + os.path.sep + cls.base_imgname + 
                              '[0-9]' + '.' + cls.img_format)
            )
        if len(names) == 0:
            return fig_number
        else:
            img_format = cls.img_format
            reg = re.compile('[0-9]*' + '(?=\.' + img_format + ')')
            try:
                match = reg.search(names[-1])
                fig_number = int(names[-1][match.start():match.end()])
            except:
                # Fit
                pass
            
        return fig_number


class FDDReporting:
    
    def __init__(self, log_filepath: str):
        """"""
        self.log_filepath = log_filepath
        self.log_index = 1
        # Image generation
        save_directory = os.path.split(log_filepath)[0]
        self.imageGenerator = FDDImageGeneration(save_directory)
        
        return None
    
    def log_exception(self, exception: FDDException, 
                      create_image: bool = True, 
                      chart_properties: MutableMapping[str,str] = None):
        """Given a specific failure, log the rule broken and give metadata
        on the broken rule
        inputs
        -------
        exception: (FDDException)
        create_image: (bool) When creating a log, choose to create an image
        showing data associated with log (default True)
        chart_properties: (dict) of mappings for matplotlib style configuration
        options. See https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html"""
        
        if create_image:
            img = self.imageGenerator.generate_image(exception, chart_properties)
            self.imageGenerator.save_image(img)
            
        with open(self.log_filepath, 'at+') as f:
            f.write("Issue #" + str(self.log_index) + '\n')
            f.write(exception.message + '\n')
            if create_image:
                f.write("See figure" + 
                        str(self.imageGenerator.image_number - 1) 
                        + '.png\n')
            f.write('\n\n')

        
        self.log_index += 1
        
        return None