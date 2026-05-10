document.addEventListener('DOMContentLoaded', function () {

    const buscador = document.getElementById('buscador');
    const filtroCategoria = document.getElementById('filtroCategoria');

    buscador.addEventListener('keyup', filtrar);
    filtroCategoria.addEventListener('change', filtrar);

    function filtrar() {
        const nombre = buscador.value.toLowerCase();
        const categoria = filtroCategoria.value.toLowerCase();
        const filas = document.querySelectorAll('#tablaProductos tbody tr');

        filas.forEach(fila => {
            const nombreFila = fila.cells[1].textContent.toLowerCase();
            const categoriaFila = fila.cells[3].textContent.toLowerCase();
            const coincideNombre = nombreFila.includes(nombre);
            const coincideCategoria = categoria === '' || categoriaFila === categoria;
            fila.style.display = coincideNombre && coincideCategoria ? '' : 'none';
        });
    }

});
