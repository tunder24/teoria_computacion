import graphviz
class AFD:
    def __init__(self, estados, alfabeto, estado_inicial, estados_aceptacion, transiciones):
        self.estados = estados
        self.alfabeto = alfabeto
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.transiciones = transiciones
        
    def graficar_automata(self):
        dot = graphviz.Digraph(format='png')

        for estado in self.estados:
            if estado in self.estados_aceptacion:
                dot.node(estado, shape='doublecircle')
            else:
                dot.node(estado)

        for transicion, destino in self.transiciones.items():
            origen, simbolo = transicion
            dot.edge(origen, destino, label=simbolo)

        dot.render('automata', format='png', cleanup=True)


    def validar_cadena(self, cadena):
        estado_actual = self.estado_inicial
        for simbolo in cadena:
            if simbolo not in self.alfabeto:
                return False  # El símbolo no está en el alfabeto
            estado_actual = self.transiciones.get((estado_actual, simbolo))
            if estado_actual is None:
                return False  # No hay transición para el símbolo actual
        return estado_actual in self.estados_aceptacion

# Definir el DFA
estados = {'q0', 'q1', 'q2'}  # EQ
alfabeto = {'a', 'b'}  # Σ
estado_inicial = 'q0'  # q0
estados_aceptacion = {'q2'}  # F
transiciones = {('q0', 'a'): 'q1', ('q0', 'b'): 'q0', ('q1', 'a'): 'q1', ('q1', 'b'): 'q2', ('q2', 'a'): 'q2'} # δ
automata = AFD(estados, alfabeto, estado_inicial, estados_aceptacion, transiciones)

automata.graficar_automata()
print("Autómata gráficado como 'automata.png'")


while True:
    cadena = input("Ingrese una cadena (compuesta por a y b), o escriba 'x' para salir: ")
    if cadena.lower() == 'x':
        break
    if automata.validar_cadena(cadena):
        print("La cadena es aceptada.")
    else:
        print("La cadena es rechazada.")