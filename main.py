import sqlite3
import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from window import Window
from database import create_tables
from menu import MenuPopup
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from datetime import datetime
import os

class Interface(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_secteur = None
        self.current_account_rowid = None
        self.exported_data = []

    def build(self):
        self.load_app_data()
        return Window()

    def load_app_data(self):
        try:
            create_tables()
            conn = sqlite3.connect('releve.db')
            c = conn.cursor()
            c.execute(
                "INSERT OR IGNORE INTO AppData (Client_secteur, localite, gerance, Police) SELECT DISTINCT secteur, 0, 0, 0 FROM Releve"
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("An error occurred while loading app data:", e)

    def get_available_secteurs(self):
        try:
            conn = sqlite3.connect('releve.db')
            c = conn.cursor()
            c.execute("SELECT Client_secteur FROM AppData")
            secteurs = [str(row[0]) for row in c.fetchall()]
            conn.close()
            return secteurs
        except sqlite3.Error as e:
            print("An error occurred while getting available secteurs:", e)
            return []

    def display_account(self):
        if self.selected_secteur is not None:
            try:
                conn = sqlite3.connect('releve.db')
                c = conn.cursor()

                c.execute("""
                    SELECT EXISTS(
                        SELECT 1 FROM AppData 
                        WHERE Client_secteur = ? AND localite = 0 AND gerance = 0 AND Police = 0
                    )
                """, (self.selected_secteur,))
                exists = c.fetchone()[0] == 1

                if exists:
                    # The row exists, execute the first query
                    c.execute("""
                        SELECT R.Localite, R.secteur, R.trn, R.ord, R.id_gerance, R.id_categorie, 
                            R.numPolice, R.nom, R.adresse, R.numCompteur, R.NbrRoues, R.index2, 
                            R.index1, R.CodeAnomalie
                        FROM Releve R
                        WHERE R.secteur = ?
                        LIMIT 1
                    """, (self.selected_secteur,))
                else:
                    # The row does not exist, execute the second query
                    c.execute("""
                        SELECT R.Localite, R.secteur, R.trn, R.ord, R.id_gerance, R.id_categorie, 
                            R.numPolice, R.nom, R.adresse, R.numCompteur, R.NbrRoues, R.index2, 
                            R.index1, R.CodeAnomalie
                        FROM Releve R
                        JOIN AppData AD ON R.Localite = AD.localite AND R.numPolice = AD.Police 
                                        AND R.id_gerance = AD.gerance
                        WHERE R.secteur = ? AND AD.Client_secteur = ? 
                        LIMIT 1
                    """, (self.selected_secteur, self.selected_secteur))

                account = c.fetchone()
                conn.close()

                if account:
                    self.update_account_fields(account)
                    self.current_account_rowid = self.get_account_rowid(account)
                else:
                    # If no account data is found, clear the account fields
                    self.update_account_fields(None)
                    self.current_account_rowid = None

            except sqlite3.Error as e:
                print("An error occurred while displaying account:", e)

    def update_account_fields(self, account):
        if self.root:
            try:
                if account is not None:
                    (
                        localite,
                        secteur,
                        trn,
                        ord,
                        gerance,
                        categorie,
                        numPolice,
                        nom,
                        adresse,
                        numCompteur,
                        NbrRoues,
                        index2,
                        index1,
                        CodeAnomalie,
                    ) = account

                    self.root.ids.localite_input.text = str(localite)
                    self.root.ids.secteur_input.text = str(secteur)
                    self.root.ids.tournee_input.text = str(trn)
                    self.root.ids.gerance_input.text = str(gerance)
                    self.root.ids.nom_input.text = str(nom)
                    self.root.ids.cat_input.text = str(categorie)
                    self.root.ids.adresse_input.text = str(adresse)
                    self.root.ids.police_input.text = str(numPolice)
                    self.root.ids.compteur_input.text = str(numCompteur)
                    self.root.ids.ancien_input.text = str(index1)
                    self.root.ids.nouveau_input.text = str(index2)
                    self.root.ids.anomalie_input.text = str(CodeAnomalie)
                    # Set other input fields as read-only
                    self.root.ids.localite_input.readonly = True
                    self.root.ids.tournee_input.readonly = True
                    self.root.ids.gerance_input.readonly = True
                    self.root.ids.nom_input.readonly = True
                    self.root.ids.cat_input.readonly = True
                    self.root.ids.adresse_input.readonly = True
                    self.root.ids.police_input.readonly = True
                    self.root.ids.compteur_input.readonly = True
                    self.root.ids.ancien_input.readonly = True
                else:
                    # Clear the input fields when account is None
                    self.root.ids.localite_input.text = ""
                    self.root.ids.secteur_input.text = ""
                    self.root.ids.tournee_input.text = ""
                    self.root.ids.gerance_input.text = ""
                    self.root.ids.nom_input.text = ""
                    self.root.ids.cat_input.text = ""
                    self.root.ids.adresse_input.text = ""
                    self.root.ids.police_input.text = ""
                    self.root.ids.compteur_input.text = ""
                    self.root.ids.ancien_input.text = ""
                    self.root.ids.nouveau_input.text = ""
                    self.root.ids.anomalie_input.text = ""
                    # Set other input fields as read-only
                    self.root.ids.localite_input.readonly = True
                    self.root.ids.tournee_input.readonly = True
                    self.root.ids.gerance_input.readonly = True
                    self.root.ids.nom_input.readonly = True
                    self.root.ids.cat_input.readonly = True
                    self.root.ids.adresse_input.readonly = True
                    self.root.ids.police_input.readonly = True
                    self.root.ids.compteur_input.readonly = True
                    self.root.ids.ancien_input.readonly = True

            except Exception as e:
                print("An error occurred while updating account fields:", e)

    def fetch_next_account(self):
        if self.selected_secteur is not None and self.current_account_rowid is not None:
            conn = sqlite3.connect('releve.db')
            c = conn.cursor()

            # Fetch the next account from the database
            c.execute("""
                SELECT R.Localite, R.secteur, R.trn, R.ord, R.id_gerance, R.id_categorie, 
                       R.numPolice, R.nom, R.adresse, R.numCompteur, R.NbrRoues, R.index2, 
                       R.index1, R.CodeAnomalie
                FROM Releve R
                WHERE R.secteur = ? AND rowid > ?
                ORDER BY rowid ASC
                LIMIT 1
            """, (self.selected_secteur, self.current_account_rowid))

            next_account = c.fetchone()
            conn.close()

            return next_account

    def fetch_previous_account(self):
        if self.selected_secteur is not None and self.current_account_rowid is not None:
            conn = sqlite3.connect('releve.db')
            c = conn.cursor()

            # Fetch the previous account from the database
            c.execute("""
                SELECT R.Localite, R.secteur, R.trn, R.ord, R.id_gerance, R.id_categorie, 
                       R.numPolice, R.nom, R.adresse, R.numCompteur, R.NbrRoues, R.index2, 
                       R.index1, R.CodeAnomalie
                FROM Releve R
                WHERE R.secteur = ? AND rowid < ?
                ORDER BY rowid DESC
                LIMIT 1
            """, (self.selected_secteur, self.current_account_rowid))

            previous_account = c.fetchone()
            conn.close()

            return previous_account

    def next_account(self):
        next_account = self.fetch_next_account()

        if next_account:
            self.update_account_fields(next_account)
            self.current_account_rowid = self.get_account_rowid(next_account)

    def previous_account(self):
        previous_account = self.fetch_previous_account()

        if previous_account:
            self.update_account_fields(previous_account)
            self.current_account_rowid = self.get_account_rowid(previous_account)

    def get_account_rowid(self, account):
        conn = sqlite3.connect('releve.db')
        c = conn.cursor()

        c.execute("""
            SELECT rowid FROM Releve 
            WHERE Localite = ? AND numPolice = ? AND id_gerance = ?
            LIMIT 1
        """, (account[0], account[6], account[4]))

        rowid = c.fetchone()[0]
        conn.close()

        return rowid

    def on_secteur_selected(self, instance, value):
        self.selected_secteur = value
        self.display_account()

    def update_releve(self):
        try:
            index2 = self.root.ids.nouveau_input.text
            anomalie = self.root.ids.anomalie_input.text

            conn = sqlite3.connect('releve.db')
            c = conn.cursor()

            # Get the primary key values (localite, gerance, police) for the current account
            c.execute(
                "SELECT Localite, id_gerance, numPolice FROM Releve WHERE rowid = ?",
                (self.current_account_rowid,)
            )
            key_values = c.fetchone()

            if key_values:
                localite, gerance, police = key_values

                # Update Releve table with the new values and current date
                c.execute(
                    "UPDATE Releve SET index2 = ?, CodeAnomalie = ?, last_update = ? WHERE Localite = ? AND id_gerance = ? AND numPolice = ?",
                    (index2, anomalie, datetime.now(), localite, gerance, police),
                )
                conn.commit()

                # Update AppData table with the current row's primary key
                c.execute(
                    "UPDATE AppData SET localite = ?, gerance = ?, Police = ? WHERE Client_secteur = ?",
                    (localite, gerance, police, self.selected_secteur),
                )
                conn.commit()

            conn.close()

        except Exception as e:
            print("An error occurred while updating releve:", e)

    
    def open_file_chooser(self):
        root = tk.Tk()
        root.withdraw() 

        file_path = filedialog.askopenfilename(
            title="Choose a File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if file_path:
            self.import_data_from_file(file_path)

    def file_chooser_callback(self, instance, selected_file, *args):  
        self.import_data_from_file(selected_file)

    def import_data_from_file(self, selected_file):
        try:
            conn = sqlite3.connect('releve.db')
            c = conn.cursor()

            # Delete existing rows in the table
            c.execute("DELETE FROM Releve")
            c.execute("DELETE FROM AppData")

            # Read the contents of the selected file
            with open(selected_file, 'r') as file:
                lines = file.readlines()

            # Insert each line as a row in the table
            for index, line in enumerate(lines):
                # Skip empty lines
                if line.strip() == '':
                    continue

                # Split the line into columns
                values = line.strip().split('#')

                # Remove leading/trailing spaces from each value
                values = [v.strip() for v in values]

                # Remove any empty values
                values = [v for v in values if v != '']

                # Add a null value if the number of values is 13
                if len(values) == 13:
                    values.append(None)

                # Ensure all 14 values are present
                if len(values) != 14:
                    print(f"Skipping invalid row at index {index}: {values}")
                    continue

                # Insert the values into the table
                c.execute(
                    "INSERT INTO Releve (Localite, secteur, trn, ord, id_gerance, id_categorie, numPolice, nom, adresse, numCompteur, NbrRoues, index2, index1, CodeAnomalie) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    values,
                )

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            self.update_releve()
        except Exception as e:
            print("An error occurred while importing the file:", e)

    def menu_open(self):
        menu = MenuPopup(interface_instance=self)
        menu.open()

    def on_recherche(self):
        localite_input = self.root.ids.localite_input
        gerance_input = self.root.ids.gerance_input
        compteur_input = self.root.ids.compteur_input
        nom_input = self.root.ids.nom_input
        adresse_input = self.root.ids.adresse_input

        # Get the values entered by the user in the input boxes
        localite = localite_input.text.strip()
        gerance = gerance_input.text.strip()
        numCompteur = compteur_input.text.strip()
        nom = nom_input.text.strip()
        adresse = adresse_input.text.strip()

        # Check if all input boxes are empty
        if not any([localite, gerance, numCompteur, nom, adresse]):
            self.show_warning_popup("Please enter values for at least one of the criteria.")
            return

        try:
            conn = sqlite3.connect('releve.db')
            c = conn.cursor()

            # Construct the SQL query based on the provided criteria
            query = "SELECT * FROM Releve WHERE "
            conditions = []

            if localite:
                conditions.append(f"Localite = '{localite}'")
            if gerance:
                conditions.append(f"id_gerance = '{gerance}'")
            if numCompteur:
                conditions.append(f"numCompteur = '{numCompteur}'")
            if nom:
                conditions.append(f"nom ='{nom}'")
            if adresse:
                conditions.append(f"adresse = '{adresse}'")

            query += " AND ".join(conditions)

            # Execute the query and fetch the first matching record
            c.execute(query)
            record = c.fetchone()

            if record:
                # Update the input boxes with the values from the matching record
                localite_input.text = str(record[0])
                self.root.ids.secteur_input.text = str(record[1])
                self.root.ids.tournee_input.text = str(record[2])
                gerance_input.text = str(record[4])
                self.root.ids.cat_input.text = str(record[5])
                compteur_input.text = str(record[6])
                self.root.ids.nom_input.text = str(record[7])
                self.root.ids.adresse_input.text = str(record[8])
                self.root.ids.compteur_input.text = str(record[9])
                # Check if the nbr_roues_input exists before updating it
                if 'nbr_roues_input' in self.root.ids:
                    self.root.ids.nbr_roues_input.text = str(record[10])
                self.root.ids.nouveau_input.text = str(record[11])
                self.root.ids.ancien_input.text = str(record[12])
                self.root.ids.anomalie_input.text = str(record[13])

                # Update the current_account_rowid to the rowid of the fetched record
                self.current_account_rowid = self.get_account_rowid(record)
            else:
                # If no records are found, display a warning pop-up
                self.show_warning_popup("No matching records found.")

            conn.close()

        except sqlite3.Error as e:
            print("An error occurred while searching:", e)

    def show_warning_popup(self, message):
        content = BoxLayout(orientation="vertical")
        label = Label(text=message)
        close_button = Button(text="OK", size_hint_y=None, height=40)

        content.add_widget(label)
        content.add_widget(close_button)

        popup = Popup(title="Warning", content=content, size_hint=(None, None), size=(300, 200))
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def enable_input_boxes(self):
        # Enable the input boxes for user input
        localite_input = self.root.ids.localite_input
        secteur_input = self.root.ids.secteur_input
        gerance_input = self.root.ids.gerance_input
        police_input = self.root.ids.police_input

        localite_input.readonly = False
        secteur_input.readonly = False
        gerance_input.readonly = False
        police_input.readonly = False

    def export_data_to_file(self):
        try:
            conn = sqlite3.connect('releve.db')
            c = conn.cursor()

            c.execute("SELECT * FROM Releve")
            data = c.fetchall()

            with open("exported_data.txt", "w") as file:
                for row in data:
                    row_str = '#'.join(map(str, row))  # Join row values with '#'
                    file.write(row_str + "\n")
            print("Data exported to exported_data.txt successfully.")

            conn.close()
        except Exception as e:
            print("An error occurred while exporting data:", e)


if __name__ == "__main__":
    sa = Interface()
    sa.run()
