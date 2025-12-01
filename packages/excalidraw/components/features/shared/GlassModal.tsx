import React, { useEffect } from "react";
import "../../NovaBoardFeatures/NovaFeatures.scss";

export interface GlassModalProps {
    title: string;
    onClose: () => void;
    children: React.ReactNode;
}

export const GlassModal: React.FC<GlassModalProps> = ({ title, onClose, children }) => {
    // Accessibility: Close on Escape key
    useEffect(() => {
        const handleEsc = (e: KeyboardEvent) => {
            if (e.key === "Escape") onClose();
        };
        window.addEventListener("keydown", handleEsc);
        return () => window.removeEventListener("keydown", handleEsc);
    }, [onClose]);

    return (
        <div className="glass-modal-overlay" onClick={onClose}>
            <div
                className="glass-modal-content"
                onClick={(e) => e.stopPropagation()}
                role="dialog"
                aria-modal="true"
                aria-labelledby="modal-title"
            >
                <div className="glass-modal-header">
                    <h3 id="modal-title">{title}</h3>
                    <button
                        className="close-button"
                        onClick={onClose}
                        aria-label="Close modal"
                    >
                        ×
                    </button>
                </div>
                <div className="glass-modal-body">
                    {children}
                </div>
            </div>
        </div>
    );
};
