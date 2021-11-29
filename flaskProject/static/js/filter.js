let i = 0;
let text = document.getElementById('filterinput');

function changeval(res) {
    if (res == 0){
        i = 0; 
        text.innerHTML = "By Tag: ";
    } else if (res == 1) {
        i = 1;
        text.innerHTML = "By Price: ";
    } else if (res == 2) {
        i = 2;
        text.innerHTML = "By Date: ";
    } else if (res == 3) {
        i = 3;
        text.innerHTML = "By Location: ";
    }
}
