function handleSongRemoval(csrf_token, addRemove) {
    document.querySelectorAll('.remove-from-library').forEach(function(button) {
        button.addEventListener('click', function() {
            var songId = this.dataset.songId;
            var songTitle = this.dataset.songTitle;

            let body = document.body;
            let confirmDiv = document.createElement('div');
            let confirmText = document.createElement('p');
            if (addRemove === 'add') {
                confirmText.textContent = `Are you sure you want to add ${songTitle} to your library?`;
            } 
            else {
                confirmText.textContent = `Are you sure you want to remove ${songTitle} from your library?`;
            }
            let buttonDiv = document.createElement('div');
            let confirmButtonYes = document.createElement('button');
            confirmButtonYes.textContent = 'Yes';
            let confirmButtonNo = document.createElement('button');
            confirmButtonNo.textContent = 'No';

            body.appendChild(confirmDiv);
            confirmDiv.appendChild(confirmText);
            confirmDiv.appendChild(buttonDiv);
            buttonDiv.appendChild(confirmButtonYes);
            buttonDiv.appendChild(confirmButtonNo);
            
            if (addRemove === 'add') {
                postUrl = '/add-to-library/';
            }
            else {
                postUrl = '/remove-from-library/';
            }

            confirmButtonYes.addEventListener('click', function() {
                fetch(postUrl + songId + '/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf_token,
                    },
                    body: JSON.stringify({})
                }).then(function(response) {
                    return response.json();
                }).then(function(data) {
                    if (data.status === 'success') {
                        var songElement = document.querySelector('[data-song-id="' + songId + '"]');
                        songElement.remove();
                    }
                });
                confirmDiv.remove();
            });

            confirmButtonNo.addEventListener('click', function() {
                confirmDiv.remove();
            }); 
        })
    });
}

