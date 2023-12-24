// Get the elements
var container = document.querySelector('.container');
var openCase = document.querySelector('#open-case');
var closedCase = document.querySelector('#closed-case');
var red = document.querySelector('.red');
var blue = document.querySelector('.blue');
var green = document.querySelector('.green');
var yellow = document.querySelector('.yellow');

// Add mouseover event listener to .container
container.addEventListener('mouseover', function() {
    openCase.style.opacity = '1';
    closedCase.style.opacity = '0';
});

// Add mouseleave event listener to .container
container.addEventListener('mouseleave', function() {
    openCase.style.opacity = '0';
    closedCase.style.opacity = '1';

    // Move each div to the center of its container and scale down
    [red, blue, green, yellow].forEach(function(div) {
        div.style.transform = 'translate(-50%, -50%) scale(0.1)';
    });
});