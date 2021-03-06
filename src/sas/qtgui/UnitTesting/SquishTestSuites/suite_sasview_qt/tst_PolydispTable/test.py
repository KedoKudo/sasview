# -*- coding: utf-8 -*-

def main():
    startApplication("sasview")
    mouseClick(waitForObject(":groupBox_6.cbCategory_QComboBox_2"), 68, 16, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":groupBox_6.cbCategory_QComboBox_2", "Cylinder"), 66, 7, 0, Qt.LeftButton)
    clickButton(waitForObject(":groupBox_7.chkPolydispersity_QCheckBox"))
    test.compare(waitForObjectExists(":qt_tabwidget_tabbar.Polydispersity_TabItem").enabled, True)
    clickTab(waitForObject(":FittingWidgetUI.tabFitting_QTabWidget_2"), "Polydispersity")
    test.compare(waitForObjectExists(":lstPoly.0_0_QModelIndex").checkState, "unchecked")
    test.compare(waitForObjectExists(":lstPoly.0_0_QModelIndex").text, "Distribution of radius_bell")
    test.compare(waitForObjectExists(":lstPoly.0_0_QModelIndex").enabled, True)
    test.compare(waitForObjectExists(":lstPoly.1_0_QModelIndex").text, "Distribution of radius")
    test.compare(waitForObjectExists(":lstPoly.1_0_QModelIndex").checkState, "unchecked")
    test.compare(waitForObjectExists(":lstPoly.1_0_QModelIndex").enabled, True)
    test.compare(waitForObjectExists(":lstPoly.2_0_QModelIndex").row, 2)
    test.compare(waitForObjectExists(":lstPoly.2_0_QModelIndex").checkState, "unchecked")
    test.compare(waitForObjectExists(":lstPoly.2_0_QModelIndex").enabled, True)
    test.compare(waitForObjectExists(":lstPoly.2_0_QModelIndex").text, "Distribution of length")
    test.compare(waitForObjectExists(":lstPoly_QComboBox").count, 5)
    test.compare(waitForObjectExists(":lstPoly_QComboBox").enabled, True)
    test.compare(waitForObjectExists(":lstPoly_QComboBox").currentIndex, 3)
    test.compare(str(waitForObjectExists(":lstPoly_QComboBox").currentText), "gaussian")
    test.compare(waitForObjectExists(":lstPoly_QComboBox").visible, True)
    test.compare(waitForObjectExists(":lstPoly.0_4_QModelIndex").text, "35")
    test.compare(waitForObjectExists(":lstPoly.0_5_QModelIndex").text, "3")
    mouseClick(waitForObject(":lstPoly_QComboBox"), 70, 19, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":lstPoly_QComboBox", "rectangle"), 63, 5, 0, Qt.LeftButton)
    test.compare(waitForObjectExists(":lstPoly.0_4_QModelIndex").text, "35")
    test.compare(waitForObjectExists(":lstPoly.0_5_QModelIndex").text, "1.70325")
    test.compare(str(waitForObjectExists(":lstPoly_QComboBox").currentText), "rectangle")
    mouseClick(waitForObject(":lstPoly_QComboBox"), 70, 11, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":lstPoly_QComboBox", "lognormal"), 52, 7, 0, Qt.LeftButton)
    test.compare(waitForObjectExists(":lstPoly.0_4_QModelIndex").text, "80")
    test.compare(waitForObjectExists(":lstPoly.0_5_QModelIndex").text, "8")
    test.compare(str(waitForObjectExists(":lstPoly_QComboBox").currentText), "lognormal")
    mouseClick(waitForObject(":lstPoly_QComboBox_2"), 48, 14, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":lstPoly_QComboBox_2", "schulz"), 26, 8, 0, Qt.LeftButton)
    test.compare(waitForObjectExists(":lstPoly.2_4_QModelIndex").text, "35")
    test.compare(waitForObjectExists(":lstPoly.2_5_QModelIndex").text, "3")
    test.compare(str(waitForObjectExists(":lstPoly_QComboBox_3").currentText), "gaussian")
    mouseClick(waitForObject(":lstPoly_QComboBox"), 43, 11, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":lstPoly_QComboBox", "array"), 28, 8, 0, Qt.LeftButton)   
    test.compare(waitForObjectExists(":QFileDialog_QFileDialog").visible, True)
    test.compare(str(waitForObjectExists(":QFileDialog_QFileDialog").windowTitle), "Choose a weight file")
    clickButton(waitForObject(":QFileDialog.Cancel_QPushButton"))
    test.compare(str(waitForObjectExists(":lstPoly_QComboBox").currentText), "schulz")
    mouseClick(waitForObjectItem(":lstPoly_QComboBox_2", "array"), 48, 8, 0, Qt.LeftButton)
    waitForObjectItem(":stackedWidget.listView_QListView_2", "test")
    doubleClickItem(":stackedWidget.listView_QListView_2", "test", 28, 5, 0, Qt.LeftButton)
    waitForObjectItem(":stackedWidget.listView_QListView_2", "1d\\_data")
    doubleClickItem(":stackedWidget.listView_QListView_2", "1d\\_data", 43, 6, 0, Qt.LeftButton)
    waitForObjectItem(":stackedWidget.listView_QListView_2", "circular\\_test\\.txt")
    clickItem(":stackedWidget.listView_QListView_2", "circular\\_test\\.txt", 102, 10, 0, Qt.LeftButton)
    clickButton(waitForObject(":FittingWidgetUI.Open_QPushButton"))
    test.compare(waitForObjectExists(":lstPoly.1_0_QModelIndex").enabled, True)
    test.compare(waitForObjectExists(":lstPoly.1_1_QModelIndex").enabled, False)
    test.compare(waitForObjectExists(":lstPoly.1_4_QModelIndex").enabled, False)
    test.compare(waitForObjectExists(":lstPoly.1_5_QModelIndex").enabled, False)
    test.compare(str(waitForObjectExists(":lstPoly_QComboBox_2").currentText), "array")
    test.compare(waitForObjectExists(":lstPoly.1_7_QModelIndex").text, "circular_test.txt")
