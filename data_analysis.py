from analysis.top_words import TopWords
from project import db


TopWords.display_all()
TopWords.display_all(today=True)
TopWords.display_right_wing()
TopWords.display_right_wing(today=True)
TopWords.display_left_wing()
TopWords.display_left_wing(today=True)

# TopWords.graph_text()

db.close()