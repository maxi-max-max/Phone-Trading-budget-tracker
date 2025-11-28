# Phone Flipper Dashboard

A full-stack web application for managing and tracking phone flipping business operations. Built with Flask backend and vanilla JavaScript frontend, featuring budget tracking, phone inventory management, and profitability analytics with Prometheus metrics.

## Features

### Core Functionality
- **Budget Management**: Track your total investment budget and update it dynamically
- **Phone Inventory**: Add, track, and manage phones throughout their lifecycle
- **State Management**: Track phone states (bought, sold, scammed)
- **Profit Analytics**: Calculate and display profit margins and loss percentages
- **Deal Evaluation**: Intelligent deal assessment with alerts for good/bad purchases

### Advanced Features
- **Prometheus Metrics**: Built-in metrics collection and monitoring at `/metrics`
- **Health Check Endpoint**: Real-time application health status
- **CORS Support**: Cross-origin requests enabled for API endpoints
- **Toast Notifications**: User-friendly feedback messages
- **Responsive Design**: Mobile-friendly interface with gradient styling
- **Test Coverage**: Unit tests with pytest and coverage reporting

## Project Structure

```
Phone-Trading-budget-tracker/
├── backend/
│   ├── app.py              # Flask application factory and route definitions
│   ├── models.py           # Database models (Phone, Budget)
│   ├── database.py         # SQLAlchemy database initialization
│   ├── logic.py            # Business logic for deal evaluation and state changes
│   └── test/
│       ├── conftest.py     # Pytest fixtures and configuration
│       └── test_app.py     # Unit tests
├── frontend/
│   ├── index.html          # Main HTML template
│   ├── css/
│   │   └── styles.css      # Application styling
│   └── js/
│       ├── app.js          # Main application logic
│       ├── api.js          # API communication layer
│       ├── components.js   # UI component creation and updates
│       └── utils.js        # Utility functions
├── Dockerfile              # Docker containerization
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Technology Stack

### Backend
- **Framework**: Flask 3.1.2
- **Database**: SQLAlchemy 2.0.44 with SQLite
- **Server**: Gunicorn 23.0.0
- **Monitoring**: Prometheus Flask Exporter
- **Testing**: pytest, pytest-cov
- **CORS**: flask-cors

### Frontend
- **Language**: Vanilla JavaScript (ES6+)
- **Styling**: CSS3 with responsive design
- **Architecture**: Component-based with modular JS files

## API Endpoints

### Budget Management
- `GET /api/budget` - Get current budget information
- `PUT /api/budget` - Update budget amount

### Phone Operations
- `GET /api/phones` - List all phones
- `POST /api/phones` - Add new phone
- `PUT /api/phones/<id>` - Update phone details
- `PATCH /api/phones/<id>/state` - Change phone state (bought → sold → scammed)
- `DELETE /api/phones/<id>` - Remove phone from inventory

### Analytics
- `GET /api/stats` - Get profit/loss statistics
- `GET /metrics` - Prometheus metrics endpoint

### Health & Status
- `GET /health` - Health check endpoint

## Getting Started

### Prerequisites
- Python 3.9+
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/maxi-max-max/Phone-Trading-budget-tracker.git
cd Phone-Trading-budget-tracker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python -m backend.app
```

The application will be available at `http://localhost:5000`

### Docker Deployment

1. **Build the Docker image**
```bash
docker build -t phone-flipper-dashboard .
```

2. **Run the container**
```bash
docker run -p 5000:5000 phone-flipper-dashboard
```

## Usage

### Managing Your Budget
1. Click the settings icon (⚙️) in the header to update your total budget
2. This represents your total investment capacity

### Adding a Phone
1. Click "Add Phone" button
2. Enter phone brand and model
3. Enter purchase price
4. Optionally add notes about the phone
5. Submit to add to inventory

### Tracking Phone States
- **Bought**: Initial state when you purchase a phone
- **Sold**: When you sell the phone (requires selling price)
- **Scammed**: If the deal falls through or money is lost

### Monitoring Performance
- View profit/loss statistics in real-time
- Get deal evaluation messages when buying/selling
- Track total money spent vs. earned

## Deal Evaluation Logic

The application provides intelligent feedback based on phone prices:

### Purchase Price Analysis
- **< $200**: Great deal alert - below market average
- **$200-$800**: Fair price - standard market rate
- **> $800**: High investment alert - requires good resale value

### Profit Analysis
- **> 30% profit**: Excellent deal confirmation
- **0-30% profit**: Small profit notification
- **Loss**: Warning with loss amount
- **Scammed**: Error message with lost amount

## Testing

Run the test suite with coverage:

```bash
pytest backend/test/ --cov=backend --cov-report=html
```

View the coverage report in `coverage_report.txt` or generated HTML report.

## Key Business Logic

### Phone Model
```python
- id: Unique identifier
- brand: Phone manufacturer
- model: Phone model name
- buy_price: Purchase price
- sell_price: Sale price (optional)
- state: bought | sold | scammed
- notes: Additional information
- profit: Calculated as (sell_price - buy_price)
```

### Budget Model
```python
- id: Unique identifier
- total_money: Current investment amount
- created_at: Initial creation time
- updated_at: Last modification time
```

## Monitoring

The application includes Prometheus metrics for monitoring:

- Access metrics at `/metrics` endpoint
- Track application uptime and health
- Monitor database connection status
- Integration with monitoring tools like Grafana

## Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support
- Advanced filtering and search
- Historical analytics and charts
- Export functionality (CSV, PDF)
- Mobile app
- Payment gateway integration
- Automated price comparison

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source. See the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Author**: maxi-max-max  
**Repository**: [Phone-Trading-budget-tracker](https://github.com/maxi-max-max/Phone-Trading-budget-tracker)  
**Status**: Active Development