// Dashboard Chart (sample data)
document.addEventListener("DOMContentLoaded", function () {

    const chartCanvas = document.getElementById("energyChart");
    if (!chartCanvas) return;

    const ctx = chartCanvas.getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            datasets: [{
                label: "Energy (kWh)",
                data: [180, 220, 200, 260, 300, 280, 310],
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            responsive: true
        }
    });
});

// Scroll animation
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
});

document.querySelectorAll(
    ".service-card, .detail-card, .dash-card, .cta-box"
).forEach(el => {
    el.classList.add("fade-in");
    observer.observe(el);
});
