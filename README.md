# Latency Metrics API

This is a FastAPI application that calculates latency metrics based on telemetry data. It provides an endpoint to query latency statistics for different regions.

## Installation

To run this application, you need Python and the dependencies listed in `requirements.txt`.

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application locally, use `uvicorn`:

```bash
uvicorn api.latency:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### API Endpoint

The main endpoint is `/api/latency`. It accepts `POST` requests with a JSON body containing the regions to query and a latency threshold.

**Request Body:**

```json
{
  "regions": ["us-east-1", "us-west-2"],
  "threshold_ms": 100.0
}
```

**Example Response:**

```json
{
  "us-east-1": {
    "avg_latency": 95.5,
    "p95_latency": 150.2,
    "avg_uptime": 99.9,
    "breaches": 10
  },
  "us-west-2": {
    "avg_latency": 120.1,
    "p95_latency": 180.5,
    "avg_uptime": 99.8,
    "breaches": 25
  }
}
```

## Contributing Guidelines

We welcome contributions to this project. Please follow these guidelines:

1.  **Fork the repository** and create a new branch for your feature or bug fix.
2.  **Make your changes** and ensure that the code is well-tested.
3.  **Submit a pull request** with a clear description of your changes.
