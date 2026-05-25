#=================================================================
# 				Analyse des performances
#=================================================================

from time import perf_counter
from main import dechiffrer_force_brute

Temps=[]
for i in range(10):
    tic=perf_counter()
    msg=dechiffrer_force_brute("corbeau_25-25-25.txt", "enigma")
    toc=perf_counter()
    print(f"Temps d'éxecution:{toc-tic}[s]")
    Temps.append(toc-tic)
somme_temps=sum(Temps)
moyenne_temps=somme_temps/len(Temps)
print(moyenne_temps)
