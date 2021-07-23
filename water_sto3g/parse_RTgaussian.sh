# This bash script will parse the gaussian log file from a RT calculation and return 3 files (1 for each direction)
# Each file should contain 5 fields: Time(a.u.) Time(fs) Dipole_X(Debye) Dipole_Z(Debye) Dipole_Z(Debye)

# Obtain log file names
#echo X Direction log file:
#read 1

#echo Y Direction log file:
#read 2

#echo Z Direction log file:
#read 3


# Obtain the dipole data, throw away useless lines
grep 'Dipole Moment' -A 1 $1 | grep -v 'Dipole Moment' | grep -v '\-\-' > dipole_x.dat
grep 'Dipole Moment' -A 1 $2 | grep -v 'Dipole Moment' | grep -v '\-\-' > dipole_y.dat
grep 'Dipole Moment' -A 1 $3 | grep -v 'Dipole Moment' | grep -v '\-\-' > dipole_z.dat

# Obtain the time data, throw away the first line
grep 'Time' $1 > time_x.dat
sed -i '.bak' '1d' time_x.dat
grep 'Time' $2 > time_y.dat
sed -i '.bak' '1d' time_y.dat
grep 'Time' $3 > time_z.dat
sed -i '.bak' '1d' time_z.dat

# Combine time and dipole
paste time_x.dat dipole_x.dat > x_data_gaussian.dat
paste time_y.dat dipole_y.dat > y_data_gaussian.dat
paste time_z.dat dipole_z.dat > z_data_gaussian.dat

# Pick out columns that contain actually data
awk '{ print $3, $5, $8, $10, $12 }' x_data_gaussian.dat > x_data_gaussian.txt
awk '{ print $3, $5, $8, $10, $12 }' y_data_gaussian.dat > y_data_gaussian.txt
awk '{ print $3, $5, $8, $10, $12 }' z_data_gaussian.dat > z_data_gaussian.txt

# Delete temporary Files
rm x_data_gaussian.dat y_data_gaussian.dat z_data_gaussian.dat
rm time_x.dat time_y.dat time_z.dat time_x.dat.bak time_y.dat.bak time_z.dat.bak
rm dipole_x.dat dipole_y.dat dipole_z.dat
echo DONE! Files generated
