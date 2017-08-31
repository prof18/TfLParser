echo '######################################'
echo 'Running velocity_parser'
python2.7 velocity_parser.py
echo '######################################'
echo 'Running velocity_interval_parser'
python2.7 velocity_interval_parser.py
echo '######################################'
echo 'Running mean_velocity'
python2.7 mean_velocity.py
echo '######################################'
echo 'Running velocity_plot'
python2.7 velocity_plot.py