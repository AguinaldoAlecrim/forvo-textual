from textual.containers import Container
from textual.widgets import  Label
from rich.text import Text


def make_label_container(  
    text: str="", id: str="", border_title: str="", border_subtitle: str=""
) -> Container:
    lbl = Label(text, id=id)
    lbl.border_title = border_title
    lbl.border_subtitle = border_subtitle    
    return Container(lbl)

def change_data_traducao(object: Label, word: str, title: str, text: str):
    if word =="": return
    object.border_title = title
    object.border_subtitle = Text(f'[ {word} ]').on(click="app.apr()")
    object.update(text)

def make_markdown(dictCambridge: dict) -> str:
    list_trad = '\n'.join([f'* {item}' for item in dictCambridge['explitrad']])
    list_explic = '\n'.join([f'* {item}' for item in dictCambridge['explicacao']])
    list_example = '\n'.join([f'* {item}' for item in dictCambridge['example']])

    markdown_text = f"# {dictCambridge['word']}\n ## Traduções\n{list_trad}\n ## Explicações:\n {list_explic}\n ## Exemplos:\n{list_example}"
    return markdown_text
