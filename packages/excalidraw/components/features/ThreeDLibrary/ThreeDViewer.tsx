import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

interface ThreeDViewerProps {
    modelId: string;
    modelUrl: string;
    onClose: () => void;
}

export const ThreeDViewer: React.FC<ThreeDViewerProps> = ({ modelId, modelUrl, onClose }) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
    const sceneRef = useRef<THREE.Scene | null>(null);
    const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
    const controlsRef = useRef<OrbitControls | null>(null);
    const frameIdRef = useRef<number>(0);
    const raycaster = useRef(new THREE.Raycaster());
    const mouse = useRef(new THREE.Vector2());

    const [tool, setTool] = useState<'view' | 'annotate' | 'measure'>('view');
    const [annotations, setAnnotations] = useState<{ id?: string, pos: THREE.Vector3, text: string }[]>([]);
    const [measurePoints, setMeasurePoints] = useState<THREE.Vector3[]>([]);
    const [distance, setDistance] = useState<number | null>(null);

    // Fetch existing annotations
    useEffect(() => {
        const fetchAnnotations = async () => {
            try {
                const res = await fetch(`http://localhost:5001/api/models/`);
                if (res.ok) {
                    const models = await res.json();
                    const currentModel = models.find((m: any) => m.id === modelId);
                    if (currentModel && currentModel.metadata && currentModel.metadata.annotations) {
                        const loadedAnnotations = currentModel.metadata.annotations.map((a: any) => ({
                            id: a.id,
                            pos: new THREE.Vector3(a.position.x, a.position.y, a.position.z),
                            text: a.text
                        }));
                        setAnnotations(loadedAnnotations);
                    }
                }
            } catch (e) {
                console.error("Failed to load annotations", e);
            }
        };
        fetchAnnotations();
    }, [modelId]);

    useEffect(() => {
        if (!containerRef.current) return;

        // Setup
        const width = containerRef.current.clientWidth;
        const height = containerRef.current.clientHeight;

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x222222);
        sceneRef.current = scene;

        const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        camera.position.z = 5;
        cameraRef.current = camera;

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);
        containerRef.current.appendChild(renderer.domElement);
        rendererRef.current = renderer;

        // Lights
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambientLight);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 10, 7);
        scene.add(directionalLight);

        // Controls
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controlsRef.current = controls;

        // Load Model
        const loader = new GLTFLoader();
        loader.load(modelUrl, (gltf) => {
            scene.add(gltf.scene);

            // Center model
            const box = new THREE.Box3().setFromObject(gltf.scene);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());

            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 * Math.tan(fov * 2));
            cameraZ *= 1.5;

            camera.position.z = cameraZ;
            controls.target = center;

        }, undefined, (error) => {
            console.error('An error happened loading the model:', error);
        });

        // Click Handler
        const onClick = async (event: MouseEvent) => {
            if (!containerRef.current || !cameraRef.current || !sceneRef.current) return;

            const rect = containerRef.current.getBoundingClientRect();
            mouse.current.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.current.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.current.setFromCamera(mouse.current, cameraRef.current);
            const intersects = raycaster.current.intersectObjects(sceneRef.current.children, true);

            if (intersects.length > 0) {
                const point = intersects[0].point;

                if (tool === 'annotate') {
                    const text = prompt("Enter annotation note:");
                    if (text) {
                        // Optimistic UI update
                        const newAnnotation = { pos: point, text };
                        setAnnotations(prev => [...prev, newAnnotation]);

                        // Save to backend
                        try {
                            await fetch(`http://localhost:5001/api/models/${modelId}/annotations`, {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    text,
                                    position: { x: point.x, y: point.y, z: point.z }
                                })
                            });
                        } catch (e) {
                            console.error("Failed to save annotation", e);
                            alert("Failed to save annotation");
                        }
                    }
                } else if (tool === 'measure') {
                    setMeasurePoints(prev => {
                        const newPoints = [...prev, point];
                        if (newPoints.length === 2) {
                            const d = newPoints[0].distanceTo(newPoints[1]);
                            setDistance(d);

                            // Draw line
                            const material = new THREE.LineBasicMaterial({ color: 0x00ff00 });
                            const geometry = new THREE.BufferGeometry().setFromPoints(newPoints);
                            const line = new THREE.Line(geometry, material);
                            sceneRef.current?.add(line);

                            return []; // Reset for next measurement
                        }
                        return newPoints;
                    });
                }
            }
        };

        renderer.domElement.addEventListener('click', onClick);

        // Animation Loop
        const animate = () => {
            frameIdRef.current = requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        };
        animate();

        // Resize Handler
        const onResize = () => {
            if (!containerRef.current || !cameraRef.current || !rendererRef.current) return;
            const width = containerRef.current.clientWidth;
            const height = containerRef.current.clientHeight;

            cameraRef.current.aspect = width / height;
            cameraRef.current.updateProjectionMatrix();
            rendererRef.current.setSize(width, height);
        };
        window.addEventListener('resize', onResize);

        // Cleanup
        return () => {
            window.removeEventListener('resize', onResize);
            cancelAnimationFrame(frameIdRef.current);
            renderer.domElement.removeEventListener('click', onClick);
            if (rendererRef.current && containerRef.current) {
                containerRef.current.removeChild(rendererRef.current.domElement);
                rendererRef.current.dispose();
            }
        };
    }, [modelUrl, tool, modelId]);

    // Render annotations
    useEffect(() => {
        if (!sceneRef.current) return;

        // Clear existing annotation meshes (simple approach)
        // In a real app, we'd track meshes by ID. Here we just re-add all.
        // Note: This is a simplification. For better perf, manage scene graph better.

        annotations.forEach(ann => {
            const geometry = new THREE.SphereGeometry(0.05, 16, 16);
            const material = new THREE.MeshBasicMaterial({ color: 0xff0000 });
            const sphere = new THREE.Mesh(geometry, material);
            sphere.position.copy(ann.pos);
            sceneRef.current?.add(sphere);
        });

    }, [annotations]);

    return (
        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
            <div ref={containerRef} style={{ width: '100%', height: '100%' }} />

            {/* Controls Overlay */}
            <div style={{ position: 'absolute', top: '10px', left: '10px', display: 'flex', gap: '5px' }}>
                <button className={`glass-btn-sm ${tool === 'view' ? 'active' : ''}`} onClick={() => setTool('view')}>👁️ View</button>
                <button className={`glass-btn-sm ${tool === 'annotate' ? 'active' : ''}`} onClick={() => setTool('annotate')}>📍 Annotate</button>
                <button className={`glass-btn-sm ${tool === 'measure' ? 'active' : ''}`} onClick={() => setTool('measure')}>📏 Measure</button>
            </div>

            {distance !== null && (
                <div style={{ position: 'absolute', top: '50px', left: '10px', background: 'rgba(0,0,0,0.7)', padding: '5px', borderRadius: '4px', color: '#4ade80' }}>
                    Distance: {distance.toFixed(2)} units
                    <button onClick={() => setDistance(null)} style={{ marginLeft: '10px', background: 'none', border: 'none', color: '#aaa', cursor: 'pointer' }}>x</button>
                </div>
            )}

            <button
                onClick={onClose}
                style={{
                    position: 'absolute',
                    top: '10px',
                    right: '10px',
                    background: 'rgba(0,0,0,0.5)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '50%',
                    width: '30px',
                    height: '30px',
                    cursor: 'pointer'
                }}
            >
                ✕
            </button>
        </div>
    );
};
