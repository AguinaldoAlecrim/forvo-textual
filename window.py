from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import (
    Header, 
    Footer, 
    Input, 
    Button, 
    Label, 
    ListView, 
    ListItem
)
from textual.containers import (
    Container, 
    Horizontal, 
    VerticalScroll, 
    Vertical
)
from textual import events
from forvoTUI import Forvo
from cabridge import Dictionary

from screens import (
    MarkdownScreen,
    HistoryScreen,
)

from funcoes import (
    make_label_container,
    change_data_traducao
)

f = Forvo()
cambridge = Dictionary()

class MyForvo(App):
    TITLE=  'FORVO'
    BINDINGS = [
        Binding(key="q", action="quit", description="Sair da aplicação")    
    ]
    CSS_PATH = "./styles/layout.css"

    def __init__(self, historySearch=[], lastCambridge={}):
        super().__init__()
        self.historySearch = historySearch
        self.lastCambridge = lastCambridge

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with Container(id="app-grid"):
            with VerticalScroll(id="left-pane"):                
                yield Label("Últimas pesquisas:",classes="header-div-left")
                self.lstV = ListView(
                        classes="lst-view"
                    )
                yield self.lstV
        
            with Horizontal(id="top-right"):
                with Container():
                    yield Label("Digite a Palavra ou expressão:")
                    self.input =  Input(id="inp-search", placeholder="Insira a palavra aqui")
                    yield self.input
                    with Horizontal(classes="div-btn"):
                        self.btn = Button(
                            variant="success",
                            label="Pesquisar", 
                            id="search-btn",
                        )
                        yield self.btn

                        self.btnRepeter = Button(
                            variant="primary",
                            label="Repetir",
                            id="btn-repetir"
                        )
                        yield self.btnRepeter

                        self.btn_hist = Button(
                            variant="primary",
                            label="Histórico",
                            id="btn_hist"
                        )
                        yield self.btn_hist

                    with Vertical(id="buttom-down"):                        
                        yield make_label_container("", 'explic', "Explicações:", "")
                        yield make_label_container("", 'traducao', "Tradução:", "")
                        yield make_label_container("", 'context', "Contexto:", "")

    def on_list_view_selected(self, event: ListView.Selected):
        if event.item.has_class("itemHistory"):
            filtered_list = filter(lambda dict: dict['word'] == str(event.item.children[0].render()), self.historySearch)
            bytedata = list(filtered_list)[0]['bytedados']
            f.repetir_audio(bytedata)

    async def execute(self, word):
        bytesdata = f.play(word)
        if bytesdata == False:
            return None # se a palavra não for encontrada sai do handler
        

        if any(dict['word'] == word for dict in self.historySearch):
            return None
        self.historySearch.append({
            "word":self.input.value,
            "bytedados": bytesdata
        })
        self.lstV.clear()
        for cdWord in self.historySearch:
            l = ListItem(Label(cdWord['word'], classes="itemList"), classes="itemHistory")
            self.lstV.append(l)
        

    async def on_button_pressed(self, event:Button.Pressed):
        if event.button.id == "search-btn":            
            word = self.input.value
            if word == "": return
            dadosWord = cambridge.getDictionary(word)
            prop_to_extract = ['explicacao', 'explitrad', 'example']
            self.lastCambridge = dict(
                        zip(
                            prop_to_extract, 
                            [dadosWord[k] for k in prop_to_extract]
                            )
                        )
            self.lastCambridge["word"] = word
            await self.execute(word)
            def organiza(aList: list) -> str:
                # Converte a lista em uma string separada por vírgulas
                string = ', '.join(aList)
                # Substitui a última vírgula por "e"
                string = string.rsplit(',', 1)
                string = ' e '.join(string)
                return string
                


            change_data_traducao(
                object=self.query_one("#traducao"), 
                title=f'Tradução - [ [bold magenta]{word}[/bold magenta] ]', 
                word=word, 
                text=organiza(dadosWord['explitrad'])
                )
            
            change_data_traducao(
                object=self.query_one("#context"), 
                title=f'Exemplos - [ [bold magenta]{word}[/bold magenta] ]', 
                word=word, 
                text=organiza(dadosWord['example'])
                )
            change_data_traducao(
                object=self.query_one("#explic"), 
                title=f'Explicações - [ [bold magenta]{word}[/bold magenta] ]', 
                word=word, 
                text=organiza(dadosWord['explicacao'])
                )
            # limpa e foca no input
            self.input.value = ""
            self.input.focus()

            

        if event.button.id == "btn-repetir":
            self.testeVerticalScroll()

        if event.button.id == "btn_hist":
            self.push_screen(HistoryScreen(self.historySearch))
    def action_apr(self):
        self.push_screen(MarkdownScreen(self.lastCambridge))


    def on_key(self, event: events.Key):
        if event.key == 'enter':
            self.btn.action_press()

    
    def updateHystori(self):
        print("isso é um tste")
        

    def testeVerticalScroll(self):
        try:
            f.repetir_audio(self.historySearch[-1]["bytedados"])
        except:
            print("error")
             
                    
if __name__ == '__main__':
    app = MyForvo()
    app.run()