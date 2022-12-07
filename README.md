# scoring project - vj mchargue veejer@gmail.com
===================
Hacked together code testing some ideas on better ways to score a collection of assets and attributes.  General idea is to translate the assets with attributes 
into mathmatical collections, or document, which can be acted upon by real data analysis techniques vs. a traditional linear programming approach.  Initial
attempt via cosine similarities did work but did not provide a true picture.  Magnitude is important (actual number of assets) for this analysis and cosine
similarities and other like approaches only provide valuable insight with normalized data.  Magnitude aware techniques will be explored in further commits.

The demo progream is determineSimilarities.py - it reads an input file of inventory (inventory.csv), loads an intentory SQL table, generates a features file
(features.csv) and loads the features table, does a site comparison, and does a site local HA analysis, and writes metrics to a metrics table.  The DB used
is sqlite and the file is inventory.db.

The committed code is a ms vscode project, so you should be able to pull the git project and have it running pretty easy.  The settings.json will need
modified for your environment.
