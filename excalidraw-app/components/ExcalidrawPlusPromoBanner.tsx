export const ExcalidrawPlusPromoBanner = ({
  isSignedIn,
}: {
  isSignedIn: boolean;
}) => {
  const PLUS_APP = import.meta.env.VITE_APP_PLUS_APP;
  const PLUS_LP = import.meta.env.VITE_APP_PLUS_LP;

  return (
    <a
      href={
        isSignedIn
          ? PLUS_APP
          : `${PLUS_LP}/plus?utm_source=excalidraw&utm_medium=app&utm_content=guestBanner#excalidraw-redirect`
      }
      target="_blank"
      rel="noopener noreferrer"
      className="plus-banner"
    >
      Excalidraw+
    </a>
  );
};
