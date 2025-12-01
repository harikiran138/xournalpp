import React, { useState, useEffect, useRef } from "react";
import { GlassModal } from "../shared/GlassModal";
import { useToast } from "../shared/GlassToast";
import "../../NovaBoardFeatures/NovaFeatures.scss";

export const AITutor = ({ onClose, elements }: { onClose: () => void, elements?: any[] }) => {
    const { showToast } = useToast();
    const [messages, setMessages] = useState<{ role: 'user' | 'ai'; text: string }[]>([
        { role: 'ai', text: 'Hello! I am your NovaBoard AI Assistant. I can help you summarize lessons, generate quizzes, or explain concepts.' }
    ]);
    const [input, setInput] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const chatEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages, isTyping]);

    const handleSend = async (textOverride?: string) => {
        const userMsg = textOverride || input;
        if (!userMsg.trim()) return;

        setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
        if (!textOverride) setInput("");
        setIsTyping(true);

        try {
            // Simplify elements context to save bandwidth
            const context = elements?.map(el => ({
                type: el.type,
                text: el.text,
                x: el.x,
                y: el.y
            })).slice(0, 50); // Limit to 50 elements

            const response = await fetch('http://localhost:5001/api/ai/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMsg,
                    context: context
                }),
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();

            setIsTyping(false);
            setMessages(prev => [...prev, { role: 'ai', text: data.text }]);
        } catch (error) {
            console.error("AI Error:", error);
            setIsTyping(false);
            showToast("⚠️ Backend offline. Using mock AI.", "error");

            // Fallback Mock Response
            setTimeout(() => {
                setMessages(prev => [...prev, { role: 'ai', text: "I'm having trouble connecting to my brain (Backend), but I'm still here! Try checking if the Python server is running." }]);
            }, 1000);
        }
    };

    return (
        <GlassModal title="🧠 Nova AI Engine" onClose={onClose}>
            <div className="ai-tutor-container">
                <div className="chat-history">
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`message ${msg.role}`}>
                            <div className="bubble">{msg.text}</div>
                        </div>
                    ))}
                    {isTyping && (
                        <div className="message ai">
                            <div className="bubble typing-indicator">
                                <span>.</span><span>.</span><span>.</span>
                            </div>
                        </div>
                    )}
                    <div ref={chatEndRef} />
                </div>

                <div style={{ display: 'flex', gap: '0.5rem', padding: '0 1rem 0.5rem 1rem', overflowX: 'auto' }}>
                    <button className="glass-btn-sm" onClick={() => handleSend("Summarize this board")}>📝 Summarize</button>
                    <button className="glass-btn-sm" onClick={() => handleSend("Create a quiz from this")}>❓ Quiz</button>
                    <button className="glass-btn-sm" onClick={() => handleSend("Explain this concept")}>💡 Explain</button>
                </div>

                <div className="chat-input-area">
                    <input
                        type="text"
                        placeholder="Ask Nova AI..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        autoFocus
                    />
                    <button onClick={() => handleSend()}>Send</button>
                </div>
            </div>
        </GlassModal>
    );
};
