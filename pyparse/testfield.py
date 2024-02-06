from datetime import datetime

tripTime = 100
tripHour = (tripTime//100 if (tripTime / 100) >= 1 else 0)

print(tripHour)
