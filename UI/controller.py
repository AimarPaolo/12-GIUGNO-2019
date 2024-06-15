import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.ordinare = []
        self.choiceIngredient = None

    def handle_ingredienti(self, e):
        self._view.txt_result.controls.clear()
        self.ordinare = []
        calorie_str = self._view.txtcalorie.value
        try:
            calorie_float = float(calorie_str)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text(f"Errore nell'inserimento delle calorie!!"))
            self._view.update_page()
            return
        self._model.buildGraph(calorie_float)
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
        self._model.buildGraph(calorie_float)
        nNodes, nEdges = self._model.getCaratteristiche()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nNodes} nodi"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nEdges} archi"))

        for key, value in self._model.stampaOrdinata().items():
            if value != 0:
                self.ordinare.append((self._model.idMap[key].display_name, self._model.idMap[key].condiment_calories, value))
        ordinata = sorted(self.ordinare, key=lambda x: x[1], reverse = True)
        for nome, calorie, value in ordinata:
            self._view.txt_result.controls.append(ft.Text(f"L'ingrediente {nome} ha {calorie} calorie ed è presente in {value} ingredienti"))
        self.fillDD()
        self._view.update_page()

    def handle_dieta(self, e):
        if self.choiceIngredient is None:
            self._view.create_alert("Selezionare un ingrediente")
            return
        soluzione, peso = self._model.getBestPath(self.choiceIngredient)
        self._view.txt_result.controls.append(
            ft.Text(f"Il massimo numero di calorie individuato è {peso} ed include i seguenti ingredienti:"))
        for elemento in soluzione:
            self._view.txt_result.controls.append(ft.Text(f"{elemento.display_name}"))
        self._view.update_page()

    def fillDD(self):
        self._view.ddingredienti.options.clear()
        for n in self._model._grafo.nodes:
            self._view.ddingredienti.options.append(ft.dropdown.Option(data=n, text=n.display_name, on_click=self.readDD))

    def readDD(self, e):
        if e.control.data is None:
            self.choiceIngredient = None
        else:
            self.choiceIngredient = e.control.data