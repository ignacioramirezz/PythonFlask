from flask import Flask, jsonify, request
from products import products

app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({"message":"como andas"})

@app.route('/products',methods=['GET'])
def devolver_products():
    return jsonify({"products": products, "message": "Products list"})

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    # por cada producto se fija si el nombre coincide con el nombre que me da, lo va retornar
    print(product_name)
    return 'received'
    # me retorna el objeto que coincide con la busqeuda

@app.route('/products/busqueda/<string:product_name>')
def get_product_lista(product_name):
    # por cada producto se fija si el nombre coincide con el nombre que me da, lo va retornar
    product_list = next((product for product in products if product['name'] == product_name),None)
    print(product_name)
    return jsonify({"product_list": product_list,"message": "get_product_lista sin chequeo"})
    # me retorna el objeto que coincide con la busqeuda

# en esta variante lo que hace es chequear el tamaño de la lista 
# para luego poder realizar el respectivo retorno del elemento de la lista
@app.route('/products/chequeo_busqueda/<string:product_name>')
def get_product_lista_chequeo(product_name):
    product_list = (product for product in products if product['name'] == product_name)
    product_list = list(product_list)
    if (len(product_list) > 0):
        return jsonify({"product_list": product_list})
    else: 
        return jsonify({"message":"No se encontro ningun elemento"})


@app.route('/products', methods=['POST'])
def insertar_producto():
    new_product = {
        "name" : request.json['name'],
        "price" : request.json['price'],
        "quantity" : request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message": "Product Added", "products": products})

@app.route('/products/<string:product_name>',methods=['PUT'])
def editar_componente(product_name):
    lista_producto = next((product for product in products if product['name'] == product_name),None)
    if (lista_producto is not None):
        lista_producto['name'] = request.json.get('name',lista_producto['name'])
        lista_producto['price'] = request.json.get('price',lista_producto['price'])
        lista_producto['quantity'] = request.json.get('quantity',lista_producto['quantity'])
        return jsonify({"message": "El componente fue modificado", "products": products})
    else:
        return jsonify({"message" : "El componente no existe"})
    

@app.route('/products/<string:product_name>',methods=['DELETE'])
def delete(product_name):
    lista_producto = (product for product in products if product['name'] == product_name)
    lista_producto2 = list(lista_producto)
    if (len(lista_producto2)==0):
        return jsonify({"message": "No se encontro el componente"})
    products.remove(lista_producto2[0])
    return jsonify({"message": "Se ha realizado el borrado", "products": products})
        

if __name__ == '__main__':
    app.run(debug=True,port=4000)