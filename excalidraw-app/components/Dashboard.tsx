import React, { useState } from "react";

import "./Dashboard.scss";

const Particles = () => {
    return (
        <div className="particles-container">
            {[...Array(15)].map((_, i) => (
                <div
                    key={i}
                    className="particle"
                    style={{
                        width: `${Math.random() * 100 + 50}px`,
                        height: `${Math.random() * 100 + 50}px`,
                        left: `${Math.random() * 100}%`,
                        top: `${Math.random() * 100}%`,
                        animationDelay: `${Math.random() * 5}s`,
                    }}
                />
            ))}
        </div>
    );
};

export const Dashboard = ({ onStartSession }: { onStartSession: () => void }) => {
    const [sessionCode, setSessionCode] = useState("");

    return (
        <div className="dashboard-container">
            <Particles />
            <header className="dashboard-header">
                <div className="logo">NovaBoard</div>
                <div className="user-profile">
                    <div className="avatar">T</div>
                    <span>Teacher</span>
                </div>
            </header>

            <main className="dashboard-main">
                <section className="welcome-section">
                    <h1>Welcome back, Teacher!</h1>
                    <p>Ready to inspire your students today?</p>
                </section>

                <section className="actions-grid">
                    <div className="action-card create-session" onClick={onStartSession}>
                        <div className="icon">➕</div>
                        <h3>New Session</h3>
                        <p>Start a new whiteboard class</p>
                    </div>

                    <div className="action-card join-session">
                        <div className="icon">🔗</div>
                        <h3>Join Session</h3>
                        <p>Enter code to join a class</p>
                        <div className="input-group">
                            <input
                                type="text"
                                placeholder="Enter Code"
                                value={sessionCode}
                                onChange={(e) => setSessionCode(e.target.value)}
                                onClick={(e) => e.stopPropagation()}
                            />
                            <button onClick={(e) => { e.stopPropagation(); alert("Join logic coming soon!"); }}>Go</button>
                        </div>
                    </div>

                    <div className="action-card library">
                        <div className="icon">📚</div>
                        <h3>Library</h3>
                        <p>Access your lessons & assets</p>
                    </div>

                    <div className="action-card analytics">
                        <div className="icon">📊</div>
                        <h3>Analytics</h3>
                        <p>View student engagement</p>
                    </div>
                </section>

                <section className="recent-sessions">
                    <h2>Recent Sessions</h2>
                    <div className="session-list">
                        <div className="session-item">
                            <div className="preview"></div>
                            <div className="info">
                                <h4>Math 101 - Calculus</h4>
                                <p>Yesterday, 10:00 AM</p>
                            </div>
                            <div className="actions">
                                <button>Resume</button>
                                <button>View Summary</button>
                            </div>
                        </div>
                        <div className="session-item">
                            <div className="preview"></div>
                            <div className="info">
                                <h4>Physics - Newton's Laws</h4>
                                <p>Nov 24, 2:00 PM</p>
                            </div>
                            <div className="actions">
                                <button>Resume</button>
                                <button>View Summary</button>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
};
