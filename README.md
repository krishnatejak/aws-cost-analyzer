# AWS Cost Analyzer

A comprehensive tool for analyzing AWS costs across accounts, providing insights, and suggesting optimizations. This tool combines AWS Cost Explorer data with CloudWatch metrics to provide actionable recommendations for cost optimization.

## Features

### 1. Cost Analysis
- Tag-based cost categorization
- Service-level cost breakdown
- Month-over-month and day-over-day trend analysis
- Cost anomaly detection
- Resource utilization tracking

### 2. Visualization Dashboard
- Interactive cost trends
- Service distribution charts
- Tag-based cost distribution
- Anomaly highlighting
- Real-time cost monitoring

### 3. Cost Optimization
- AI-powered recommendations
- Resource rightsizing suggestions
- Reserved Instance optimization
- Graviton migration opportunities
- Idle resource detection

## Prerequisites

1. AWS Account with appropriate permissions
   - Cost Explorer access
   - CloudWatch access
   - Organizations access (for multi-account setup)

2. Python 3.8+
3. Node.js 16+
4. AWS CLI configured

## Installation

1. Clone the repository:
```bash
git clone https://github.com/krishnatejak/aws-cost-analyzer.git
cd aws-cost-analyzer
```

2. Set up Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Configure AWS credentials:
```bash
aws configure
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

1. Start the backend server:
```bash
python app.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Access the dashboard at http://localhost:3000

## Project Structure

```
aws-cost-analyzer/
├── backend/
│   ├── app.py                 # Flask application
│   ├── cost_analyzer.py       # Main analysis logic
│   ├── utils/
│   │   ├── aws_utils.py      # AWS API helpers
│   │   └── data_utils.py     # Data processing utilities
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/           # Custom React hooks
│   │   └── utils/           # Frontend utilities
│   └── package.json
└── requirements.txt
```

## Configuration

The tool can be configured through environment variables or a config file:

```yaml
# config.yaml
aws:
  regions:
    - us-east-1
    - eu-west-1
  accounts:
    - name: Production
      id: "123456789012"
    - name: Development
      id: "987654321098"

analysis:
  anomaly_threshold: 20
  utilization_threshold: 40
  report_schedule: "daily"
```

## Recommendations Engine

The recommendations are generated based on several data sources and best practices:

1. AWS Well-Architected Framework guidelines
2. Resource utilization patterns
3. AWS pricing models comparison
4. Historical usage patterns
5. CloudWatch metrics analysis

Recommendations include:
- Instance rightsizing based on CPU/memory utilization
- Graviton migration opportunities based on workload compatibility
- Reserved Instance and Savings Plan opportunities
- Idle resource identification
- Storage class optimization

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- AWS Cost Explorer API
- AWS CloudWatch API
- React and Recharts for visualization
