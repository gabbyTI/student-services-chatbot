import React, { useState } from 'react';
import LoginPage from './components/LoginPage';
import Portal from './components/Portal';
import FloatingChatButton from './components/FloatingChatButton';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleLogin = (username, password) => {
    // Mock authentication - accept any non-empty credentials
    if (username.trim() && password.trim()) {
      setIsLoggedIn(true);
      return true;
    }
    return false;
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setIsChatOpen(false);
  };

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="App">
      {!isLoggedIn ? (
        <LoginPage onLogin={handleLogin} />
      ) : (
        <>
          <Portal onLogout={handleLogout} />
          <FloatingChatButton onClick={toggleChat} />
          {isChatOpen && (
            <ChatWindow 
              isOpen={isChatOpen} 
              onClose={() => setIsChatOpen(false)} 
            />
          )}
        </>
      )}
    </div>
  );
}

export default App;
