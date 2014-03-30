#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime

# http://www.cra-arc.gc.ca/E/pub/tg/t4037/t4037-e.html#P1185_82580

historyFile = open('trade_history.csv', 'rt')
fieldnames = [
    'Processed',
    'Traded Amount',
    'Traded Currency',
    'For Amount',
    'For Currency',
    'CAD/BTC']
historyReader = csv.DictReader(
    historyFile,
    fieldnames=fieldnames,
    delimiter=',',
    quotechar='"')

reportFieldNames = fieldnames[:]
reportFieldNames.append('Fees Percent')
reportFieldNames.append('Fees')
reportFieldNames.append('Total BTC')
reportFieldNames.append('Average Cost')
reportFieldNames.append('Capital Gain')
reportFieldNames.append('Total Capital Gain For The Year')

totalBTC = 0
averageCost = 0
year = 0
reportFile = None
reportWriter = None
FEES_BEFORE_20130705 = 0.03
FEES = 0.015


def closeFile(reportFile):
    if reportFile is not None:
        reportFile.close()


def getFees(date):
    if date < datetime.datetime(2013, 7, 5):
        fees = FEES_BEFORE_20130705
    else:
        fees = FEES
    return fees


next(historyReader)  # skip header

for row in reversed(list(historyReader)):
    costPerBtc = float(row['CAD/BTC'])
    date = datetime.datetime.strptime(row['Processed'], "%Y-%m-%d %H:%M:%S")
    feesPercent = getFees(date)
    if year != date.year:
        closeFile(reportFile)
        year = date.year
        totalCapitalGainForTheYear = 0
        reportFile = open('tax_report_' + str(year) + '.csv', 'wt')
        reportWriter = csv.DictWriter(
            reportFile,
            delimiter=',',
            fieldnames=reportFieldNames,
            quotechar='"')
        reportWriter.writer.writerow(reportWriter.fieldnames)
    if row['Traded Currency'] == 'CAD':  # buy
        nbBtcTransaction = float(row['For Amount'])
        fees = feesPercent * costPerBtc * nbBtcTransaction
        averageCost = round(
            (averageCost * totalBTC + (costPerBtc * nbBtcTransaction + fees)) /
            (totalBTC + nbBtcTransaction),
            8)
        totalBTC += nbBtcTransaction
    else:  # sell
        nbBtcTransaction = float(row['Traded Amount'])
        fees = feesPercent * costPerBtc * nbBtcTransaction
        profitTransaction = round(nbBtcTransaction * costPerBtc - fees, 8)
        capitalGainTransaction = round(
            profitTransaction -
            nbBtcTransaction *
            averageCost,
            8)
        totalCapitalGainForTheYear += capitalGainTransaction
        totalBTC -= nbBtcTransaction
        row.update(
            {'Capital Gain': capitalGainTransaction,
             'Total Capital Gain For The Year': totalCapitalGainForTheYear})
    row.update(
        {'Total BTC': totalBTC,
         'Average Cost': averageCost,
         'Fees Percent': feesPercent,
         'Fees': fees})
    reportWriter.writerow(row)

closeFile(reportFile)
historyFile.close()
