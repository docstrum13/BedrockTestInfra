"""
Unit tests for CDK stacks
"""

import aws_cdk as cdk
from aws_cdk.assertions import Template
from stacks.vpc_stack import VpcStack
from stacks.bedrock_stack import BedrockStack

def test_vpc_stack_creates_vpc():
    """Test that VPC stack creates a VPC"""
    app = cdk.App()
    config = {
        'project_name': 'test-app',
        'environment': 'test',
        'vpc_cidr': '10.0.0.0/16',
        'max_azs': 2
    }
    
    stack = VpcStack(app, "TestVpcStack", config=config)
    template = Template.from_stack(stack)
    
    # Check that a VPC is created
    template.has_resource_properties("AWS::EC2::VPC", {
        "CidrBlock": "10.0.0.0/16"
    })

def test_bedrock_stack_creates_role():
    """Test that Bedrock stack creates IAM role"""
    app = cdk.App()
    config = {
        'project_name': 'test-app',
        'environment': 'test'
    }
    
    stack = BedrockStack(app, "TestBedrockStack", config=config)
    template = Template.from_stack(stack)
    
    # Check that an IAM role is created
    template.has_resource_properties("AWS::IAM::Role", {
        "AssumeRolePolicyDocument": {
            "Statement": [{
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }]
        }
    })