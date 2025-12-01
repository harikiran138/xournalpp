import React, { useState, useEffect } from "react";
import QRCode from "qrcode";
import "./SessionManager.scss";

interface Session {
    id: string;
    title: string;
    startTime: Date;
    boardState?: any;
    recording?: string;
}

export const SessionManager = () => {
    const [currentSession, setCurrentSession] = useState<Session | null>(null);
    const [qrDataUrl, setQrDataUrl] = useState<string>("");
    const [joinUrl, setJoinUrl] = useState<string>("");

    const createSession = () => {
        const sessionId = `session-${Date.now()}`;
        const session: Session = {
            id: sessionId,
            title: `Session ${new Date().toLocaleString()}`,
            startTime: new Date(),
        };

        const url = `${window.location.origin}/student/join/${sessionId}`;
        setJoinUrl(url);

        // Generate QR Code
        QRCode.toDataURL(url, { width: 300 }).then(setQrDataUrl);

        setCurrentSession(session);
        localStorage.setItem("currentSession", JSON.stringify(session));
    };

    const endSession = () => {
        if (currentSession) {
            // Save to history
            const history = JSON.parse(localStorage.getItem("sessionHistory") || "[]");
            history.push(currentSession);
            localStorage.setItem("sessionHistory", JSON.stringify(history));
            localStorage.removeItem("currentSession");
            setCurrentSession(null);
        }
    };

    useEffect(() => {
        const saved = localStorage.getItem("currentSession");
        if (saved) {
            const session = JSON.parse(saved);
            setCurrentSession(session);
            const url = `${window.location.origin}/student/join/${session.id}`;
            setJoinUrl(url);
            QRCode.toDataURL(url, { width: 300 }).then(setQrDataUrl);
        }
    }, []);

    if (!currentSession) {
        return (
            <div className="session-manager">
                <button className="create-session-btn" onClick={createSession}>
                    📝 Start New Session
                </button>
            </div>
        );
    }

    return (
        <div className="session-manager active">
            <div className="session-info">
                <h3>🟢 Live Session</h3>
                <p>{currentSession.title}</p>
            </div>

            <div className="join-options">
                <div className="qr-code">
                    {qrDataUrl && <img src={qrDataUrl} alt="Join QR" />}
                    <p>Scan to Join</p>
                </div>

                <div className="join-link">
                    <input type="text" value={joinUrl} readOnly />
                    <button onClick={() => navigator.clipboard.writeText(joinUrl)}>
                        📋 Copy
                    </button>
                </div>
            </div>

            <button className="end-session-btn" onClick={endSession}>
                ⏹️ End Session
            </button>
        </div>
    );
};

export const StudentCounter = ({ count }: { count: number }) => (
    <div className="student-counter">
        <span className="icon">👥</span>
        <span className="count">{count}</span>
        <span className="label">Students</span>
    </div>
);
