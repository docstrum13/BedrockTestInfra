"""
Bedrock Stack: Sets up Bedrock agent and IAM roles
This creates your AI agent and permissions
"""

from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_kms as kms,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct

class BedrockStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, config: dict, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        self.config = config
        
        # Create KMS key for encryption
        self.kms_key = kms.Key(
            self, "KMSKey",
            description=f"KMS key for {config['project_name']} - {config['environment']}",
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Create IAM role for Lambda functions
        self.lambda_role = iam.Role(
            self, "LambdaRole",
            role_name=f"{config['project_name']}-lambda-role-{config['environment']}",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AWSXRayDaemonWriteAccess")
            ],
            inline_policies={
                "BedrockAccess": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "bedrock:InvokeAgent",
                                "bedrock:GetAgent",
                                "bedrock:ListAgents"
                            ],
                            resources=["*"]
                        )
                    ]
                ),
                "KMSAccess": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            effect=iam.Effect.ALLOW,
                            actions=[
                                "kms:Encrypt",
                                "kms:Decrypt",
                                "kms:GenerateDataKey"
                            ],
                            resources=[self.kms_key.key_arn]
                        )
                    ]
                )
            }
        )
        
        # Note: Bedrock Agent creation is typically done through the console
        # We'll provide placeholders for the IDs you'll get from there
        self.agent_id = "PLACEHOLDER_AGENT_ID"
        self.agent_alias_id = "PLACEHOLDER_ALIAS_ID"
        
        # Outputs
        CfnOutput(
            self, "LambdaRoleArn",
            value=self.lambda_role.role_arn,
            export_name=f"{config['project_name']}-lambda-role-arn-{config['environment']}"
        )