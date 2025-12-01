import React, { useState } from "react";
import { GlassModal } from "../shared/GlassModal";
import { useToast } from "../shared/GlassToast";
import "../../NovaBoardFeatures/NovaFeatures.scss";

export const ThreeDLibrary = ({ onClose }: { onClose: () => void }) => {
    const { showToast } = useToast();
    const [isLaunching, setIsLaunching] = useState(false);

    const handleLaunch = async () => {
        setIsLaunching(true);
        showToast("🚀 Launching Nova3D...", "info");
        try {
            const res = await fetch('/api/nova3d/launch', {
                method: 'POST'
            });

            if (res.ok) {
                showToast("✨ Nova3D Launched!", "success");
            } else {
                const data = await res.json();
                console.error("Launch failed:", data);
                showToast("❌ Launch failed. Is FreeCAD installed?", "error");
            }
        } catch (e) {
            console.error("Launch error:", e);
            showToast("❌ Connection error", "error");
        } finally {
            setIsLaunching(false);
        }
    };

    return (
        <GlassModal title="🧊 Nova3D" onClose={onClose}>
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                gap: '2rem',
                textAlign: 'center',
                padding: '2rem'
            }}>
                <div style={{ fontSize: '4rem' }}>🧊</div>

                <div>
                    <h2 style={{ color: 'white', marginBottom: '1rem' }}>Nova3D</h2>
                    <p style={{ color: 'rgba(255,255,255,0.7)', maxWidth: '400px', lineHeight: '1.6' }}>
                        Nova3D is powered by FreeCAD, the open-source parametric 3D modeler.
                        Design real-life objects of any size.
                    </p>
                </div>

                <div style={{ display: 'flex', gap: '1rem', flexDirection: 'column' }}>
                    <button
                        onClick={handleLaunch}
                        className="glass-btn"
                        disabled={isLaunching}
                        style={{
                            padding: '1rem 2rem',
                            fontSize: '1.2rem',
                            display: 'inline-flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '0.5rem',
                            cursor: isLaunching ? 'wait' : 'pointer',
                            minWidth: '200px'
                        }}
                    >
                        {isLaunching ? "Launching..." : "🚀 Launch Nova3D"}
                    </button>

                    <a
                        href="https://github.com/FreeCAD/FreeCAD.git"
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                            color: 'rgba(255,255,255,0.5)',
                            textDecoration: 'none',
                            fontSize: '0.9rem'
                        }}
                    >
                        Source Code
                    </a>
                </div>
            </div>
        </GlassModal>
    );
};
