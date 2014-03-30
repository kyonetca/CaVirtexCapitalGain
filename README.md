CaVirtexCapitalGain
===================

This script generate a capital gain report file for each years you traded on CaVirtex. It uses the adjusted cost base to calculate the capital gain for your tax return.

You need to download your trade history file from CaVirtex https://www.cavirtex.com/trade_history_csv

Place the file named trade_history.csv in your CaVirtexCapitalGain directory

<pre>
$ python capitalGain.py 
</pre>

The script will generate a report file tax_report_20XX.csv for each year you sold bitcoins on CaVirtex.

Disclamer
=========

Use at your own risk. If you traded Litecoins the report may not be accurate. I'm not affiliated with CaVirtex. 
