from flask_restful import Resource, reqparse

#reqparse
#bibilioteca que recebe os elementos da requisicao - nome, estrelas, diarias e cidades

hoteis = [
    {
        'hotel_id': 'A-01',
        'nome': 'Best Western Aracaju',
        'estrelas': 4.5,
        'diaria': 420.34,
        'cidade': 'Aracaju'
    },

       {
        'hotel_id': 'A-02',
        'nome': 'Malai Manso',
        'estrelas': 5.0,
        'diaria': 850.50,
        'cidade': 'Mato Grosso'
    },

       {
        'hotel_id': 'A-03',
        'nome': 'Hard Rock Curitiba',
        'estrelas': 4.2,
        'diaria': 280.50,
        'cidade':'Curitiba'
    },

]


#sera um recurso da API
class Hoteis(Resource):
    def get(self):
        return {'hoteis ': hoteis }

class Hotel(Resource):
    #criar uma varialvel, instanciar um requestParser
    argumentos = reqparse.RequestParser()
    #adicionar o argumento
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade') 
    
    def busca_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self,hotel_id):
        hotel = Hotel.busca_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message':'Hotel not found.'}, 404 #not found

    def post(self,hotel_id):
        #construtor / chave e valor
        dados = Hotel.argumentos.parse_args()

        novo_hotel = {
            #hotel_id é passado via path na URL///
            'hotel_id': hotel_id,
            'nome': dados['nome'],
            'estrelas': dados['estrelas'],
            'diaria': dados['diaria'],
            'cidade': dados['cidade']
        }

        hoteis.append(novo_hotel)
        return novo_hotel, 200 #status ok

    #diferente do post o put substitui caso o id já exista
    def put(self,hotel_id):
        dados = Hotel.argumentos.parse_args()
        #para não precisar repetir os atributos de novo_hotel
        #utilizamos os kwargs ** então desempacotamos dados

        novo_hotel = {'hotel_id': hotel_id, **dados}
        
        hotel = Hotel.busca_hotel(hotel_id)
        if hotel:
            #função update nativa do python para atualizar dados
            hotel.update(novo_hotel)
            return novo_hotel, 200 #status ok
        hoteis.append(novo_hotel)
        return novo_hotel, 201 #created 
    def delete(self,hotel_id):
        #com isso o sistema irá entender que o id referenciado é da lista já criada antes.
        global hoteis 
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id']!= hotel_id]
        return {'message': 'Hotel deleted.'}