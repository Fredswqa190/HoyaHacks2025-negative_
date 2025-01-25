import React, { useState } from 'react';
import axios from 'axios';
import { useTheme } from '@mui/material/styles';
import './chat.css';

interface Message {
    sender: 'user' | 'bot';
    text: string;
}

const Chatbot: React.FC = () => {
    const [userInput, setUserInput] = useState<string>('');
    const [chatHistory, setChatHistory] = useState<Message[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const theme = useTheme();

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUserInput(event.target.value);
    };

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!userInput.trim()) return;

        const newMessage: Message = { sender: 'user', text: userInput };
        setChatHistory([...chatHistory, newMessage]);
        setUserInput('');
        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('http://localhost:5000/chat', { message: userInput });
            const botMessage: Message = { sender: 'bot', text: response.data.response };
            setChatHistory([...chatHistory, newMessage, botMessage]);
        } catch (error) {
            console.error('Error sending message to the chatbot:', error);
            setError('Failed to get response from the chatbot.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="chat-container" style={{ backgroundColor: theme.palette.mode === 'dark' ? '#333' : '#f9f9f9' }}>
            <div className="chat-header">
                <h1>Chat with Sentinel</h1>
            </div>
            <div className="chat-history">
                {chatHistory.map((message, index) => (
                    <div key={index} className={`chat-message ${message.sender}`}>
                        <div className="avatar">{message.sender === 'user' ? '👤' : '🤖'}</div>
                        <div className="message-text">{message.text}</div>
                    </div>
                ))}
                {loading && <div className="loading">Loading...</div>}
                {error && <div className="error">{error}</div>}
            </div>
            <form onSubmit={handleSubmit} className="chat-form">
                <input
                    type="text"
                    value={userInput}
                    onChange={handleInputChange}
                    placeholder="Type your message here..."
                    className="chat-input"
                />
                <button type="submit" className="chat-submit">Send</button>
            </form>
        </div>
    );
};

export default Chatbot;