const sidebar = document.getElementById("side-bar");
const sidebarOverlay = document.getElementById("sidebar-overlay")
function openSidebar() {
    sidebar.classList.remove("-translate-x-100"); // Use the correct class name
    sidebarOverlay.classList.remove("-translate-x-200")
    console.log("Sidebar opened");
}



function closeSidebar() {
    sidebar.classList.add("-translate-x-100");
    sidebarOverlay.classList.add("-translate-x-200")
    console.log("Sidebar closed");
}

const openBtn = document.getElementById("open-btn");
const closeBtn = document.getElementById("close-btn");
openBtn.onclick = openSidebar;
closeBtn.onclick = closeSidebar;


function showGlobalLoading() {
    document.getElementById("globalLoader").classList.remove("hidden");
    document.getElementById("globalLoader").classList.add("flex");
    console.log("Hiiiiiiiiiiiii i am Loading")
}