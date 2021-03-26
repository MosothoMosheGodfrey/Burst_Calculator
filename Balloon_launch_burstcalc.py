
from __future__ import division
import math


'''The calculator estimates the amount of gas needed to launch a high altitude balloon and achieve a desired ascent rate and burst altitude. Important imput parameters are the payload (+ parachute) mass and balloon mass in grams.'''


Payload_Mass=1500 # grams
Balloon_Mass=1000 # grams
Altitude_target_Burst=33000 # meters

# <<<<<<<<<<<<<<<<<<<<<<<     Visit http://habhub.org/calc/ verify the values    >>>>>>>>>>>>>>>>>>>>>>>>>>>

Balloon_cd=0.3 # -OR- 0.25 is mostly used for Ballon air drag, HAB-1500
Burst_diameter=7.86 # meters | Brust diameter, HAB-1500
Grav_acc_cont=9.80665 # m / s^2 | Gravitational acceleration
Desired_Ascent_rate=0  # m / s  |   If the ascent rate is smaller then 4.8 m/s the Balloon can result in a floater.
Gas_density=0.1786 # kg / m^3  |   Density Helium at 0 [degC] and 101 kPa
Air_density=1.2050 # kg / m^3  |   Density Air at 20 [degC] and 101 kPa
Air_density_model=7238.3

# Convert to kg
Payload_Mass /= 1000.0
Balloon_Mass /= 1000.0

Burst_volume = (4 / 3.0) * math.pi * math.pow(Burst_diameter / 2.0, 3)
if Altitude_target_Burst > 0:
    Launch_volume = Burst_volume * math.exp((-Altitude_target_Burst) / Air_density_model)
    launch_radius = math.pow((3 * Launch_volume) / (4 * math.pi), 1 / 3.0)
else:
    raise Exception('Target_Burst_alt needs to be > 0, if 0 is assumed to be ground-level')

Launch_site_area = math.pi * math.pow(launch_radius, 2)
Launch_volume = (4 / 3.0) * math.pi * math.pow(launch_radius, 3)
Relative_density_difference = Air_density - Gas_density
gross_lift = Launch_volume * Relative_density_difference
Neck_lift = (gross_lift - Balloon_Mass) * 1000
Total_Mass = Payload_Mass + Balloon_Mass # Add parachute Mass also. 
Free_lift = (gross_lift - Total_Mass) * Grav_acc_cont
if gross_lift <= Total_Mass:
    raise Exception('Altitude unreachable for this configuration')

Ascent_rate = round(math.sqrt(Free_lift / (0.5 * Balloon_cd * Launch_site_area * Air_density)),2)
volume_ratio = Launch_volume / Burst_volume
Burst_altitude = -(Air_density_model) * math.log(volume_ratio)
Time_2_Burst = str(int(round(round(round(( (Burst_altitude / Ascent_rate) / 60.0),2),1),0)))

print 'Results :'
print  'Neck_lift = ',str(Neck_lift) +' g',' | Payload_Mass = ',str(Payload_Mass) +' kg',' | Ascent_rate = ', str(Ascent_rate)+' m/s',
print ' ' 
print  'Burst_altitude = ',str(Burst_altitude) +' m',' | Time_to_Burst = ',str(Time_2_Burst) +' min',' | volume_ratio = ', str(volume_ratio)+' [Launch_volume/Burst_volume]',

