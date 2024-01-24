# seng_kedro

## Overview

This is a Kedro pipeline developed to use the modules developed

## Configuring Great Expectations and Mlflow

install great-expectations and mlflow 

`pip install great-expectations`

`pip install kedro-mlflow`

### Great Expectations setup

### Mlflow setup 

- Run `kedro mlflow init`
- Configure `conf/local/mlflow.yml`

## TO DO List

[] Develop testing
[x] Use great-expectations hooks 
[x] Create pipelines without kedro's autoregister
[x] Use mlflow
[] Multiple experiments
[] Remove debug runs from Kedro Tracking

## Follow up 

* Dynamic Pipelines: https://github.com/kedro-org/kedro/issues/2627
* Multiple experiments: https://github.com/kedro-org/kedro/issues/1606