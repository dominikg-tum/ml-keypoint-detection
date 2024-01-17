import React, { useEffect, useRef, useState } from "react";

const Classifier = () => {
    const canvasRef = useRef();
    const imageRef = useRef();
    const videoRef = useRef();

    const [result, setResult] = useState("");

    // fetch camera feed
    useEffect(() => {
        async function getCameraStream() {
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: false,
                video: true,
            });

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
        };

        getCameraStream();
    }, []);

    // send images to the API 
    useEffect(() => {
        // TODO:
    }, []);

    const playCameraStream = () => {
        if (videoRef.current) {
            videoRef.current.play();
        }
    };

    return (
        <>
            <header>
                <h1>Facial Keypoint Predictor</h1>
            </header>
            <main>
                <video ref={videoRef} onCanPlay={() => playCameraStream()} />
            </main>
        </>
    )
};

export default Classifier;