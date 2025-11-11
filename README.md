# AI-Powered Chatbot for Student Services

A React-based frontend application for a Final Year Project that provides an AI-powered chatbot interface for student services. The application includes a mock authentication system, a student portal dashboard, and an interactive chatbot interface.

## Features

### 🔐 Authentication System
- Clean login interface with username/password fields
- Mock authentication (accepts any non-empty credentials)
- Responsive design

### 📚 Student Portal Dashboard
- Welcome dashboard with service cards
- Quick access to various student services:
  - Course Registration
  - Library Services
  - Financial Services
  - Academic Records
  - Housing Services
  - Career Services

### 🤖 AI Chatbot Interface
- Floating chat button in bottom-right corner
- Interactive chat window with message bubbles
- User messages appear on the right (blue)
- Bot messages appear on the left (white)
- Typing indicator with animation
- 1-2 second response delay to simulate real API calls

### 💬 Mock Response System
The chatbot currently uses a comprehensive mock response system with keywords for:
- Library hours and services
- Course registration
- Tuition and payment information
- Housing and dormitory services
- Academic records and grades
- Career services and job opportunities
- General greetings and help

## Installation & Setup

1. **Install Dependencies**
   ```bash
   cd student-chatbot
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```
   
   The application will open at `http://localhost:3000`

3. **Build for Production**
   ```bash
   npm run build
   ```

## Usage

### Login
- Use any username and password (both fields must be non-empty)
- Click "Login" to access the student portal

### Using the Chatbot
1. Click the floating chat button (💬) in the bottom-right corner
2. Type your message in the input field
3. Press Enter or click the send button (📤)
4. Wait for the bot's response (1-2 second delay)

### Example Questions to Try
- "library hours" - Get library opening hours
- "register course" - Information about course registration
- "tuition" - Check tuition balance
- "housing" - Housing and dormitory information
- "grades" - Academic performance information
- "help" - General assistance

## Project Structure

```
src/
├── App.js                 # Main application component
├── App.css               # Global application styles
├── index.js              # Application entry point
├── components/
│   ├── LoginPage.js      # Authentication interface
│   ├── LoginPage.css     # Login page styles
│   ├── Portal.js         # Student dashboard
│   ├── Portal.css        # Dashboard styles
│   ├── FloatingChatButton.js  # Chat toggle button
│   ├── FloatingChatButton.css # Button styles
│   ├── ChatWindow.js     # Main chat interface
│   ├── ChatWindow.css    # Chat window styles
│   ├── MessageInput.js   # Message input component
│   └── MessageInput.css  # Input field styles
└── services/
    └── chatbotService.js # Mock responses & Amazon Lex integration placeholder
```

## Customizing Mock Responses

### Adding New Responses
Edit `src/services/chatbotService.js` to add new keyword-response pairs:

```javascript
const mockResponses = {
  // Add your new responses here
  'new keyword': 'Your response message',
  'another keyword': 'Another response message'
};
```

### Modifying Existing Responses
Simply update the response text for any existing keyword in the `mockResponses` object.

### Adding Dynamic Responses
You can create more complex response logic by modifying the `getChatbotResponse` function:

```javascript
export const getChatbotResponse = (userMessage) => {
  return new Promise((resolve) => {
    const message = userMessage.toLowerCase();
    
    // Add custom logic here
    if (message.includes('time')) {
      resolve(`The current time is ${new Date().toLocaleTimeString()}`);
      return;
    }
    
    // ... rest of the function
  });
};
```

## Amazon Lex Integration (Future)

The codebase is structured to easily integrate with Amazon Lex when ready:

1. **Install AWS SDK**
   ```bash
   npm install aws-sdk
   ```

2. **Update chatbotService.js**
   - Replace the `sendToAmazonLex` function with actual Lex integration
   - Add your AWS credentials, bot ID, and region
   - Update the `getChatbotResponse` function to call Lex instead of mock responses

3. **Example Integration Code**
   ```javascript
   import AWS from 'aws-sdk';

   const lexRuntimeV2 = new AWS.LexRuntimeV2({
     region: 'YOUR_REGION',
     credentials: new AWS.Credentials('ACCESS_KEY', 'SECRET_KEY')
   });

   export const sendToAmazonLex = async (message, userId = 'default-user') => {
     const lexParams = {
       botId: 'YOUR_BOT_ID',
       botAliasId: 'YOUR_BOT_ALIAS_ID',
       localeId: 'en_US',
       sessionId: userId,
       text: message
     };

     try {
       const response = await lexRuntimeV2.recognizeText(lexParams).promise();
       return response.messages[0].content;
     } catch (error) {
       console.error('Error calling Amazon Lex:', error);
       throw error;
     }
   };
   ```

## Styling & Customization

### Color Scheme
The application uses a purple gradient theme. Main colors:
- Primary: `#667eea` to `#764ba2`
- Background: `#f5f7fa`
- Text: `#333`
- Borders: `#e1e5e9`

### Responsive Design
The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (320px - 767px)

### Custom Styling
Each component has its own CSS file. Modify these files to change:
- Colors and gradients
- Layout and spacing
- Animations and transitions
- Typography

## Development Notes

### Code Quality
- Components are functional and use React Hooks
- Clean separation of concerns
- Responsive design principles
- Accessible UI elements

### Performance
- Optimized animations
- Efficient state management
- Lazy loading ready
- Production build optimized

### Scalability
- Modular component structure
- Easy to add new features
- Service layer abstraction
- Configuration-driven responses

## Demo Instructions

1. **Login Demo**: Use any username/password combination
2. **Portal Navigation**: Explore different service cards
3. **Chatbot Demo**: Try various questions like:
   - "What are the library hours?"
   - "How do I register for a course?"
   - "What's my tuition balance?"
   - "Tell me about housing options"

## Troubleshooting

### Common Issues

1. **npm install fails**: Try deleting `node_modules` and `package-lock.json`, then run `npm install` again
2. **Port 3000 in use**: Use `npm start -- --port 3001` to run on a different port
3. **Styling issues**: Clear browser cache and hard refresh

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Future Enhancements

- Real authentication system
- Backend API integration
- Amazon Lex chatbot integration
- User session persistence
- Advanced chat features (file upload, voice input)
- Admin panel for response management
- Analytics and usage tracking

## License

This project is for educational purposes as part of a Final Year Project.
