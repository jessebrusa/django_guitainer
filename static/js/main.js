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


document.getElementById('dropdownButton').addEventListener('click', function() {
    var dropdownMenu = document.getElementById('dropdownMenu');
    dropdownMenu.classList.toggle('show');
});


async function fetchUrls(urls, imgUrl, lyricsUrl, mp3Url, karaokeUrl, tabUrl) {
    var promises = urls.map(async url => {
        if (url !== null) {
            try {
                let response = await fetch(url);
                let data = await response.json();
                console.log(`Response from ${url}:`, data);

                if (url === imgUrl) {
                    if (response.ok) {
                        console.log('img success');
                    } else {
                        console.log('img failure');
                    }
                } else if (url === lyricsUrl) {
                    if (response.ok) {
                        console.log('Lyrics success');
                    } else {
                        console.log('Lyrics failure');
                    }
                } else if (url === mp3Url) {
                    if (response.ok) {
                        console.log('Mp3 success');
                    } else {
                        console.log('Mp3 failure');
                    }
                } else if (url === karaokeUrl) {
                    if (response.ok) {
                        console.log('Karaoke success');
                    } else {
                        console.log('Karaoke failure');
                    }
                }
                else if (url === tabUrl) {
                    if (response.ok) {
                        console.log('Tab success');
                    } else {
                        console.log('Tab failure');
                    }
                }

                return data;
            } catch (error) {
                console.error(`Error from ${url}:`, error);
            }
        }
    });

    var results = await Promise.allSettled(promises);
    console.log('All fetches are complete');
}