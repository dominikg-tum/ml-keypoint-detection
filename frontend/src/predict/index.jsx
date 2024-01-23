import React, { useEffect, useRef, useState } from "react";
import ShowKeypoints from './ShowKeypoints'; // Import ShowKeypoints component

const Classifier = () => {
    const canvasRef = useRef();
    const imageRef = useRef();
    const videoRef = useRef();

    const [result, setResult] = useState("");

    const captureImageFromCamera = () => {
        if (videoRef.current && canvasRef.current) {
            const context = canvasRef.current.getContext('2d');
            context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
            imageRef.current = canvasRef.current.toDataURL('image/png');
        }
    };

    const playCameraStream = () => {
        if (videoRef.current) {
            videoRef.current.play();
        }
    };

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

    return (
        <>
            <header>
                <h1>Facial Keypoint Predictor</h1>
            </header>
            <main>
                <div>
                    <video ref={videoRef} onCanPlay={() => playCameraStream()} id="video" />
                    <canvas ref={canvasRef} />
                </div>
                <div>
                    <p>Result: {result}</p>
                </div>
                <ShowKeypoints
                    captureImageFromCamera={captureImageFromCamera}
                    imageRef={imageRef}
                    canvasRef={canvasRef}
                    setResult={setResult}
                />
            </main>
        </>
    )
};

export default Classifier;