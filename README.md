# python-data-science
This repo contains Python examples for the "Data Programming" Introductory 
course of the [MSc Program of Data Science](http://msc-data-science.iit.demokritos.gr), organzied by NCSR Demokritos and the University of the Peloponnese. 

## Notebooks
The following notebooks can be used as short tutorials on the respective subjects

 1. Python basics: [1-intro-to-python.ipynb](https://nbviewer.jupyter.org/github/tyiannak/python-data-science/blob/master/notebooks/1-intro-to-python.ipynb])
 2. Intro to numpy and pandas for basic data handling [2-numpy_and_pandas.ipynb](https://nbviewer.jupyter.org/github/tyiannak/python-data-science/blob/master/notebooks/2-numpy_and_pandas.ipynb])
 3. Visualization using matplotlib and plotly [3-visualization.ipynb](https://nbviewer.jupyter.org/github/tyiannak/python-data-science/blob/master/notebooks/3-visualization.ipynb])

## Scripts   
The following scripts are 
 1. `scripts/cl_example.py` demonstrates how to use `argparse` to use command-line arguments in a python script. 
 The particular example generates a visualization of a list of Gaussian distributions. Usage example:
 ```python
python3 cl_example.py -m 0 5 10 15 20 -s 1 1 1 7 2 -n 5000 5000 5000 10000 5000 --names "x1" "x2" "x3" "x4" "x5" -b 100 --normalize
```