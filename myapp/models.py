"""
Beschreibung: Definiert die Datenmodelle der App, welche die Struktur der Datenbanktabellen abbilden. Diese Modelle werden von Django ORM (Object-Relational Mapping) verwendet, um Datenbankoperationen zu abstrahieren.
Zweck: Repräsentiert die Datenstruktur der App und bietet eine hochgradig abstrahierte Schnittstelle zur Datenmanipulation.
"""

from django.db import models


class GSL_grouped_ISK_2022(models.Model):
    STR_NR = models.IntegerField(primary_key=True)
    LAENGE = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    STR_KURZNAME = models.CharField(max_length=255)
    STR_KM_ANF = models.CharField(max_length=255)
    STR_KM_END = models.CharField(max_length=255)
    ISK_NETZ = models.CharField(max_length=255)
    BAHNNUTZUNG = models.CharField(max_length=255)
    BETREIBERART = models.CharField(max_length=255)
    geometry = models.TextField()

    class Meta:
        db_table = 'GSL_grouped_ISK_2022'


class GSL_ISK_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    #STR_NR = models.IntegerField(primary_key=True)
    STR_KURZNAME = models.CharField(max_length=255)
    STR_KM_ANF = models.CharField(max_length=255)
    STR_KM_END = models.CharField(max_length=255)
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    RI = models.CharField(max_length=255)
    LAENGE = models.IntegerField()
    DB_BETRIEB = models.CharField(max_length=255)
    ISK_NETZ = models.CharField(max_length=255)
    BAHNNUTZUNG = models.CharField(max_length=255)
    BETREIBERART = models.CharField(max_length=255)
    SONDERFALL = models.CharField(max_length=255)
    SONST_VERTR = models.CharField(max_length=255)
    AUSLAND = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='gsl')

    class Meta:
        db_table = 'GSL_ISK_2022'




class SML_ISK_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    #STR_NR = models.IntegerField(primary_key=True)
    RI = models.CharField(max_length=255)
    STR_KURZNAME = models.CharField(max_length=255)
    STR_KM_ANF = models.CharField(max_length=255)
    STR_KM_END = models.CharField(max_length=255)
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    LAENGE = models.IntegerField()
    ELEKTR = models.CharField(max_length=255)
    BAHNART = models.CharField(max_length=255)
    GL_ANZ = models.IntegerField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='sml')


    class Meta:
        db_table = 'SML_ISK_2022'


class weichen_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255) 
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key = True)
    #STR_NR = models.IntegerField()
    LAGE_KM = models.CharField(max_length=255)
    LAGE_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    RIL_100 = models.CharField(max_length=255) 
    GLEISART = models.IntegerField()
    WK_NR = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()


    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='weichen')

    class Meta:
        db_table = 'weichen_ISK_2022'

class stuetzauwerke_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key=True)
    #STR_NR = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    LAGE = models.CharField(max_length=255)
    LAENGE = models.IntegerField()
    BAUART = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='stuetzbauwerke')


    class Meta:
        db_table = 'stuetzauwerke_ISK_2022'


class schallschutzwaende_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key=True)
    #STR_NR = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    LAENGE = models.IntegerField()
    LAGE = models.CharField(max_length=255)
    BAUART = models.CharField(max_length=255)
    MIN_HOEHE = models.FloatField()
    MAX_HOEHE = models.FloatField()
    GLEISABSTAND = models.FloatField()
    MATERIAL_WAND = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='schallschutzwaende')


    class Meta:
        db_table = 'schallschutzwaende_ISK_2022'



class ETCS_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    #str_nr = models.IntegerField(primary_key=True) 
    str_name = models.CharField(max_length=255)
    heute_ohne_ETCS = models.FloatField()
    heute_ETCS_Level_1 = models.FloatField()
    heute_ETCS_Level_2 = models.FloatField()
    geplant_ETCS_L1LS = models.FloatField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='ETCS')


    class Meta:
        db_table = 'ETCS_2022'



class traffic_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    #STR_NR = models.IntegerField(primary_key=True)
    AverageAnualTFlow = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='traffic')

    class Meta:
        db_table = 'traffic_2022'


class hlk_zeitraum_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    HLK_Name = models.CharField(max_length=255)
    #STR_NR = models.IntegerField(primary_key=True)
    Zeitraum = models.CharField(max_length=255)

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='HLK_Zeitraum')


    class Meta:
        db_table = 'hlk_zeitraum_2022'


class bruecken_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key=True)
    ANLAGEN_UNR = models.IntegerField()
    #STR_NR = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    RIL_100 = models.CharField(max_length=255)
    STR_MEHRFACHZUORD = models.CharField(max_length=255)
    FLAECHE = models.CharField(max_length=255)
    BR_BEZ = models.CharField(max_length=255)
    BAUART = models.CharField(max_length=255)
    BESCHREIBUNG = models.CharField(max_length=255)
    ZUST_KAT = models.CharField(max_length=255)
    WL_SERVICEEINR = models.CharField(max_length=255)
    Match = models.CharField(max_length=255)
    GEOGR_BREITE = models.FloatField()
    GEOGR_LAENGE = models.FloatField()
    lat = models.FloatField()
    lon = models.FloatField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='bruecken')


    class Meta:
        db_table = 'bruecken_ISK_2022'


class bahnuebergaenge_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR_FABA = models.IntegerField(primary_key=True)
    ANLAGEN_NR_LST = models.CharField(max_length=255)
    #STR_NR = models.IntegerField()
    LAGE_KM = models.CharField(max_length=255)
    LAGE_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    RIL_100 = models.CharField(max_length=255)
    UEB_WACH_ART = models.CharField(max_length=255)
    ZUGGEST = models.CharField(max_length=255)
    WL_SERVICEEINR = models.CharField(max_length=255)
    Matching = models.FloatField()
    Abs_Dif_cm = models.CharField(max_length=255)
    breite = models.FloatField()
    laenge = models.FloatField()
    lat = models.FloatField()
    lon = models.FloatField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='bahnuebergaenge')


    class Meta:
        db_table = 'bahnuebergaenge_ISK_2022'


class tunnel_ISK_2022(models.Model):
    LAND = models.CharField(max_length=255)
    EIU = models.CharField(max_length=255)
    REGION = models.CharField(max_length=255)
    NETZ = models.CharField(max_length=255)
    ANLAGEN_NR = models.IntegerField(primary_key=True)
    #STR_NR = models.IntegerField()
    VON_KM = models.CharField(max_length=255)
    BIS_KM = models.CharField(max_length=255)
    VON_KM_I = models.IntegerField()
    BIS_KM_I = models.IntegerField()
    RIKZ = models.IntegerField()
    RIL_100 = models.CharField(max_length=255)
    STR_MEHRFACHZUORD = models.CharField(max_length=255)
    LAENGE = models.IntegerField()
    ANZ_STR_GL = models.IntegerField()
    QUERSCHN = models.CharField(max_length=255)
    BAUWEISE = models.CharField(max_length=255)
    WL_SERVICEEINR = models.CharField(max_length=255)
    Matching = models.CharField(max_length=255)
    geometry = models.TextField()

    gsl_grouped_isk_2022 = models.ForeignKey(GSL_grouped_ISK_2022, on_delete=models.CASCADE, db_column='STR_NR', related_name='tunnel')

    class Meta:
        db_table = 'tunnel_ISK_2022'



class bahnsteige_ISK_2022(models.Model):
    ID = models.IntegerField(primary_key=True)
    zugangsmoeglichkeit_bstg = models.CharField(max_length=255)
    stufenfreiheit = models.CharField(max_length=255)
    zuganzeiger_dsa_fia = models.CharField(max_length=255)
    lautsprecher_dsa_akustik_modul = models.CharField(max_length=255)
    taktiles_leitsystem_bstg = models.CharField(max_length=255)
    taktiler_weg_oeffentlicher_bereich_bstg = models.CharField(max_length=255)
    stufenmarkierung_treppen = models.CharField(max_length=255)
    taktile_handlaufschilder_treppen_rampen = models.CharField(max_length=255)
    wegeleitsystem = models.CharField(max_length=255)
    ist_baulaenge_bstgdaecher_eigentum_db = models.CharField(max_length=255)
    ist_baulaenge_bstgdaecher_eigentum_dritter = models.CharField(max_length=255)
    nicht_zugaenglicher_bereich = models.CharField(max_length=255)
    denkmalschutz_bstgdach = models.CharField(max_length=255)
    laenge_bstg_unter_halle = models.CharField(max_length=255)
    laenge_ueberbauung = models.CharField(max_length=255)
    anzahl_wsh = models.CharField(max_length=255)
    anzahl_wsh_halle_dach_ueberb = models.CharField(max_length=255)

    class Meta:
        db_table = 'bahnsteige_ISK_2022'



class stationen_ISK_2022(models.Model):
    number = models.IntegerField(primary_key=True)
    ifopt = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    priceCategory = models.CharField(max_length=255)
    hasParking = models.BooleanField()
    hasBicycleParking = models.BooleanField()
    hasLocalPublicTransport = models.BooleanField()
    hasPublicFacilities = models.BooleanField()
    hasLockerSystem = models.BooleanField()
    hasTaxiRank = models.BooleanField()
    hasTravelNecessities = models.BooleanField()
    hasSteplessAccess = models.BooleanField()
    hasMobilityService = models.BooleanField()
    hasWiFi = models.BooleanField()
    hasTravelCenter = models.BooleanField()
    hasRailwayMission = models.BooleanField()
    hasDBLounge = models.BooleanField()
    hasLostAndFound = models.BooleanField()
    hasCarRental = models.BooleanField()
    federalState = models.CharField(max_length=255)
    regionalbereich_number = models.IntegerField()
    regionalbereich_name = models.CharField(max_length=255)
    regionalbereich_shortName = models.CharField(max_length=255)
    aufgabentraeger_shortName = models.CharField(max_length=255)
    aufgabentraeger_name = models.CharField(max_length=255)
    localServiceStaff_availability_monday_fromTime = models.TimeField()
    localServiceStaff_availability_monday_toTime = models.TimeField()
    localServiceStaff_availability_tuesday_fromTime = models.TimeField()
    localServiceStaff_availability_tuesday_toTime = models.TimeField()
    localServiceStaff_availability_wednesday_fromTime = models.TimeField()
    localServiceStaff_availability_wednesday_toTime = models.TimeField()
    localServiceStaff_availability_thursday_fromTime = models.TimeField()
    localServiceStaff_availability_thursday_toTime = models.TimeField()
    localServiceStaff_availability_friday_fromTime = models.TimeField()
    localServiceStaff_availability_friday_toTime = models.TimeField()
    localServiceStaff_availability_saturday_fromTime = models.TimeField()
    localServiceStaff_availability_saturday_toTime = models.TimeField()
    localServiceStaff_availability_sunday_fromTime = models.TimeField()
    localServiceStaff_availability_sunday_toTime = models.TimeField()
    localServiceStaff_availability_holiday_fromTime = models.TimeField()
    localServiceStaff_availability_holiday_toTime = models.TimeField()
    timeTableOffice_email = models.EmailField()
    timeTableOffice_name = models.CharField(max_length=255)
    szentrale_number = models.IntegerField()
    szentrale_publicPhoneNumber = models.CharField(max_length=255)
    szentrale_name = models.CharField(max_length=255)
    stationManagement_number = models.IntegerField()
    stationManagement_name = models.CharField(max_length=255)
    evaNumbers_number = models.IntegerField()
    evaNumbers_geographicCoordinates = models.CharField(max_length=255)
    ril100Identifiers_rilIdentifier = models.CharField(max_length=255)
    ril100Identifiers_isMain = models.BooleanField()
    ril100Identifiers_hasSteamPermission = models.BooleanField()
    ril100Identifiers_steamPermission = models.CharField(max_length=255)
    ril100Identifiers_geographicCoordinates = models.CharField(max_length=255)
    ril100Identifiers_primaryLocationCode = models.CharField(max_length=255)
    productLine_productLine = models.CharField(max_length=255)
    productLine_segment = models.CharField(max_length=255)

    class Meta:
        db_table = 'stationen_ISK_2022'




