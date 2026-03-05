let startSquare = null;
const socket = io();

socket.on('board_update', (data) => {
    document.querySelector('.board').innerHTML = data.html;
})

function handleClick(element) {
    const square = element.id;

    if (!startSquare) {
        startSquare = square;
        return;
    }

    const endSquare = square;

    socket.emit('player_move', { 'move_start': startSquare, 'move_desti': endSquare})

    //window.location.href =
    //    `/?move_start=${startSquare}&move_desti=${endSquare}`;

    startSquare = null;
}