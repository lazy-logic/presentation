# Dompell - Talent Connection Platform

A modern web application built with NiceGUI that connects trainees, employers, and training institutions in a comprehensive talent management ecosystem.

## Features

### 🎯 Multi-Role Dashboard System
- **Trainee Dashboard**: Profile management, skill tracking, portfolio showcase
- **Employer Dashboard**: Job posting, candidate search, application management
- **Institution Dashboard**: Training program management, student tracking, analytics

### 🎨 Modern UI/UX
- Responsive design with Tailwind CSS
- Dompell brand identity with Royal Blue (#0055B8) color scheme
- Clean, professional interface with intuitive navigation
- Mobile-friendly responsive layouts

### 🔐 Authentication & Authorization
- JWT-based authentication system
- Role-based access control (TRAINEE, EMPLOYER, INSTITUTION, ADMIN)
- Secure login/registration with email verification
- Password reset functionality

### 📊 Analytics & Insights
- Enrollment trends and statistics
- Program performance metrics
- User engagement analytics
- Real-time dashboard updates

## Technology Stack

- **Backend**: Python with NiceGUI framework
- **Frontend**: Modern HTML/CSS with Tailwind CSS
- **Authentication**: JWT tokens with refresh mechanism
- **API Integration**: RESTful API with Dompell backend
- **Icons**: Lucide React icon library
- **Typography**: Raleway and Open Sans fonts

## API Integration

The application integrates with the Dompell API (https://dompell-server.onrender.com) providing:
- User authentication and management
- Organization and training program management
- Trainee profile and portfolio management
- Employer services and job management

## Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lazy-logic/presentation.git
cd presentation
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

5. Open your browser and navigate to `http://localhost:8080`

## Project Structure

```
├── app/
│   ├── pages/
│   │   ├── auth/          # Authentication pages
│   │   ├── trainee/       # Trainee dashboard and features
│   │   ├── employer/      # Employer dashboard and features
│   │   ├── institution/   # Institution dashboard and features
│   │   └── shared/        # Shared components and pages
│   ├── components/        # Reusable UI components
│   └── utils/            # Utility functions and helpers
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Brand Guidelines

**Dompell Brand Identity:**
- Primary Color: Royal Blue (#0055B8)
- Text Colors: Charcoal (#1A1A1A), Slate Gray (#4D4D4D)
- Background: Light Mist (#F2F7FB)
- Typography: Raleway (body), Open Sans (headings)
- Logo: Network/Hub icon in Royal Blue

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary software developed for Dompell.

## Contact

For questions or support, please contact the development team.
