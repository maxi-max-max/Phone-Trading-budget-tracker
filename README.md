# Phone Resale Manager

A full-stack web application for managing phone resale business operations, tracking inventory, profits, and budget.

## Features

- **CRUD Operations**: Add, view, update, and delete phone inventory
- **Budget Tracking**: Monitor available funds and transaction history
- **State Management**: Track phones through bought → sold → scammed states
- **Statistics Dashboard**: View total profits, losses, and inventory status
- **Deal Evaluation**: Get automated feedback on purchase and sale decisions
- **Hide/Show Phones**: Temporarily hide phones from view (frontend only)

## Tech Stack

**Backend:**
- Python 3.x
- Flask
- SQLAlchemy
- SQLite

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript (ES6 modules)

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/phone-resale-manager.git
cd phone-resale-manager
Step 2: Install Python Dependencies
bashpip install flask flask-sqlalchemy flask-cors
Or use requirements.txt if provided:
bashpip install -r requirements.txt
Step 3: Run the Application
bashpython app.py
The application will start on http://127.0.0.1:5000
Step 4: Access the Application
Open your web browser and navigate to:
http://localhost:5000
Project Structure
phone-resale-manager/
├── app.py                 # Flask backend with API endpoints
├── models.py              # Database models (optional separate file)
├── database.py            # Database initialization
├── logic.py               # Business logic for deal evaluation
├── phone_manager.db       # SQLite database (auto-generated)
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── styles.css         # CSS styling
│   ├── app.js             # Main application logic
│   ├── api.js             # API communication module
│   ├── components.js      # UI components
│   └── utils.js           # Utility functions
Usage
Setting Your Budget

Click the settings icon (⚙️) next to the budget display
Enter your available budget amount
Click "Update Budget"

Adding a Phone

Click "Add New Phone" button
Fill in:

Brand (e.g., Apple, Samsung)
Model (e.g., iPhone 13)
Buy Price
Notes (optional)


Click "Add Phone"

Managing Phone States
Mark as Sold:

Click "Mark Sold" button
Enter the selling price
System calculates profit/loss automatically

Mark as Scammed:

Click "Mark Scammed" if transaction was fraudulent
Budget adjusts accordingly

Hide from View:

Click "Hide" button to temporarily remove from display
Does not delete from database
Does not affect budget calculations

Viewing Statistics
The dashboard automatically displays:

Total phones bought
Total phones sold
Total profit/loss
Total lost to scams

API Endpoints
MethodEndpointDescriptionGET/api/phonesGet all phonesPOST/api/phonesAdd new phonePUT/api/phones/<id>/stateUpdate phone stateDELETE/api/phones/<id>Delete phoneGET/api/budgetGet current budgetPOST/api/budgetUpdate budgetGET/api/statsGet statistics
Database Schema
Budget Table

id: Integer (Primary Key)
total_money: Float
created_at: DateTime
updated_at: DateTime

Phone Table

id: Integer (Primary Key)
model: String (100)
brand: String (50)
buy_price: Float
sell_price: Float (nullable)
state: String (20) - Values: 'bought', 'sold', 'scammed'
notes: Text (nullable)
created_at: DateTime
updated_at: DateTime

Troubleshooting
Port Already in Use
If port 5000 is already in use:
bash# Kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Or run on a different port
flask run --port 5001
Database Issues
To reset the database:
bash# Delete the existing database
rm phone_manager.db

# Restart the application (database will be recreated)
python app.py
CORS Errors
Make sure flask-cors is installed:
bashpip install flask-cors
Development
To run in development mode with auto-reload:
bashexport FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
License
[Your chosen license]
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Author
[Your Name]

---

## Also Create a `requirements.txt` File

Create a file named `requirements.txt` in your project root:
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
This allows users to install all dependencies with one command:
bashpip install -r requirements.txt
These instructions will allow anyone to clone your repository and run your application immediately following the steps!
