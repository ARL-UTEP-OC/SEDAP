rulesToPy.py

This file will take formatted WEKA output (after generating a classifier) and create python equivalent model files that can be used in the GUI.

Steps:

1. Generate a classifier (REPTree and J48 have been tested) and save the output buffer.
2. Modify the output buffer so that only the classification tree is present in the file
3. execute the following:
	python rulesToPy.py sampleInput.xml  > <output filename>.py
	
The resulting file should be used as the Model input file in the GUI
