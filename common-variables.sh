#!/bin/sh
export profile="demo"
export region="eu-west-1"
export aws_account_id=$(aws sts get-caller-identity --query 'Account' --profile $profile | tr -d '\"')
#export aws_account_id="000000000000"
export template="lambda-mongo-data-api"
export bucket="<your-bucket>"
export prefix="tmp/sam"
export python_version="python3.6"
export source_build_folder=../../build
export target_package_folder=../../package

#Lambda variables
export lambda_folder=../../lambda_mongo
export lambda_file="lambda_crud_mongo_records.py"
export lambda_creds="mongo_config.py"

#Layers variables
export packages_path=~/tmp/lambda_package/lib # venv package location
export bash_dir=$(pwd) # current bash root directory
export layers_zip_file="mongodb-layer.zip"
export target_layer_path=${source_build_folder}/python/lib/${python_version}/site-packages
export zip_file="lambda-mongo-data-api.zip"
export layer_name="aws_mongo"
export layer_version=4