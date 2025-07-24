# E-commerce SQL Agent Dashboard

A modern, responsive single-page dashboard for interacting with the e-commerce SQL agent API.

## Features

- **Natural Language Queries**: Ask questions in plain English about your e-commerce data
- **Real-time SQL Generation**: See the generated SQL queries for your questions
- **Live Results**: Execute queries and view results instantly
- **Database Health Monitoring**: Check connection status and available tables
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Clean, professional interface with loading states and error handling

## How to Use

### 1. Start the Backend

Make sure your FastAPI backend is running on `http://127.0.0.1:8000`:

```bash
cd ../backend
# Install dependencies and start the server
# The dashboard expects the API to be available at http://127.0.0.1:8000
```

### 2. Start the Frontend

```bash
npm install
npm run dev
```

The dashboard will be available at `http://localhost:5173`

### 3. Using the Dashboard

#### Query Input

- Enter your question in natural language in the text area
- Examples:
  - "What are the top 5 selling products?"
  - "Show me customer orders from last month"
  - "Which products have the highest ratings?"
  - "How many orders were placed in each store?"

#### Query Execution

- Click "Execute Query" or press `Ctrl+Enter` to run your query
- Adjust "Max Tables" setting to control how many database tables the AI considers
- Use "Clear Results" to remove previous results

#### Results Display

The dashboard shows:

- **Question**: Your original question
- **Relevant Tables**: Which database tables were used
- **Generated SQL**: The actual SQL query created by the AI
- **Execution Result**: The data returned from the database

#### Database Information

View available databases (zepto, blinkit, instamart) and their tables at the bottom of the page.

## API Endpoints Used

- `POST /ask-sql` - Execute natural language queries
- `GET /health` - Check API health and available tables
- `GET /tables` - List all available tables
- `GET /tables/search` - Search for relevant tables

## Technical Details

### Frontend Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Axios** for API communication
- **React Router** for navigation
- **CSS3** with modern styling (gradients, shadows, animations)

### Key Components

- `SQLDashboard.tsx` - Main dashboard component
- `api.ts` - API service for backend communication
- `app-router.tsx` - Application routing

### Error Handling

- Connection errors to the backend
- Invalid queries
- Server errors
- Loading states during query execution

## Development

### Project Structure

```
src/
├── components/
│   ├── SQLDashboard.tsx
│   └── SQLDashboard.css
├── services/
│   └── api.ts
├── routes/
│   └── app-router.tsx
├── App.tsx
└── main.tsx
```

### Adding Features

- Modify `SQLDashboard.tsx` for UI changes
- Update `api.ts` for new API endpoints
- Extend CSS in `SQLDashboard.css` for styling

### Configuration

- API base URL is configurable in `src/services/api.ts`
- Default: `http://127.0.0.1:8000`
