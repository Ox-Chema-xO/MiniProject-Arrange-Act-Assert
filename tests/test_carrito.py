# tests/test_carrito.py

import pytest
from src.carrito import Carrito, Producto
from src.factories import ProductoFactory

def test_agregar_producto_nuevo():
    """
    AAA:
    Arrange: Se crea un carrito y se genera un producto.
    Act: Se agrega el producto al carrito.
    Assert: Se verifica que el carrito contiene un item con el producto y cantidad 1.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Laptop", precio=1000.00)
    
    # Act
    carrito.agregar_producto(producto,cantidad=1)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].producto.nombre == "Laptop"
    assert items[0].cantidad == 1


def test_agregar_producto_existente_incrementa_cantidad():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se agrega el mismo producto nuevamente aumentando la cantidad.
    Assert: Se verifica que la cantidad del producto se incrementa en el item.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Mouse", precio=50.00, stock=7)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act
    carrito.agregar_producto(producto, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 3


def test_remover_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con cantidad 3.
    Act: Se remueve una unidad del producto.
    Assert: Se verifica que la cantidad del producto se reduce a 2.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Teclado", precio=75.00)
    carrito.agregar_producto(producto, cantidad=3)
    
    # Act
    carrito.remover_producto(producto, cantidad=1)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 2


def test_remover_producto_completo():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se remueve la totalidad de la cantidad del producto.
    Assert: Se verifica que el producto es eliminado del carrito.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Monitor", precio=300.00)
    carrito.agregar_producto(producto, cantidad=2)
    
    # Act
    carrito.remover_producto(producto, cantidad=2)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0


def test_actualizar_cantidad_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 5.
    Assert: Se verifica que la cantidad se actualiza correctamente.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Auriculares", precio=150.00)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act
    carrito.actualizar_cantidad(producto, nueva_cantidad=5)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 1
    assert items[0].cantidad == 5


def test_actualizar_cantidad_a_cero_remueve_producto():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act: Se actualiza la cantidad del producto a 0.
    Assert: Se verifica que el producto se elimina del carrito.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Cargador", precio=25.00)
    carrito.agregar_producto(producto, cantidad=3)
    
    # Act
    carrito.actualizar_cantidad(producto, nueva_cantidad=0)
    
    # Assert
    items = carrito.obtener_items()
    assert len(items) == 0


def test_calcular_total():
    """
    AAA:
    Arrange: Se crea un carrito y se agregan varios productos con distintas cantidades.
    Act: Se calcula el total del carrito.
    Assert: Se verifica que el total es la suma correcta de cada item (precio * cantidad).
    """
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Impresora", precio=200.00)
    producto2 = ProductoFactory(nombre="Escáner", precio=150.00)
    carrito.agregar_producto(producto1, cantidad=2)  # Total 400
    carrito.agregar_producto(producto2, cantidad=1)  # Total 150
    
    # Act
    total = carrito.calcular_total()
    
    # Assert
    assert total == 550.00


def test_aplicar_descuento():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto con una cantidad determinada.
    Act: Se aplica un descuento del 10% al total.
    Assert: Se verifica que el total con descuento sea el correcto.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Tablet", precio=500.00)
    carrito.agregar_producto(producto, cantidad=2)  # Total 1000
    
    # Act
    total_con_descuento = carrito.aplicar_descuento(10)
    
    # Assert
    assert total_con_descuento == 900.00


def test_aplicar_descuento_limites():
    """
    AAA:
    Arrange: Se crea un carrito y se agrega un producto.
    Act y Assert: Se verifica que aplicar un descuento fuera del rango [0, 100] genere un error.
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Smartphone", precio=800.00)
    carrito.agregar_producto(producto, cantidad=1)
    
    # Act y Assert
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(150)
    with pytest.raises(ValueError):
        carrito.aplicar_descuento(-5)

def test_vaciar_items():
    """
    AAA
    Arrange: Se crea un carrito y se agrega tres productos
    Act y Assert: Se verifica que al vaciar el carrito, la lista de items quede vacía y el total sea 0
    """
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Monitor", precio=300.00)
    producto2 = ProductoFactory(nombre="Televisor", precio=1300.00)
    producto3 = ProductoFactory(nombre="Dvd", precio=400.00)
    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=2)
    carrito.agregar_producto(producto3, cantidad=1)
    
    # Act
    carrito.vaciar()

    # Assert
    lista_items = carrito.obtener_items()
    assert len(lista_items) == 0
    assert carrito.calcular_total() == 0

def test_dscto_condicional_exitoso():
    """
    AAA
    Arrange: Se crea un carrito y se agrega dos productos
    Act y Assert: Se verifica que al aplicar el descuento condicional en el caso 
    que se supere el minimo sea correcto
    """
    #Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Monitor", precio=300.00)
    producto2 = ProductoFactory(nombre="Dvd", precio=400.00)
    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=1)
    
    #Act
    total_a_pagar = carrito.aplicar_descuento_condicional(porcentaje=15,minimo=500)

    #Assert
    assert total_a_pagar == 595.00

def test_dscto_condicional_fallido():
    """
    AAA
    Arrange: Se crea un carrito y se agrega un producto
    Act y Assert: Se verifica que al aplicar el descuento condicional en el caso 
    que no se supere el minimo se retorne el total
    """
    #Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Monitor", precio=300.00)
    carrito.agregar_producto(producto1, cantidad=1)
    
    #Act
    total_a_pagar = carrito.aplicar_descuento_condicional(porcentaje=15,minimo=500)

    #Assert
    assert total_a_pagar == 300.00

def test_agregar_producto_dentro_de_stock(carrito, producto_generico):
    """
    AAA:
    Arrange: carrito y producto ya estan listos por fixture
    Act:
    Assert: 
    """
    # Arrange
    # carrito y producto ya estan listos por fixture
    # producto generico cuenta con una cantidad en stock de 7
    # Act
    carrito.agregar_producto(producto_generico,cantidad=5)
    
    # Assert
    item = carrito.obtener_items().pop()
    assert item.cantidad == 5

def test_agregar_producto_fuera_de_stock():
    """
    AAA:
    Arrange: Se crea un carrito y se genera un producto.
    Act: Se agrega el producto al carrito.
    Assert: Se verifica que se lanza un error al intentar agregar un producto
    con cantidad superior al stock
    """
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="Laptop", precio=1000.00, stock=7)
    
    # Act y Assert
    with pytest.raises(ValueError):
        carrito.agregar_producto(producto, cantidad=8)

def test_obtener_items_ordenados_por_criterio():
    # Arrange
    carrito = Carrito()
    producto1 = ProductoFactory(nombre="Monitor", precio=300.00)
    producto2 = ProductoFactory(nombre="Televisor", precio=1300.00)
    producto3 = ProductoFactory(nombre="Dvd", precio=400.00)
    carrito.agregar_producto(producto1, cantidad=1)
    carrito.agregar_producto(producto2, cantidad=1)
    carrito.agregar_producto(producto3, cantidad=1)
    
    # Act
    items_ordenados_por_nombre = carrito.obtener_items_ordenados("nombre")
    items_ordenados_por_precio = carrito.obtener_items_ordenados("Precio")

    # Assert
    assert [item.producto.nombre for item in items_ordenados_por_nombre] == ["Dvd","Monitor","Televisor"]
    assert [item.producto.precio for item in items_ordenados_por_precio] == [300.00, 400.00, 1300.00]

@pytest.mark.parametrize(
    "cantidad, porcentaje, minimo, esperado",
    [
        (1, 10, 200, 100),
        (2, 10, 200, 180),
        (3, 20, 250, 240),
    ]
)
def test_dscto_condicional_varios_casos(
    carrito, producto_generico, cantidad, porcentaje, minimo, esperado
):
    # Arrange: producto_generico tiene un precio de 100 y stock 7
    carrito.agregar_producto(producto_generico, cantidad=cantidad)

    # Act
    total_a_pagar = carrito.aplicar_descuento_condicional(porcentaje, minimo)

    # Assert
    assert total_a_pagar == esperado

def test_calcular_impuestos(carrito, producto_generico):
    """
    Red: Se espera que calcular_impuestos retorne el valor del impuesto.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=4)
    
    # Act
    impuesto = carrito.calcular_impuestos(10)  

    # Assert
    assert impuesto == 40.00

def test_aplicar_cupon_con_limite(carrito, producto_generico):
    """
    Red: Se espera que al aplicar un cupón, el descuento no supere el límite máximo.
    """
    # Arrange
    carrito.agregar_producto(producto_generico, cantidad=5)

    # Act
    total_con_cupon = carrito.aplicar_cupon(20, 50) 

    # Assert
    assert total_con_cupon == 450.00

def test_agregar_producto_excede_stock():
    """
    Red: Se espera que al intentar agregar una cantidad mayor a la disponible en stock se lance un ValueError.
    """
    # Arrange: Se crea un producto y un carrito
    # Suponemos que el producto tiene 5 unidades en stock.
    
    producto = Producto("ProductoStock", 100.00, 5)
    carrito = Carrito()

    # Act & Assert
    with pytest.raises(ValueError):
        carrito.agregar_producto(producto, cantidad=6)