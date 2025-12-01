import React from "react";
import { ToastProvider } from "../features/shared/GlassToast";
import { AITutor as AITutorComponent } from "../features/AITutor/AITutor";
import { ThreeDLibrary as ThreeDLibraryComponent } from "../features/ThreeDLibrary/ThreeDLibrary";
import { VideoLibrary as VideoLibraryComponent } from "../features/VideoLibrary/VideoLibrary";
import { GlassModal as GlassModalComponent, GlassModalProps } from "../features/shared/GlassModal";

// Re-export GlassModal directly
export const GlassModal = GlassModalComponent;
export type { GlassModalProps };

// Wrap features in ToastProvider to ensure toast functionality works
export const AITutor = (props: any) => (
    <ToastProvider>
        <AITutorComponent {...props} />
    </ToastProvider>
);

export const ThreeDLibrary = (props: any) => (
    <ToastProvider>
        <ThreeDLibraryComponent {...props} />
    </ToastProvider>
);

export const VideoLibrary = (props: any) => (
    <ToastProvider>
        <VideoLibraryComponent {...props} />
    </ToastProvider>
);
