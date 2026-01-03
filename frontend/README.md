# Mental Coach Frontend

A modern, accessible Next.js frontend for the Mental Coach AI chat application. Features a clean chat interface with dark mode support, responsive design, and excellent accessibility.

## Prerequisites

- Node.js 18+ and npm (or yarn/pnpm)
- The backend API running on `http://localhost:8000` (see `../api/README.md` for backend setup)

## Integration with Backend

This frontend is fully integrated with the FastAPI backend located in the `../api/` folder:

- **Automatic Connection**: Connects to `http://localhost:8000` by default
- **Health Monitoring**: Displays real-time backend connection status
- **Error Handling**: Shows clear error messages if the backend is unavailable
- **CORS Ready**: Backend is configured to accept requests from the frontend

## Quick Start

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

That's it! The frontend will automatically connect to the backend API running on port 8000.

## Available Scripts

- `npm run dev` - Start the development server (with hot reload)
- `npm run build` - Build the production version
- `npm start` - Start the production server (requires `npm run build` first)
- `npm run lint` - Run ESLint to check for code issues

## Features

- ✨ **Modern UI** - Clean, professional design with smooth animations
- 🌓 **Dark Mode** - Toggle between light and dark themes (saves preference)
- 📱 **Responsive** - Works beautifully on desktop, tablet, and mobile
- ♿ **Accessible** - Keyboard navigation, focus states, and ARIA labels
- 💬 **Real-time Chat** - Interactive chat interface with message history
- ⚡ **Fast** - Built with Next.js 14 for optimal performance

## Configuration

The frontend connects to the backend API at `http://localhost:8000` by default. To change this:

1. Create a `.env.local` file in the `frontend` directory
2. Add: `NEXT_PUBLIC_API_URL=http://your-api-url:port`

## Troubleshooting

**Frontend won't connect to backend:**
- Make sure the backend is running on port 8000
- Check that CORS is enabled in the backend (it should be by default)
- Verify the API URL in `.env.local` if you've customized it

**Port 3000 already in use:**
- Next.js will automatically try the next available port (3001, 3002, etc.)
- Or specify a custom port: `npm run dev -- -p 3001`

**Build errors:**
- Make sure all dependencies are installed: `npm install`
- Clear the `.next` folder and try again: `rm -rf .next && npm run build`

## Project Structure

```
frontend/
├── app/              # Next.js App Router pages
│   ├── layout.tsx   # Root layout with theme provider
│   ├── page.tsx     # Main chat page
│   └── globals.css  # Global styles and theme variables
├── components/       # React components
│   ├── ChatInterface.tsx  # Main chat container
│   ├── ChatMessage.tsx    # Individual message component
│   ├── ChatInput.tsx      # Message input component
│   ├── ThemeProvider.tsx  # Theme context provider
│   └── ThemeToggle.tsx    # Dark/light mode toggle
├── lib/             # Utilities
│   └── api.ts       # API client for backend communication
└── package.json     # Dependencies and scripts
```

## Deployment

This frontend is ready to deploy to Vercel:

1. Push your code to GitHub
2. Import the project in Vercel
3. Set the `NEXT_PUBLIC_API_URL` environment variable to your backend URL
4. Deploy!

The frontend will work seamlessly with the backend API.
