let startSquare = null;

function handleClick(element) {
    const square = element.id;

    if (!startSquare) {
        startSquare = square;
        console.log("clicked on start " + square);
        return;
    }

    const endSquare = square;
    console.log("clicked on end " + square);

    window.location.href =
        `/?move_start=${startSquare}&move_desti=${endSquare}`;

    startSquare = null;
}