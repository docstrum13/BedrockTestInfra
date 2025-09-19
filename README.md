# README.md
# My Bedrock CDK Project

This project uses AWS CDK to create a backend infrastructure for a Bedrock agent that will be consumed by an Angular SPA.

## Architecture Overview

- **VPC**: Private network for secure communication
- **API Gateway**: REST API endpoint for the frontend
- **Lambda Functions**: Handle requests and interact with Bedrock
- **Bedrock Agent**: AI agent for answering questions and performing tasks
- **CloudWatch**: Monitoring and alerting

## Project Structure

```
my-bedrock-project/
├── app.py                          # Main CDK app
├── stacks/                         # CDK stack definitions
├── lambda_functions/               # Lambda function code
├── config/                         # Environment configurations
└── scripts/                        # Deployment scripts
```

## Prerequisites

1. AWS CLI configured with SSO
2. Python 3.8+
3. Node.js (for CDK)
4. Bedrock Agent created in AWS Console

## Setup Instructions

1. **Clone and setup environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure your Bedrock Agent IDs:**
   - Update `stacks/bedrock_stack.py` with your actual agent ID and alias ID

3. **Update configuration:**
   - Edit `config/dev.yaml` with your email for alerts
   - Adjust other settings as needed

4. **Deploy:**
   ```bash
   # First time setup
   cdk bootstrap --profile your-aws-profile

   # Deploy to dev environment
   AWS_PROFILE=your-aws-profile ./scripts/deploy.sh dev
   ```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /bedrock/chat` - Chat with Bedrock agent

## Environment Variables

The Lambda functions use these environment variables:
- `BEDROCK_AGENT_ID` - Your Bedrock agent ID
- `BEDROCK_AGENT_ALIAS_ID` - Your Bedrock agent alias ID
- `ENVIRONMENT` - Current environment (dev/staging/prod)

## Monitoring

CloudWatch dashboards and alarms are automatically created to monitor:
- Lambda function errors and duration
- API Gateway request count and latency
- Email notifications for critical issues