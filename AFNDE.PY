import graphviz

class AFND_e:
    
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

        for transicion, destinos in self.transiciones.items():
            origen, simbolo = transicion
            for destino in destinos:
                if simbolo:
                    dot.edge(origen, destino, label=simbolo)
                else:
                    dot.edge(origen, destino, label='ε')

        dot.render('automata_afnd_e', format='png', cleanup=True)
        print("Autómata gráficado como 'automata_afnd_e.png'")


    def validar_cadena(self, cadena):
        estados_actuales = self.clausura_epsilon({self.estado_inicial})
        for simbolo in cadena:
            nuevos_estados = set()
            for estado in estados_actuales:
                transiciones_estado = self.transiciones.get((estado, simbolo), set())
                nuevos_estados.update(transiciones_estado)
            estados_actuales = self.clausura_epsilon(nuevos_estados)
        return any(estado in self.estados_aceptacion for estado in estados_actuales)

    def clausura_epsilon(self, estados):
        estados_clausura = set(estados)
        for estado in estados:
            epsilon_transiciones = self.transiciones.get((estado, ''), set())
            estados_clausura.update(epsilon_transiciones)
        if estados_clausura == estados:
            return estados
        else:
            return self.clausura_epsilon(estados_clausura)


estados = {'q0', 'q1', 'q2', 'q3'}  # Estados
alfabeto = {'0', '1'}  # Alfabeto
estado_inicial = 'q0'  # Estado inicial
estados_aceptacion = {'q3'}  # Estados de aceptación
transiciones = {('q0', ''): {'q1', 'q3'}, ('q1', '1'): {'q1'}, ('q1', ''): {'q2'}, ('q2', '0'): {'q3'}, ('q3', ''): {'q0'}}
automata = AFND_e(estados, alfabeto, estado_inicial, estados_aceptacion, transiciones)

automata.graficar_automata()


while True:
    cadena = input("Ingrese una cadena (compuesta por 0s y 1s), o escriba 'x' para salir: ")
    if cadena.lower() == 'x':
        break
    if automata.validar_cadena(cadena):
        print("La cadena es aceptada")
    else:
        print("La cadena es rechazada")
