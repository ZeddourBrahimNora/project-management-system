
function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

let csrfToken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {

    let draggedTask = null;

    function updateTaskStatus(taskId, newStatus) {
        fetch(`/update_task_status/${taskId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify({
                status: newStatus
            })
        }).then(response => response.json()).then(data => {
            if (data.error) {
                console.error(data.error);
                alert('Une erreur s\'est produite. Veuillez réessayer.');
            }
        });
    }

    document.querySelectorAll('.task').forEach(task => {
        task.addEventListener('dragstart', function() {
            draggedTask = this;
        });

        task.addEventListener('dragend', function() {
            draggedTask = null;
        });
    });

    document.querySelectorAll('.task-column').forEach(column => {
        column.addEventListener('dragover', function(e) {
            e.preventDefault(); 
        });

        column.addEventListener('drop', function(e) {
            e.preventDefault();
            if (draggedTask) {
                this.appendChild(draggedTask);
                let newStatus = this.id;
                let taskId = draggedTask.dataset.taskId;
                updateTaskStatus(taskId, newStatus);
            }
        });
    });
});
