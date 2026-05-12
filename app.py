from flask import Flask, render_template
from entities.user import User
from entities.producto import Producto
from entities.cliente import Cliente
from entities.orden import Orden
from entities.pago import Pago

app = Flask(__name__)



@app.route('/')
def index():
    ordenes = Orden.get_all()
    return render_template('index.html',
                           total_productos=len(Producto.get_all()),
                           total_clientes=len(Cliente.get_all()),
                           total_ordenes=len(ordenes),
                           ordenes=ordenes[:10])



@app.route('/productos')
def vista_productos():
    return render_template('productos.html',
                           productos=Producto.get_all(),
                           categorias=Producto.get_categorias())



@app.route('/clientes')
def vista_clientes():
    return render_template('clientes.html',
                           clientes=Cliente.get_all())



@app.route('/ordenes')
def vista_ordenes():
    return render_template('ordenes.html',
                           ordenes=Orden.get_all(),
                           clientes=Cliente.get_all(),
                           usuarios=User.get_all(),
                           productos=Producto.get_all())


@app.route('/ordenes/<int:id>/detalle')
def vista_detalle_orden(id):
    orden = Orden.get_by_id(id)
    detalle = Orden.get_detalle(id)
    return render_template('detalle_orden.html',
                           orden=orden,
                           detalle=detalle)



@app.route('/pagos')
def vista_pagos():
    return render_template('pagos.html',
                           pagos=Pago.get_all())



@app.route('/usuarios')
def vista_usuarios():
    return render_template('usuarios.html',
                           usuarios=User.get_all())



@app.route('/reportes')
def vista_reportes():
    return render_template('reportes.html',
                           mas_vendidos=Orden.reporte_mas_vendidos())


@app.route('/productos/sin-ventas')
def productos_sin_ventas():
    """Muestra productos que nunca se han vendido"""
    # Si pusiste el método en producto.py:
    productos = Producto.get_productos_nunca_vendidos()
    
    return render_template('productos_sin_ventas.html',
                          productos=productos,
                          total_sin_ventas=len(productos))


if __name__ == '__main__':
    app.run()
