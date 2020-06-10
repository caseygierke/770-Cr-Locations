# TableProcessor.py


# This runs the other files so that they all happen with one initial compile

print('Running SummaryStats')
import SummaryStats

print('Running addStatus')
import addStatus

print('Running getWatershed')
import getWatershed

print('Running ChromiumLocationsDBsetup.py')
import ChromiumLocationsDBsetup

print('Running TablesOut')
import TablesOut

print('Running tablesToExcel')
import tablesToExcel


