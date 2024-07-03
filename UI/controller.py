import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = self._model.getAllYears()
        self._listShape = self._model.getAllShapes()
        self.listSight = self._model.detStates()

    def selectState(self, e):
        self.state = e.control.data

    def fillDD(self):
        for st in self.listSight:
            self._view.ddstate.options.append(ft.dropdown.Option(text=f"{st}",
                                                                 data=st,
                                                                 on_click=self.selectState))
        for s in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()

        state = self.state.id
        shape = self._view.ddshape.value
        if state is None or shape is None:
            self._view.create_alert('seleziona i campi richiesti')
            return
        stats = self._model.creaGrafo(shape, state)
        self._view.txt_result.controls.append(ft.Text(stats))
        self._view.btn_path.disabled = False
        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        maxC = self._view.maxCity.value
        if maxC is None:
            self._view.create_alert('seleziona un numero max di città')
            return
        try:
            IntMaxC = int(maxC)
        except ValueError:
            self._view.create_alert('campo non valido')
            return
        if IntMaxC <=1:
            self._view.create_alert('campo non valido')
            return

        sol, maxPeso = self._model.get_path(IntMaxC)
        self._view.txtOut2.controls.append(ft.Text(f"Percorso di peso={maxPeso}"))
        for i in range(len(sol)-1):
            self._view.txtOut2.controls.append(ft.Text(f"{sol[i]}-->{sol[i+1]} peso="
                                                       f"{self._model.grafo[sol[i]][sol[i+1]]['weight']}"))
        self._view.update_page()
