document.addEventListener('DOMContentLoaded', function () {

    const buscador = document.getElementById('buscador');

    buscador.addEventListener('keyup', function () {
        const termino = buscador.value.toLowerCase();
        const filas = document.querySelectorAll('#tablaClientes tbody tr');

        filas.forEach(fila => {
            const nombre = fila.cells[1].textContent.toLowerCase();
            fila.style.display = nombre.includes(termino) ? '' : 'none';
        });
    });

});
