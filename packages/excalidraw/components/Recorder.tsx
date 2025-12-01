import React, { useState, useRef } from "react";

import "./Recorder.scss";

export const Recorder = () => {
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const chunksRef = useRef<Blob[]>([]);

    const startRecording = async () => {
        try {
            const canvas = document.querySelector("canvas");
            if (!canvas) {
                alert("Canvas not found!");
                return;
            }

            // Capture canvas stream (30 FPS)
            const canvasStream = canvas.captureStream(30);

            // Capture audio stream
            const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });

            // Combine streams
            const combinedStream = new MediaStream([
                ...canvasStream.getVideoTracks(),
                ...audioStream.getAudioTracks(),
            ]);

            const mediaRecorder = new MediaRecorder(combinedStream, {
                mimeType: "video/webm;codecs=vp9",
            });

            mediaRecorderRef.current = mediaRecorder;
            chunksRef.current = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    chunksRef.current.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(chunksRef.current, { type: "video/webm" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `novaboard-session-${new Date().toISOString()}.webm`;
                a.click();
                URL.revokeObjectURL(url);
            };

            mediaRecorder.start();
            setIsRecording(true);
        } catch (err) {
            console.error("Error starting recording:", err);
            alert("Could not start recording. Please allow microphone access.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            // Stop all tracks to release microphone
            mediaRecorderRef.current.stream.getTracks().forEach((track) => track.stop());
        }
    };

    return (
        <button
            className={`recorder-button ${isRecording ? "recording" : ""}`}
            onClick={isRecording ? stopRecording : startRecording}
            title={isRecording ? "Stop Recording" : "Start Recording"}
        >
            <div className="record-dot"></div>
            {isRecording ? "Recording..." : "Record"}
        </button>
    );
};
