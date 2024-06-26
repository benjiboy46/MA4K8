# MA4K8
MA4K8 Project Code

This repository contains all necessary code for Benjamin McIntyre's MA4K8 Project for the University of Warwick, UK.

Built upon the NDlib python library.

Files named graphWHK.py, graphOWNMODEL.py and graphFJ.py initialise the network on which to run the opinion dynamics model.

Files AdaptedFJ.py, AdaptedWHK.py and OwnModel.py contain the opinion dynamics models. The AdaptedWHK.py has referenced the author of the original code, which I have adapted. The other files are my own.

Note that AdaptedFJ refers to the Adapted DeGroot Model - it is called FJ after the Friedkin-Johnsen model. The Adapted DeGroot Model can also be interpreted as an adapted Friedkin-Johnsen model, hence the name. 

The file parameter.py contains all the necessary parameters for the networks.

Files runMODELS.py, test.py and resultsplotter.py are used for running the models and outputting data.

customcolour.py is a small edit on authors original code - just to change colour scheme for plots.

The orginal author mentioned is __author__ = 'Cecilia Toccaceli'
