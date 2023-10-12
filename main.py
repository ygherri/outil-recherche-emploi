import sys
import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit, QListWidget, QFormLayout, QLabel, QHBoxLayout, QComboBox, QDateEdit, QMessageBox
from PySide6.QtCore import Qt

class RechercheStageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Outil de Recherche de Stage/Alternance")
        self.setGeometry(100, 100, 800, 600)

        self.conn = sqlite3.connect("recherche_stage.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS candidatures (
            id INTEGER PRIMARY KEY,
            type TEXT,
            etat TEXT,
            date TEXT,
            entreprise TEXT,
            poste TEXT,
            lien TEXT,
            texte TEXT,
            destinataire TEXT,
            notes TEXT,
            relance TEXT,
            rendezvous TEXT
        )''')

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.add_button = QPushButton("Ajouter Candidature")
        self.add_button.clicked.connect(self.ajouter_candidature)
        self.layout.addWidget(self.add_button)

    def ajouter_candidature(self):
        dialog = CandidatureDialog(self)
        if dialog.exec_():
            values = dialog.get_values()
            self.cursor.execute('''INSERT INTO candidatures (type, etat, date, entreprise, poste, lien, texte, destinataire, notes, relance, rendezvous) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', values)
            self.conn.commit()
            self.rafraichir_liste()

    def rafraichir_liste(self):
        self.list_widget.clear()
        self.cursor.execute("SELECT id, entreprise, poste FROM candidatures")
        for row in self.cursor.fetchall():
            id, entreprise, poste = row
            self.list_widget.addItem(f"{entreprise} - {poste} (ID: {id})")

class CandidatureDialog(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Ajouter une Candidature")
        self.setGeometry(200, 200, 400, 400)

        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Stage", "Alternance", "Emploi"])
        self.form_layout.addRow("Type d'Annonce:", self.type_combo)

        self.etat_combo = QComboBox()
        self.etat_combo.addItems(["Oui", "Non", "En Attente"])
        self.form_layout.addRow("État:", self.etat_combo)

        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat("dd-MM-yyyy")
        self.form_layout.addRow("Date:", self.date_edit)

        self.entreprise_line = QLineEdit()
        self.form_layout.addRow("Entreprise:", self.entreprise_line)

        self.poste_line = QLineEdit()
        self.form_layout.addRow("Poste:", self.poste_line)

        self.lien_line = QLineEdit()
        self.form_layout.addRow("Lien de l'Annonce:", self.lien_line)

        self.texte_text = QTextEdit()
        self.form_layout.addRow("Texte de l'Annonce:", self.texte_text)

        self.destinataire_line = QLineEdit()
        self.form_layout.addRow("Destinataire:", self.destinataire_line)

        self.notes_text = QTextEdit()
        self.form_layout.addRow("Notes Personnelles:", self.notes_text)

        self.relance_line = QLineEdit()
        self.form_layout.addRow("Date de Relance:", self.relance_line)

        self.rendezvous_line = QLineEdit()
        self.form_layout.addRow("Date de Rendez-vous:", self.rendezvous_line)

        self.layout.addLayout(self.form_layout)

        button_layout = QHBoxLayout()
        self.ajouter_button = QPushButton("Ajouter")
        self.annuler_button = QPushButton("Annuler")
        button_layout.addWidget(self.ajouter_button)
        button_layout.addWidget(self.annuler_button)
        self.layout.addLayout(button_layout)

        self.ajouter_button.clicked.connect(self.accept)
        self.annuler_button.clicked.connect(self.reject)

    def get_values(self):
        type = self.type_combo.currentText()
        etat = self.etat_combo.currentText()
        date = self.date_edit.date().toString("dd-MM-yyyy")
        entreprise = self.entreprise_line.text()
        poste = self.poste_line.text()
        lien = self.lien_line.text()
        texte = self.texte_text.toPlainText()
        destinataire = self.destinataire_line.text()
        notes = self.notes_text.toPlainText()
        relance = self.relance_line.text()
        rendezvous = self.rendezvous_line.text()
        return (type, etat, date, entreprise, poste, lien, texte, destinataire, notes, relance, rendezvous)

def main():
    app = QApplication(sys.argv)
    window = RechercheStageApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
