#!/bin/bash

# Try to open the application if installed in standard locations
if [ -d "/Applications/FreeCAD.app" ]; then
    echo "Launching FreeCAD from /Applications..."
    open -a FreeCAD
    exit 0
fi

# Try to open via 'open' command (if in PATH or known by LaunchServices)
if open -Ra "FreeCAD" >/dev/null 2>&1; then
    echo "Launching FreeCAD via system..."
    open -a FreeCAD
    exit 0
fi

# Fallback: Error out
echo "Error: FreeCAD application not found in /Applications or system path."
exit 1
