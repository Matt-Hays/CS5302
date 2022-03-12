
    const popupParent = document.getElementById('popup-parent');
    popupParent.onmouseover = function() {
        document.getElementById('popup').style.visibility = 'visible';
    };
    popupParent.onmouseout = function() {
        document.getElementById('popup').style.visibility = 'hidden';
    };

