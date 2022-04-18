from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys


class WebView(QWebEngineView):
	def __init__(self, parent):
		super().__init__(parent)
	def createWindow(self, webWindowType):
		return main_demo.browser


class MainDemo(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setWindowTitle('MitasTech Browser By Stelios Mitas')
		self.setWindowIcon(QIcon('icons/penguin.png'))
		self.showMaximized()
		self.show()
		
		#----------URL-----------#
		self.urlbar = QLineEdit()
		# Press Enter to Navigate to url
		self.urlbar.returnPressed.connect(self.navigate_to_url)
		#----Add Tab Bar---------#
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		# -----Closing Tabs-----------#
		self.tabs.setTabsClosable(True)
		#--Set slot for close button--#
		self.tabs.tabCloseRequested.connect(self.close_current_tab)
		self.add_new_tab(QUrl('file:///C:/Users/steli/OneDrive/Desktop/MitasTechBrowser/index.html'), 'Homepage')
		self.setCentralWidget(self.tabs)
		new_tab_action = QAction(QIcon('icons/add_page.png'), 'New Page', self)
		new_tab_action.triggered.connect(self.add_new_tab)
		#---------Navigation Bar--------------#
		navigation_bar = QToolBar('Navigation')
		#---------Set Icon Size---------------#
		navigation_bar.setIconSize(QSize(16, 16))
		self.addToolBar(navigation_bar)
		#---------Add Navigation and Refresh buttons-----------------#
		back_button = QAction(QIcon('icons/back.png'), 'Back', self)
		forward_button = QAction(QIcon('icons/forward.png'), 'Forward', self)
		stop_button = QAction(QIcon('icons/stop.png'), 'Stop', self)
		reload_button = QAction(QIcon('icons/renew.png'), 'Reload', self)
		back_button.triggered.connect(self.tabs.currentWidget().back)
		forward_button.triggered.connect(self.tabs.currentWidget().forward)
		stop_button.triggered.connect(self.tabs.currentWidget().stop)
		reload_button.triggered.connect(self.tabs.currentWidget().reload)
		#--Add buttons to the navigaiton bar--#
		navigation_bar.addAction(back_button)
		navigation_bar.addAction(forward_button)
		navigation_bar.addAction(stop_button)
		navigation_bar.addAction(reload_button)
		navigation_bar.addSeparator()
		navigation_bar.addWidget(self.urlbar)

	
	# In response to the Enter button, set the URL currently
	# accessed by the browser to the URL entered by the user
	def navigate_to_url(self):
		current_url = QUrl(self.urlbar.text())
		if current_url.scheme() == '':
			current_url.setScheme('http')
		self.tabs.currentWidget().load(current_url)


	#----Update the link to the address bar----#
	def renew_urlbar(self, url, browser=None):
		# URLs not updated for non-current windows
		if browser != self.tabs.currentWidget():
			return
		self.urlbar.setText(url.toString())
		self.urlbar.setCursorPosition(0)


	#-------------------Add new tab--------------------#
	def add_new_tab(self, qurl=QUrl(''), label='Blank'):
		#-------Set Browser--------#
		self.browser = WebView(self)
		self.browser.load(qurl)
		#-----------Index Tags------------------#
		i = self.tabs.addTab(self.browser, label)
		self.tabs.setCurrentIndex(i)
		self.browser.urlChanged.connect(lambda qurl, browser=self.browser: self.renew_urlbar(qurl, self.browser))
		#-----------------------------Change the tab title to something relevant to the page---------------------------------------#
		self.browser.loadFinished.connect(lambda _, i=i, browser=self.browser: self.tabs.setTabText(i, self.browser.page().title()))
	
	
	# -----Double click on the tab bar to open a new page-----#
	def tab_open(self, i):
		if i == -1:
			self.add_new_tab(QUrl('file:///C:/Users/steli/OneDrive/Desktop/MitasTechBrowser/index.html'), 'Homepage')
	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		self.renew_urlbar(qurl, self.tabs.currentWidget())
	def close_current_tab(self, i):
		#--Don't close if there is only one current tab--#
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)



if __name__ == '__main__':
        #-------Create an instance of the QApplication class---------#
	my_application = QApplication(sys.argv) 
	main_demo = MainDemo()
	main_demo.show()
	my_application.exec_()
