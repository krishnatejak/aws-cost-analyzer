# AWS Cost Analyzer

A comprehensive tool for analyzing AWS costs across services with AI-powered recommendations

## Features

- Cost analysis across all AWS services
- Resource utilization tracking
- AI-powered optimization recommendations
- Interactive visualizations
- Custom reporting

## Installation

1. Clone the repository:
```bash
git clone https://github.com/krishnatejak/aws-cost-analyzer.git
cd aws-cost-analyzer
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Configure AWS credentials:
```bash
aws configure
```

## Usage

1. Start the backend server:
```bash
cd backend
python app.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Access the dashboard at http://localhost:3000

## Architecture

The application consists of:

1. Backend Services:
   - Cost Analysis Engine
   - Resource Utilization Tracker
   - ML-powered Recommendation Engine
   - Service-specific Analyzers

2. Frontend Components:
   - Interactive Dashboards
   - Cost Visualization
   - Recommendation Display
   - Export Capabilities

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.