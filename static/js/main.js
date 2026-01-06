// Function to open the modal
function openAddModal() {
    document.getElementById("addModal").style.display = "block";
}

// Function to close the modal
function closeAddModal() {
    document.getElementById("addModal").style.display = "none";
}

// Close modal if user clicks outside of it
window.onclick = function(event) {
    const modal = document.getElementById("addModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}