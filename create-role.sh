#!/bin/sh

#This Script creates a Lambda role and attaches the policies

#Settings
. ./common-variables.sh

#Setup Lambda Role
role_name=lambda-mongo-data-api
aws iam create-role --role-name ${role_name} \
    --assume-role-policy-document file://../../IAM/assume-role-lambda.json \
    --profile $profile || true

#Add and attach cloudwatch_policy
cloudwatch_policy=AWSLambdaBasicExecutionRole
role_policy_arn="arn:aws:iam::aws:policy/service-role/${cloudwatch_policy}"
aws iam attach-role-policy \
    --role-name "${role_name}" \
    --policy-arn "${role_policy_arn}"  --profile ${profile} || true