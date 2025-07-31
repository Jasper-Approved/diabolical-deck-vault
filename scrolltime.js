// scrolltime.js

document.addEventListener("DOMContentLoaded", function () {
  const scrollTime = document.body.getAttribute("data-scroll-time");

  const gradients = {
    morning: "linear-gradient(#f0ece2, #d3d3d3)",
    midday: "linear-gradient(#ffe9b3, #ffd6a5)",
    twilight: "linear-gradient(#c1b6fc, #ffb4ed)",
    night: "linear-gradient(#1e1e2f, #3a3a5c)",
    glitch: "linear-gradient(#ffefef, #cfcfcf)"
  };

  document.body.style.background = gradients[scrollTime] || gradients.glitch;

  console.log("Scroll time:", scrollTime);
});
