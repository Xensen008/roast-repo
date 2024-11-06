export const API_URL = import.meta.env.MODE === 'production' 
  ? 'https://roast-repo.onrender.com'  // Update with actual backend URL
  : 'http://localhost:8000';