"""
VPC Stack: Creates network infrastructure
This sets up your private network in AWS
"""

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput
)
from constructs import Construct

class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, config: dict, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        self.config = config
        
        # Create VPC
        self.vpc = ec2.Vpc(
            self, "VPC",
            vpc_name=f"{config['project_name']}-vpc-{config['environment']}",
            ip_addresses=ec2.IpAddresses.cidr(config['vpc_cidr']),
            max_azs=config['max_azs'],
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                )
            ],
            enable_dns_hostnames=True,
            enable_dns_support=True
        )
        
        # Output VPC ID
        CfnOutput(
            self, "VpcId",
            value=self.vpc.vpc_id,
            export_name=f"{config['project_name']}-vpc-id-{config['environment']}"
        )