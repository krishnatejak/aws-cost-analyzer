# AWS Cost Analyzer

A comprehensive tool for analyzing AWS costs across services with AI-powered recommendations and visualizations.

## Features

### 1. Cost Analysis
- Tag-based cost categorization
- Service-level cost breakdown
- Month-over-month and day-over-day trend analysis
- Cost anomaly detection
- Resource utilization tracking

### 2. Service-specific Analysis
- **EC2 Analysis**
  - Instance utilization metrics
  - Graviton migration opportunities
  - Reserved Instance optimization
  - Right-sizing recommendations

- **RDS Analysis**
  - Database instance metrics
  - Aurora migration opportunities
  - Storage optimization
  - Performance insights

- **Storage Analysis**
  - S3 bucket analysis
  - Lifecycle management recommendations
  - Storage class optimization
  - Access pattern analysis

- **Network Analysis**
  - VPC endpoint optimization
  - NAT gateway utilization
  - Data transfer costs
  - Transit Gateway analysis

### 3. Visualization Dashboard
- Interactive cost trends
- Service distribution charts
- Tag-based cost distribution
- Anomaly highlighting
- Real-time cost monitoring

### 4. Cost Optimization
- AI-powered recommendations
- Resource rightsizing suggestions
- Reserved Instance optimization
- Graviton migration opportunities
- Idle resource detection

## Prerequisites

1. AWS Account with appropriate permissions:
   - Cost Explorer access
   - CloudWatch access
   - Organizations access (for multi-account setup)
   - ReadOnlyAccess for services being analyzed

2. Local Development:
   - Python 3.11+
   - Node.js 18+
   - Docker and Docker Compose (optional)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/krishnatejak/aws-cost-analyzer.git
cd aws-cost-analyzer
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your AWS credentials and configuration
```

3. Start the application:
```bash
docker-compose up --build
```

The application will be available at:
- Web UI: http://localhost:80
- Backend API: http://localhost:80/api

### Manual Setup

1. Backend Setup:
```bash
# Setup Python environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Start the backend server with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 --worker-class gevent app:app
```

2. Frontend Setup:
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

## Project Structure

```
aws-cost-analyzer/
├── backend/
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration
│   ├── service_analyzers/     # Service-specific analyzers
│   │   ├── ec2_analyzer.py
│   │   ├── rds_analyzer.py
│   │   ├── storage_analyzer.py
│   │   └── network_analyzer.py
│   ├── routes/               # API routes
│   │   ├── cost_routes.py
│   │   ├── service_routes.py
│   │   └── optimization_routes.py
│   └── utils/                # Utility functions
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   ├── hooks/          # Custom hooks
│   │   └── utils/          # Frontend utilities
│   └── public/
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Backend Dockerfile
└── frontend/Dockerfile     # Frontend Dockerfile
```

## API Documentation

### Cost Analysis Endpoints

- `GET /api/v1/cost/overview`
  - Get overall cost analysis across services

- `GET /api/v1/cost/service/{service_name}`
  - Get detailed cost analysis for a specific service

- `GET /api/v1/cost/trends`
  - Get cost trends with customizable time ranges

### Service Analysis Endpoints

- `GET /api/v1/services/ec2/instances`
  - Get EC2 instance analysis

- `GET /api/v1/services/rds/instances`
  - Get RDS instance analysis

### Optimization Endpoints

- `GET /api/v1/optimization/recommendations`
  - Get cost optimization recommendations

- `GET /api/v1/optimization/savings-plan`
  - Get Savings Plan recommendations

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes:
```bash
git commit -m 'Add some amazing feature'
```

4. Push to the branch:
```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request

## Docker Commands

1. Build and start services:
```bash
docker-compose up --build
```

2. Start services in background:
```bash
docker-compose up -d
```

3. Stop services:
```bash
docker-compose down
```

4. View logs:
```bash
docker-compose logs -f
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1
AWS_PROFILE=default

# Backend Configuration
FLASK_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# Frontend Configuration
REACT_APP_API_URL=http://localhost/api/v1
```

## Security Features

- Multi-stage Docker builds for minimal attack surface
- Non-root user execution in containers
- Environment-based configuration
- Regular dependency updates
- Health checks for all services
- Secure python virtual environment
- Optimized Gunicorn worker configuration

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Support

- Report bugs by creating an issue
- Request features through pull requests
- Contact maintainers for support