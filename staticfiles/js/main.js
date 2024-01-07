function handleItemRemoval(csrf_token) {
    document.querySelectorAll('.remove-item').forEach(function(button) {
        button.addEventListener('click', function() {
            var itemId = this.dataset.itemId;
            var itemTitle = this.dataset.itemTitle;
            var itemAction = this.dataset.itemAction;
            var itemLocation = this.dataset.itemLocation;

            let body = document.body;
            let overlayDiv = document.createElement('div');
            overlayDiv.id = 'overlayDiv';
            let confirmDiv = document.createElement('div');
            confirmDiv.id = 'confirmDiv';
            let confirmText = document.createElement('p');
            confirmText.classList.add('confirmText');
            if (itemAction === 'add') {
                confirmText.textContent = `Are you sure you want to add ${itemTitle} to ${itemLocation}?`;
                confirmDiv.id = 'confirmDivAdd';
            } 
            else {
                confirmText.textContent = `Are you sure you want to remove ${itemTitle} from ${itemLocation}?`;
            }
            let buttonDiv = document.createElement('div');
            let confirmButtonYes = document.createElement('button');
            confirmButtonYes.textContent = 'Yes';
            confirmButtonYes.id = 'confirmButtonYes';
            let confirmButtonNo = document.createElement('button');
            confirmButtonNo.id = 'cancelButton'
            confirmButtonNo.textContent = 'Cancel';

            body.appendChild(overlayDiv);
            overlayDiv.appendChild(confirmDiv);
            confirmDiv.appendChild(confirmText);
            confirmDiv.appendChild(buttonDiv);
            buttonDiv.appendChild(confirmButtonYes);
            buttonDiv.appendChild(confirmButtonNo);
            
            if (itemAction === 'add') {
                postUrl = '/add-to-library/';
                confirmButtonYes.id = 'confirmButtonYesAdd';
            }
            else {
                postUrl = '/remove-from-library/';
            }

            if (itemLocation !== 'library') {
                var groupId = this.dataset.groupId;
                var userId = this.dataset.userId;

                var itemId = groupId + '/' + userId;
                postUrl = '/remove-user/';
            }

            confirmButtonYes.addEventListener('click', function() {
                fetch(postUrl + itemId + '/', {
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
                        var songElement = document.querySelector('[data-item-id="' + itemId + '"]');
                        if (itemLocation === 'library') {
                            songElement.remove();
                        } 
                        location.reload();
                    }
                });
                overlayDiv.remove();
                confirmDiv.remove();
            });

            confirmButtonNo.addEventListener('click', function() {
                overlayDiv.remove();
                confirmDiv.remove();
            }); 
        })
    });
}

function createConfirmationDialog(text, url, csrftoken, redirect, color) {
    let body = document.body;
    let overlayDiv = document.createElement('div');
    overlayDiv.id = 'overlayDiv';
    let confirmDiv = document.createElement('div');
    confirmDiv.id = 'confirmDiv';
    let confirmText = document.createElement('p');
    confirmText.classList.add('confirmText');
    confirmText.textContent = text;
    let buttonDiv = document.createElement('div');
    let confirmButtonYes = document.createElement('button');
    confirmButtonYes.id = 'confirmButtonYes';
    confirmButtonYes.textContent = 'Yes';
    let confirmButtonNo = document.createElement('button');
    confirmButtonNo.id = 'cancelButton'
    confirmButtonNo.textContent = 'No';

    if (color === 'green') {
        confirmDiv.id = 'confirmDivAdd';
    }

    body.appendChild(overlayDiv);
    overlayDiv.appendChild(confirmDiv);
    confirmDiv.appendChild(confirmText);
    confirmDiv.appendChild(buttonDiv);
    buttonDiv.appendChild(confirmButtonYes);
    buttonDiv.appendChild(confirmButtonNo);

    confirmButtonYes.addEventListener('click', function() {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({})
        }).then(function(response) {
            return response.json()
        }).then(function(data) {
            if (redirect === 'stay') {
                location.reload();

            } else {
                window.location.href = '/library/'; 
            }
        });
    });


    confirmButtonNo.addEventListener('click', function() {
        body.removeChild(overlayDiv);
    });
}


let dropdownButton = document.getElementById('dropdownButton')
if (dropdownButton) {
    dropdownButton.addEventListener('click', function() {
        var dropdownMenu = document.getElementById('dropdownMenu');
        dropdownMenu.classList.toggle('show');
    });
}

async function fetchUrls(urls, imgUrl, lyricsUrl, mp3Url, karaokeUrl, tabUrl) {
    let lyricsLabel = document.getElementById('lyricsLabel');
    let mp3Label = document.getElementById('mp3Label');
    let karaokeLabel = document.getElementById('karaokeLabel');
    let tabLabel = document.getElementById('tabLabel');
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
                        lyricsLabel.style.color = '#27AB11';
                    } else {
                        console.log('Lyrics failure');
                        lyricsLabel.style.color = '#8C0E0E';
                    }
                } else if (url === mp3Url) {
                    if (response.ok) {
                        console.log('Mp3 success');
                        mp3Label.style.color = '#27AB11';
                    } else {
                        console.log('Mp3 failure');
                        mp3Label.style.color = '#8C0E0E';
                    }
                } else if (url === karaokeUrl) {
                    if (response.ok) {
                        console.log('Karaoke success');
                        karaokeLabel.style.color = '#27AB11';
                    } else {
                        console.log('Karaoke failure');
                        karaokeLabel.style.color = '#8C0E0E';
                    }
                }
                else if (url === tabUrl) {
                    if (response.ok) {
                        console.log('Tab success');
                        tabLabel.style.color = '#27AB11';
                    } else {
                        console.log('Tab failure');
                        tabLabel.style.color = '#8C0E0E';
                    }
                }

                return data;
            } catch (error) {
                console.error(`Error from ${url}:`, error);
            }
        }
    });

    await Promise.allSettled(promises);
    console.log('All fetches are complete');
}