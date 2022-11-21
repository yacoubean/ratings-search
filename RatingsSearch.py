import sys
import requests
import json

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QStackedWidget
)


def begin_search(search_term):

    api_search_url = "https://imdb-api.com/en/API/Search/k_t8n76yvz/"+search_term
    api_search_response = requests.get(api_search_url)
    search_results = json.loads(api_search_response.text)
    results_list = []
    result_ids = []

    if len(search_results["errorMessage"]) == 0:
        if search_results["results"]:
            result_num = 0
            for search_result in search_results["results"]:
                result_num += 1

                results_list.append(
                    str(result_num)
                    + ": " + search_result["title"]
                    + " " + search_result["description"]
                )
                result_ids.append(search_result["id"])

            results_list.append(result_ids)
            return results_list

        else:
            results_list.append("No show was found")
            return results_list
    else:
        results_list.append(search_results["errorMessage"])
        return results_list


def display_ratings(self, list_id):

    api_rating_url = "https://imdb-api.com/en/API/Ratings/k_t8n76yvz/" + list_id
    api_rating_response = requests.get(api_rating_url)
    rating_results = json.loads(api_rating_response.text)
    result_text = ""

    if len(rating_results["errorMessage"]) == 0:
        if rating_results["fullTitle"]:
            result_text = result_text + "Title: " + rating_results["fullTitle"] + '\n\n'
        if rating_results["imDb"]:
            result_text = result_text + "imDb: " + rating_results["imDb"] + '\n'
        if rating_results["metacritic"]:
            result_text = result_text + "metacritic: " + rating_results["metacritic"] + '\n'
        if rating_results["rottenTomatoes"]:
            result_text = result_text + "rottenTomatoes: " + rating_results["rottenTomatoes"] + '\n'
        if rating_results["theMovieDb"]:
            result_text = result_text + "theMovieDb: " + rating_results["theMovieDb"] + '\n'
        if rating_results["filmAffinity"]:
            result_text = result_text + "filmAffinity: " + rating_results["filmAffinity"] + '\n'
    else:
        result_text = result_text + rating_results["errorMessage"]

    result_label = QLabel()
    result_label.setText(result_text)
    result_label.setStyleSheet('font-size:12pt')
    self.results_box.addWidget(result_label)
    self.results_box.setCurrentIndex(1)


class SearchResults(QWidget):

    def __init__(self, results_list):
        super().__init__()

        self.results_box = QStackedWidget()
        self.results_buttons = QWidget()
        self.results_layout = QVBoxLayout()
        i = 0

        results_ids = results_list[len(results_list)-1]

        for search_result in results_list:
            if isinstance(search_result, str) and i < 10:
                results_btn = QPushButton(search_result)
                results_btn.setFlat(True)
                results_btn.setStyleSheet("text-align:left; font-size:10pt")
                results_btn.pressed.connect(lambda list_id=results_ids[i]: display_ratings(self, list_id))
                self.results_layout.addWidget(results_btn)
                i += 1

        self.results_buttons.setLayout(self.results_layout)
        self.results_box.addWidget(self.results_buttons)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Show Ratings Search")
        self.outer_layout = QVBoxLayout()
        self.search_layout = QHBoxLayout()
        self.results_box = QStackedWidget()

        self.search_label = QLabel("Search:")
        self.search_text_box = QLineEdit(self)
        self.search_text_box.returnPressed.connect(self.ratings_search)
        self.utility_area = QLabel()
        self.utility_area.setMinimumWidth(50)
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_text_box)
        self.search_layout.addWidget(self.utility_area)

        self.outer_layout.addLayout(self.search_layout)

        self.setLayout(self.outer_layout)

    def ratings_search(self):
        self.clear_prev_results()

        self.utility_area.setText("Searching...")
        app.processEvents()
        search_result = begin_search(self.search_text_box.text())
        self.results_box = SearchResults(search_result).results_box
        self.outer_layout.addWidget(self.results_box)
        self.utility_area.setText("")

    def clear_prev_results(self):
        num_widgets = self.outer_layout.count() - 1
        while num_widgets > 0:
            this_widget = self.outer_layout.itemAt(num_widgets).widget()
            this_widget.deleteLater()
            num_widgets -= 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_window = MainWindow()
    app_window.show()
    sys.exit(app.exec_())
