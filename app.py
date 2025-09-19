#!/usr/bin/env python3
"""
Main CDK application entry point
This file orchestrates all your stacks
"""

import aws_cdk as cdk
import yaml
import os
from stacks.vpc_stack import VpcStack
from stacks.bedrock_stack import BedrockStack
from stacks.api_stack import ApiStack
from stacks.monitoring_stack import MonitoringStack

# Load configuration based on environment
environment = os.environ.get('CDK_ENV', 'dev')
config_file = f'config/{environment}.yaml'

with open(config_file, 'r') as f:
    config = yaml.safe_load(f)

app = cdk.App()

# Get AWS account and region from environment or use defaults
env = cdk.Environment(
    account=os.environ.get('CDK_DEFAULT_ACCOUNT'),
    region=os.environ.get('CDK_DEFAULT_REGION', 'us-east-1')
)

# Create stacks in dependency order
vpc_stack = VpcStack(
    app, 
    f"{config['project_name']}-vpc-{environment}",
    config=config,
    env=env
)

bedrock_stack = BedrockStack(
    app,
    f"{config['project_name']}-bedrock-{environment}",
    config=config,
    env=env
)

api_stack = ApiStack(
    app,
    f"{config['project_name']}-api-{environment}",
    vpc=vpc_stack.vpc,
    bedrock_agent_id=bedrock_stack.agent_id,
    bedrock_agent_alias_id=bedrock_stack.agent_alias_id,
    lambda_role=bedrock_stack.lambda_role,
    kms_key=bedrock_stack.kms_key,
    config=config,
    env=env
)

monitoring_stack = MonitoringStack(
    app,
    f"{config['project_name']}-monitoring-{environment}",
    api_stack=api_stack,
    bedrock_stack=bedrock_stack,
    config=config,
    env=env
)

app.synth()