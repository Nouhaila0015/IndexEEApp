from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout



kv_code = """
<Window>:
    orientation: "vertical"
    spacing: 10

    BoxLayout:
        size_hint_y: None
        height: 50
        Label:
            text: "Gestion Relevée des Index"
            bold: True
            size_hint_x: .9
        Button:
            text: "..."
            size_hint_x: .1
            on_release: app.menu_open()
        Button:
            id: button
            text: "Ok"
            size_hint_x: .1
            on_release: app.update_releve()
    GridLayout:
        cols: 2
        spacing: (20, 10)

        Label:
            text: "Localité"
        Label:
            text: "Secteur"
        
        TextInput:
            id: localite_input
            hint_text: "Localité"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height
        Spinner:
            id: secteur_input
            text: "Select Secteur"
            values: app.get_available_secteurs()
            on_text: app.on_secteur_selected(self, self.text)  

        Label:
            text: "Tournée"
        Label:
            text: "Gérance"
        
        TextInput:
            id: tournee_input
            hint_text: "Tournée"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height
        TextInput:
            id: gerance_input
            hint_text: "Gérance"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height

        Label:
            text: "Nom"
        Label:
            text: "Cat"
        
        TextInput:
            id: nom_input
            hint_text: "Nom"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height
        TextInput:
            id: cat_input
            hint_text: "Cat"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height

        Label:
            text: "Adresse"
        Label:
            text: "Police"
        
        TextInput:
            id: adresse_input
            hint_text: "Adresse"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height
        TextInput:
            id: police_input
            hint_text: "Police"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height

        Label:
            text: "Compteur"
        Label:
            text: ""
        
        TextInput:
            id: compteur_input
            hint_text: "Compteur"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height
        Label:

        Label:
            text: "Ancien Index"
        Label:
            text: "Nouveau Index"
        
        TextInput:
            id: ancien_input
            hint_text: "Ancien Index"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height
        TextInput:
            id: nouveau_input
            hint_text: "Nouveau Index"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height

        Label:
            text: "Anomalie"
        TextInput:
            id: anomalie_input
            hint_text: "Anomalie"
            multiline: False
            size_hint_x: 0.3
            height: self.minimum_height

    BoxLayout:
        spacing: 0
        size_hint_y: 0.1
        Button:
            text: "Précédent"
            size_hint_x: 0.2
            on_release: app.previous_account()
        Button:
            text: "Suivant"
            size_hint_x: 0.2
            on_release: app.next_account()
        Button:
            text: "Recherche"
            size_hint_x: 0.2
            on_release: app.on_recherche()
"""



Builder.load_string(kv_code)


class Window(BoxLayout):
    pass

