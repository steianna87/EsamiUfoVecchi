import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.year = None
        self.state = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = self._model.getAllYears()
        self._listShape = self._model.getAllShapes()
        self._listYearSight = self._model.getYearsAndSight()

    def selectState(self, e):
        self.state = e.control.data

    def fillDD(self):
        for y, tot in self._listYearSight:
            self._view.ddyear.options.append(ft.dropdown.Option(text=f"{y}, sightings={tot}",
                                                                data=y,
                                                                on_click=self.handle_graph))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        year = e.control.data

        stats = self._model.creaGrafo(year)
        self._view.txt_result.controls.append(ft.Text(stats))
        self._view.btn_analizza.disabled = False
        self._view.btn_path.disabled = False

        self._view.ddstate.options.clear()
        self.state = None
        for c in self._model.grafo.nodes:
            self._view.ddstate.options.append(ft.dropdown.Option(text=f"{c}",
                                                                 data=c,
                                                                 on_click=self.selectState))

        self._view.update_page()

    def handle_analizza(self, e):
        if self.state is None:
            self._view.create_alert('seleziona uno stato')
            return
        prec, succ, conn = self._model.getAnalisi(self.state)
        self._view.txt_result.controls.append(ft.Text(f"Precedenti: {prec}\nSuccessivi: {succ}"))
        self._view.txt_result.controls.append(ft.Text(f"Stati raggiungibili ({len(conn)}): {conn}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        if self.state is None:
            self._view.create_alert('campo non valido')
            return

        sol = self._model.get_path(self.state)
        self._view.txtOut2.controls.append(ft.Text(f"Percorso di lunghezza={len(sol)}"))
        for i in range(len(sol)-1):
            self._view.txtOut2.controls.append(ft.Text(f"{sol[i]}-->{sol[i+1]}"))
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
