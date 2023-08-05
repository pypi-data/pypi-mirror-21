[![travis-CI](https://travis-ci.org/eltonlaw/impyute.svg?branch=master)](https://travis-ci.org/eltonlaw/impyute)


# impyute

impyute is a library of missing data imputation algorithms written in Python 3. This library was designed to be super lightweight, here's a sneak peak at what impyute can do. 

``` python3
>>> from impyute.datasets import random_uniform
>>> raw_data = random_uniform(shape=(5, 5), missingness="mcar", th=0.2)
>>> print(raw_data)
[[  1.   0.   4.   0.   1.]
 [  1.  nan   6.   4.  nan]
 [  5.   0.  nan   1.   3.]
 [  2.   1.   5.   4.   6.]
 [  2.   1.   0.   0.   6.]]
>>> from impyute.imputations.cs import mean_imputation   
>>> complete_data = random_imputation(raw_data) 
>>> print(complete_data)
[[ 1.    0.    4.    0.    1.  ]
 [ 1.    0.5   6.    4.    4.  ]
 [ 5.    0.    3.75  1.    3.  ]
 [ 2.    1.    5.    4.    6.  ]
 [ 2.    1.    0.    0.    6.  ]]
```

## Features

* Imputation of Cross Sectional Data
    * Multivariate Imputation by Chained Equations
    * Expectation Maximization
    * Mean Imputation
    * Mode Imputation
    * Median Imputation
    * Random Imputation
* Imputation of Time Series Data
    * Autoregressive Integrated Moving Average
    * Expectation Maximization with the Kalman Filter
    * Last Observation Carried Forward
* Raw and Complete Dataset Generation
* Diagnostic Tools
    * Loggers
    * Dataset Properties


## Install

To install impyute, run the following:

``` shell
$ pip install impyute
```

## Documentation

Documentation is available here: http://impyute.readthedocs.io/

## Contributing

Check out https://github.com/eltonlaw/impyute/blob/master/CONTRIBUTING.md


