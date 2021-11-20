from app import App
from view.scrape_view import ScrapeView
from view.upload_view import UploadView
from view.download_view import DownloadView
from  flask_cors import CORS
# from .view import upload_view
# from .view import download_view

app = App([
    ScrapeView(),
    UploadView(),
    DownloadView()
])
app.run()
