document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;

    function applyLabel() {
        var isDark = document.documentElement.getAttribute("data-theme") === "dark";
        btn.textContent = isDark ? "☀️ Light mode" : "🌙 Dark mode";
    }

    btn.addEventListener("click", function () {
        var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        try { localStorage.setItem("aurafi-theme", next); } catch (e) {}
        applyLabel();
    });

    applyLabel();
});
