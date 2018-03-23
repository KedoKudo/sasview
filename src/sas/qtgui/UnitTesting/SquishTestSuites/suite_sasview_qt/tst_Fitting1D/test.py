# -*- coding: utf-8 -*-

def main():
    startApplication("sasview")
    clickButton(waitForObject(":groupBox.cmdLoad_QPushButton"))
    waitForObjectItem(":stackedWidget.listView_QListView", "test")
    doubleClickItem(":stackedWidget.listView_QListView", "test", 38, 7, 0, Qt.LeftButton)
    waitForObjectItem(":stackedWidget.listView_QListView", "1d\\_data")
    doubleClickItem(":stackedWidget.listView_QListView", "1d\\_data", 40, 7, 0, Qt.LeftButton)
    waitForObjectItem(":stackedWidget.listView_QListView", "cyl\\_400\\_20\\.txt")
    doubleClickItem(":stackedWidget.listView_QListView", "cyl\\_400\\_20\\.txt", 94, 5, 0, Qt.LeftButton)
    clickButton(waitForObject(":groupBox.cmdSendTo_QPushButton"))
    mouseClick(waitForObject(":groupBox_6.cbCategory_QComboBox_2"), 162, 13, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":groupBox_6.cbCategory_QComboBox_2", "Cylinder"), 143, 10, 0, Qt.LeftButton)
    waitForObjectItem(":groupBox_6.lstParams_QTreeView_4", "length")
    clickItem(":groupBox_6.lstParams_QTreeView_4", "length", 12, 12, 0, Qt.LeftButton)
    waitForObjectItem(":groupBox_6.lstParams_QTreeView_4", "radius")
    clickItem(":groupBox_6.lstParams_QTreeView_4", "radius", 12, 9, 0, Qt.LeftButton)
    waitForObjectItem(":groupBox_6.lstParams_QTreeView_4", "radius\\_bell")
    clickItem(":groupBox_6.lstParams_QTreeView_4", "radius\\_bell", 14, 11, 0, Qt.LeftButton)
    clickButton(waitForObject(":FittingWidgetUI.cmdFit_QPushButton"))
    snooze(6)
    test.compare(waitForObjectExists(":lstParams.26.223_QModelIndex").text, "26.223")
    test.compare(waitForObjectExists(":lstParams.26.223_QModelIndex").row, 4)
    test.compare(waitForObjectExists(":lstParams.26.223_QModelIndex").column, 1)
    test.compare(waitForObjectExists(":lstParams.19.45_QModelIndex").column, 1)
    test.compare(waitForObjectExists(":lstParams.19.45_QModelIndex").text, "19.45")
    test.compare(waitForObjectExists(":lstParams.19.45_QModelIndex").row, 5)
    test.compare(waitForObjectExists(":lstParams.883.92_QModelIndex").text, "883.92")
    test.compare(waitForObjectExists(":lstParams.883.92_QModelIndex").column, 1)
    test.compare(waitForObjectExists(":lstParams.883.92_QModelIndex").row, 6)
    test.compare(waitForObjectExists(":Error_HeaderViewItem").visualIndex, 2)
    test.compare(waitForObjectExists(":Error_HeaderViewItem").text, "Error")
    test.compare(str(waitForObjectExists(":groupBox_9.lblChi2Value_QLabel_2").text), "0.00035705")
    test.compare(str(waitForObjectExists(":qt_workspacechild.Graph1_QWorkspaceTitleBar_2").windowTitle), "Graph1")
    test.compare(waitForObjectExists(":qt_workspacechild.Graph1_QWorkspaceTitleBar_2").visible, True)
    test.compare(waitForObjectExists(":qt_workspacechild.Graph3_QWorkspaceTitleBar_4").visible, True)
    test.compare(str(waitForObjectExists(":qt_workspacechild.Graph3_QWorkspaceTitleBar_4").windowTitle), "Graph3")
    test.compare(str(waitForObjectExists(":qt_workspacechild.Graph2_QWorkspaceTitleBar_2").windowTitle), "Graph2")
    test.compare(waitForObjectExists(":qt_workspacechild.Graph2_QWorkspaceTitleBar_2").visible, True)
    waitForObjectItem(":groupBox.treeView_QTreeView", "cyl\\_400\\_20\\.txt")
    clickItem(":groupBox.treeView_QTreeView", "cyl\\_400\\_20\\.txt", -8, 9, 0, Qt.LeftButton)
    test.compare(waitForObjectExists(":cyl_400_20.txt.barbell [cyl_400_20.txt]_QModelIndex").text, "barbell [cyl_400_20.txt]")
    test.compare(waitForObjectExists(":cyl_400_20.txt.barbell [cyl_400_20.txt]_QModelIndex").checkState, "checked")
    test.compare(waitForObjectExists(":cyl_400_20.txt.Residuals for barbell[cyl_400_20.txt]_QModelIndex").checkState, "checked")
    test.compare(waitForObjectExists(":cyl_400_20.txt.Residuals for barbell[cyl_400_20.txt]_QModelIndex").text, "Residuals for barbell[cyl_400_20.txt]")
    test.compare(waitForObjectExists(":cyl_400_20.txt.Residuals for barbell[cyl_400_20.txt]_QModelIndex").enabled, True)