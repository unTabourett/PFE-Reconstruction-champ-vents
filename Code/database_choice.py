# filename_extract.py
import os

def extract_file_names(dossier):
	fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
	return fichiers

def choix_db(dossier):
	names = extract_file_names(dossier)
	if not names:
		print("No CSV files found in the directory.")
		return None

	print("Choose a database (tap a number):\n df_xx.csv : xx points pour l'interpolation")
	for i, name in enumerate(names):
		print(f"{i}. {name}")
	print(len(names),"Erreur-Interpolation : Calcul de l'évolution des erreurs L1 et L2 selon le nombre de points d'interpolation")
	# Demander à l'utilisateur de faire un choix
	while True:
		try:
			choix = int(input("Enter the number of your choice: "))
			if 0 <= choix < len(names):
				return names[choix]
			elif choix == len(names):
				return "Erreur-Interpolation"
			else:
				print("Invalid choice, please try again.")
		except ValueError:
			print("Please enter a valid number.")

