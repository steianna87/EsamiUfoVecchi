import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = self._model.getAllYears()
        self._listShape = self._model.getAllShapes()

    def selectState(self, e):
        self.state = e.control.data

    def fillDD(self):
        for y in self._listYear:
            if y > 1905:
                self._view.ddyear.options.append(ft.dropdown.Option(y))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        try:
            year = self._view.ddyear.value
        except TypeError:
            self._view.create_alert('seleziona un anno')
            return
        day = self.checkIntTextField(self._view.numDay)
        if day < 1 or day > 180:
            self._view.create_alert('seleziona un numero di giorni tra 1 e 180')

        stats = self._model.creaGrafo(day, year)
        self._view.txt_result.controls.append(ft.Text(stats))
        self._view.btn_path.disabled = False

        for c in self._model.grafo.nodes:
            self._view.ddTarget.options.append(ft.dropdown.Option(c))

        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        target = self._view.ddTarget.value
        IntMaxD = self.checkIntTextField(self._view.maxD)
        IntMinC = self.checkIntTextField(self._view.minCity)
        if IntMinC <= 1 or IntMaxD <= 0 or target is None:
            self._view.create_alert('campo non valido')
            return

        sol, maxPeso = self._model.get_path(target, IntMaxD, IntMinC)
        self._view.txtOut2.controls.append(ft.Text(f"Percorso di peso={maxPeso}"))
        for i in range(len(sol)-1):
            self._view.txtOut2.controls.append(ft.Text(f"{sol[i]}-->{sol[i+1]} peso="
                                                       f"{self._model.grafo[sol[i]][sol[i+1]]['weight']}"))
        self._view.update_page()

    def checkIntTextField(self, text: ft.TextField):
        val = text.value
        if val is None:
            return 0
        try:
            Intval = int(val)
        except ValueError:
            return 0
        return Intval
