#!/usr/bin/env bash
python outbreak_starter.py grid_1.txt grid_1_output.txt
python analysis.py grid_1_output.txt

python outbreak_starter.py grid_4.txt grid_4_output.txt
python analysis.py grid_4_output.txt

python outbreak_starter.py grid_shortcut_1.txt grid_shortcut_1_output.txt
python analysis.py grid_shortcut_1_output.txt

python outbreak_starter.py grid_shortcut_4.txt grid_shortcut_4_output.txt
python analysis.py grid_shortcut_4_output.txt

python outbreak_starter.py scalefree_high.txt scalefree_high_output.txt
python analysis.py scalefree_high_output.txt

python outbreak_starter.py scalefree_low.txt scalefree_low_output.txt
python analysis.py scalefree_low_output.txt
