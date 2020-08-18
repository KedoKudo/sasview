import sys
import numpy as np
import unittest
from unittest.mock import mock_open, patch
import webbrowser
import logging

from unittest.mock import MagicMock

from PyQt5 import QtGui, QtWidgets

# set up import paths
import path_prepare

from sas.qtgui.UnitTesting.TestUtils import QtSignalSpy

from sas.sascalc.fit.AbstractFitEngine import FResult
from sas.sascalc.fit.AbstractFitEngine import FitData1D
from sasmodels.sasview_model import load_standard_models
from sas.qtgui.Plotting.PlotterData import Data1D

import sas.qtgui.Utilities.GuiUtils as GuiUtils
# Local
from sas.qtgui.Utilities.GridPanel import BatchOutputPanel

if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)

class BatchOutputPanelTest(unittest.TestCase):
    '''Test the batch output dialog'''
    def setUp(self):
        '''Create the dialog'''
        # dummy perspective
        class dummy_manager(object):
            _parent = QtWidgets.QWidget()
            def communicator(self):
                return GuiUtils.Communicate()
            def communicate(self):
                return GuiUtils.Communicate()
        self.widget = BatchOutputPanel(parent=dummy_manager(), output_data=self.output_for_test())
        test_table = {"p1":[1,2,3],
                      "p2":[4,5,None],
                      "":["a",credits,],
                      "":[]}

    def tearDown(self):
        '''Destroy the GUI'''
        self.widget.close()
        self.widget = None

    def output_for_test(self):
        ''' define DATA1D structure for testing'''
        # dummy parameter set
        m = None
        for m in load_standard_models():
            if m.name == "core_shell_ellipsoid":
                model = m()
        self.assertIsNotNone(m)
        data = Data1D(x=[1,2], y=[3,4], dx=[0.1, 0.1], dy=[0.,0.])
        fit_data = FitData1D(x=[1,2], y=[3,4], data=data)
        param_list = ['sld_shell', 'sld_solvent']
        output = FResult(model=model, data=fit_data, param_list=param_list)
        output.sas_data = data
        output.theory = np.array([0.1,0.2])
        output.pvec = np.array([0.1, 0.02])
        output.residuals = np.array([0.01, 0.02])
        output.fitness = 9000.0
        output.fitter_id = 200
        output.stderr = [0.001, 0.001]
        output_data = [[output],[output]]
        return output_data

    def testDefaults(self):
        '''Test the GUI in its default state'''
        self.assertIsInstance(self.widget, QtWidgets.QMainWindow)
        # Default title
        self.assertEqual(self.widget.windowTitle(), "Batch Fitting Results")

        # non-modal window
        self.assertFalse(self.widget.isModal())

    def testActionLoadData(self):
        '''Test CSV data loader'''
        test_csv = mock_open(read_data = ("""\
File generated by SasView\n
Chi2,Data,scale,background,radius_equat_core,x_core,thick_shell,x_polar_shell,sld_core,sld_shell,sld_solvent,theta,phi,\n
1917.8,cyl_400_40.txt,1,0.001,20,3,30,1,-85.088,-97.636,-92.797,0,0,\n
2.6169,cyl_400_20.txt,1,0.001,20,3,30,1,914.64,906.09,905.67,0,0,\n
"""))
        logging.info = MagicMock()
        self.widget.setupTableFromCSV = MagicMock()

        # No filename given
        QtWidgets.QFileDialog.getOpenFileName = MagicMock(return_value=[""])
        self.widget.actionLoadData()
        # Assure parser wasn't called and logging got a message
        self.assertTrue(logging.info.called_once())
        self.assertIn("No data", logging.info.call_args[0][0])

        # Filename given
        QtWidgets.QFileDialog.getOpenFileName = MagicMock(return_value="test")
        with patch('builtins.open', test_csv):
            self.widget.actionLoadData()
            # Assure parser was called
            self.assertTrue(self.widget.actionLoadData)
            self.widget.setupTableFromCSV.assert_called_once()
            self.assertIn("File generated by SasView", self.widget.setupTableFromCSV.call_args[0][0][0])

    def notestPlotFits(self):
        '''Test plot generation from selected table rows'''
        # mock tested calls
        #GuiUtils.Communicate.plot
        spy_plot_signal = QtSignalSpy(self.widget.communicate, self.widget.communicate().plotFromNameSignal)
        # Select row #1
        self.widget.tblParams.selectRow(0)
        QtWidgets.QApplication.processEvents()

        # See that the signal was emitted
        self.assertEqual(spy_plot_signal.count(), 1)
        self.assertIn("ddd", str(spy_plot_signal.called()[0]['args'][0]))


    def testDataFromTable(self):
        '''Test dictionary generation from data'''
        params = self.widget.dataFromTable(self.widget.tblParams)
        self.assertEqual(len(params), 13)
        self.assertEqual(params['Chi2'][0], '9000')
        self.assertEqual(params['Data'][1], '')
        self.assertEqual(params['sld_solvent'][1], '0.02')

    def testActionSendToExcel(self):
        '''Test Excel bindings'''
        pass

    def testActionSaveFile(self):
        '''Test file save'''
        self.widget.writeBatchToFile = MagicMock()

        # user cancels dialog
        QtWidgets.QFileDialog.getSaveFileName = MagicMock(return_value=("","BOOP"))
        # write not called
        self.widget.actionSaveFile()
        self.widget.writeBatchToFile.assert_not_called()

        # user chooses proper name
        QtWidgets.QFileDialog.getSaveFileName = MagicMock(return_value=("plop","BOOP"))
        # write called
        self.widget.actionSaveFile()
        self.widget.writeBatchToFile.assert_called_once()

    def testSetupTableFromCSV(self):
        '''Test generation of grid table rows from a CSV file'''
        pass


