# -*- coding: utf-8 -*-
"""
Lista dos autores monitorados, separada em Patronos e Fundadores.
Para adicionar/remover um autor, basta editar as listas abaixo.
O nome deve ser escrito como você quer buscar no Estante Virtual.
"""

PATRONOS = [
    "Adelino Fontoura", "Álvares de Azevedo", "Araújo Porto-Alegre", "Artur de Oliveira",
    "Basílio da Gama", "Bernardo Guimarães", "Casimiro de Abreu", "Castro Alves",
    "Cláudio Manoel da Costa", "Evaristo da Veiga", "Fagundes Varela", "França Júnior",
    "Francisco Adolfo de Varnhagen", "Francisco Otaviano", "Franklin Távora",
    "Gonçalves de Magalhães", "Gonçalves Dias", "Gregório de Matos", "Hipólito da Costa",
    "João Francisco Lisboa", "Joaquim Caetano da Silva", "Joaquim Manuel de Macedo",
    "Joaquim Serra", "José Bonifácio", "José de Alencar", "Júlio Ribeiro",
    "Junqueira Freire", "Laurindo Rabelo", "Maciel Monteiro", "Manuel Antônio de Almeida",
    "Martins Pena", "Pardal Mallet", "Pedro Luís", "Raul Pompeia", "Sousa Caldas",
    "Tavares Bastos", "Teófilo Dias", "Tobias Barreto", "Tomás Antônio Gonzaga",
    "Visconde do Rio Branco",
]

FUNDADORES = [
    "Afonso Celso", "Alberto de Oliveira", "Alcindo Guanabara", "Aluísio Azevedo",
    "Araripe Júnior", "Artur Azevedo", "Carlos de Laet", "Carlos Magalhães de Azeredo",
    "Clóvis Beviláqua", "Coelho Neto", "Domício da Gama", "Eduardo Prado",
    "Filinto de Almeida", "Franklin Dória", "Garcia Redondo", "Graça Aranha",
    "Guimarães Passos", "Inglês de Sousa", "J. M. Pereira da Silva", "Joaquim Nabuco",
    "José do Patrocínio", "José Veríssimo", "Lúcio de Mendonça", "Luís Guimarães Júnior",
    "Luís Murat", "Machado de Assis", "Medeiros e Albuquerque", "Olavo Bilac",
    "Oliveira Lima", "Pedro Rabelo", "Raimundo Correia", "Rodrigo Octavio",
    "Rui Barbosa", "Salvador de Mendonça", "Silva Ramos", "Sílvio Romero",
    "Teixeira de Melo", "Urbano Duarte", "Valentim Magalhães", "Visconde de Taunay",
    "Julia Lopes de Almeida",
]

# Lista completa usada pelo script
TODOS = [(nome, "Patrono") for nome in PATRONOS] + [(nome, "Fundador") for nome in FUNDADORES]
