Hi!

This is a simple script to convert raw hand history files into ACR-style format. The converted files will be saved in a `converted_hands` directory within the same directory as the raw hand history files. If any errors occur, they will be logged to a `error_log.txt` file in the same directory as the raw hand history files. 


# Initial Setup
To install the required dependencies, run `conda env create -f environment.yaml` in your terminal. You only have to run this once on each machine. 

#Running
To use it, run `conda activate poker-env` to activate the environment and then run `python convert.py` If you're running this using the "Run" button in VSCode, make sure to select the `poker-env` interpreter using the 'Select Interpreter' command in the command palette.

You will be prompted to select the raw hand history files directory using a file dialog.





