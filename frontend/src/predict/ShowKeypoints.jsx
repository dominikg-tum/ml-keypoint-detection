import React, { useEffect } from "react";

const ShowKeypoints = ({ captureImageFromCamera, imageRef, canvasRef, setResult }) => {
    useEffect(() => {
        const interval = setInterval(async () => {
            captureImageFromCamera();

            if (imageRef.current) {
                const formData = new FormData();
                formData.append('image', imageRef.current);

                const response = await fetch('/predict', {
                    method: "POST",
                    body: formData,
                });

                if (response.status === 200) {
                    const keypoints = await response.json();
                    drawKeypoints(keypoints); // Draw keypoints
                } else {
                    const errorMessage = await response.text();
                    setResult(errorMessage);
                }
            }
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    // draw keypoints on the canvas
    const drawKeypoints = (keypoints) => {
        const ctx = canvasRef.current.getContext('2d');
        ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);  // clear the canvas

        keypoints.forEach(([x, y]) => {
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI);
            ctx.fillStyle = 'red';
            ctx.fill();
        });
    };

    return null;
}

export default ShowKeypoints;