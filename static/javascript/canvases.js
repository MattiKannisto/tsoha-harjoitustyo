const canvas = document.getElementById("projectCanvas");
const context = canvas.getContext('2d');
context.fillStyle = 'rgb(0, 255, 0)';
context.fillRect(50, 50, 100, 150);
context.font = "30px Arial";
context.fillText("Hello World", 10, 50);
