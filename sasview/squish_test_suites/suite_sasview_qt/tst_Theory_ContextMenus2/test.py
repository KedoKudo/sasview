# -*- coding: utf-8 -*-

def main():
    startApplication("sasview")
    clickTab(waitForObject(":Data Explorer.DataLoadWidget_DataExplorerWindow"), "Theory")
    mouseClick(waitForObject(":groupBox_6.cbCategory_QComboBox"), 58, 6, 0, Qt.LeftButton)
    mouseClick(waitForObjectItem(":groupBox_6.cbCategory_QComboBox", "Cylinder"), 45, 2, 0, Qt.LeftButton)
    clickButton(waitForObject(":FittingWidgetUI.cmdPlot_QPushButton_2"))
    clickButton(waitForObject(":groupBox_7.chk2DView_QCheckBox"))
    clickButton(waitForObject(":FittingWidgetUI.cmdPlot_QPushButton_2"))
    #test.compare(waitForObjectExists(":qt_workspacechild_FigureCanvasQTAgg_2").visible, True)
    waitForObjectItem(":groupBox_2.freezeView_QTreeView", "M1 [barbell2d]")
    clickItem(":groupBox_2.freezeView_QTreeView", "M1 [barbell2d]", 56, 5, 0, Qt.LeftButton)
    openItemContextMenu(waitForObject(":groupBox_2.freezeView_QTreeView"), "M1 [barbell2d]", 56, 5, 0)
    activateItem(waitForObjectItem(":MainWindow_QMenu", "Quick 3DPlot (slow)"))
    sendEvent("QWheelEvent", waitForObject(":LogDockWidget.qt_dockwidget_floatbutton_QTextBrowser"), 596, 10, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":LogDockWidget.qt_dockwidget_floatbutton_QTextBrowser"), 599, 13, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":LogDockWidget.qt_dockwidget_floatbutton_QTextBrowser"), 601, 16, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":LogDockWidget.qt_dockwidget_floatbutton_QTextBrowser"), 601, 16, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":LogDockWidget.qt_dockwidget_floatbutton_QTextBrowser"), 601, 16, -120, 0, 2)
    sendEvent("QWheelEvent", waitForObject(":LogDockWidget.qt_dockwidget_floatbutton_QTextBrowser"), 601, 16, -120, 0, 2)
    openItemContextMenu(waitForObject(":groupBox_2.freezeView_QTreeView"), "M1 [barbell2d]", 85, 6, 0)
    activateItem(waitForObjectItem(":MainWindow_QMenu", "Edit Mask"))
    test.compare(waitForObjectExists(":MaskEditorUI_MaskEditor").visible, True)
    test.compare(str(waitForObjectExists(":MaskEditorUI_MaskEditor").windowTitle), "Mask Editor for M1 [barbell2d]")
    test.vp("VP1")
