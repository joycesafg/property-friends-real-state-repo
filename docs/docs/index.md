# property-friends-real-state documentation!

## Description

The goal of the project is to build a pipeline to train and deploy a ML Model ensuring reproducibility and scalability

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `aws s3 sync` to recursively sync files in `data/` up to `s3://model-datasets/data/`.
* `make sync_data_down` will use `aws s3 sync` to recursively sync files from `s3://model-datasets/data/` to `data/`.


