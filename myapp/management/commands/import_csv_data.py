import csv
from django.core.management.base import BaseCommand
from myapp.models import GSL, Tunnel, Weiche, Bruecke  # Ensure models are correctly imported

class Command(BaseCommand):
    help = 'Load data from CSV files into the corresponding Django models'


    def handle(self, *args, **options):
        
        self.import_tunnel()
        self.import_gsl()
        self.import_weiche()
        self.import_bruecke()

    #def handle(self, *args, **options):
     #   self.import_from_csv('myapp/data_files/GSL.csv', GSL, delimiter=';')
      #  self.import_from_csv('myapp/data_files/Tunnel.csv', Tunnel, delimiter=';')
       # self.import_from_csv('myapp/data_files/Weichen.csv', Weiche, delimiter=';')
        #self.import_from_csv('myapp/data_files/Brücken.csv', Bruecke, delimiter=';')

    def import_gsl(self):
        with open('myapp/data_files/GSL.csv', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                gsl_instance = GSL(
                    land=row['LAND'],
                    eiu=row['EIU'],
                    region=row['REGION'],
                    netz=row['NETZ'],
                    str_nr=int(row['STR_NR']),
                    str_kurzname=row['STR_KURZNAME'],
                    str_km_anf=row['STR_KM_ANF'],
                    str_km_end=row['STR_KM_END'],
                    von_km=row['VON_KM'],
                    bis_km=row['BIS_KM'],
                    von_km_i=int(row['VON_KM_I']),
                    bis_km_i=int(row['BIS_KM_I']),
                    ri=int(row['RI']),
                    laenge=int(row['LAENGE']),
                    db_betrieb=row['DB_BETRIEB'],
                    isk_netz=row['ISK_NETZ'],
                    bahnnutzung=row['BAHNNUTZUNG'],
                    betreiberart=row['BETREIBERART'],
                    sonderfall=row['SONDERFALL'],
                    sonst_vertr=row['SONST_VERTR'],
                    ausland=row['AUSLAND']
                )
                gsl_instance.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded GSL entry: {gsl_instance}'))

    def import_bruecke(self):
        with open('myapp/data_files/Brücken.csv', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                bruecke_instance = Bruecke(
                    land=row['LAND'],
                    eiu=row['EIU'],
                    region=row['REGION'],
                    netz=row['NETZ'],
                    anlagen_nr=row['ANLAGEN_NR'],
                    anlagen_unr=row['ANLAGEN_UNR'],
                    str_nr=int(row['STR_NR']),
                    von_km=row['VON_KM'],
                    bis_km=row['BIS_KM'],
                    von_km_i=row['VON_KM_I'],
                    bis_km_i=row['BIS_KM_I'],
                    rikz=row['RIKZ'],
                    ril_100=row['RIL_100'],
                    str_mehrfachzuord=row['STR_MEHRFACHZUORD'],
                    flaeche=row['FLAECHE'],
                    br_bez=row['BR_BEZ'],
                    bauart=row['BAUART'],
                    beschreibung=row['BESCHREIBUNG'],
                    zust_kat=row['ZUST_KAT'],
                    wl_serviceeinr=row['WL_SERVICEEINR'],
                )
                bruecke_instance.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded Brücke entry: {bruecke_instance}'))

    def import_tunnel(self):
        with open('myapp/data_files/Tunnel.csv', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                tunnel_instance = Tunnel(
                    land=row['LAND'],
                    eiu=row['EIU'],
                    region=row['REGION'],
                    netz=row['NETZ'],
                    anlagen_nr=row['ANLAGEN_NR'],
                    str_nr=int(row['STR_NR']),
                    von_km=row['VON_KM'],
                    bis_km=row['BIS_KM'],
                    von_km_i=row['VON_KM_I'],
                    bis_km_i=row['BIS_KM_I'],
                    rikz=row['RIKZ'],
                    ril_100=row['RIL_100'],
                    str_mehrfachzuord=row['STR_MEHRFACHZUORD'],
                    laenge=row['LAENGE'],
                    anz_str_gl=row['ANZ_STR_GL'],
                    querschn=row['QUERSCHN'],
                    bauweise=row['BAUWEISE'],
                    wl_serviceeinr=row['WL_SERVICEEINR'],
                )
                tunnel_instance.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded Tunnel entry: {tunnel_instance}'))

    def import_weiche(self):
        with open('myapp/data_files/Weichen.csv', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                weiche_instance = Weiche(
                    land=row['LAND'],
                    eiu=row['EIU'],
                    region=row['REGION'],
                    netz=row['NETZ'],
                    anlagen_nr=row['ANLAGEN_NR'],
                    str_nr=int(row['STR_NR']),
                    lage_km=row['LAGE_KM'],
                    lage_km_i=row['LAGE_KM_I'],
                    rikz=row['RIKZ'],
                    ril_100=row['RIL_100'],
                    gleisart=row['GLEISART'],
                    wk_nr=row['WK_NR'],
                    wl_serviceeinr=row['WL_SERVICEEINR'],
                )
                weiche_instance.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded Weiche entry: {weiche_instance}'))
