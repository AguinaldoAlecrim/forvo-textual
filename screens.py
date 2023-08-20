from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll, Grid, Vertical
from textual.widgets import (
    Label, 
    MarkdownViewer, 
    Button, 
    ListItem,
    ListView
    )

from funcoes import make_markdown



class HistoryScreen(Screen):
    """Screen with a dialog to quit."""
    def __init__(self, historySearch):
        super().__init__()
        self.historySearch = historySearch

    def compose(self) -> ComposeResult:
        l = []
        for x in self.historySearch:
            l.append(Label(x['word']))

         
        yield Grid(
            Vertical(
                Label("Repetir"),
                ListView(id="list-history"),
                id="popup-dialog"            
            ),
            Horizontal(            
                Button("Fechar", variant="primary", id="cancel"),
                id="barbutton"
            ),
            id="dialog",
        )
    def on_mount(self):
        self.query_one('#list-history').clear()
        
        for cdWord in self.historySearch:
            l = ListItem(Label(cdWord['word'], classes="itemList"), classes="itemHistory")
            self.query_one('#list-history').append(l)
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":            
            self.app.pop_screen()


class MarkdownScreen(Screen):
    def __init__(self, dictmark):
        super().__init__()
        self.dictmark = dictmark

    def compose(self) -> ComposeResult:
        yield Grid(
            Vertical(
                MarkdownViewer(make_markdown(self.dictmark),show_table_of_contents=True),
                id='popup-dialog'
            ),
            Horizontal(            
                Button("Fechar", variant="warning", id="quitMD"),
                id="barbutton"
            ),
            id="modalMD"
        )
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'quitMD':
            self.app.pop_screen()
