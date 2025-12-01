import React from "react";
import { GlassModal } from "../shared/GlassModal";
import { useToast } from "../shared/GlassToast";
import "../../NovaBoardFeatures/NovaFeatures.scss";

export const VideoLibrary = ({ onClose }: { onClose: () => void }) => {
    const { showToast } = useToast();
    const videos = [
        { id: 1, title: "Intro to Calculus", duration: "10:24", category: "Math" },
        { id: 2, title: "Newton's Laws", duration: "15:30", category: "Physics" },
        { id: 3, title: "Cell Structure", duration: "08:45", category: "Biology" },
        { id: 4, title: "World War II", duration: "22:10", category: "History" },
    ];

    const handlePlayVideo = (title: string) => {
        showToast(`▶️ Playing: ${title}`, "info");
        // In a real implementation, this would open the FloatingVideoPlayer
        onClose();
    };

    return (
        <GlassModal title="🎥 Video Engine" onClose={onClose}>
            <div className="video-list">
                {videos.map((video) => (
                    <div key={video.id} className="video-item" onClick={() => handlePlayVideo(video.title)}>
                        <div className="video-thumbnail">
                            <span style={{ fontSize: '0.8rem', position: 'absolute', bottom: '4px', right: '4px', background: 'rgba(0,0,0,0.8)', padding: '2px 4px', borderRadius: '4px' }}>{video.duration}</span>
                        </div>
                        <div className="video-info">
                            <h4>{video.title}</h4>
                            <p>{video.category}</p>
                        </div>
                    </div>
                ))}
            </div>
        </GlassModal>
    );
};
